# %% NEW FILE Role BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 20 "model.ump"
import os

class Role():
    rolesById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Role Attributes
    #Role Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aContract):
        self._contract = None
        self._party = None
        self._credit = None
        self._debt = None
        self._id = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._debt = []
        self._credit = []
        didAddContract = self.setContract(aContract)
        if not didAddContract :
            raise RuntimeError ("Unable to create role due to contract. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Role.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Role.rolesById.pop(anOldId, None)
        Role.rolesById[aId] = self
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return Role.rolesById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (Role.getWithId(aId) is None)

    # Code from template association_GetMany
    def getDebt1(self, index):
        aDebt = self._debt[index]
        return aDebt

    def getDebt2(self):
        newDebt = tuple(self._debt)
        return newDebt

    def numberOfDebt(self):
        number = len(self._debt)
        return number

    def hasDebt(self):
        has = len(self._debt) > 0
        return has

    def indexOfDebt(self, aDebt):
        index = (-1 if not aDebt in self._debt else self._debt.index(aDebt))
        return index

    # Code from template association_GetMany
    def getCredit1(self, index):
        aCredit = self._credit[index]
        return aCredit

    def getCredit2(self):
        newCredit = tuple(self._credit)
        return newCredit

    def numberOfCredit(self):
        number = len(self._credit)
        return number

    def hasCredit(self):
        has = len(self._credit) > 0
        return has

    def indexOfCredit(self, aCredit):
        index = (-1 if not aCredit in self._credit else self._credit.index(aCredit))
        return index

    # Code from template association_GetOne
    def getParty(self):
        return self._party

    def hasParty(self):
        has = not (self._party is None)
        return has

    # Code from template association_GetOne
    def getContract(self):
        return self._contract

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfDebt():
        return 0

    # Code from template association_AddManyToOne
    def addDebt1(self, aName, aAntecedent, aConsequent, aContract, aCreditor):
        from .LegalPosition import LegalPosition
        return LegalPosition(aName, aAntecedent, aConsequent, aContract, self, aCreditor)

    def addDebt2(self, aDebt):
        wasAdded = False
        if (aDebt) in self._debt :
            return False
        existingDebtor = aDebt.getDebtor()
        isNewDebtor = not (existingDebtor is None) and not self == existingDebtor
        if isNewDebtor :
            aDebt.setDebtor(self)
        else :
            self._debt.append(aDebt)
        wasAdded = True
        return wasAdded

    def removeDebt(self, aDebt):
        wasRemoved = False
        #Unable to remove aDebt, as it must always have a debtor
        if not self == aDebt.getDebtor() :
            self._debt.remove(aDebt)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addDebtAt(self, aDebt, index):
        wasAdded = False
        if self.addDebt(aDebt) :
            if index < 0 :
                index = 0
            if index > self.numberOfDebt() :
                index = self.numberOfDebt() - 1
            self._debt.remove(aDebt)
            self._debt.insert(index, aDebt)
            wasAdded = True
        return wasAdded

    def addOrMoveDebtAt(self, aDebt, index):
        wasAdded = False
        if (aDebt) in self._debt :
            if index < 0 :
                index = 0
            if index > self.numberOfDebt() :
                index = self.numberOfDebt() - 1
            self._debt.remove(aDebt)
            self._debt.insert(index, aDebt)
            wasAdded = True
        else :
            wasAdded = self.addDebtAt(aDebt, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfCredit():
        return 0

    # Code from template association_AddManyToOne
    def addCredit1(self, aName, aAntecedent, aConsequent, aContract, aDebtor):
        from .LegalPosition import LegalPosition
        return LegalPosition(aName, aAntecedent, aConsequent, aContract, aDebtor, self)

    def addCredit2(self, aCredit):
        wasAdded = False
        if (aCredit) in self._credit :
            return False
        existingCreditor = aCredit.getCreditor()
        isNewCreditor = not (existingCreditor is None) and not self == existingCreditor
        if isNewCreditor :
            aCredit.setCreditor(self)
        else :
            self._credit.append(aCredit)
        wasAdded = True
        return wasAdded

    def removeCredit(self, aCredit):
        wasRemoved = False
        #Unable to remove aCredit, as it must always have a creditor
        if not self == aCredit.getCreditor() :
            self._credit.remove(aCredit)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addCreditAt(self, aCredit, index):
        wasAdded = False
        if self.addCredit(aCredit) :
            if index < 0 :
                index = 0
            if index > self.numberOfCredit() :
                index = self.numberOfCredit() - 1
            self._credit.remove(aCredit)
            self._credit.insert(index, aCredit)
            wasAdded = True
        return wasAdded

    def addOrMoveCreditAt(self, aCredit, index):
        wasAdded = False
        if (aCredit) in self._credit :
            if index < 0 :
                index = 0
            if index > self.numberOfCredit() :
                index = self.numberOfCredit() - 1
            self._credit.remove(aCredit)
            self._credit.insert(index, aCredit)
            wasAdded = True
        else :
            wasAdded = self.addCreditAt(aCredit, index)
        return wasAdded

    # Code from template association_SetOptionalOneToMandatoryMany
    def setParty(self, aParty):
        #
        # This source of this source generation is association_SetOptionalOneToMandatoryMany.jet
        # This set file assumes the generation of a maximumNumberOfXXX method does not exist because
        # it's not required (No upper bound)
        #
        wasSet = False
        existingParty = self._party
        if existingParty is None :
            if not (aParty is None) :
                if aParty.addRole(self) :
                    existingParty = aParty
                    wasSet = True
        elif not (existingParty is None) :
            if aParty is None :
                if existingParty.minimumNumberOfRoles() < existingParty.numberOfRoles() :
                    existingParty.removeRole(self)
                    existingParty = aParty
                    # aParty == null
                    wasSet = True
            else :
                if existingParty.minimumNumberOfRoles() < existingParty.numberOfRoles() :
                    existingParty.removeRole(self)
                    aParty.addRole(self)
                    existingParty = aParty
                    wasSet = True
        if wasSet :
            self._party = existingParty
        return wasSet

    # Code from template association_SetOneToMandatoryMany
    def setContract(self, aContract):
        from .Contract import Contract
        wasSet = False
        #Must provide contract to role
        if aContract is None :
            return wasSet
        if not (self._contract is None) and self._contract.numberOfRoles() <= Contract.minimumNumberOfRoles() :
            return wasSet
        existingContract = self._contract
        self._contract = aContract
        if not (existingContract is None) and not existingContract == aContract :
            didRemove = existingContract.removeRole(self)
            if not didRemove :
                self._contract = existingContract
                return wasSet
        self._contract.addRole(self)
        wasSet = True
        return wasSet

    def delete(self):
        Role.rolesById.pop(self.getId(), None)
        i = len(self._debt)
        while i > 0 :
            aDebt = self._debt[i - 1]
            aDebt.delete()
            i -= 1

        i = len(self._credit)
        while i > 0 :
            aCredit = self._credit[i - 1]
            aCredit.delete()
            i -= 1

        if not (self._party is None) :
            if self._party.numberOfRoles() <= 1 :
                self._party.delete()
            else :
                placeholderParty = self._party
                self._party = None
                placeholderParty.removeRole(self)
        placeholderContract = self._contract
        self._contract = None
        if not (placeholderContract is None) :
            placeholderContract.removeRole(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]" + str(os.linesep) + "  " + "party = " + str(((format(id(self.getParty()), "x")) if not (self.getParty() is None) else "null")) + str(os.linesep) + "  " + "contract = " + ((format(id(self.getContract()), "x")) if not (self.getContract() is None) else "null")

    def getDebt(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getDebt1(argv[0])
        if len(argv) == 0 :
            return self.getDebt2()
        raise TypeError("No method matches provided parameters")

    def getCredit(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getCredit1(argv[0])
        if len(argv) == 0 :
            return self.getCredit2()
        raise TypeError("No method matches provided parameters")

    def addDebt(self, *argv):
        from .Contract import Contract
        from .LegalPosition import LegalPosition
        from .LegalSituation import LegalSituation
        if len(argv) == 5 and isinstance(argv[0], str) and isinstance(argv[1], LegalSituation) and isinstance(argv[2], LegalSituation) and isinstance(argv[3], Contract) and isinstance(argv[4], Role) :
            return self.addDebt1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], LegalPosition) :
            return self.addDebt2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addCredit(self, *argv):
        from .Contract import Contract
        from .LegalPosition import LegalPosition
        from .LegalSituation import LegalSituation
        if len(argv) == 5 and isinstance(argv[0], str) and isinstance(argv[1], LegalSituation) and isinstance(argv[2], LegalSituation) and isinstance(argv[3], Contract) and isinstance(argv[4], Role) :
            return self.addCredit1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], LegalPosition) :
            return self.addCredit2(argv[0])
        raise TypeError("No method matches provided parameters")
