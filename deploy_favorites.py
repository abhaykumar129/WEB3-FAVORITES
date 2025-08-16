from web3 import Web3
from dotenv import load_dotenv
from vyper import compile_code
import os
from encrypt_key import KEYSTORE_PATH
from eth_account import Account
import getpass

load_dotenv()

RPC_URL = os.getenv("RPC_URL")


def main():
    print("Let's read in the Vyper code and deploy it to the blockchain!")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    with open("favorites.vy", "r") as favorites_file:
        favorites_code = favorites_file.read()
        compliation_details = compile_code(
            favorites_code, output_formats=["bytecode", "abi"]
        ) 
    # breakpoint() # Set a breakpoint here to inspect the contract object


    chain_id = 31337  # Make sure this matches your virtual or anvil network!

    print("Getting environment variables...")
    my_address = os.getenv("MY_ADDRESS")

    # private_key = os.getenv("PRIVATE_KEY")
    private_key = decrypt_key()

    # Create the contract in Python
    favorites_contract = w3.eth.contract(
        abi=compliation_details["abi"], bytecode=compliation_details["bytecode"]
    )
       
    # Submit the transaction that deploys the contract
    nonce = w3.eth.get_transaction_count(my_address)

    # We could do this next line as a shortcut :)
    # tx_hash = favorites_contract.constructor().transact()

    print("Building the transaction...")
    transaction = favorites_contract.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            # "gasPrice": 1,
            "from": my_address,
            "nonce": nonce,
        }
    )

    print("Signing transaction...")
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("We signed it, check it out:")
    print(signed_txn)

    print("Deploying Contract!")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


def decrypt_key() -> str:
    with open(KEYSTORE_PATH, "r") as fp:
        encrypted_account = fp.read()
        password = getpass.getpass("Enter your password for your keystore.json:\n")
        key = Account.decrypt(encrypted_account, password)
        print("Decrypted key!")
        return key


if __name__ == "__main__":
    main()
    

    
