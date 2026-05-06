# %% NEW FILE MoneyValue BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 181 "model.ump"
# line 350 "model.ump"

class MoneyValue():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MoneyValue Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aValue, aCurrency):
        self._currency = None
        self._value = None
        self._value = aValue
        self._currency = aCurrency

    #------------------------
    # INTERFACE
    #------------------------
    def setValue(self, aValue):
        wasSet = False
        self._value = aValue
        wasSet = True
        return wasSet

    def setCurrency(self, aCurrency):
        wasSet = False
        self._currency = aCurrency
        wasSet = True
        return wasSet

    def getValue(self):
        return self._value

    def getCurrency(self):
        return self._currency

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "value" + ":" + str(self.getValue()) + "," + "currency" + ":" + str(self.getCurrency()) + "]"
