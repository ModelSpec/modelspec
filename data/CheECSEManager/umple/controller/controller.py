import calendar
from datetime import datetime
from typing import List

from ..generated_model_layer import *

class CheECSEManagerController:
    def __init__(self):
        self.cheECSEManager = CheECSEManager()

    def updateFacilityManager(self, password: str) -> None:
        error = isValidManagerPassword(password)
        if error != "":
            raise ValueError(error)
        manager = self.cheECSEManager.getManager()
        if manager is None:
            raise ValueError("Manager does not exist")
        manager.setPassword(password)
        return

    def addShelf(self, id: str, nrColumns: int, nrRows: int) -> None :
        if not id:
            raise ValueError("The id must be three characters long.")
        
        trimmedID = id.strip()
        if len(trimmedID) != 3:
            raise ValueError("The id must be three characters long.")
        if not trimmedID[0].isalpha():
            raise ValueError("The first character must be a letter.")
        if not trimmedID[1:].isdigit():
            raise ValueError("The second and third characters must be digits.")

        if Shelf.hasWithId(trimmedID):
            raise ValueError(f"The shelf {trimmedID} already exists.")

        if nrColumns < 1:
            raise ValueError("Number of columns must be greater than zero.")

        if nrRows < 1:
            raise ValueError("Number of rows must be greater than zero.")

        if nrRows > 10:
            raise ValueError("Number of rows must be at the most ten.")

        shelf = self.cheECSEManager.addShelve(trimmedID)
        for column in range(1, nrColumns + 1):
            for row in range(1, nrRows + 1):
                shelf.addLocation(column, row)
        return
   
    def deleteShelf(self, id: str) -> None:
        shelf = Shelf.getWithId(id)
        if shelf is None:
            raise ValueError(f"The shelf {id} does not exist.")

        if any(location.hasCheeseWheel() for location in shelf.getLocations()):
            raise ValueError("Cannot delete a shelf that contains cheese wheels.")

        # delete all locations first
        for location in shelf.getLocations():
            location.delete()
        self.cheECSEManager.removeShelve(shelf)
        shelf.delete()
        return
   
    def displayShelf(self, id: str) -> TOShelf:
        shelf = Shelf.getWithId(id)
        
        if shelf is None:
            return None

        shelfTO = TOShelf(shelf.getId())
        for loc in shelf.getLocations():
            if loc.getColumn() not in shelfTO.getColumnNrs():
                shelfTO.addColumnNr(loc.getColumn())
            if loc.getRow() not in shelfTO.getRowNrs():
                shelfTO.addRowNr(loc.getRow())
            if loc.hasCheeseWheel():
                cw = loc.getCheeseWheel()
                shelfTO.addCheeseWheelID(cw.getId())
                shelfTO.addMonthsAged(cw.getMonthsAged())
            else:
                shelfTO.addCheeseWheelID(None)
                shelfTO.addMonthsAged(None)
        return shelfTO
        
   # #returns all shelves
    def displayShelves(self) -> List[TOShelf]:
        shelves = self.cheECSEManager.getShelves()
        if len(shelves) == 0:
            return []

        shelfTOs = [] # list of TOShelf objects
        for shelf in shelves:
            shelfTO = TOShelf(shelf.getId())
            for loc in shelf.getLocations():
                if loc.getColumn() not in shelfTO.getColumnNrs():
                    shelfTO.addColumnNr(loc.getColumn())
                if loc.getRow() not in shelfTO.getRowNrs():
                    shelfTO.addRowNr(loc.getRow())
                if loc.hasCheeseWheel():
                    cw = loc.getCheeseWheel()
                    shelfTO.addCheeseWheelID(cw.getId())
                    shelfTO.addMonthsAged(cw.getMonthsAged())
                else:
                    shelfTO.addCheeseWheelID(None)
                    shelfTO.addMonthsAged(None)
            shelfTOs.append(shelfTO)
        return shelfTOs
   
    def registerFarmer(self, email: str, password: str, name: str, address: str) -> None:
        error = ""
        error += isValidFarmerPassword(password)
        error += isValidFarmer(email)
        if error != "":
            raise ValueError(error)
        if address is None or address == "":
            raise ValueError("Address must not be empty.")
        if User.getWithEmail(email) != None:
            raise ValueError("The farmer email already exists.")
        farmer = self.cheECSEManager.addFarmer(email, password, address)
        if name != None:
            farmer.setName(name)
        return

    def updateFarmer(self, email: str, newPassword: str, newName: str, newAddress: str) -> None:
        error = ""
        error += isValidFarmerPassword(newPassword)
        if error != "":
            raise ValueError(error)
        if newAddress is None or newAddress == "":
            raise ValueError("Address must not be empty.")
        farmer = User.getWithEmail(email)
        if not isinstance(farmer, Farmer):
            raise ValueError(f"The farmer with email {email} does not exist.")
        farmer.setPassword(newPassword)
        farmer.setName(newName)
        farmer.setAddress(newAddress)
        return

    def deleteFarmer(self, email: str) -> None:
        farmer = User.getWithEmail(email)
        if not isinstance(farmer, Farmer):
            raise ValueError(f"The farmer with email {email} does not exist.")
        if farmer.numberOfPurchases() != 0:
            raise ValueError("Cannot delete farmer who has supplied cheese.")
        farmer.delete()
        return
   
    def displayFarmer(self, email: str) -> TOFarmer:
        farmer = User.getWithEmail(email)
        if not isinstance(farmer, Farmer):
            return None
        farmerTO = TOFarmer(farmer.getEmail(), farmer.getPassword(), farmer.getName(), farmer.getAddress())
        for purchase in farmer.getPurchases():
            for cw in purchase.getCheeseWheels():
                farmerTO.addCheeseWheelID(cw.getId())
                farmerTO.addPurchaseDate(cw.getPurchase().getTransactionDate())
                farmerTO.addMonthsAged(cw.getMonthsAged())
                farmerTO.addIsSpoiled(cw.getIsSpoiled())
        return farmerTO

   # #returns all farmers
    def displayFarmers(self) -> List[TOFarmer]:
        farmers = self.cheECSEManager.getFarmers()
        if len(farmers) == 0:
            return []
        TOFarmers = []
        for farmer in farmers:
            farmerTO = TOFarmer(farmer.getEmail(), farmer.getPassword(), farmer.getName(), farmer.getAddress())
            for purchase in farmer.getPurchases():
                for cw in purchase.getCheeseWheels():
                    farmerTO.addCheeseWheelID(cw.getId())
                    farmerTO.addPurchaseDate(cw.getPurchase().getTransactionDate())
                    farmerTO.addMonthsAged(cw.getMonthsAged())
                    farmerTO.addIsSpoiled(cw.getIsSpoiled())
            TOFarmers.append(farmerTO)
        return TOFarmers

    def buyCheeseWheelsFromFarmer(self, emailFarmer: str, purchaseDate: datetime, nrCheeseWheels: int, monthsAged: str) -> None:
        # validate nrCheeseWheels (feature expects this exact message)
        if nrCheeseWheels is None or not isinstance(nrCheeseWheels, int) or nrCheeseWheels <= 0:
            raise ValueError("nrCheeseWheels must be greater than zero.")

        # validate monthsAged literal per feature
        allowed = [str(CheeseWheel.MaturationPeriod.Six), str(CheeseWheel.MaturationPeriod.Twelve), str(CheeseWheel.MaturationPeriod.TwentyFour), str(CheeseWheel.MaturationPeriod.ThirtySix)]
        if monthsAged not in allowed:
            raise ValueError("The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix.")

        # accept either a date object or an ISO date string
        if purchaseDate is None:
            raise ValueError("Invalid purchase date")

        farmer = User.getWithEmail(emailFarmer)
        if not isinstance(farmer, Farmer):
            raise ValueError(f"The farmer with email {emailFarmer} does not exist.")

        # Create a Purchase 
        # Farmer.addPurchase(transactionDate, cheECSEManager) -> Purchase
        purchase = farmer.addPurchase(purchaseDate, self.cheECSEManager)

        # Map literal monthsAged to CheeseWheel.MaturationPeriod enum
        maturation = CheeseWheel.MaturationPeriod[monthsAged]

        # Add the requested number of cheese wheels to the purchase
        for _ in range(nrCheeseWheels):
            purchase.addCheeseWheel(maturation, False, self.cheECSEManager)

        return

    def assignCheeseWheelToShelf(self, cheeseWheelID: int, shelfID: str, columnNr: int, rowNr: int) -> None:
        # Find shelf by id
        shelf = Shelf.getWithId(shelfID)
        if shelf is None:
            raise ValueError(f"The shelf with id {shelfID} does not exist.")

        # Check shelf has locations
        if not shelf.hasLocations():
            raise ValueError("The shelf has no locations.")

        # Find the target location by column and row
        targetLocation = None
        for loc in shelf.getLocations():
            if loc.getColumn() == columnNr and loc.getRow() == rowNr:
                targetLocation = loc
                break
        if targetLocation is None:
            raise ValueError("The shelf location does not exist.")

        # Check if location is already occupied
        if targetLocation.hasCheeseWheel():
            raise ValueError("The shelf location is already occupied.")

        cheese = None
        for cw in self.cheECSEManager.getCheeseWheels():
            if cw.getId() == cheeseWheelID:
                cheese = cw
                break
        if cheese is None:
            raise ValueError(f"The cheese wheel with id {cheeseWheelID} does not exist.")

        # Cannot place spoiled cheese
        if cheese.isIsSpoiled():
            raise ValueError("Cannot place a spoiled cheese wheel on a shelf.")

        # Assign cheese wheel to the location (model manages associations)
        targetLocation.setCheeseWheel(cheese)
        return

    def removeCheeseWheelFromShelf(self, cheeseWheelID: str) -> None:
        # Find cheese wheel by searching manager's cheese wheels
        cheese = None
        for cw in self.cheECSEManager.getCheeseWheels():
            if cw.getId() == cheeseWheelID:
                cheese = cw
                break
        if cheese is None:
            raise ValueError(f"The cheese wheel with id {cheeseWheelID} does not exist.")

        # Check if it's on a shelf/location
        if not cheese.hasLocation():
            raise ValueError("The cheese wheel is not on any shelf.")

        # Remove the cheese wheel from its current location
        cheese.setLocation(None)
        return 

    def updateCheeseWheel(self, cheeseWheelID: str, newMonthsAged: str, newIsSpoiled: bool) -> None:
        # validate monthsAged enum values
        validMonths = [str(CheeseWheel.MaturationPeriod.Six), str(CheeseWheel.MaturationPeriod.Twelve), str(CheeseWheel.MaturationPeriod.TwentyFour), str(CheeseWheel.MaturationPeriod.ThirtySix)]
        if newMonthsAged not in validMonths:
            raise ValueError("The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix.")

        # find the cheese wheel by ID
        cheeseWheel = None
        for wheel in self.cheECSEManager.getCheeseWheels():
            if wheel.getId() == int(cheeseWheelID):
                cheeseWheel = wheel
                break

        if cheeseWheel is None:
            raise ValueError(f"The cheese wheel with id {cheeseWheelID} does not exist.")

        # validate monthsAged - can only increase
        currentMonths = cheeseWheel.getMonthsAged()
        currentMonthsValue = validMonths.index(str(currentMonths))
        newMonthsValue = validMonths.index(newMonthsAged)
        if newMonthsValue < currentMonthsValue:
            raise ValueError("Cannot decrease the monthsAged of a cheese wheel.")

        # update the cheese wheel
        cheeseWheel.setMonthsAged(CheeseWheel.MaturationPeriod[newMonthsAged])
        cheeseWheel.setIsSpoiled(newIsSpoiled)
        transactions = self.cheECSEManager.getTransactions()
        if newIsSpoiled:
            cheeseWheel.setLocation(None)
            for order in transactions:
                if isinstance(order, Order) and cheeseWheel in order.getCheeseWheels():
                    order.removeCheeseWheel(cheeseWheel)
        for order in transactions:
            if isinstance(order, Order) and cheeseWheel.getMonthsAged() != order.getMonthsAged():
                order.removeCheeseWheel(cheeseWheel)

        return

    def displayCheeseWheel(self, cheeseWheelID: int) -> TOCheeseWheel:
        # find the cheese wheel by ID
        cheeseWheel = None
        for wheel in self.cheECSEManager.getCheeseWheels():
            if wheel.getId() == cheeseWheelID:
                cheeseWheel = wheel
                break
        if not cheeseWheel:
            return None

        # get purchase date
        purchaseDate = cheeseWheel.getPurchase().getTransactionDate()
        # get shelf information
        shelfID = None
        column = -1
        row = -1
        if cheeseWheel.hasLocation():
            location = cheeseWheel.getLocation()
            shelfID = location.getShelf().getId()
            column = location.getColumn()
            row = location.getRow()

        # check if cheese wheel is ordered
        isOrdered = cheeseWheel.hasOrder()

        # create TOCheeseWheel object
        cheeseWheelTO = TOCheeseWheel(aId=cheeseWheel.getId(), aMonthsAged=cheeseWheel.getMonthsAged(), aIsSpoiled=cheeseWheel.getIsSpoiled(), aPurchaseDate=purchaseDate, aShelfID=shelfID, aColumn=column, aRow=row, aIsOrdered=isOrdered)
        return cheeseWheelTO

    #returns all cheese wheels
    def displayCheeseWheels(self) -> List[TOCheeseWheel]:
        cheeseWheels = self.cheECSEManager.getCheeseWheels()
        if len(cheeseWheels) == 0:
            return []

        TOCheeseWheels = []
        for cheeseWheel in cheeseWheels:
            # get purchase date
            purchaseDate = cheeseWheel.getPurchase().getTransactionDate()

            # get shelf information
            shelfID = None
            column = -1
            row = -1
            if cheeseWheel.hasLocation():
                location = cheeseWheel.getLocation()
                shelfID = location.getShelf().getId()
                column = location.getColumn()
                row = location.getRow()

            # check if cheese wheel is ordered
            isOrdered = cheeseWheel.hasOrder()

            # create TOCheeseWheel object
            cheeseWheelTO = TOCheeseWheel(
                cheeseWheel.getId(),
                cheeseWheel.getMonthsAged(),
                cheeseWheel.getIsSpoiled(),
                purchaseDate,
                shelfID,
                column,
                row,
                isOrdered,
            )
            TOCheeseWheels.append(cheeseWheelTO)

        return TOCheeseWheels
   
    def sellCheeseWheelsToWholesaleCompany(self, nameCompany: str, orderDate: datetime, nrCheeseWheels: int, monthsAged: str, deliveryDate: datetime) -> None:
        # validate nrCheeseWheels
        if nrCheeseWheels is None or not isinstance(nrCheeseWheels, int) or nrCheeseWheels <= 0:
            raise ValueError("nrCheeseWheels must be greater than zero.")

        # validate monthsAged literal
        allowed = [str(CheeseWheel.MaturationPeriod.Six), str(CheeseWheel.MaturationPeriod.Twelve), str(CheeseWheel.MaturationPeriod.TwentyFour), str(CheeseWheel.MaturationPeriod.ThirtySix)]
        if monthsAged not in allowed:
            raise ValueError("The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix.")

        # parse/validate dates
        if orderDate is None:
            raise ValueError("Invalid order date")

        if deliveryDate is None:
            raise ValueError("Invalid delivery date")

        # delivery must be after order
        if deliveryDate < orderDate:
            raise ValueError("The delivery date must be on or after the transaction date.")

        company = WholesaleCompany.getWithName(nameCompany)
        if company is None:
            raise ValueError(f"The wholesale company {nameCompany} does not exist.")

        # create Order via company.addOrder(transactionDate, cheECSEManager, nrCheeseWheels, maturationEnum, deliveryDate)
        maturationEnum = CheeseWheel.MaturationPeriod[monthsAged]
        order = company.addOrder(orderDate, self.cheECSEManager, nrCheeseWheels, maturationEnum, deliveryDate)

        # select available cheese wheels from purchases (oldest purchases first)
        needed = nrCheeseWheels
        nrMonths = {"Six": 6, "Twelve": 12, "TwentyFour": 24, "ThirtySix": 36}[monthsAged]
        # manager.getTransactions() includes purchases and existing orders; filter Purchase instances
        transactions = list(self.cheECSEManager.getTransactions())
        transactions = sorted(transactions, key=lambda t: t.getTransactionDate())
        for tx in transactions:
            if not isinstance(tx, Purchase):
                continue
            purchase = tx
            # only cheese wheels that are mature by the delivery date are available
            purchaseDate = purchase.getTransactionDate()
            month = purchaseDate.month - 1 + nrMonths
            year = purchaseDate.year + month // 12
            month = month % 12 + 1
            day = min(purchaseDate.day, calendar.monthrange(year, month)[1])
            if purchaseDate.replace(year=year, month=month, day=day) > deliveryDate:
                continue
            # iterate cheese wheels in purchase
            for cheese in purchase.getCheeseWheels():
                if needed == 0:
                    break
                # match maturation and availability
                if cheese.getMonthsAged() == maturationEnum and not cheese.getIsSpoiled() and cheese.getOrder() is None:
                    order.addCheeseWheel(cheese)
                    needed -= 1
            if needed == 0:
                break

        return
   

    def addWholesaleCompany(self, name: str, address: str) -> None:
        if name is None or name == "":
            raise ValueError("Name must not be empty.")
        if address is None or address == "":
            raise ValueError("Address must not be empty.")
        for company in self.cheECSEManager.getCompanies():
            if company.getName() == name:
                raise ValueError("The wholesale company already exists.")
        self.cheECSEManager.addCompany(name, address)
        return

    def updateWholesaleCompany(self, name: str, newName: str, newAddress: str) -> None:
        if name is None or name == "":
            raise ValueError("The name must not be empty.")
        if newName is None or newName == "":
            raise ValueError("The name must not be empty.")
        if newAddress is None or newAddress == "":
            raise ValueError("The address must not be empty.")
        company = WholesaleCompany.getWithName(name)
        if company is None:
            raise ValueError(f"The wholesale company {name} does not exist.")
        newNamecompany = WholesaleCompany.getWithName(newName)
        if name != newName and newNamecompany is not None:
            raise ValueError(f"The wholesale company {newName} already exists.")
        company.setName(newName)
        company.setAddress(newAddress)
        return

    def deleteWholesaleCompany(self, name: str) -> None:
        company = WholesaleCompany.getWithName(name)
        if company is None:
            raise ValueError(f"The wholesale company {name} does not exist.")
        if company.numberOfOrders() != 0:
            raise ValueError("Cannot delete a wholesale company that has ordered cheese.")
        company.delete()
        return

    def displayWholesaleCompany(self, name: str) -> TOWholesaleCompany:
        company = WholesaleCompany.getWithName(name)
        if company == None:
            return None
        companyTO = TOWholesaleCompany(company.getName(), company.getAddress())
        for order in company.getOrders():
                companyTO.addOrderDate(order.getTransactionDate())
                companyTO.addMonthsAged(order.getMonthsAged())
                companyTO.addNrCheeseWheelsOrdered(order.getNrCheeseWheels())
                companyTO.addNrCheeseWheelsMissing(order.getNrCheeseWheels() - order.numberOfCheeseWheels())
                companyTO.addDeliveryDate(order.getDeliveryDate())
        return companyTO

   # #returns all wholesale companies
    def displayWholesaleCompanies(self) -> List[TOWholesaleCompany]:
        companies = self.cheECSEManager.getCompanies()
        if len(companies) == 0:
            return []
        TOCompanies = []
        for company in companies:
            companyTO = TOWholesaleCompany(company.getName(), company.getAddress())
            for order in company.getOrders():
                companyTO.addOrderDate(order.getTransactionDate())
                companyTO.addMonthsAged(order.getMonthsAged())
                companyTO.addNrCheeseWheelsOrdered(order.getNrCheeseWheels())
                companyTO.addNrCheeseWheelsMissing(order.getNrCheeseWheels() - order.numberOfCheeseWheels())
                companyTO.addDeliveryDate(order.getDeliveryDate())
            TOCompanies.append(companyTO)
        return TOCompanies

def isValidManagerPassword(password:str) -> str:
    if password is None or password == "":
        return "Password must not be empty."
    if len(password) < 4:
        return "Password must be at least 4 characters long."
    if not("!" in password) and not("#" in password) and not("$" in password):
        return "Password must contain a special character from !, #, or $."
    if not any(c.isupper() for c in password):
        return "Password must contain an uppercase character."
    if not any(c.islower() for c in password):
        return "Password must contain a lowercase character."
    return ""

def isValidFarmerPassword(password:str) -> str:
    if password is None or password == "":
        return "Password must not be empty."
    return ""

def isValidFarmer(email:str) -> str:
    if email == "manager@cheecse.fr":
        return "Email cannot be manager@cheecse.fr."
    if email is None or email == "":
        return "Email cannot be empty"
    if not("@" in email):
        return "Email must contain @ symbol."
    if " " in email:
        return "Email must not contain spaces."
    if email.find("@") == 0:
        return "Email must have characters before @."
    if email.rfind(".") < email.find("@"):
        return "Email must contain a dot after @."
    if email.rfind(".") == len(email)-1:
        return "Email must have characters after dot."
    return ""