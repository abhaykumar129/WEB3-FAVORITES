
# pragma version 0.4.3


# @license MIT



struct Person:
   favorite_number:uint256
   name:String[100]


my_name:public(String[100])

my_favorite_number:public(uint256)

list_of_numbers:public(uint256[5])   #0,0,0,0,0
list_of_people:public(Person[5])  #(7,PATRIC),(16,"ABHAY"),(77,RAMOJI),(44,"GAUR"),(Japnoor,99)
index:public(uint256)

name_to_favorite_number:public(HashMap[String[100],uint256])



#Constructor
@deploy
def __init__():
    self.my_favorite_number =7
    self.index =0
    self.my_name = "ABHAY"



@external
def store(new_number:uint256):
    self.my_favorite_number = new_number
    # self.retrieve()



@external
@view
def retrieve() -> uint256:
    return self.my_favorite_number



@external
def add_numbers(name:String[100],favorite_number:uint256):
    # self.list_of_numbers[0] = favorite_number

    # Add favorite number to the numbers list
    self.list_of_numbers[self.index] = favorite_number
    
    
    # add the person to the person's list
    new_person:Person  = Person(favorite_number = favorite_number,name = name)
    self.list_of_people[self.index] = new_person
    
    

    # add the person TO THE HasHmap
    self.name_to_favorite_number[name] =favorite_number
    
    # self.index = self.index + 1
    # OR
    self.index+=1