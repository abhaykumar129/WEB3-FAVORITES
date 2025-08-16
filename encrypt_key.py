
from eth_account import Account
import getpass
from pathlib import Path
import json

KEYSTORE_PATH = Path(".keystore.json")

def main():
    # input for your private key
    private_key = getpass.getpass("Enter your private key:\n")
    my_account = Account.from_key(private_key)

    password = getpass.getpass("Enter a password:\n")
    encrypted_account = my_account.encrypt(password)

    print(f"Saving to {KEYSTORE_PATH}...")
    with KEYSTORE_PATH.open("w") as fp:
        json.dump(encrypted_account, fp)

if __name__ == "__main__":
    main()
