"""Definition of meta model 'House'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'House'
nsURI = 'House'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
BMType = EEnum('BMType', literals=['WOOD', 'BRICK', 'CONCRETE'])


@abstract
class Basement(EObject, metaclass=MetaEClass):

    size = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    house = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, size=None, name=None, house=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if size is not None:
            self.size = size

        if name is not None:
            self.name = name

        if house is not None:
            self.house = house


class House(EObject, metaclass=MetaEClass):

    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    buildingMaterial = EAttribute(eType=BMType, unique=True, derived=False, changeable=True)
    basement = EReference(ordered=True, unique=True, containment=False, derived=False)
    jobLogs = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, address=None, buildingMaterial=None, basement=None, jobLogs=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if address is not None:
            self.address = address

        if buildingMaterial is not None:
            self.buildingMaterial = buildingMaterial

        if basement is not None:
            self.basement = basement

        if jobLogs:
            self.jobLogs.extend(jobLogs)


class Carport(EObject, metaclass=MetaEClass):

    doublePort = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    flatRoof = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    semiDetachedWithCarport = EReference(
        ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, doublePort=None, flatRoof=None, semiDetachedWithCarport=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if doublePort is not None:
            self.doublePort = doublePort

        if flatRoof is not None:
            self.flatRoof = flatRoof

        if semiDetachedWithCarport is not None:
            self.semiDetachedWithCarport = semiDetachedWithCarport


class Garage(EObject, metaclass=MetaEClass):

    automatic = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    semiDetachedWithGarage = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, automatic=None, semiDetachedWithGarage=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if automatic is not None:
            self.automatic = automatic

        if semiDetachedWithGarage is not None:
            self.semiDetachedWithGarage = semiDetachedWithGarage


class Company(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    address = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    jobLogs = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, name=None, address=None, jobLogs=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if address is not None:
            self.address = address

        if jobLogs:
            self.jobLogs.extend(jobLogs)


class JobLog(EObject, metaclass=MetaEClass):

    hours = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    price = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    house = EReference(ordered=True, unique=True, containment=False, derived=False)
    company = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, hours=None, price=None, house=None, company=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if hours is not None:
            self.hours = hours

        if price is not None:
            self.price = price

        if house is not None:
            self.house = house

        if company is not None:
            self.company = company


class ConcreteBasement(Basement):

    quality = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)

    def __init__(self, *, quality=None, **kwargs):

        super().__init__(**kwargs)

        if quality is not None:
            self.quality = quality


class EarthBasement(Basement):

    humidity = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)

    def __init__(self, *, humidity=None, **kwargs):

        super().__init__(**kwargs)

        if humidity is not None:
            self.humidity = humidity


@abstract
class SemiDetached(House):

    garden = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    windows = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)

    def __init__(self, *, garden=None, windows=None, **kwargs):

        super().__init__(**kwargs)

        if garden is not None:
            self.garden = garden

        if windows is not None:
            self.windows = windows


class SemiDetachedWithCarport(SemiDetached):

    carports = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, carports=None, **kwargs):

        super().__init__(**kwargs)

        if carports:
            self.carports.extend(carports)


class SemiDetachedWithGarage(SemiDetached):

    garage = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, garage=None, **kwargs):

        super().__init__(**kwargs)

        if garage is not None:
            self.garage = garage
