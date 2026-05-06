# %% NEW FILE Contract BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
import os
from enum import Enum, auto

class Contract():
    contractsById = dict()
    #------------------------
    # ENUMERATIONS
    #------------------------
    class ContractStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Form = auto()
        Active = auto()
        SuccessfulTermination = auto()
        UnsuccessfulTermination = auto()

    class ContractStatusActive(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Null = auto()
        InEffect = auto()
        Suspension = auto()
        Unassign = auto()
        Rescission = auto()

    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Contract Attributes
    #Contract Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId):
        self._parentContract = None
        self._terminators = None
        self._subContracts = None
        self._assets = None
        self._parties = None
        self._roles = None
        self._legalPositions = None
        self._statusActive = None
        self._status = None
        self._id = None
        self.resetStatus()
        self.resetStatusActive()
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._legalPositions = []
        self._roles = []
        self._parties = []
        self._assets = []
        self._subContracts = []
        self._terminators = []

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Contract.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Contract.contractsById.pop(anOldId, None)
        Contract.contractsById[aId] = self
        return wasSet

    # Code from template attribute_SetDefaulted
    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def resetStatus(self):
        wasReset = False
        self._status = self.getDefaultStatus()
        wasReset = True
        return wasReset

    # Code from template attribute_SetDefaulted
    def setStatusActive(self, aStatusActive):
        wasSet = False
        self._statusActive = aStatusActive
        wasSet = True
        return wasSet

    def resetStatusActive(self):
        wasReset = False
        self._statusActive = self.getDefaultStatusActive()
        wasReset = True
        return wasReset

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return Contract.contractsById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (Contract.getWithId(aId) is None)

    def getStatus(self):
        return self._status

    # Code from template attribute_GetDefaulted
    def getDefaultStatus(self):
        return Contract.ContractStatus.Form

    def getStatusActive(self):
        return self._statusActive

    # Code from template attribute_GetDefaulted
    def getDefaultStatusActive(self):
        return Contract.ContractStatusActive.Null

    # Code from template association_GetMany
    def getLegalPosition(self, index):
        aLegalPosition = self._legalPositions[index]
        return aLegalPosition

    def getLegalPositions(self):
        newLegalPositions = tuple(self._legalPositions)
        return newLegalPositions

    def numberOfLegalPositions(self):
        number = len(self._legalPositions)
        return number

    def hasLegalPositions(self):
        has = len(self._legalPositions) > 0
        return has

    def indexOfLegalPosition(self, aLegalPosition):
        index = (-1 if not aLegalPosition in self._legalPositions else self._legalPositions.index(aLegalPosition))
        return index

    # Code from template association_GetMany
    def getRole(self, index):
        aRole = self._roles[index]
        return aRole

    def getRoles(self):
        newRoles = tuple(self._roles)
        return newRoles

    def numberOfRoles(self):
        number = len(self._roles)
        return number

    def hasRoles(self):
        has = len(self._roles) > 0
        return has

    def indexOfRole(self, aRole):
        index = (-1 if not aRole in self._roles else self._roles.index(aRole))
        return index

    # Code from template association_GetMany
    def getParty(self, index):
        aParty = self._parties[index]
        return aParty

    def getParties(self):
        newParties = tuple(self._parties)
        return newParties

    def numberOfParties(self):
        number = len(self._parties)
        return number

    def hasParties(self):
        has = len(self._parties) > 0
        return has

    def indexOfParty(self, aParty):
        index = (-1 if not aParty in self._parties else self._parties.index(aParty))
        return index

    # Code from template association_GetMany
    def getAsset(self, index):
        aAsset = self._assets[index]
        return aAsset

    def getAssets(self):
        newAssets = tuple(self._assets)
        return newAssets

    def numberOfAssets(self):
        number = len(self._assets)
        return number

    def hasAssets(self):
        has = len(self._assets) > 0
        return has

    def indexOfAsset(self, aAsset):
        index = (-1 if not aAsset in self._assets else self._assets.index(aAsset))
        return index

    # Code from template association_GetMany
    def getSubContract(self, index):
        aSubContract = self._subContracts[index]
        return aSubContract

    def getSubContracts(self):
        newSubContracts = tuple(self._subContracts)
        return newSubContracts

    def numberOfSubContracts(self):
        number = len(self._subContracts)
        return number

    def hasSubContracts(self):
        has = len(self._subContracts) > 0
        return has

    def indexOfSubContract(self, aSubContract):
        index = (-1 if not aSubContract in self._subContracts else self._subContracts.index(aSubContract))
        return index

    # Code from template association_GetMany
    def getTerminator(self, index):
        aTerminator = self._terminators[index]
        return aTerminator

    def getTerminators(self):
        newTerminators = tuple(self._terminators)
        return newTerminators

    def numberOfTerminators(self):
        number = len(self._terminators)
        return number

    def hasTerminators(self):
        has = len(self._terminators) > 0
        return has

    def indexOfTerminator(self, aTerminator):
        index = (-1 if not aTerminator in self._terminators else self._terminators.index(aTerminator))
        return index

    # Code from template association_GetOne
    def getParentContract(self):
        return self._parentContract

    def hasParentContract(self):
        has = not (self._parentContract is None)
        return has

    # Code from template association_IsNumberOfValidMethod
    def isNumberOfLegalPositionsValid(self):
        isValid = self.numberOfLegalPositions() >= Contract.minimumNumberOfLegalPositions()
        return isValid

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfLegalPositions():
        return 2

    # Code from template association_AddMandatoryManyToOne
    def addLegalPosition1(self, aName, aAntecedent, aConsequent, aDebtor, aCreditor):
        from .LegalPosition import LegalPosition
        aNewLegalPosition = LegalPosition(aName, aAntecedent, aConsequent, self, aDebtor, aCreditor)
        return aNewLegalPosition

    def addLegalPosition2(self, aLegalPosition):
        wasAdded = False
        if (aLegalPosition) in self._legalPositions :
            return False
        existingContract = aLegalPosition.getContract()
        isNewContract = not (existingContract is None) and not self == existingContract
        if isNewContract and existingContract.numberOfLegalPositions() <= Contract.minimumNumberOfLegalPositions() :
            return wasAdded
        if isNewContract :
            aLegalPosition.setContract(self)
        else :
            self._legalPositions.append(aLegalPosition)
        wasAdded = True
        return wasAdded

    def removeLegalPosition(self, aLegalPosition):
        wasRemoved = False
        #Unable to remove aLegalPosition, as it must always have a contract
        if self == aLegalPosition.getContract() :
            return wasRemoved
        #contract already at minimum (2)
        if self.numberOfLegalPositions() <= Contract.minimumNumberOfLegalPositions() :
            return wasRemoved
        self._legalPositions.remove(aLegalPosition)
        wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addLegalPositionAt(self, aLegalPosition, index):
        wasAdded = False
        if self.addLegalPosition(aLegalPosition) :
            if index < 0 :
                index = 0
            if index > self.numberOfLegalPositions() :
                index = self.numberOfLegalPositions() - 1
            self._legalPositions.remove(aLegalPosition)
            self._legalPositions.insert(index, aLegalPosition)
            wasAdded = True
        return wasAdded

    def addOrMoveLegalPositionAt(self, aLegalPosition, index):
        wasAdded = False
        if (aLegalPosition) in self._legalPositions :
            if index < 0 :
                index = 0
            if index > self.numberOfLegalPositions() :
                index = self.numberOfLegalPositions() - 1
            self._legalPositions.remove(aLegalPosition)
            self._legalPositions.insert(index, aLegalPosition)
            wasAdded = True
        else :
            wasAdded = self.addLegalPositionAt(aLegalPosition, index)
        return wasAdded

    # Code from template association_IsNumberOfValidMethod
    def isNumberOfRolesValid(self):
        isValid = self.numberOfRoles() >= Contract.minimumNumberOfRoles()
        return isValid

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRoles():
        return 2

    # Code from template association_AddMandatoryManyToOne
    def addRole1(self, aId):
        from .Role import Role
        aNewRole = Role(aId, self)
        return aNewRole

    def addRole2(self, aRole):
        wasAdded = False
        if (aRole) in self._roles :
            return False
        existingContract = aRole.getContract()
        isNewContract = not (existingContract is None) and not self == existingContract
        if isNewContract and existingContract.numberOfRoles() <= Contract.minimumNumberOfRoles() :
            return wasAdded
        if isNewContract :
            aRole.setContract(self)
        else :
            self._roles.append(aRole)
        wasAdded = True
        return wasAdded

    def removeRole(self, aRole):
        wasRemoved = False
        #Unable to remove aRole, as it must always have a contract
        if self == aRole.getContract() :
            return wasRemoved
        #contract already at minimum (2)
        if self.numberOfRoles() <= Contract.minimumNumberOfRoles() :
            return wasRemoved
        self._roles.remove(aRole)
        wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addRoleAt(self, aRole, index):
        wasAdded = False
        if self.addRole(aRole) :
            if index < 0 :
                index = 0
            if index > self.numberOfRoles() :
                index = self.numberOfRoles() - 1
            self._roles.remove(aRole)
            self._roles.insert(index, aRole)
            wasAdded = True
        return wasAdded

    def addOrMoveRoleAt(self, aRole, index):
        wasAdded = False
        if (aRole) in self._roles :
            if index < 0 :
                index = 0
            if index > self.numberOfRoles() :
                index = self.numberOfRoles() - 1
            self._roles.remove(aRole)
            self._roles.insert(index, aRole)
            wasAdded = True
        else :
            wasAdded = self.addRoleAt(aRole, index)
        return wasAdded

    # Code from template association_IsNumberOfValidMethod
    def isNumberOfPartiesValid(self):
        isValid = self.numberOfParties() >= Contract.minimumNumberOfParties()
        return isValid

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfParties():
        return 2

    # Code from template association_AddManyToManyMethod
    def addParty(self, aParty):
        wasAdded = False
        if (aParty) in self._parties :
            return False
        self._parties.append(aParty)
        if aParty.indexOfContract(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aParty.addContract(self)
            if not wasAdded :
                self._parties.remove(aParty)
        return wasAdded

    # Code from template association_AddMStarToMany
    def removeParty(self, aParty):
        wasRemoved = False
        if not (aParty) in self._parties :
            return wasRemoved
        if self.numberOfParties() <= Contract.minimumNumberOfParties() :
            return wasRemoved
        oldIndex = (-1 if not aParty in self._parties else self._parties.index(aParty))
        self._parties.remove(oldIndex)
        if aParty.indexOfContract(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aParty.removeContract(self)
            if not wasRemoved :
                self._parties.insert(oldIndex, aParty)
        return wasRemoved

    # Code from template association_SetMStarToMany
    def setParties(self, *newParties):
        newParties = list(newParties)
        wasSet = False
        verifiedParties = []
        for aParty in newParties:
            if (aParty) in verifiedParties :
                continue
            verifiedParties.append(aParty)

        if len(verifiedParties) != len(newParties) or len(verifiedParties) < Contract.minimumNumberOfParties() :
            return wasSet
        oldParties = self._parties.copy()
        self._parties.clear()
        for aNewParty in verifiedParties:
            self._parties.append(aNewParty)
            if (aNewParty) in oldParties :
                oldParties.remove(aNewParty)
            else :
                aNewParty.addContract(self)

        for anOldParty in oldParties:
            anOldParty.removeContract(self)

        wasSet = True
        return wasSet

    # Code from template association_AddIndexControlFunctions
    def addPartyAt(self, aParty, index):
        wasAdded = False
        if self.addParty(aParty) :
            if index < 0 :
                index = 0
            if index > self.numberOfParties() :
                index = self.numberOfParties() - 1
            self._parties.remove(aParty)
            self._parties.insert(index, aParty)
            wasAdded = True
        return wasAdded

    def addOrMovePartyAt(self, aParty, index):
        wasAdded = False
        if (aParty) in self._parties :
            if index < 0 :
                index = 0
            if index > self.numberOfParties() :
                index = self.numberOfParties() - 1
            self._parties.remove(aParty)
            self._parties.insert(index, aParty)
            wasAdded = True
        else :
            wasAdded = self.addPartyAt(aParty, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfAssets():
        return 0

    # Code from template association_AddManyToOne
    def addAsset1(self, aId):
        from .Asset import Asset
        return Asset(aId, self)

    def addAsset2(self, aAsset):
        wasAdded = False
        if (aAsset) in self._assets :
            return False
        existingContract = aAsset.getContract()
        isNewContract = not (existingContract is None) and not self == existingContract
        if isNewContract :
            aAsset.setContract(self)
        else :
            self._assets.append(aAsset)
        wasAdded = True
        return wasAdded

    def removeAsset(self, aAsset):
        wasRemoved = False
        #Unable to remove aAsset, as it must always have a contract
        if not self == aAsset.getContract() :
            self._assets.remove(aAsset)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addAssetAt(self, aAsset, index):
        wasAdded = False
        if self.addAsset(aAsset) :
            if index < 0 :
                index = 0
            if index > self.numberOfAssets() :
                index = self.numberOfAssets() - 1
            self._assets.remove(aAsset)
            self._assets.insert(index, aAsset)
            wasAdded = True
        return wasAdded

    def addOrMoveAssetAt(self, aAsset, index):
        wasAdded = False
        if (aAsset) in self._assets :
            if index < 0 :
                index = 0
            if index > self.numberOfAssets() :
                index = self.numberOfAssets() - 1
            self._assets.remove(aAsset)
            self._assets.insert(index, aAsset)
            wasAdded = True
        else :
            wasAdded = self.addAssetAt(aAsset, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfSubContracts():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addSubContract(self, aSubContract):
        wasAdded = False
        if (aSubContract) in self._subContracts :
            return False
        existingParentContract = aSubContract.getParentContract()
        if existingParentContract is None :
            aSubContract.setParentContract(self)
        elif not self == existingParentContract :
            existingParentContract.removeSubContract(aSubContract)
            self.addSubContract(aSubContract)
        else :
            self._subContracts.append(aSubContract)
        wasAdded = True
        return wasAdded

    def removeSubContract(self, aSubContract):
        wasRemoved = False
        if (aSubContract) in self._subContracts :
            self._subContracts.remove(aSubContract)
            aSubContract.setParentContract(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addSubContractAt(self, aSubContract, index):
        wasAdded = False
        if self.addSubContract(aSubContract) :
            if index < 0 :
                index = 0
            if index > self.numberOfSubContracts() :
                index = self.numberOfSubContracts() - 1
            self._subContracts.remove(aSubContract)
            self._subContracts.insert(index, aSubContract)
            wasAdded = True
        return wasAdded

    def addOrMoveSubContractAt(self, aSubContract, index):
        wasAdded = False
        if (aSubContract) in self._subContracts :
            if index < 0 :
                index = 0
            if index > self.numberOfSubContracts() :
                index = self.numberOfSubContracts() - 1
            self._subContracts.remove(aSubContract)
            self._subContracts.insert(index, aSubContract)
            wasAdded = True
        else :
            wasAdded = self.addSubContractAt(aSubContract, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfTerminators():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addTerminator(self, aTerminator):
        wasAdded = False
        if (aTerminator) in self._terminators :
            return False
        existingTerminated = aTerminator.getTerminated()
        if existingTerminated is None :
            aTerminator.setTerminated(self)
        elif not self == existingTerminated :
            existingTerminated.removeTerminator(aTerminator)
            self.addTerminator(aTerminator)
        else :
            self._terminators.append(aTerminator)
        wasAdded = True
        return wasAdded

    def removeTerminator(self, aTerminator):
        wasRemoved = False
        if (aTerminator) in self._terminators :
            self._terminators.remove(aTerminator)
            aTerminator.setTerminated(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addTerminatorAt(self, aTerminator, index):
        wasAdded = False
        if self.addTerminator(aTerminator) :
            if index < 0 :
                index = 0
            if index > self.numberOfTerminators() :
                index = self.numberOfTerminators() - 1
            self._terminators.remove(aTerminator)
            self._terminators.insert(index, aTerminator)
            wasAdded = True
        return wasAdded

    def addOrMoveTerminatorAt(self, aTerminator, index):
        wasAdded = False
        if (aTerminator) in self._terminators :
            if index < 0 :
                index = 0
            if index > self.numberOfTerminators() :
                index = self.numberOfTerminators() - 1
            self._terminators.remove(aTerminator)
            self._terminators.insert(index, aTerminator)
            wasAdded = True
        else :
            wasAdded = self.addTerminatorAt(aTerminator, index)
        return wasAdded

    # Code from template association_SetOptionalOneToMany
    def setParentContract(self, aParentContract):
        wasSet = False
        existingParentContract = self._parentContract
        self._parentContract = aParentContract
        if not (existingParentContract is None) and not existingParentContract == aParentContract :
            existingParentContract.removeSubContract(self)
        if not (aParentContract is None) :
            aParentContract.addSubContract(self)
        wasSet = True
        return wasSet

    def delete(self):
        from .Party import Party
        Contract.contractsById.pop(self.getId(), None)

        while len(self._legalPositions) > 0 :
            aLegalPosition = self._legalPositions[len(self._legalPositions) - 1]
            aLegalPosition.delete()
            self._legalPositions.remove(aLegalPosition)

        while len(self._roles) > 0 :
            aRole = self._roles[len(self._roles) - 1]
            aRole.delete()
            self._roles.remove(aRole)

        copyOfParties = self._parties.copy()
        self._parties.clear()
        for aParty in copyOfParties:
            if aParty.numberOfContracts() <= Party.minimumNumberOfContracts() :
                aParty.delete()
            else :
                aParty.removeContract(self)

        i = len(self._assets)
        while i > 0 :
            aAsset = self._assets[i - 1]
            aAsset.delete()
            i -= 1

        while not self._subContracts.isEmpty() :
            self._subContracts[0].setParentContract(None)

        while not self._terminators.isEmpty() :
            self._terminators[0].setTerminated(None)

        if not (self._parentContract is None) :
            placeholderParentContract = self._parentContract
            self._parentContract = None
            placeholderParentContract.removeSubContract(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]" + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "statusActive" + "=" + (((self.getStatusActive().__str__().replaceAll("  ", "    ")) if not self.getStatusActive() == self else "this") if not (self.getStatusActive() is None) else "null")

    def addLegalPosition(self, *argv):
        from .LegalSituation import LegalSituation
        from .Role import Role
        from .LegalPosition import LegalPosition
        if len(argv) == 5 and isinstance(argv[0], str) and isinstance(argv[1], LegalSituation) and isinstance(argv[2], LegalSituation) and isinstance(argv[3], Role) and isinstance(argv[4], Role) :
            return self.addLegalPosition1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], LegalPosition) :
            return self.addLegalPosition2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addRole(self, *argv):
        from .Role import Role
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addRole1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Role) :
            return self.addRole2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addAsset(self, *argv):
        from .Asset import Asset
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addAsset1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Asset) :
            return self.addAsset2(argv[0])
        raise TypeError("No method matches provided parameters")
