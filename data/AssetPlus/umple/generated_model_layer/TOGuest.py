# %% NEW FILE TOGuest BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 130 "model.ump"
# line 261 "model.ump"
from .TOUser import TOUser

class TOGuest(TOUser):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber):
        super().__init__(aEmail, aName, aPassword, aPhoneNumber)

    #------------------------
    # INTERFACE
    #------------------------
    def delete(self):
        super().delete()
