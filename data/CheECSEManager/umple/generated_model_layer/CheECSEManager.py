#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 4 "../model.ump"
# line 154 "../model.ump"

class CheECSEManager():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #CheECSEManager Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._robot = None
        self._companies = None
        self._transactions = None
        self._cheeseWheels = None
        self._shelves = None
        self._farmers = None
        self._manager = None
        self._farmers = []
        self._shelves = []
        self._cheeseWheels = []
        self._transactions = []
        self._companies = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getManager(self):
        return self._manager

    def hasManager(self):
        has = not (self._manager is None)
        return has

    # Code from template association_GetMany 
    def getFarmer(self, index):
        aFarmer = self._farmers[index]
        return aFarmer

    def getFarmers(self):
        newFarmers = tuple(self._farmers)
        return newFarmers

    def numberOfFarmers(self):
        number = len(self._farmers)
        return number

    def hasFarmers(self):
        has = len(self._farmers) > 0
        return has

    def indexOfFarmer(self, aFarmer):
        index = (-1 if not aFarmer in self._farmers else self._farmers.index(aFarmer))
        return index

    # Code from template association_GetMany 
    def getShelve(self, index):
        aShelve = self._shelves[index]
        return aShelve

    def getShelves(self):
        newShelves = tuple(self._shelves)
        return newShelves

    def numberOfShelves(self):
        number = len(self._shelves)
        return number

    def hasShelves(self):
        has = len(self._shelves) > 0
        return has

    def indexOfShelve(self, aShelve):
        index = (-1 if not aShelve in self._shelves else self._shelves.index(aShelve))
        return index

    # Code from template association_GetMany 
    def getCheeseWheel(self, index):
        aCheeseWheel = self._cheeseWheels[index]
        return aCheeseWheel

    def getCheeseWheels(self):
        newCheeseWheels = tuple(self._cheeseWheels)
        return newCheeseWheels

    def numberOfCheeseWheels(self):
        number = len(self._cheeseWheels)
        return number

    def hasCheeseWheels(self):
        has = len(self._cheeseWheels) > 0
        return has

    def indexOfCheeseWheel(self, aCheeseWheel):
        index = (-1 if not aCheeseWheel in self._cheeseWheels else self._cheeseWheels.index(aCheeseWheel))
        return index

    # Code from template association_GetMany 
    def getTransaction(self, index):
        aTransaction = self._transactions[index]
        return aTransaction

    def getTransactions(self):
        newTransactions = tuple(self._transactions)
        return newTransactions

    def numberOfTransactions(self):
        number = len(self._transactions)
        return number

    def hasTransactions(self):
        has = len(self._transactions) > 0
        return has

    def indexOfTransaction(self, aTransaction):
        index = (-1 if not aTransaction in self._transactions else self._transactions.index(aTransaction))
        return index

    # Code from template association_GetMany 
    def getCompany(self, index):
        aCompany = self._companies[index]
        return aCompany

    def getCompanies(self):
        newCompanies = tuple(self._companies)
        return newCompanies

    def numberOfCompanies(self):
        number = len(self._companies)
        return number

    def hasCompanies(self):
        has = len(self._companies) > 0
        return has

    def indexOfCompany(self, aCompany):
        index = (-1 if not aCompany in self._companies else self._companies.index(aCompany))
        return index

    # Code from template association_GetOne 
    def getRobot(self):
        return self._robot

    def hasRobot(self):
        has = not (self._robot is None)
        return has

    # Code from template association_SetOptionalOneToOne 
    def setManager(self, aNewManager):
        wasSet = False
        if not (self._manager is None) and not self._manager == aNewManager and self == self._manager.getCheECSEManager() :
            #Unable to setManager, as existing manager would become an orphan
            return wasSet
        self._manager = aNewManager
        anOldCheECSEManager = (aNewManager.getCheECSEManager()) if not (aNewManager is None) else None
        if not self == anOldCheECSEManager :
            if not (anOldCheECSEManager is None) :
                anOldCheECSEManager.manager = None
            if not (self._manager is None) :
                self._manager.setCheECSEManager(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfFarmers():
        return 0

    # Code from template association_AddManyToOne 
    def addFarmer1(self, aEmail, aPassword, aAddress):
        from ..generated_model_layer import Farmer
        return Farmer(aEmail, aPassword, aAddress, self)

    def addFarmer2(self, aFarmer):
        wasAdded = False
        if (aFarmer) in self._farmers :
            return False
        existingCheECSEManager = aFarmer.getCheECSEManager()
        isNewCheECSEManager = not (existingCheECSEManager is None) and not self == existingCheECSEManager
        if isNewCheECSEManager :
            aFarmer.setCheECSEManager(self)
        else :
            self._farmers.append(aFarmer)
        wasAdded = True
        return wasAdded

    def removeFarmer(self, aFarmer):
        wasRemoved = False
        #Unable to remove aFarmer, as it must always have a cheECSEManager
        if not self == aFarmer.getCheECSEManager() :
            self._farmers.remove(aFarmer)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addFarmerAt(self, aFarmer, index):
        wasAdded = False
        if self.addFarmer(aFarmer) :
            if index < 0 :
                index = 0
            if index > self.numberOfFarmers() :
                index = self.numberOfFarmers() - 1
            self._farmers.remove(aFarmer)
            self._farmers.insert(index, aFarmer)
            wasAdded = True
        return wasAdded

    def addOrMoveFarmerAt(self, aFarmer, index):
        wasAdded = False
        if (aFarmer) in self._farmers :
            if index < 0 :
                index = 0
            if index > self.numberOfFarmers() :
                index = self.numberOfFarmers() - 1
            self._farmers.remove(aFarmer)
            self._farmers.insert(index, aFarmer)
            wasAdded = True
        else :
            wasAdded = self.addFarmerAt(aFarmer, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfShelves():
        return 0

    # Code from template association_AddManyToOne 
    def addShelve1(self, aId):
        from ..generated_model_layer.Shelf import Shelf
        return Shelf(aId, self)

    def addShelve2(self, aShelve):
        wasAdded = False
        if (aShelve) in self._shelves :
            return False
        existingCheECSEManager = aShelve.getCheECSEManager()
        isNewCheECSEManager = not (existingCheECSEManager is None) and not self == existingCheECSEManager
        if isNewCheECSEManager :
            aShelve.setCheECSEManager(self)
        else :
            self._shelves.append(aShelve)
        wasAdded = True
        return wasAdded

    def removeShelve(self, aShelve):
        wasRemoved = False
        #Unable to remove aShelve, as it must always have a cheECSEManager
        if not self == aShelve.getCheECSEManager() :
            self._shelves.remove(aShelve)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addShelveAt(self, aShelve, index):
        wasAdded = False
        if self.addShelve(aShelve) :
            if index < 0 :
                index = 0
            if index > self.numberOfShelves() :
                index = self.numberOfShelves() - 1
            self._shelves.remove(aShelve)
            self._shelves.insert(index, aShelve)
            wasAdded = True
        return wasAdded

    def addOrMoveShelveAt(self, aShelve, index):
        wasAdded = False
        if (aShelve) in self._shelves :
            if index < 0 :
                index = 0
            if index > self.numberOfShelves() :
                index = self.numberOfShelves() - 1
            self._shelves.remove(aShelve)
            self._shelves.insert(index, aShelve)
            wasAdded = True
        else :
            wasAdded = self.addShelveAt(aShelve, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfCheeseWheels():
        return 0

    # Code from template association_AddManyToOne 
    def addCheeseWheel1(self, aMonthsAged, aIsSpoiled, aPurchase):
        from ..generated_model_layer.CheeseWheel import CheeseWheel
        return CheeseWheel(aMonthsAged, aIsSpoiled, aPurchase, self)

    def addCheeseWheel2(self, aCheeseWheel):
        wasAdded = False
        if (aCheeseWheel) in self._cheeseWheels :
            return False
        existingCheECSEManager = aCheeseWheel.getCheECSEManager()
        isNewCheECSEManager = not (existingCheECSEManager is None) and not self == existingCheECSEManager
        if isNewCheECSEManager :
            aCheeseWheel.setCheECSEManager(self)
        else :
            self._cheeseWheels.append(aCheeseWheel)
        wasAdded = True
        return wasAdded

    def removeCheeseWheel(self, aCheeseWheel):
        wasRemoved = False
        #Unable to remove aCheeseWheel, as it must always have a cheECSEManager
        if not self == aCheeseWheel.getCheECSEManager() :
            self._cheeseWheels.remove(aCheeseWheel)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addCheeseWheelAt(self, aCheeseWheel, index):
        wasAdded = False
        if self.addCheeseWheel(aCheeseWheel) :
            if index < 0 :
                index = 0
            if index > self.numberOfCheeseWheels() :
                index = self.numberOfCheeseWheels() - 1
            self._cheeseWheels.remove(aCheeseWheel)
            self._cheeseWheels.insert(index, aCheeseWheel)
            wasAdded = True
        return wasAdded

    def addOrMoveCheeseWheelAt(self, aCheeseWheel, index):
        wasAdded = False
        if (aCheeseWheel) in self._cheeseWheels :
            if index < 0 :
                index = 0
            if index > self.numberOfCheeseWheels() :
                index = self.numberOfCheeseWheels() - 1
            self._cheeseWheels.remove(aCheeseWheel)
            self._cheeseWheels.insert(index, aCheeseWheel)
            wasAdded = True
        else :
            wasAdded = self.addCheeseWheelAt(aCheeseWheel, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfTransactions():
        return 0

    # Code from template association_AddManyToOne 
    def addTransaction(self, aTransaction):
        wasAdded = False
        if (aTransaction) in self._transactions :
            return False
        existingCheECSEManager = aTransaction.getCheECSEManager()
        isNewCheECSEManager = not (existingCheECSEManager is None) and not self == existingCheECSEManager
        if isNewCheECSEManager :
            aTransaction.setCheECSEManager(self)
        else :
            self._transactions.append(aTransaction)
        wasAdded = True
        return wasAdded

    def removeTransaction(self, aTransaction):
        wasRemoved = False
        #Unable to remove aTransaction, as it must always have a cheECSEManager
        if not self == aTransaction.getCheECSEManager() :
            self._transactions.remove(aTransaction)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addTransactionAt(self, aTransaction, index):
        wasAdded = False
        if self.addTransaction(aTransaction) :
            if index < 0 :
                index = 0
            if index > self.numberOfTransactions() :
                index = self.numberOfTransactions() - 1
            self._transactions.remove(aTransaction)
            self._transactions.insert(index, aTransaction)
            wasAdded = True
        return wasAdded

    def addOrMoveTransactionAt(self, aTransaction, index):
        wasAdded = False
        if (aTransaction) in self._transactions :
            if index < 0 :
                index = 0
            if index > self.numberOfTransactions() :
                index = self.numberOfTransactions() - 1
            self._transactions.remove(aTransaction)
            self._transactions.insert(index, aTransaction)
            wasAdded = True
        else :
            wasAdded = self.addTransactionAt(aTransaction, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfCompanies():
        return 0

    # Code from template association_AddManyToOne 
    def addCompany1(self, aName, aAddress):
        from ..generated_model_layer.WholesaleCompany import WholesaleCompany
        return WholesaleCompany(aName, aAddress, self)

    def addCompany2(self, aCompany):
        wasAdded = False
        if (aCompany) in self._companies :
            return False
        existingCheECSEManager = aCompany.getCheECSEManager()
        isNewCheECSEManager = not (existingCheECSEManager is None) and not self == existingCheECSEManager
        if isNewCheECSEManager :
            aCompany.setCheECSEManager(self)
        else :
            self._companies.append(aCompany)
        wasAdded = True
        return wasAdded

    def removeCompany(self, aCompany):
        wasRemoved = False
        #Unable to remove aCompany, as it must always have a cheECSEManager
        if not self == aCompany.getCheECSEManager() :
            self._companies.remove(aCompany)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addCompanyAt(self, aCompany, index):
        wasAdded = False
        if self.addCompany(aCompany) :
            if index < 0 :
                index = 0
            if index > self.numberOfCompanies() :
                index = self.numberOfCompanies() - 1
            self._companies.remove(aCompany)
            self._companies.insert(index, aCompany)
            wasAdded = True
        return wasAdded

    def addOrMoveCompanyAt(self, aCompany, index):
        wasAdded = False
        if (aCompany) in self._companies :
            if index < 0 :
                index = 0
            if index > self.numberOfCompanies() :
                index = self.numberOfCompanies() - 1
            self._companies.remove(aCompany)
            self._companies.insert(index, aCompany)
            wasAdded = True
        else :
            wasAdded = self.addCompanyAt(aCompany, index)
        return wasAdded

    # Code from template association_SetOptionalOneToOne 
    def setRobot(self, aNewRobot):
        wasSet = False
        if not (self._robot is None) and not self._robot == aNewRobot and self == self._robot.getCheECSEManager() :
            #Unable to setRobot, as existing robot would become an orphan
            return wasSet
        self._robot = aNewRobot
        anOldCheECSEManager = (aNewRobot.getCheECSEManager()) if not (aNewRobot is None) else None
        if not self == anOldCheECSEManager :
            if not (anOldCheECSEManager is None) :
                anOldCheECSEManager.robot = None
            if not (self._robot is None) :
                self._robot.setCheECSEManager(self)
        wasSet = True
        return wasSet

    def delete(self):
        existingManager = self._manager
        self._manager = None
        if not (existingManager is None) :
            existingManager.delete()
            existingManager.setCheECSEManager(None)

        while len(self._farmers) > 0 :
            aFarmer = self._farmers[len(self._farmers) - 1]
            aFarmer.delete()
            self._farmers.remove(aFarmer)

        while len(self._shelves) > 0 :
            aShelve = self._shelves[len(self._shelves) - 1]
            aShelve.delete()
            self._shelves.remove(aShelve)

        while len(self._cheeseWheels) > 0 :
            aCheeseWheel = self._cheeseWheels[len(self._cheeseWheels) - 1]
            aCheeseWheel.delete()
            self._cheeseWheels.remove(aCheeseWheel)

        while len(self._transactions) > 0 :
            aTransaction = self._transactions[len(self._transactions) - 1]
            aTransaction.delete()
            self._transactions.remove(aTransaction)

        while len(self._companies) > 0 :
            aCompany = self._companies[len(self._companies) - 1]
            aCompany.delete()
            self._companies.remove(aCompany)

        existingRobot = self._robot
        self._robot = None
        if not (existingRobot is None) :
            existingRobot.delete()
            existingRobot.setCheECSEManager(None)

    def addFarmer(self, *argv):
        from ..generated_model_layer.Farmer import Farmer
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) :
            return self.addFarmer1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Farmer) :
            return self.addFarmer2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addShelve(self, *argv):
        from ..generated_model_layer.Shelf import Shelf
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addShelve1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Shelf) :
            return self.addShelve2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addCheeseWheel(self, *argv):
        from ..generated_model_layer.CheeseWheel import CheeseWheel
        from ..generated_model_layer.Purchase import Purchase
        if len(argv) == 3 and isinstance(argv[0], CheeseWheel.MaturationPeriod) and isinstance(argv[1], bool) and isinstance(argv[2], Purchase) :
            return self.addCheeseWheel1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], CheeseWheel) :
            return self.addCheeseWheel2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addCompany(self, *argv):
        from ..generated_model_layer.WholesaleCompany import WholesaleCompany
        if len(argv) == 2 and isinstance(argv[0], str) and isinstance(argv[1], str) :
            return self.addCompany1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], WholesaleCompany) :
            return self.addCompany2(argv[0])
        raise TypeError("No method matches provided parameters")

