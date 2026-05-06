"""Definition of meta model 'biketourplus'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'biketourplus'
nsURI = 'biketourplus'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
Status = EEnum('Status', literals=['NotAssigned', 'Assigned',
               'Paid', 'Started', 'Finished', 'Cancelled', 'Banned'])

LodgeRating = EEnum('LodgeRating', literals=['OneStar',
                    'TwoStars', 'ThreeStars', 'FourStars', 'FiveStars'])


class BikeTourPlus(EObject, metaclass=MetaEClass):

    startDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    nrWeeks = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    priceOfGuidePerWeek = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    manager = EReference(ordered=True, unique=True, containment=True, derived=False)
    guides = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    participants = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    bookedItems = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    gear = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    combos = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    comboItems = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    lodges = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    bikeTours = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, startDate=None, nrWeeks=None, priceOfGuidePerWeek=None, manager=None, guides=None, participants=None, bookedItems=None, gear=None, combos=None, comboItems=None, lodges=None, bikeTours=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if startDate is not None:
            self.startDate = startDate

        if nrWeeks is not None:
            self.nrWeeks = nrWeeks

        if priceOfGuidePerWeek is not None:
            self.priceOfGuidePerWeek = priceOfGuidePerWeek

        if manager is not None:
            self.manager = manager

        if guides:
            self.guides.extend(guides)

        if participants:
            self.participants.extend(participants)

        if bookedItems:
            self.bookedItems.extend(bookedItems)

        if gear:
            self.gear.extend(gear)

        if combos:
            self.combos.extend(combos)

        if comboItems:
            self.comboItems.extend(comboItems)

        if lodges:
            self.lodges.extend(lodges)

        if bikeTours:
            self.bikeTours.extend(bikeTours)


@abstract
class User(EObject, metaclass=MetaEClass):

    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    password = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, email=None, password=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if email is not None:
            self.email = email

        if password is not None:
            self.password = password


class BookedItem(EObject, metaclass=MetaEClass):

    quantity = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    participant = EReference(ordered=True, unique=True, containment=False, derived=False)
    item = EReference(ordered=True, unique=True, containment=False, derived=False)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, quantity=None, participant=None, item=None, bikeTourPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if quantity is not None:
            self.quantity = quantity

        if participant is not None:
            self.participant = participant

        if item is not None:
            self.item = item

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


@abstract
class BookableItem(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    bookedItems = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, name=None, bookedItems=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if bookedItems:
            self.bookedItems.extend(bookedItems)


class ComboItem(EObject, metaclass=MetaEClass):

    quantity = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    combo = EReference(ordered=True, unique=True, containment=False, derived=False)
    gear = EReference(ordered=True, unique=True, containment=False, derived=False)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, quantity=None, combo=None, gear=None, bikeTourPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if quantity is not None:
            self.quantity = quantity

        if combo is not None:
            self.combo = combo

        if gear is not None:
            self.gear = gear

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


class Lodge(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    rating = EAttribute(eType=LodgeRating, unique=True, derived=False, changeable=True)
    bikeTours = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, name=None, address=None, rating=None, bikeTours=None, bikeTourPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if rating is not None:
            self.rating = rating

        if bikeTours:
            self.bikeTours.extend(bikeTours)

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


class BikeTour(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    startWeek = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    endWeek = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    participants = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    guide = EReference(ordered=True, unique=True, containment=False, derived=False)
    lodge = EReference(ordered=True, unique=True, containment=False, derived=False)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, startWeek=None, endWeek=None, participants=None, guide=None, lodge=None, bikeTourPlus=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if startWeek is not None:
            self.startWeek = startWeek

        if endWeek is not None:
            self.endWeek = endWeek

        if participants:
            self.participants.extend(participants)

        if guide is not None:
            self.guide = guide

        if lodge is not None:
            self.lodge = lodge

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


class Manager(User):

    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, bikeTourPlus=None, **kwargs):

        super().__init__(**kwargs)

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


@abstract
class NamedUser(User):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    emergencyContact = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None, emergencyContact=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if emergencyContact is not None:
            self.emergencyContact = emergencyContact


class Gear(BookableItem):

    pricePerWeek = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    comboItems = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, pricePerWeek=None, comboItems=None, bikeTourPlus=None, **kwargs):

        super().__init__(**kwargs)

        if pricePerWeek is not None:
            self.pricePerWeek = pricePerWeek

        if comboItems:
            self.comboItems.extend(comboItems)

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


class Combo(BookableItem):

    discount = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    comboItems = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, discount=None, comboItems=None, bikeTourPlus=None, **kwargs):

        super().__init__(**kwargs)

        if discount is not None:
            self.discount = discount

        if comboItems:
            self.comboItems.extend(comboItems)

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


class Guide(NamedUser):

    bikeTours = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, bikeTours=None, bikeTourPlus=None, **kwargs):

        super().__init__(**kwargs)

        if bikeTours:
            self.bikeTours.extend(bikeTours)

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus


class Participant(NamedUser):

    nrWeeks = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    weekAvailableFrom = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    weekAvailableUntil = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    lodgeRequired = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    authorizationCode = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    refundedPercentageAmount = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=Status, unique=True, derived=False, changeable=True)
    bikeTour = EReference(ordered=True, unique=True, containment=False, derived=False)
    bookedItems = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    bikeTourPlus = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, nrWeeks=None, weekAvailableFrom=None, weekAvailableUntil=None, lodgeRequired=None, authorizationCode=None, refundedPercentageAmount=None, status=None, bikeTour=None, bookedItems=None, bikeTourPlus=None, **kwargs):

        super().__init__(**kwargs)

        if nrWeeks is not None:
            self.nrWeeks = nrWeeks

        if weekAvailableFrom is not None:
            self.weekAvailableFrom = weekAvailableFrom

        if weekAvailableUntil is not None:
            self.weekAvailableUntil = weekAvailableUntil

        if lodgeRequired is not None:
            self.lodgeRequired = lodgeRequired

        if authorizationCode is not None:
            self.authorizationCode = authorizationCode

        if refundedPercentageAmount is not None:
            self.refundedPercentageAmount = refundedPercentageAmount

        if status is not None:
            self.status = status

        if bikeTour is not None:
            self.bikeTour = bikeTour

        if bookedItems:
            self.bookedItems.extend(bookedItems)

        if bikeTourPlus is not None:
            self.bikeTourPlus = bikeTourPlus
