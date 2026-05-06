"""Definition of meta model 'cheecsemanager'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'cheecsemanager'
nsURI = 'cheecsemanager'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
MaturationPeriod = EEnum('MaturationPeriod', literals=['Six', 'Twelve', 'TwentyFour', 'ThirtySix'])


class CheECSEManager(EObject, metaclass=MetaEClass):

    manager = EReference(ordered=True, unique=True, containment=False, derived=False)
    farmers = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    shelves = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    cheeseWheels = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    transactions = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    companies = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    robot = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, manager=None, farmers=None, shelves=None, cheeseWheels=None, transactions=None, companies=None, robot=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if manager is not None:
            self.manager = manager

        if farmers:
            self.farmers.extend(farmers)

        if shelves:
            self.shelves.extend(shelves)

        if cheeseWheels:
            self.cheeseWheels.extend(cheeseWheels)

        if transactions:
            self.transactions.extend(transactions)

        if companies:
            self.companies.extend(companies)

        if robot is not None:
            self.robot = robot


@abstract
class User(EObject, metaclass=MetaEClass):

    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True, iD=True)
    password = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, email=None, password=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if email is not None:
            self.email = email

        if password is not None:
            self.password = password


class WholesaleCompany(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)
    orders = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, cheECSEManager=None, name=None, address=None, orders=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager

        if orders:
            self.orders.extend(orders)


class Shelf(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True, iD=True)
    robot = EReference(ordered=True, unique=True, containment=False, derived=False)
    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)
    locations = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, robot=None, cheECSEManager=None, id=None, locations=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if robot is not None:
            self.robot = robot

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager

        if locations:
            self.locations.extend(locations)


class ShelfLocation(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True, iD=True)
    column = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    row = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    cheeseWheel = EReference(ordered=True, unique=True, containment=False, derived=False)
    shelf = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, cheeseWheel=None, shelf=None, id=None, column=None, row=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if column is not None:
            self.column = column

        if row is not None:
            self.row = row

        if cheeseWheel is not None:
            self.cheeseWheel = cheeseWheel

        if shelf is not None:
            self.shelf = shelf


class CheeseWheel(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True, iD=True)
    monthsAged = EAttribute(eType=MaturationPeriod, unique=True, derived=False, changeable=True)
    isSpoiled = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    robot = EReference(ordered=True, unique=True, containment=False, derived=False)
    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)
    purchase = EReference(ordered=True, unique=True, containment=False, derived=False)
    location = EReference(ordered=True, unique=True, containment=False, derived=False)
    order = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, robot=None, cheECSEManager=None, id=None, monthsAged=None, isSpoiled=None, purchase=None, location=None, order=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if monthsAged is not None:
            self.monthsAged = monthsAged

        if isSpoiled is not None:
            self.isSpoiled = isSpoiled

        if robot is not None:
            self.robot = robot

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager

        if purchase is not None:
            self.purchase = purchase

        if location is not None:
            self.location = location

        if order is not None:
            self.order = order


@abstract
class Transaction(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True, iD=True)
    transactionDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, cheECSEManager=None, id=None, transactionDate=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if transactionDate is not None:
            self.transactionDate = transactionDate

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager


class Robot(EObject, metaclass=MetaEClass):

    isFacingAisle = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)
    currentShelf = EReference(ordered=True, unique=True, containment=False, derived=False)
    currentCheeseWheel = EReference(ordered=True, unique=True, containment=False, derived=False)
    log = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, cheECSEManager=None, isFacingAisle=None, currentShelf=None, currentCheeseWheel=None, log=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if isFacingAisle is not None:
            self.isFacingAisle = isFacingAisle

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager

        if currentShelf is not None:
            self.currentShelf = currentShelf

        if currentCheeseWheel is not None:
            self.currentCheeseWheel = currentCheeseWheel

        if log:
            self.log.extend(log)


class LogEntry(EObject, metaclass=MetaEClass):

    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    robot = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, robot=None, description=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if description is not None:
            self.description = description

        if robot is not None:
            self.robot = robot


class TOFarmer(EObject, metaclass=MetaEClass):

    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    password = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    cheeseWheelIDs = EAttribute(eType=EInt, unique=False, derived=False, changeable=True, upper=-1)
    purchaseDates = EAttribute(eType=EDate, unique=False, derived=False, changeable=True, upper=-1)
    monthsAgeds = EAttribute(eType=MaturationPeriod, unique=False,
                             derived=False, changeable=True, upper=-1)
    isSpoileds = EAttribute(eType=EBoolean, unique=False, derived=False, changeable=True, upper=-1)

    def __init__(self, *, email=None, password=None, name=None, address=None, cheeseWheelIDs=None, purchaseDates=None, monthsAgeds=None, isSpoileds=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if email is not None:
            self.email = email

        if password is not None:
            self.password = password

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if cheeseWheelIDs:
            self.cheeseWheelIDs.extend(cheeseWheelIDs)

        if purchaseDates:
            self.purchaseDates.extend(purchaseDates)

        if monthsAgeds:
            self.monthsAgeds.extend(monthsAgeds)

        if isSpoileds:
            self.isSpoileds.extend(isSpoileds)


class TOWholesaleCompany(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    orderDates = EAttribute(eType=EDate, unique=False, derived=False, changeable=True, upper=-1)
    monthsAgeds = EAttribute(eType=MaturationPeriod, unique=False,
                             derived=False, changeable=True, upper=-1)
    nrCheeseWheelsOrdereds = EAttribute(
        eType=EInt, unique=False, derived=False, changeable=True, upper=-1)
    nrCheeseWheelsMissings = EAttribute(
        eType=EInt, unique=False, derived=False, changeable=True, upper=-1)
    deliveryDates = EAttribute(eType=EDate, unique=False, derived=False, changeable=True, upper=-1)

    def __init__(self, *, name=None, address=None, orderDates=None, monthsAgeds=None, nrCheeseWheelsOrdereds=None, nrCheeseWheelsMissings=None, deliveryDates=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if orderDates:
            self.orderDates.extend(orderDates)

        if monthsAgeds:
            self.monthsAgeds.extend(monthsAgeds)

        if nrCheeseWheelsOrdereds:
            self.nrCheeseWheelsOrdereds.extend(nrCheeseWheelsOrdereds)

        if nrCheeseWheelsMissings:
            self.nrCheeseWheelsMissings.extend(nrCheeseWheelsMissings)

        if deliveryDates:
            self.deliveryDates.extend(deliveryDates)


class TOShelf(EObject, metaclass=MetaEClass):

    shelfID = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    cheeseWheelIDs = EAttribute(eType=EInt, unique=False, derived=False, changeable=True, upper=-1)
    columnNrs = EAttribute(eType=EInt, unique=False, derived=False, changeable=True, upper=-1)
    rowNrs = EAttribute(eType=EInt, unique=False, derived=False, changeable=True, upper=-1)
    monthsAgeds = EAttribute(eType=MaturationPeriod, unique=False,
                             derived=False, changeable=True, upper=-1)

    def __init__(self, *, shelfID=None, cheeseWheelIDs=None, columnNrs=None, rowNrs=None, monthsAgeds=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if shelfID is not None:
            self.shelfID = shelfID

        if cheeseWheelIDs:
            self.cheeseWheelIDs.extend(cheeseWheelIDs)

        if columnNrs:
            self.columnNrs.extend(columnNrs)

        if rowNrs:
            self.rowNrs.extend(rowNrs)

        if monthsAgeds:
            self.monthsAgeds.extend(monthsAgeds)


class TOCheeseWheel(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    monthsAged = EAttribute(eType=MaturationPeriod, unique=True, derived=False, changeable=True)
    isSpoiled = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    purchaseDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    shelfID = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    column = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    row = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    isOrdered = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)

    def __init__(self, *, id=None, monthsAged=None, isSpoiled=None, purchaseDate=None, shelfID=None, column=None, row=None, isOrdered=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if monthsAged is not None:
            self.monthsAged = monthsAged

        if isSpoiled is not None:
            self.isSpoiled = isSpoiled

        if purchaseDate is not None:
            self.purchaseDate = purchaseDate

        if shelfID is not None:
            self.shelfID = shelfID

        if column is not None:
            self.column = column

        if row is not None:
            self.row = row

        if isOrdered is not None:
            self.isOrdered = isOrdered


class FacilityManager(User):

    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, cheECSEManager=None, **kwargs):

        super().__init__(**kwargs)

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager


class Farmer(User):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    cheECSEManager = EReference(ordered=True, unique=True, containment=False, derived=False)
    purchases = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, cheECSEManager=None, name=None, address=None, purchases=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if cheECSEManager is not None:
            self.cheECSEManager = cheECSEManager

        if purchases:
            self.purchases.extend(purchases)


class Purchase(Transaction):

    cheeseWheels = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    farmer = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, cheeseWheels=None, farmer=None, **kwargs):

        super().__init__(**kwargs)

        if cheeseWheels:
            self.cheeseWheels.extend(cheeseWheels)

        if farmer is not None:
            self.farmer = farmer


class Order(Transaction):

    nrCheeseWheels = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    monthsAged = EAttribute(eType=MaturationPeriod, unique=True, derived=False, changeable=True)
    deliveryDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    cheeseWheels = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    company = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, cheeseWheels=None, company=None, nrCheeseWheels=None, monthsAged=None, deliveryDate=None, **kwargs):

        super().__init__(**kwargs)

        if nrCheeseWheels is not None:
            self.nrCheeseWheels = nrCheeseWheels

        if monthsAged is not None:
            self.monthsAged = monthsAged

        if deliveryDate is not None:
            self.deliveryDate = deliveryDate

        if cheeseWheels:
            self.cheeseWheels.extend(cheeseWheels)

        if company is not None:
            self.company = company
