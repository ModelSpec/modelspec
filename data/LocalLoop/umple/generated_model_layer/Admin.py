# %% NEW FILE Admin BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 58 "model.ump"
# line 187 "model.ump"
from .Role import Role

class Admin(Role):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        super().__init__()

    #------------------------
    # INTERFACE
    #------------------------
    def delete(self):
        super().delete()
