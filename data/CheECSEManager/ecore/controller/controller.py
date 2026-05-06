import calendar
from datetime import datetime
from typing import List
from pyecore.ecore import *

# from generated_model_layer import *
from ..generated_model_layer import *

class CheECSEManagerController:
    def __init__(self):
        self.cheECSEManager = CheECSEManager()

    def updateFacilityManager(self, password: str) -> None:
        error = isValidManagerPassword(password)
        if error != "":
            raise ValueError(error)
        manager = self.cheECSEManager.manager
        if manager is None:
            raise ValueError("Manager does not exist")
        # update the password
        manager.password = password
        return  # success  

    def addShelf(self, id: str, nrColumns: int, nrRows: int) -> None:
        if not id:
            raise ValueError("The id must be three characters long.")
    
        trimmedID = id.strip()
        if len(trimmedID) != 3:
            raise ValueError("The id must be three characters long.")
        if not trimmedID[0].isalpha():
            raise ValueError("The first character must be a letter.")
        if not trimmedID[1:].isdigit():
            raise ValueError("The second and third characters must be digits.")
        shelfExists = False
        for s in self.cheECSEManager.shelves:
            if s.id == id:
                shelfExists = True
                break
        if shelfExists:
            raise ValueError(f"The shelf {trimmedID} already exists.")
        if nrColumns < 1:
            raise ValueError("Number of columns must be greater than zero.")
        if nrRows < 1:
            raise ValueError("Number of rows must be greater than zero.")
        if nrRows > 10:
            raise ValueError("Number of rows must be at the most ten.")

        shelf = Shelf(id=trimmedID, cheECSEManager=self.cheECSEManager)
        locId = 1
        for column in range(1, nrColumns + 1):
            for row in range(1, nrRows + 1):
                loc = ShelfLocation(
                    id=locId,
                    column=column,
                    row=row
                )
                locId += 1
                shelf.locations.append(loc)
        self.cheECSEManager.shelves.add(shelf)
        return

    def deleteShelf(self, id: int) -> None:
        # find the shelf in the manager
        shelf = None
        for s in self.cheECSEManager.shelves:
            if s.id == id:
                shelf = s
                break
        if shelf is None:
            raise ValueError(f"The shelf {id} does not exist.")

        # check if any ShelfLocation contains a CheeseWheel
        for loc in shelf.locations:
            if loc.cheeseWheel is not None:
                raise ValueError("Cannot delete a shelf that contains cheese wheels.")
        # delete all locations 
        shelf.locations.clear()
        # remove shelf from manager
        self.cheECSEManager.shelves.remove(shelf)
        return  
     
    def displayShelf(self, id: str) -> TOShelf:
        # find the shelf in the manager
        shelf = None
        for s in self.cheECSEManager.shelves:
            if s.id == id:
                shelf = s
                break
        if shelf is None:
            return None  

        # build the TOShelf transfer object 
        shelfTO = TOShelf(shelfID=id)

        # collect location info
        for loc in shelf.locations:
            # add column/row values
            if loc.column not in shelfTO.columnNrs:
                shelfTO.columnNrs.append(loc.column)
            if loc.row not in shelfTO.rowNrs:
                shelfTO.rowNrs.append(loc.row)
            # add cheese info if present
            if loc.cheeseWheel is not None:
                cw = loc.cheeseWheel
                shelfTO.cheeseWheelIDs.append(cw.id)
                shelfTO.monthsAgeds.append(cw.monthsAged)
            else:
                # keep consistent structure: append placeholders
                shelfTO.cheeseWheelIDs.append(None)
                shelfTO.monthsAgeds.append(None)
        return shelfTO
        

    def displayShelves(self) -> List[TOShelf]:
        shelves = self.cheECSEManager.shelves
        if len(shelves) == 0:
            return None  

        shelfTOs = []  # list of TOShelf transfer objects
        # loop through each shelf
        for shelf in shelves:
            shelfTO = TOShelf(shelfID=shelf.id)

            # for each shelf, collect its locations
            for loc in shelf.locations:
                # columns
                if loc.column not in shelfTO.columnNrs:
                    shelfTO.columnNrs.append(loc.column)
                # rows
                if loc.row not in shelfTO.rowNrs:
                    shelfTO.rowNrs.append(loc.row)

                # cheese wheels in each location (if any)
                if loc.cheeseWheel is not None:
                    cw = loc.cheeseWheel
                    shelfTO.cheeseWheelIDs.append(cw.id)
                    shelfTO.monthsAgeds.append(cw.monthsAged)
                else:
                    # no cheese in that location
                    shelfTO.cheeseWheelIDs.append(None)
                    shelfTO.monthsAgeds.append(None)

            # add to result list
            shelfTOs.append(shelfTO)

        return shelfTOs
     

    def registerFarmer(self, email: str, password: str, name: str, address: str) -> None:
        error = ""
        error += isValidFarmer(email)
        error += isValidFarmerPassword(password)
        if error != "":
            raise ValueError(error)
        if address is None or address == "":
            raise ValueError("Address must not be empty.")
        farmers = self.cheECSEManager.farmers
        for f in farmers:
            if f.email == email:
                raise ValueError("The farmer email already exists.")
        farmer = Farmer(email=email, password=password, name=name, address=address, cheECSEManager=self.cheECSEManager)
        self.cheECSEManager.farmers.add(farmer)
        return

    def updateFarmer(self, email: str, newPassword: str, newName: str, newAddress: str) -> None:
        error = ""
        error += isValidFarmerPassword(newPassword)
        if error != "":
            raise ValueError(error)
        if newAddress is None or newAddress == "":
            raise ValueError("Address must not be empty.")
        farmers = self.cheECSEManager.farmers
        farmer = None
        for f in farmers:
            if f.email == email:
                farmer = f
                break
        if farmer is None:
            raise ValueError(f"The farmer with email {email} does not exist.")
        farmer.password = newPassword
        farmer.name = newName
        farmer.address = newAddress
        return

    def deleteFarmer(self, email: str) -> None:
        farmers = self.cheECSEManager.farmers
        farmer = None
        for f in farmers:
            if f.email == email:
                farmer = f
                break
        if farmer is None:
            raise ValueError(f"The farmer with email {email} does not exist.")
        if len(f.purchases) > 0:
            raise ValueError("Cannot delete farmer who has supplied cheese.")
        farmers.remove(farmer)
        return
       
    def displayFarmer(self, email: str) -> TOFarmer:
        farmers = self.cheECSEManager.farmers
        farmer = None
        for f in farmers:
            if f.email == email:
                farmer = f
                break
        if farmer is None:
            return None
        farmerTO = TOFarmer(email=farmer.email, address=farmer.address, password=farmer.password, name=farmer.name)
        for purchase in farmer.purchases:
            for cw in purchase.cheeseWheels:
                farmerTO.cheeseWheelIDs.append(cw.id)
                farmerTO.purchaseDates.append(cw.purchase.transactionDate)
                farmerTO.monthsAgeds.append(cw.monthsAged)
                farmerTO.isSpoileds.append(cw.isSpoiled)
        return farmerTO
       
   # #returns all farmers
    def displayFarmers(self) -> List[TOFarmer]:
        farmers = self.cheECSEManager.farmers
        if len(farmers) == 0:
            return []
        farmersTO = []
        for farmer in farmers:
            farmerTO = TOFarmer(email=farmer.email, address=farmer.address, password=farmer.password, name=farmer.name)
            for purchase in farmer.purchases:
                for cw in purchase.cheeseWheels:
                    farmerTO.cheeseWheelIDs.append(cw.id)
                    farmerTO.purchaseDates.append(cw.purchase.transactionDate)
                    farmerTO.monthsAgeds.append(cw.monthsAged)
                    farmerTO.isSpoileds.append(cw.isSpoiled)
            farmersTO.append(farmerTO)
        return farmersTO
       
    def buyCheeseWheelsFromFarmer(self, emailFarmer: str, purchaseDate: datetime, nrCheeseWheels: int, monthsAged: str) -> None:
        # validate nrCheeseWheels (feature expects this exact message)
        if nrCheeseWheels is None or not isinstance(nrCheeseWheels, int) or nrCheeseWheels <= 0:
            raise ValueError("nrCheeseWheels must be greater than zero.")

        # validate monthsAged literal per feature
        allowed = [str(MaturationPeriod.Six), str(MaturationPeriod.Twelve), str(MaturationPeriod.TwentyFour), str(MaturationPeriod.ThirtySix)]
        if monthsAged not in allowed:
            raise ValueError("The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix.")

        # accept either a date object or an ISO date string
        if purchaseDate is None:
            raise ValueError("Invalid purchase date")

        farmers = self.cheECSEManager.farmers
        farmer = None
        for f in farmers:
            if f.email == emailFarmer:
                farmer = f
                break
        if farmer is None:
            raise ValueError(f"The farmer with email {emailFarmer} does not exist.")

        # Create a Purchase 
        purchaseId = len(self.cheECSEManager.transactions) + 1
        purchase = Purchase(transactionDate=EDate.from_string(purchaseDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z')), id=purchaseId, cheECSEManager=self.cheECSEManager, farmer=farmer)
        
        # Map literal monthsAged to CheeseWheel.MaturationPeriod enum
        maturation = getattr(MaturationPeriod, monthsAged)

        # Add the requested number of cheese wheels to the purchase
        for _ in range(nrCheeseWheels):
            cwId = len(self.cheECSEManager.cheeseWheels) + 1
            cw = CheeseWheel(cheECSEManager=self.cheECSEManager, id=cwId, monthsAged=maturation, isSpoiled=False)
            purchase.cheeseWheels.append(cw)
            self.cheECSEManager.cheeseWheels.append(cw)

        self.cheECSEManager.transactions.append(purchase)
        return

    def assignCheeseWheelToShelf(self, cheeseWheelID: int, shelfID: str, columnNr: int, rowNr: int) -> None:
        shelf = None
        for s in self.cheECSEManager.shelves:
            if s.id == shelfID:
                shelf = s
                break
        if shelf is None:
           raise ValueError(f"The shelf with id {shelfID} does not exist.")
        if len(shelf.locations) == 0:
            raise ValueError("The shelf has no locations.")
        
        targetLocation = None
        for loc in shelf.locations:
            if loc.column == columnNr and loc.row == rowNr:
                targetLocation = loc
                break
        if targetLocation is None:
            raise ValueError("The shelf location does not exist.")
        
        if targetLocation.cheeseWheel is not None:
            raise ValueError("The shelf location is already occupied.")
        
        cheese = None
        for cw in self.cheECSEManager.cheeseWheels:
            if cw.id == cheeseWheelID:
                cheese = cw
                break
        if cheese is None:
            raise ValueError(f"The cheese wheel with id {cheeseWheelID} does not exist.")

        if cheese.isSpoiled:
            raise ValueError("Cannot place a spoiled cheese wheel on a shelf.")

        cheeseCurrentLocation = cheese.location
        if cheeseCurrentLocation is not None:
            cheeseCurrentLocation.cheeseWheel = None
        targetLocation.cheeseWheel = cheese
        return
   

    def removeCheeseWheelFromShelf(self, cheeseWheelID: str) -> None:
        cheeseWheel = None
        for cw in self.cheECSEManager.cheeseWheels:
            if cw.id == cheeseWheelID:
                cheeseWheel = cw
                break
        if cheeseWheel is None:
            raise ValueError(f"The cheese wheel with id {cheeseWheelID} does not exist.")
        if cheeseWheel.location is None:
            raise ValueError("The cheese wheel is not on any shelf.")
        loc = cheeseWheel.location
        loc.cheeseWheel = None
        cheeseWheel.location = None
        return 
   

    def updateCheeseWheel(self, cheeseWheelID: str, newMonthsAged: str, newIsSpoiled: bool) -> None:
        # validate monthsAged enum values
        validMonths = [str(MaturationPeriod.Six), str(MaturationPeriod.Twelve), str(MaturationPeriod.TwentyFour), str(MaturationPeriod.ThirtySix)]
        if newMonthsAged not in validMonths:
            raise ValueError("The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix.")
    
        #find cheese wheel by id
        cheeseWheel = None
        for wheel in self.cheECSEManager.cheeseWheels:
            if wheel.id == cheeseWheelID:
                cheeseWheel = wheel
                break
        if cheeseWheel is None:
            raise ValueError(f"The cheese wheel with id {cheeseWheelID} does not exist.")
        
        # validate monthsAged - can only increase
        currentMonths = cheeseWheel.monthsAged
        currentMonthsValue = validMonths.index(str(currentMonths))
        newMonthsValue = validMonths.index(newMonthsAged)

        if newMonthsValue < currentMonthsValue:
            raise ValueError("Cannot decrease the monthsAged of a cheese wheel.")
        
        cheeseWheel.monthsAged = getattr(MaturationPeriod, newMonthsAged)
        cheeseWheel.isSpoiled = newIsSpoiled

        transactions = self.cheECSEManager.transactions
        if newIsSpoiled:
            loc = cheeseWheel.location
            if loc is not None:
                cheeseWheel.location = None
                loc.cheeseWheel = None

            for order in transactions:
                if isinstance(order, Order) and cheeseWheel.order == order:
                    order.cheeseWheels.remove(cheeseWheel)
                    cheeseWheel.order = None
        
        for order in transactions:
            if isinstance(order, Order) and cheeseWheel.order == order:
                if cheeseWheel.monthsAged != order.monthsAged:
                    order.cheeseWheels.remove(cheeseWheel)
                    cheeseWheel.order = None

        return

    # to review 
    def displayCheeseWheel(self, cheeseWheelID: str) -> TOCheeseWheel:
        # find cheese wheel by ID
        cheeseWheel = None
        for wheel in self.cheECSEManager.cheeseWheels:
            if wheel.id == cheeseWheelID:
                cheeseWheel = wheel
                break
        if cheeseWheel is None:
            return None

        # get purchase date
        purchaseDate = cheeseWheel.purchase.transactionDate
        # get shelf info
        shelfID = None
        column = -1
        row = -1
        if cheeseWheel.location is not None:
            location = cheeseWheel.location
            # find which shelf contains this location
            for shelf in self.cheECSEManager.shelves:
                if location in shelf.locations:
                    shelfID = shelf.id
                    break
            column = location.column
            row = location.row
        
        # check if cheese wheel is ordered
        isOrdered = cheeseWheel.order is not None
        
        # create TOCheeseWheel object
        cheeseWheelTO = TOCheeseWheel(
            id=int(cheeseWheel.id),
            monthsAged=cheeseWheel.monthsAged,
            isSpoiled=cheeseWheel.isSpoiled,
            purchaseDate=purchaseDate,
            shelfID=shelfID,
            column=column,
            row=row,
            isOrdered=isOrdered,
        )
        return cheeseWheelTO


   # #returns all cheese wheels
   # to review
    def displayCheeseWheels(self) -> List[TOCheeseWheel]:
        cheeseWheels = self.cheECSEManager.cheeseWheels
        if len(cheeseWheels) == 0:
            return None
        
        TOCheeseWheels = []
        for cheeseWheel in cheeseWheels:
            # get purchase date
            purchaseDate = cheeseWheel.purchase.transactionDate

            # get shelf location
            shelfID = None
            column = -1
            row = -1
            if cheeseWheel.location is not None:
                location = cheeseWheel.location
                # find which shelf contains this location
                for shelf in self.cheECSEManager.shelves:
                    if location in shelf.locations:
                        shelfID = shelf.id
                        break
                column = location.column
                row = location.row
            
            # check if ordered
            isOrdered = cheeseWheel.order is not None

            # create TOCheeseWheel object
            cheeseWheelTO = TOCheeseWheel(
                id=int(cheeseWheel.id),
                monthsAged=cheeseWheel.monthsAged,
                isSpoiled=cheeseWheel.isSpoiled,
                purchaseDate=purchaseDate,
                shelfID=shelfID,
                column=column,
                row=row,
                isOrdered=isOrdered,
            )
            TOCheeseWheels.append(cheeseWheelTO)

        return TOCheeseWheels

    def sellCheeseWheelsToWholesaleCompany(self, nameCompany: str, orderDate: datetime, nrCheeseWheels: int, monthsAged: str, deliveryDate: datetime) -> None:
        if nrCheeseWheels is None or nrCheeseWheels <= 0:
            raise ValueError("nrCheeseWheels must be greater than zero.")
        
        allowed = [str(MaturationPeriod.Six), str(MaturationPeriod.Twelve), str(MaturationPeriod.TwentyFour), str(MaturationPeriod.ThirtySix)]
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
        
        companies = self.cheECSEManager.companies
        company = None
        for c in companies:
            if c.name == nameCompany:
                company = c
                break
        if company is None:
            raise ValueError(f"The wholesale company {nameCompany} does not exist.")
        
        maturationEnum = getattr(MaturationPeriod, monthsAged)

        nextOrderId = len(self.cheECSEManager.transactions) + 1
        order = Order(id=nextOrderId, company=company, nrCheeseWheels=nrCheeseWheels, monthsAged=maturationEnum, deliveryDate=EDate.from_string(deliveryDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z')), transactionDate=EDate.from_string(orderDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z')))
        company.orders.append(order)

        needed = nrCheeseWheels
        nrMonths = {"Six": 6, "Twelve": 12, "TwentyFour": 24, "ThirtySix": 36}[monthsAged]

        transactions = list(self.cheECSEManager.transactions)
        transactions.sort(key=lambda t: t.transactionDate)

        for tx in transactions:
            if not isinstance(tx, Purchase):
                continue

            purchase = tx

            # only cheese wheels that are mature by the delivery date are available
            purchaseDate = purchase.transactionDate
            month = purchaseDate.month - 1 + nrMonths
            year = purchaseDate.year + month // 12
            month = month % 12 + 1
            day = min(purchaseDate.day, calendar.monthrange(year, month)[1])
            if purchaseDate.replace(year=year, month=month, day=day) > deliveryDate:
                continue

            for cheese in purchase.cheeseWheels:
                if needed == 0:
                    break

                if cheese.monthsAged == maturationEnum and not cheese.isSpoiled and cheese.order is None:
                    order.cheeseWheels.append(cheese)
                    needed -= 1

            if needed == 0:
                break
        self.cheECSEManager.transactions.append(order)
        return


    def addWholesaleCompany(self, name: str, address: str) -> None:
        if name is None or name == "":
            raise ValueError("Name must not be empty.")
        if address is None or address == "":
            raise ValueError("Address must not be empty.")
        companies = self.cheECSEManager.companies
        for c in companies:
            if c.name == name:
                raise ValueError("The wholesale company already exists.")
        wholesaleCompany = WholesaleCompany(name=name, address=address, cheECSEManager=self.cheECSEManager)
        self.cheECSEManager.companies.append(wholesaleCompany)
        return

    def updateWholesaleCompany(self, name: str, newName: str, newAddress: str) -> None:
        if name is None or name == "":
            raise ValueError("The name must not be empty.")
        if newName is None or newName == "":
            raise ValueError("The name must not be empty.")
        if newAddress is None or newAddress == "":
            raise ValueError("The address must not be empty.")
        companies = self.cheECSEManager.companies
        existingCompany = None
        newNameCompany = None
        for c in companies:
            if c.name == name:
                existingCompany = c
            if c.name == newName:
                newNameCompany = c
        if existingCompany is None:
            raise ValueError(f"The wholesale company {name} does not exist.")
        if name != newName and newNameCompany is not None:
            raise ValueError(f"The wholesale company {newName} already exists.")
        existingCompany.name = newName
        existingCompany.address = newAddress
        return
 
    def deleteWholesaleCompany(self, name: str) -> None:
        companies = self.cheECSEManager.companies
        existingCompany = None
        for c in companies:
            if c.name == name:
                existingCompany = c
                break
        if existingCompany is None:
            raise ValueError(f"The wholesale company {name} does not exist.")
        if len(existingCompany.orders) > 0:
            raise ValueError("Cannot delete a wholesale company that has ordered cheese.")
        companies.remove(existingCompany)
        return

    def displayWholesaleCompany(self, name: str) -> TOWholesaleCompany:
        companies = self.cheECSEManager.companies
        existingCompany = None
        for c in companies:
            if c.name == name:
                existingCompany = c
                break
        if existingCompany is None:
            return None
        companyTO = TOWholesaleCompany(name=existingCompany.name, address=existingCompany.address)
        for order in existingCompany.orders:
            companyTO.orderDates.append(order.transactionDate)
            companyTO.monthsAgeds.append(order.monthsAged)
            companyTO.nrCheeseWheelsOrdereds.append(order.nrCheeseWheels)
            companyTO.nrCheeseWheelsMissings.append(order.nrCheeseWheels - len(order.cheeseWheels))
            companyTO.deliveryDates.append(order.deliveryDate)
        return companyTO

   # #returns all wholesale companies
    def displayWholesaleCompanies(self) -> List[TOWholesaleCompany]:
        companies = self.cheECSEManager.companies
        if len(companies) == 0:
            return []
        TOCompanies = []
        for c in companies:
            companyTO = TOWholesaleCompany(name=c.name, address=c.address)
            for order in c.orders:
                companyTO.orderDates.append(order.transactionDate)
                companyTO.monthsAgeds.append(order.monthsAged)
                companyTO.nrCheeseWheelsOrdereds.append(order.nrCheeseWheels)
                companyTO.nrCheeseWheelsMissings.append(order.nrCheeseWheels - len(order.cheeseWheels))
                companyTO.deliveryDates.append(order.deliveryDate)
            TOCompanies.append(companyTO)
        return TOCompanies

def isValidFarmerPassword(password: str) -> str:
    if password is None or password == "":
        return "Password must not be empty."
    return ""

def isValidManagerPassword(password: str) -> str:
    if len(password) < 4:
        return "Password must be at least 4 characters long."
    if not ("!" in password) and not ("#" in password) and not ("$" in password):
        return "Password must contain a special character from !, #, or $."
    if not any(c.isupper() for c in password):
        return "Password must contain an uppercase character."
    if not any(c.islower() for c in password):
        return "Password must contain a lowercase character."
    return ""

def isValidFarmer(email: str) -> str:
    if email == 'manager@cheecse.fr':
        return "Email cannot be manager@cheecse.fr."
    if email is None or email == "":
        return "Email must not be empty."
    if "@" not in email:
        return "Email must contain @ symbol."
    if " " in email:
        return "Email must not contain spaces."
    atIndex = email.index("@")
    if atIndex == 0:
        return "Email must have characters before @."
    if "." not in email[atIndex:]:
        return "Email must contain a dot after @."
    dotIndex = email.rindex(".")
    if dotIndex == len(email) - 1:
        return "Email must have characters after dot."
    return ""
