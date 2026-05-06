# %% NEW FILE LegalSituation BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 61 "model.ump"
from .Situation import Situation

class LegalSituation(Situation):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #LegalSituation Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTime):
        self._consequentOf = None
        self._antecedentOf = None
        super().__init__(aTime)
        self._antecedentOf = []
        self._consequentOf = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getAntecedentOf1(self, index):
        aAntecedentOf = self._antecedentOf[index]
        return aAntecedentOf

    def getAntecedentOf2(self):
        newAntecedentOf = tuple(self._antecedentOf)
        return newAntecedentOf

    def numberOfAntecedentOf(self):
        number = len(self._antecedentOf)
        return number

    def hasAntecedentOf(self):
        has = len(self._antecedentOf) > 0
        return has

    def indexOfAntecedentOf(self, aAntecedentOf):
        index = (-1 if not aAntecedentOf in self._antecedentOf else self._antecedentOf.index(aAntecedentOf))
        return index

    # Code from template association_GetMany
    def getConsequentOf1(self, index):
        aConsequentOf = self._consequentOf[index]
        return aConsequentOf

    def getConsequentOf2(self):
        newConsequentOf = tuple(self._consequentOf)
        return newConsequentOf

    def numberOfConsequentOf(self):
        number = len(self._consequentOf)
        return number

    def hasConsequentOf(self):
        has = len(self._consequentOf) > 0
        return has

    def indexOfConsequentOf(self, aConsequentOf):
        index = (-1 if not aConsequentOf in self._consequentOf else self._consequentOf.index(aConsequentOf))
        return index

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfAntecedentOf():
        return 0

    # Code from template association_AddManyToOne
    def addAntecedentOf1(self, aName, aConsequent, aContract, aDebtor, aCreditor):
        from .LegalPosition import LegalPosition
        return LegalPosition(aName, self, aConsequent, aContract, aDebtor, aCreditor)

    def addAntecedentOf2(self, aAntecedentOf):
        wasAdded = False
        if (aAntecedentOf) in self._antecedentOf :
            return False
        existingAntecedent = aAntecedentOf.getAntecedent()
        isNewAntecedent = not (existingAntecedent is None) and not self == existingAntecedent
        if isNewAntecedent :
            aAntecedentOf.setAntecedent(self)
        else :
            self._antecedentOf.append(aAntecedentOf)
        wasAdded = True
        return wasAdded

    def removeAntecedentOf(self, aAntecedentOf):
        wasRemoved = False
        #Unable to remove aAntecedentOf, as it must always have a antecedent
        if not self == aAntecedentOf.getAntecedent() :
            self._antecedentOf.remove(aAntecedentOf)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addAntecedentOfAt(self, aAntecedentOf, index):
        wasAdded = False
        if self.addAntecedentOf(aAntecedentOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfAntecedentOf() :
                index = self.numberOfAntecedentOf() - 1
            self._antecedentOf.remove(aAntecedentOf)
            self._antecedentOf.insert(index, aAntecedentOf)
            wasAdded = True
        return wasAdded

    def addOrMoveAntecedentOfAt(self, aAntecedentOf, index):
        wasAdded = False
        if (aAntecedentOf) in self._antecedentOf :
            if index < 0 :
                index = 0
            if index > self.numberOfAntecedentOf() :
                index = self.numberOfAntecedentOf() - 1
            self._antecedentOf.remove(aAntecedentOf)
            self._antecedentOf.insert(index, aAntecedentOf)
            wasAdded = True
        else :
            wasAdded = self.addAntecedentOfAt(aAntecedentOf, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfConsequentOf():
        return 0

    # Code from template association_AddManyToOne
    def addConsequentOf1(self, aName, aAntecedent, aContract, aDebtor, aCreditor):
        from .LegalPosition import LegalPosition
        return LegalPosition(aName, aAntecedent, self, aContract, aDebtor, aCreditor)

    def addConsequentOf2(self, aConsequentOf):
        wasAdded = False
        if (aConsequentOf) in self._consequentOf :
            return False
        existingConsequent = aConsequentOf.getConsequent()
        isNewConsequent = not (existingConsequent is None) and not self == existingConsequent
        if isNewConsequent :
            aConsequentOf.setConsequent(self)
        else :
            self._consequentOf.append(aConsequentOf)
        wasAdded = True
        return wasAdded

    def removeConsequentOf(self, aConsequentOf):
        wasRemoved = False
        #Unable to remove aConsequentOf, as it must always have a consequent
        if not self == aConsequentOf.getConsequent() :
            self._consequentOf.remove(aConsequentOf)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addConsequentOfAt(self, aConsequentOf, index):
        wasAdded = False
        if self.addConsequentOf(aConsequentOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfConsequentOf() :
                index = self.numberOfConsequentOf() - 1
            self._consequentOf.remove(aConsequentOf)
            self._consequentOf.insert(index, aConsequentOf)
            wasAdded = True
        return wasAdded

    def addOrMoveConsequentOfAt(self, aConsequentOf, index):
        wasAdded = False
        if (aConsequentOf) in self._consequentOf :
            if index < 0 :
                index = 0
            if index > self.numberOfConsequentOf() :
                index = self.numberOfConsequentOf() - 1
            self._consequentOf.remove(aConsequentOf)
            self._consequentOf.insert(index, aConsequentOf)
            wasAdded = True
        else :
            wasAdded = self.addConsequentOfAt(aConsequentOf, index)
        return wasAdded

    def delete(self):
        i = len(self._antecedentOf)
        while i > 0 :
            aAntecedentOf = self._antecedentOf[i - 1]
            aAntecedentOf.delete()
            i -= 1

        i = len(self._consequentOf)
        while i > 0 :
            aConsequentOf = self._consequentOf[i - 1]
            aConsequentOf.delete()
            i -= 1

        super().delete()

    def getAntecedentOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getAntecedentOf1(argv[0])
        if len(argv) == 0 :
            return self.getAntecedentOf2()
        raise TypeError("No method matches provided parameters")

    def getConsequentOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getConsequentOf1(argv[0])
        if len(argv) == 0 :
            return self.getConsequentOf2()
        raise TypeError("No method matches provided parameters")

    def addAntecedentOf(self, *argv):
        from .Contract import Contract
        from .Role import Role
        from .LegalPosition import LegalPosition
        if len(argv) == 5 and isinstance(argv[0], str) and isinstance(argv[1], LegalSituation) and isinstance(argv[2], Contract) and isinstance(argv[3], Role) and isinstance(argv[4], Role) :
            return self.addAntecedentOf1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], LegalPosition) :
            return self.addAntecedentOf2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addConsequentOf(self, *argv):
        from .Contract import Contract
        from .Role import Role
        from .LegalPosition import LegalPosition
        if len(argv) == 5 and isinstance(argv[0], str) and isinstance(argv[1], LegalSituation) and isinstance(argv[2], Contract) and isinstance(argv[3], Role) and isinstance(argv[4], Role) :
            return self.addConsequentOf1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], LegalPosition) :
            return self.addConsequentOf2(argv[0])
        raise TypeError("No method matches provided parameters")
