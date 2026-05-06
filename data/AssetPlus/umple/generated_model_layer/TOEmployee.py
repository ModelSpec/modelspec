# %% NEW FILE TOEmployee BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 142 "model.ump"
# line 271 "model.ump"
from .TOHotelStaff import TOHotelStaff

class TOEmployee(TOHotelStaff):
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
