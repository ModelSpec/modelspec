# %% NEW FILE Party BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 16 "model.ump"

class Party():
    partysById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Party Attributes
    #Party Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, *allRoles):
        allRoles = list(allRoles)
        self._rightHolderOf = None
        self._liableOf = None
        self._performerOf = None
        self._assets = None
        self._roles = None
        self._contracts = None
        self._id = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._contracts = []
        self._roles = []
        didAddRoles = self.setRoles(*allRoles)
        if not didAddRoles :
            raise RuntimeError ("Unable to create Party, must have at least 1 roles. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._assets = []
        self._performerOf = []
        self._liableOf = []
        self._rightHolderOf = []

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Party.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Party.partysById.pop(anOldId, None)
        Party.partysById[aId] = self
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return Party.partysById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (Party.getWithId(aId) is None)

    # Code from template association_GetMany
    def getContract(self, index):
        aContract = self._contracts[index]
        return aContract

    def getContracts(self):
        newContracts = tuple(self._contracts)
        return newContracts

    def numberOfContracts(self):
        number = len(self._contracts)
        return number

    def hasContracts(self):
        has = len(self._contracts) > 0
        return has

    def indexOfContract(self, aContract):
        index = (-1 if not aContract in self._contracts else self._contracts.index(aContract))
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
    def getPerformerOf1(self, index):
        aPerformerOf = self._performerOf[index]
        return aPerformerOf

    def getPerformerOf2(self):
        newPerformerOf = tuple(self._performerOf)
        return newPerformerOf

    def numberOfPerformerOf(self):
        number = len(self._performerOf)
        return number

    def hasPerformerOf(self):
        has = len(self._performerOf) > 0
        return has

    def indexOfPerformerOf(self, aPerformerOf):
        index = (-1 if not aPerformerOf in self._performerOf else self._performerOf.index(aPerformerOf))
        return index

    # Code from template association_GetMany
    def getLiableOf1(self, index):
        aLiableOf = self._liableOf[index]
        return aLiableOf

    def getLiableOf2(self):
        newLiableOf = tuple(self._liableOf)
        return newLiableOf

    def numberOfLiableOf(self):
        number = len(self._liableOf)
        return number

    def hasLiableOf(self):
        has = len(self._liableOf) > 0
        return has

    def indexOfLiableOf(self, aLiableOf):
        index = (-1 if not aLiableOf in self._liableOf else self._liableOf.index(aLiableOf))
        return index

    # Code from template association_GetMany
    def getRightHolderOf1(self, index):
        aRightHolderOf = self._rightHolderOf[index]
        return aRightHolderOf

    def getRightHolderOf2(self):
        newRightHolderOf = tuple(self._rightHolderOf)
        return newRightHolderOf

    def numberOfRightHolderOf(self):
        number = len(self._rightHolderOf)
        return number

    def hasRightHolderOf(self):
        has = len(self._rightHolderOf) > 0
        return has

    def indexOfRightHolderOf(self, aRightHolderOf):
        index = (-1 if not aRightHolderOf in self._rightHolderOf else self._rightHolderOf.index(aRightHolderOf))
        return index

    # Code from template association_IsNumberOfValidMethod
    def isNumberOfContractsValid(self):
        isValid = self.numberOfContracts() >= Party.minimumNumberOfContracts()
        return isValid

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfContracts():
        return 1

    # Code from template association_AddManyToManyMethod
    def addContract(self, aContract):
        wasAdded = False
        if (aContract) in self._contracts :
            return False
        self._contracts.append(aContract)
        if aContract.indexOfParty(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aContract.addParty(self)
            if not wasAdded :
                self._contracts.remove(aContract)
        return wasAdded

    # Code from template association_AddMStarToMany
    def removeContract(self, aContract):
        wasRemoved = False
        if not (aContract) in self._contracts :
            return wasRemoved
        if self.numberOfContracts() <= Party.minimumNumberOfContracts() :
            return wasRemoved
        oldIndex = (-1 if not aContract in self._contracts else self._contracts.index(aContract))
        self._contracts.remove(oldIndex)
        if aContract.indexOfParty(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aContract.removeParty(self)
            if not wasRemoved :
                self._contracts.insert(oldIndex, aContract)
        return wasRemoved

    # Code from template association_SetMStarToMany
    def setContracts(self, *newContracts):
        newContracts = list(newContracts)
        wasSet = False
        verifiedContracts = []
        for aContract in newContracts:
            if (aContract) in verifiedContracts :
                continue
            verifiedContracts.append(aContract)

        if len(verifiedContracts) != len(newContracts) or len(verifiedContracts) < Party.minimumNumberOfContracts() :
            return wasSet
        oldContracts = self._contracts.copy()
        self._contracts.clear()
        for aNewContract in verifiedContracts:
            self._contracts.append(aNewContract)
            if (aNewContract) in oldContracts :
                oldContracts.remove(aNewContract)
            else :
                aNewContract.addParty(self)

        for anOldContract in oldContracts:
            anOldContract.removeParty(self)

        wasSet = True
        return wasSet

    # Code from template association_AddIndexControlFunctions
    def addContractAt(self, aContract, index):
        wasAdded = False
        if self.addContract(aContract) :
            if index < 0 :
                index = 0
            if index > self.numberOfContracts() :
                index = self.numberOfContracts() - 1
            self._contracts.remove(aContract)
            self._contracts.insert(index, aContract)
            wasAdded = True
        return wasAdded

    def addOrMoveContractAt(self, aContract, index):
        wasAdded = False
        if (aContract) in self._contracts :
            if index < 0 :
                index = 0
            if index > self.numberOfContracts() :
                index = self.numberOfContracts() - 1
            self._contracts.remove(aContract)
            self._contracts.insert(index, aContract)
            wasAdded = True
        else :
            wasAdded = self.addContractAt(aContract, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRoles():
        return 1

    # Code from template association_AddMNToOptionalOne
    def addRole(self, aRole):
        wasAdded = False
        if (aRole) in self._roles :
            return False
        existingParty = aRole.getParty()
        if not (existingParty is None) and existingParty.numberOfRoles() <= Party.minimumNumberOfRoles() :
            return wasAdded
        elif not (existingParty is None) :
            existingParty.roles.remove(aRole)
        self._roles.append(aRole)
        self.setParty(aRole, self)
        wasAdded = True
        return wasAdded

    def removeRole(self, aRole):
        wasRemoved = False
        if (aRole) in self._roles and self.numberOfRoles() > Party.minimumNumberOfRoles() :
            self._roles.remove(aRole)
            self.setParty(aRole, None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_SetMNToOptionalOne
    def setRoles(self, *newRoles):
        newRoles = list(newRoles)
        wasSet = False
        if len(newRoles) < Party.minimumNumberOfRoles() :
            return wasSet
        checkNewRoles = []
        partyToNewRoles = dict()
        for aRole in newRoles:
            if (aRole) in checkNewRoles :
                return wasSet
            elif not (aRole.getParty() is None) and not self == aRole.getParty() :
                existingParty = aRole.getParty()
                if not (existingParty) in partyToNewRoles :
                    partyToNewRoles[existingParty] = int(existingParty.numberOfRoles())
                currentCount = partyToNewRoles.get(existingParty)
                nextCount = currentCount - 1
                if nextCount < 1 :
                    return wasSet
                partyToNewRoles[existingParty] = int(nextCount)
            checkNewRoles.append(aRole)

        self._roles = list(filter(lambda a : not a in checkNewRoles, self._roles))
        for orphan in self._roles:
            self.setParty(orphan, None)

        self._roles.clear()
        for aRole in newRoles:
            if not (aRole.getParty() is None) :
                aRole.getParty().roles.remove(aRole)
            self.setParty(aRole, self)
            self._roles.append(aRole)

        wasSet = True
        return wasSet

    # Code from template association_GetPrivate
    def setParty(self, aRole, aParty):
        try :
            aRole._party = aParty
        except :
            raise RuntimeError ("Issue internally setting aParty to aRole")

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

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfAssets():
        return 0

    # Code from template association_AddManyToManyMethod
    def addAsset(self, aAsset):
        wasAdded = False
        if (aAsset) in self._assets :
            return False
        self._assets.append(aAsset)
        if aAsset.indexOfOwner(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aAsset.addOwner(self)
            if not wasAdded :
                self._assets.remove(aAsset)
        return wasAdded

    # Code from template association_RemoveMany
    def removeAsset(self, aAsset):
        wasRemoved = False
        if not (aAsset) in self._assets :
            return wasRemoved
        oldIndex = (-1 if not aAsset in self._assets else self._assets.index(aAsset))
        self._assets.remove(oldIndex)
        if aAsset.indexOfOwner(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aAsset.removeOwner(self)
            if not wasRemoved :
                self._assets.insert(oldIndex, aAsset)
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
    def minimumNumberOfPerformerOf():
        return 0

    # Code from template association_AddManyToManyMethod
    def addPerformerOf(self, aPerformerOf):
        wasAdded = False
        if (aPerformerOf) in self._performerOf :
            return False
        self._performerOf.append(aPerformerOf)
        if aPerformerOf.indexOfPerformer(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aPerformerOf.addPerformer(self)
            if not wasAdded :
                self._performerOf.remove(aPerformerOf)
        return wasAdded

    # Code from template association_RemoveMany
    def removePerformerOf(self, aPerformerOf):
        wasRemoved = False
        if not (aPerformerOf) in self._performerOf :
            return wasRemoved
        oldIndex = (-1 if not aPerformerOf in self._performerOf else self._performerOf.index(aPerformerOf))
        self._performerOf.remove(oldIndex)
        if aPerformerOf.indexOfPerformer(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aPerformerOf.removePerformer(self)
            if not wasRemoved :
                self._performerOf.insert(oldIndex, aPerformerOf)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addPerformerOfAt(self, aPerformerOf, index):
        wasAdded = False
        if self.addPerformerOf(aPerformerOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfPerformerOf() :
                index = self.numberOfPerformerOf() - 1
            self._performerOf.remove(aPerformerOf)
            self._performerOf.insert(index, aPerformerOf)
            wasAdded = True
        return wasAdded

    def addOrMovePerformerOfAt(self, aPerformerOf, index):
        wasAdded = False
        if (aPerformerOf) in self._performerOf :
            if index < 0 :
                index = 0
            if index > self.numberOfPerformerOf() :
                index = self.numberOfPerformerOf() - 1
            self._performerOf.remove(aPerformerOf)
            self._performerOf.insert(index, aPerformerOf)
            wasAdded = True
        else :
            wasAdded = self.addPerformerOfAt(aPerformerOf, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfLiableOf():
        return 0

    # Code from template association_AddManyToManyMethod
    def addLiableOf(self, aLiableOf):
        wasAdded = False
        if (aLiableOf) in self._liableOf :
            return False
        self._liableOf.append(aLiableOf)
        if aLiableOf.indexOfLiable(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aLiableOf.addLiable(self)
            if not wasAdded :
                self._liableOf.remove(aLiableOf)
        return wasAdded

    # Code from template association_RemoveMany
    def removeLiableOf(self, aLiableOf):
        wasRemoved = False
        if not (aLiableOf) in self._liableOf :
            return wasRemoved
        oldIndex = (-1 if not aLiableOf in self._liableOf else self._liableOf.index(aLiableOf))
        self._liableOf.remove(oldIndex)
        if aLiableOf.indexOfLiable(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aLiableOf.removeLiable(self)
            if not wasRemoved :
                self._liableOf.insert(oldIndex, aLiableOf)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addLiableOfAt(self, aLiableOf, index):
        wasAdded = False
        if self.addLiableOf(aLiableOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfLiableOf() :
                index = self.numberOfLiableOf() - 1
            self._liableOf.remove(aLiableOf)
            self._liableOf.insert(index, aLiableOf)
            wasAdded = True
        return wasAdded

    def addOrMoveLiableOfAt(self, aLiableOf, index):
        wasAdded = False
        if (aLiableOf) in self._liableOf :
            if index < 0 :
                index = 0
            if index > self.numberOfLiableOf() :
                index = self.numberOfLiableOf() - 1
            self._liableOf.remove(aLiableOf)
            self._liableOf.insert(index, aLiableOf)
            wasAdded = True
        else :
            wasAdded = self.addLiableOfAt(aLiableOf, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfRightHolderOf():
        return 0

    # Code from template association_AddManyToManyMethod
    def addRightHolderOf(self, aRightHolderOf):
        wasAdded = False
        if (aRightHolderOf) in self._rightHolderOf :
            return False
        self._rightHolderOf.append(aRightHolderOf)
        if aRightHolderOf.indexOfRightHolder(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aRightHolderOf.addRightHolder(self)
            if not wasAdded :
                self._rightHolderOf.remove(aRightHolderOf)
        return wasAdded

    # Code from template association_RemoveMany
    def removeRightHolderOf(self, aRightHolderOf):
        wasRemoved = False
        if not (aRightHolderOf) in self._rightHolderOf :
            return wasRemoved
        oldIndex = (-1 if not aRightHolderOf in self._rightHolderOf else self._rightHolderOf.index(aRightHolderOf))
        self._rightHolderOf.remove(oldIndex)
        if aRightHolderOf.indexOfRightHolder(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aRightHolderOf.removeRightHolder(self)
            if not wasRemoved :
                self._rightHolderOf.insert(oldIndex, aRightHolderOf)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addRightHolderOfAt(self, aRightHolderOf, index):
        wasAdded = False
        if self.addRightHolderOf(aRightHolderOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfRightHolderOf() :
                index = self.numberOfRightHolderOf() - 1
            self._rightHolderOf.remove(aRightHolderOf)
            self._rightHolderOf.insert(index, aRightHolderOf)
            wasAdded = True
        return wasAdded

    def addOrMoveRightHolderOfAt(self, aRightHolderOf, index):
        wasAdded = False
        if (aRightHolderOf) in self._rightHolderOf :
            if index < 0 :
                index = 0
            if index > self.numberOfRightHolderOf() :
                index = self.numberOfRightHolderOf() - 1
            self._rightHolderOf.remove(aRightHolderOf)
            self._rightHolderOf.insert(index, aRightHolderOf)
            wasAdded = True
        else :
            wasAdded = self.addRightHolderOfAt(aRightHolderOf, index)
        return wasAdded

    def delete(self):
        from .Contract import Contract
        Party.partysById.pop(self.getId(), None)
        copyOfContracts = self._contracts.copy()
        self._contracts.clear()
        for aContract in copyOfContracts:
            if aContract.numberOfParties() <= Contract.minimumNumberOfParties() :
                aContract.delete()
            else :
                aContract.removeParty(self)

        for aRole in self._roles:
            self.setParty(aRole, None)

        self._roles.clear()
        copyOfAssets = self._assets.copy()
        self._assets.clear()
        for aAsset in copyOfAssets:
            aAsset.removeOwner(self)

        copyOfPerformerOf = self._performerOf.copy()
        self._performerOf.clear()
        for aPerformerOf in copyOfPerformerOf:
            aPerformerOf.removePerformer(self)

        copyOfLiableOf = self._liableOf.copy()
        self._liableOf.clear()
        for aLiableOf in copyOfLiableOf:
            aLiableOf.removeLiable(self)

        copyOfRightHolderOf = self._rightHolderOf.copy()
        self._rightHolderOf.clear()
        for aRightHolderOf in copyOfRightHolderOf:
            aRightHolderOf.removeRightHolder(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]"

    def getPerformerOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getPerformerOf1(argv[0])
        if len(argv) == 0 :
            return self.getPerformerOf2()
        raise TypeError("No method matches provided parameters")

    def getLiableOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getLiableOf1(argv[0])
        if len(argv) == 0 :
            return self.getLiableOf2()
        raise TypeError("No method matches provided parameters")

    def getRightHolderOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getRightHolderOf1(argv[0])
        if len(argv) == 0 :
            return self.getRightHolderOf2()
        raise TypeError("No method matches provided parameters")
