"""Definition of meta model 'AssetPlus'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'AssetPlus'
nsURI = 'AssetPlus'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
TimeEstimate = EEnum('TimeEstimate', literals=[
                     'lessThanADay', 'oneToThreeDays', 'threeToSevenDays', 'oneToThreeWeeks', 'threeOrMoreWeeks'])

PriorityLevel = EEnum('PriorityLevel', literals=['Urgent', 'Normal', 'Low'])


class AssetPlus(EObject, metaclass=MetaEClass):

    employees = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    guests = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    manager = EReference(ordered=True, unique=True, containment=True, derived=False)
    maintenanceTickets = EReference(ordered=True, unique=True,
                                    containment=True, derived=False, upper=-1)
    assetTypes = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    specificAssets = EReference(ordered=True, unique=True,
                                containment=True, derived=False, upper=-1)

    def __init__(self, *, employees=None, guests=None, manager=None, maintenanceTickets=None, assetTypes=None, specificAssets=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if employees:
            self.employees.extend(employees)

        if guests:
            self.guests.extend(guests)

        if manager is not None:
            self.manager = manager

        if maintenanceTickets:
            self.maintenanceTickets.extend(maintenanceTickets)

        if assetTypes:
            self.assetTypes.extend(assetTypes)

        if specificAssets:
            self.specificAssets.extend(specificAssets)


@abstract
class User(EObject, metaclass=MetaEClass):

    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    password = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    phoneNumber = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    raisedTickets = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)

    def __init__(self, *, email=None, name=None, password=None, phoneNumber=None, raisedTickets=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if email is not None:
            self.email = email

        if name is not None:
            self.name = name

        if password is not None:
            self.password = password

        if phoneNumber is not None:
            self.phoneNumber = phoneNumber

        if raisedTickets:
            self.raisedTickets.extend(raisedTickets)


class MaintenanceTicket(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    raisedOnDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    timeToResolve = EAttribute(eType=TimeEstimate, unique=True, derived=False, changeable=True)
    priority = EAttribute(eType=PriorityLevel, unique=True, derived=False, changeable=True)
    ticketRaiser = EReference(ordered=True, unique=True, containment=False, derived=False)
    ticketFixer = EReference(ordered=True, unique=True, containment=False, derived=False)
    fixApprover = EReference(ordered=True, unique=True, containment=False, derived=False)
    ticketNotes = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    ticketImages = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    asset = EReference(ordered=True, unique=True, containment=False, derived=False)
    assetPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, raisedOnDate=None, description=None, timeToResolve=None, priority=None, ticketRaiser=None, ticketFixer=None, fixApprover=None, ticketNotes=None, ticketImages=None, asset=None, assetPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if raisedOnDate is not None:
            self.raisedOnDate = raisedOnDate

        if description is not None:
            self.description = description

        if timeToResolve is not None:
            self.timeToResolve = timeToResolve

        if priority is not None:
            self.priority = priority

        if ticketRaiser is not None:
            self.ticketRaiser = ticketRaiser

        if ticketFixer is not None:
            self.ticketFixer = ticketFixer

        if fixApprover is not None:
            self.fixApprover = fixApprover

        if ticketNotes:
            self.ticketNotes.extend(ticketNotes)

        if ticketImages:
            self.ticketImages.extend(ticketImages)

        if asset is not None:
            self.asset = asset

        if assetPlus is not None:
            self.assetPlus = assetPlus


class MaintenanceNote(EObject, metaclass=MetaEClass):

    date = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    noteTaker = EReference(ordered=True, unique=True, containment=False, derived=False)
    ticket = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, date=None, description=None, noteTaker=None, ticket=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if date is not None:
            self.date = date

        if description is not None:
            self.description = description

        if noteTaker is not None:
            self.noteTaker = noteTaker

        if ticket is not None:
            self.ticket = ticket


class TicketImage(EObject, metaclass=MetaEClass):

    imageURL = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    ticket = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, imageURL=None, ticket=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if imageURL is not None:
            self.imageURL = imageURL

        if ticket is not None:
            self.ticket = ticket


class SpecificAsset(EObject, metaclass=MetaEClass):

    assetNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    floorNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    roomNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    purchaseDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    maintenanceTickets = EReference(ordered=True, unique=True,
                                    containment=False, derived=False, upper=-1)
    assetType = EReference(ordered=True, unique=True, containment=False, derived=False)
    assetPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, assetNumber=None, floorNumber=None, roomNumber=None, purchaseDate=None, maintenanceTickets=None, assetType=None, assetPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if assetNumber is not None:
            self.assetNumber = assetNumber

        if floorNumber is not None:
            self.floorNumber = floorNumber

        if roomNumber is not None:
            self.roomNumber = roomNumber

        if purchaseDate is not None:
            self.purchaseDate = purchaseDate

        if maintenanceTickets:
            self.maintenanceTickets.extend(maintenanceTickets)

        if assetType is not None:
            self.assetType = assetType

        if assetPlus is not None:
            self.assetPlus = assetPlus


class AssetType(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    expectedLifeSpan = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    image = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    specificAssets = EReference(ordered=True, unique=True,
                                containment=False, derived=False, upper=-1)
    assetPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, name=None, expectedLifeSpan=None, image=None, specificAssets=None, assetPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if expectedLifeSpan is not None:
            self.expectedLifeSpan = expectedLifeSpan

        if image is not None:
            self.image = image

        if specificAssets:
            self.specificAssets.extend(specificAssets)

        if assetPlus is not None:
            self.assetPlus = assetPlus


class TOMaintenanceNote(EObject, metaclass=MetaEClass):

    date = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    noteTakerEmail = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, date=None, description=None, noteTakerEmail=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if date is not None:
            self.date = date

        if description is not None:
            self.description = description

        if noteTakerEmail is not None:
            self.noteTakerEmail = noteTakerEmail


@abstract
class TOUser(EObject, metaclass=MetaEClass):

    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    password = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    phoneNumber = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    ticketsRaised = EAttribute(eType=EInt, unique=True, derived=False, changeable=True, upper=-1)

    def __init__(self, *, email=None, name=None, password=None, phoneNumber=None, ticketsRaised=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if email is not None:
            self.email = email

        if name is not None:
            self.name = name

        if password is not None:
            self.password = password

        if phoneNumber is not None:
            self.phoneNumber = phoneNumber

        if ticketsRaised:
            self.ticketsRaised.extend(ticketsRaised)


class TOAssetType(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    expectedLifeSpan = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    imageURL = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None, expectedLifeSpan=None, imageURL=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if expectedLifeSpan is not None:
            self.expectedLifeSpan = expectedLifeSpan

        if imageURL is not None:
            self.imageURL = imageURL


class TOSpecificAsset(EObject, metaclass=MetaEClass):

    assetNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    floorNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    roomNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    purchaseDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    assetType = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, assetNumber=None, floorNumber=None, roomNumber=None, purchaseDate=None, assetType=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if assetNumber is not None:
            self.assetNumber = assetNumber

        if floorNumber is not None:
            self.floorNumber = floorNumber

        if roomNumber is not None:
            self.roomNumber = roomNumber

        if purchaseDate is not None:
            self.purchaseDate = purchaseDate

        if assetType is not None:
            self.assetType = assetType


class TOMaintenanceTicket(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    raisedOnDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    raisedByEmail = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    fixedByEmail = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    timeToResolve = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    priority = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    approvalRequired = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    assetName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    expectedLifeSpanInDays = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    purchaseDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    floorNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    roomNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    imageURLs = EAttribute(eType=EString, unique=True, derived=False, changeable=True, upper=-1)
    noteDates = EAttribute(eType=EDate, unique=True, derived=False, changeable=True, upper=-1)
    noteDescriptions = EAttribute(eType=EString, unique=True,
                                  derived=False, changeable=True, upper=-1)
    noteTakerEmails = EAttribute(eType=EString, unique=True,
                                 derived=False, changeable=True, upper=-1)

    def __init__(self, *, id=None, raisedOnDate=None, description=None, raisedByEmail=None, status=None, fixedByEmail=None, timeToResolve=None, priority=None, approvalRequired=None, assetName=None, expectedLifeSpanInDays=None, purchaseDate=None, floorNumber=None, roomNumber=None, imageURLs=None, noteDates=None, noteDescriptions=None, noteTakerEmails=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if raisedOnDate is not None:
            self.raisedOnDate = raisedOnDate

        if description is not None:
            self.description = description

        if raisedByEmail is not None:
            self.raisedByEmail = raisedByEmail

        if status is not None:
            self.status = status

        if fixedByEmail is not None:
            self.fixedByEmail = fixedByEmail

        if timeToResolve is not None:
            self.timeToResolve = timeToResolve

        if priority is not None:
            self.priority = priority

        if approvalRequired is not None:
            self.approvalRequired = approvalRequired

        if assetName is not None:
            self.assetName = assetName

        if expectedLifeSpanInDays is not None:
            self.expectedLifeSpanInDays = expectedLifeSpanInDays

        if purchaseDate is not None:
            self.purchaseDate = purchaseDate

        if floorNumber is not None:
            self.floorNumber = floorNumber

        if roomNumber is not None:
            self.roomNumber = roomNumber

        if imageURLs:
            self.imageURLs.extend(imageURLs)

        if noteDates:
            self.noteDates.extend(noteDates)

        if noteDescriptions:
            self.noteDescriptions.extend(noteDescriptions)

        if noteTakerEmails:
            self.noteTakerEmails.extend(noteTakerEmails)


@abstract
class HotelStaff(User):

    maintenanceNotes = EReference(ordered=True, unique=True,
                                  containment=False, derived=False, upper=-1)
    maintenanceTasks = EReference(ordered=True, unique=True,
                                  containment=False, derived=False, upper=-1)

    def __init__(self, *, maintenanceNotes=None, maintenanceTasks=None, **kwargs):

        super().__init__(**kwargs)

        if maintenanceNotes:
            self.maintenanceNotes.extend(maintenanceNotes)

        if maintenanceTasks:
            self.maintenanceTasks.extend(maintenanceTasks)


class Guest(User):

    assetPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, assetPlus=None, **kwargs):

        super().__init__(**kwargs)

        if assetPlus is not None:
            self.assetPlus = assetPlus


class TOGuest(TOUser):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


@abstract
class TOHotelStaff(TOUser):

    ticketFixed = EAttribute(eType=EInt, unique=True, derived=False, changeable=True, upper=-1)

    def __init__(self, *, ticketFixed=None, **kwargs):

        super().__init__(**kwargs)

        if ticketFixed:
            self.ticketFixed.extend(ticketFixed)


class Employee(HotelStaff):

    assetPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, assetPlus=None, **kwargs):

        super().__init__(**kwargs)

        if assetPlus is not None:
            self.assetPlus = assetPlus


class Manager(HotelStaff):

    ticketsForApproval = EReference(ordered=True, unique=True,
                                    containment=False, derived=False, upper=-1)
    assetPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, ticketsForApproval=None, assetPlus=None, **kwargs):

        super().__init__(**kwargs)

        if ticketsForApproval:
            self.ticketsForApproval.extend(ticketsForApproval)

        if assetPlus is not None:
            self.assetPlus = assetPlus


class TOEmployee(TOHotelStaff):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class TOManager(TOHotelStaff):

    ticketApproved = EAttribute(eType=EInt, unique=True, derived=False, changeable=True, upper=-1)

    def __init__(self, *, ticketApproved=None, **kwargs):

        super().__init__(**kwargs)

        if ticketApproved:
            self.ticketApproved.extend(ticketApproved)
