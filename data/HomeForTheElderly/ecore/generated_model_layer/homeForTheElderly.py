"""Definition of meta model 'homeForTheElderly'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'homeForTheElderly'
nsURI = 'homeForTheElderly'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class HomeForTheElderly(EObject, metaclass=MetaEClass):

    departments = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    people = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, departments=None, people=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if departments:
            self.departments.extend(departments)

        if people:
            self.people.extend(people)


class Department(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True, iD=True)
    rooms = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    homeForTheElderly = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, rooms=None, homeForTheElderly=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if rooms:
            self.rooms.extend(rooms)

        if homeForTheElderly is not None:
            self.homeForTheElderly = homeForTheElderly


class Category(EObject, metaclass=MetaEClass):

    price = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    type = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    rooms = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, price=None, type=None, rooms=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if price is not None:
            self.price = price

        if type is not None:
            self.type = type

        if rooms:
            self.rooms.extend(rooms)


class Room(EObject, metaclass=MetaEClass):

    roomNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    beds = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    department = EReference(ordered=True, unique=True, containment=False, derived=False)
    category = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, roomNumber=None, beds=None, department=None, category=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if roomNumber is not None:
            self.roomNumber = roomNumber

        if beds:
            self.beds.extend(beds)

        if department is not None:
            self.department = department

        if category is not None:
            self.category = category


class Bed(EObject, metaclass=MetaEClass):

    bedNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    person = EReference(ordered=True, unique=True, containment=False, derived=False)
    staies = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    room = EReference(ordered=True, unique=True, containment=False, derived=False)
    proposals = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, bedNumber=None, person=None, staies=None, room=None, proposals=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if bedNumber is not None:
            self.bedNumber = bedNumber

        if person is not None:
            self.person = person

        if staies:
            self.staies.extend(staies)

        if room is not None:
            self.room = room

        if proposals:
            self.proposals.extend(proposals)


class Proposal(EObject, metaclass=MetaEClass):

    status = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    validated = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    bed = EReference(ordered=True, unique=True, containment=False, derived=False)
    person = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, status=None, validated=None, bed=None, person=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if status is not None:
            self.status = status

        if validated is not None:
            self.validated = validated

        if bed is not None:
            self.bed = bed

        if person is not None:
            self.person = person


class Stay(EObject, metaclass=MetaEClass):

    intakeDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    endDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    person = EReference(ordered=True, unique=True, containment=False, derived=False)
    bed = EReference(ordered=True, unique=True, containment=False, derived=False)
    invoiceItems = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, intakeDate=None, endDate=None, person=None, bed=None, invoiceItems=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if intakeDate is not None:
            self.intakeDate = intakeDate

        if endDate is not None:
            self.endDate = endDate

        if person is not None:
            self.person = person

        if bed is not None:
            self.bed = bed

        if invoiceItems:
            self.invoiceItems.extend(invoiceItems)


class Person(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True, iD=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    birthdate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    registrationDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    abilities = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    staies = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    invoices = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    bed = EReference(ordered=True, unique=True, containment=False, derived=False)
    proposals = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    homeForTheElderly = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, name=None, birthdate=None, registrationDate=None, abilities=None, staies=None, invoices=None, bed=None, proposals=None, homeForTheElderly=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if name is not None:
            self.name = name

        if birthdate is not None:
            self.birthdate = birthdate

        if registrationDate is not None:
            self.registrationDate = registrationDate

        if abilities is not None:
            self.abilities = abilities

        if staies:
            self.staies.extend(staies)

        if invoices:
            self.invoices.extend(invoices)

        if bed is not None:
            self.bed = bed

        if proposals:
            self.proposals.extend(proposals)

        if homeForTheElderly is not None:
            self.homeForTheElderly = homeForTheElderly


class Invoice(EObject, metaclass=MetaEClass):

    invoiceDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    outstandingAmount = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    person = EReference(ordered=True, unique=True, containment=False, derived=False)
    invoiceLines = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, invoiceDate=None, outstandingAmount=None, status=None, person=None, invoiceLines=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if invoiceDate is not None:
            self.invoiceDate = invoiceDate

        if outstandingAmount is not None:
            self.outstandingAmount = outstandingAmount

        if status is not None:
            self.status = status

        if person is not None:
            self.person = person

        if invoiceLines:
            self.invoiceLines.extend(invoiceLines)


class InvoiceItem(EObject, metaclass=MetaEClass):

    invoiceLine = EReference(ordered=True, unique=True, containment=False, derived=False)
    stay = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, invoiceLine=None, stay=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if invoiceLine is not None:
            self.invoiceLine = invoiceLine

        if stay is not None:
            self.stay = stay


class InvoiceLine(EObject, metaclass=MetaEClass):

    invoice = EReference(ordered=True, unique=True, containment=False, derived=False)
    invoiceItem = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, invoice=None, invoiceItem=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if invoice is not None:
            self.invoice = invoice

        if invoiceItem is not None:
            self.invoiceItem = invoiceItem
