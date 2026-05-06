"""Definition of meta model 'BusTransportationManagementSystem'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'BusTransportationManagementSystem'
nsURI = 'BusTransportationManagementSystem'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
Shift = EEnum('Shift', literals=['Morning', 'Afternoon', 'Night'])


class BTMS(EObject, metaclass=MetaEClass):

    vehicles = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    routes = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    assignments = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    drivers = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    schedules = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, vehicles=None, routes=None, assignments=None, drivers=None, schedules=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if vehicles:
            self.vehicles.extend(vehicles)

        if routes:
            self.routes.extend(routes)

        if assignments:
            self.assignments.extend(assignments)

        if drivers:
            self.drivers.extend(drivers)

        if schedules:
            self.schedules.extend(schedules)


class BusVehicle(EObject, metaclass=MetaEClass):

    licencePlate = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    routeAssignments = EReference(ordered=True, unique=True,
                                  containment=False, derived=False, upper=-1)

    def __init__(self, *, licencePlate=None, routeAssignments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if licencePlate is not None:
            self.licencePlate = licencePlate

        if routeAssignments:
            self.routeAssignments.extend(routeAssignments)


class Route(EObject, metaclass=MetaEClass):

    number = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    routeAssignments = EReference(ordered=True, unique=True,
                                  containment=False, derived=False, upper=-1)

    def __init__(self, *, number=None, routeAssignments=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if number is not None:
            self.number = number

        if routeAssignments:
            self.routeAssignments.extend(routeAssignments)


class RouteAssignment(EObject, metaclass=MetaEClass):

    date = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    bus = EReference(ordered=True, unique=True, containment=False, derived=False)
    route = EReference(ordered=True, unique=True, containment=False, derived=False)
    driverSchedules = EReference(ordered=True, unique=True,
                                 containment=False, derived=False, upper=-1)

    def __init__(self, *, date=None, bus=None, route=None, driverSchedules=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if date is not None:
            self.date = date

        if bus is not None:
            self.bus = bus

        if route is not None:
            self.route = route

        if driverSchedules:
            self.driverSchedules.extend(driverSchedules)


class Driver(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    driverSchedules = EReference(ordered=True, unique=True,
                                 containment=False, derived=False, upper=-1)

    def __init__(self, *, id=None, name=None, driverSchedules=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if name is not None:
            self.name = name

        if driverSchedules:
            self.driverSchedules.extend(driverSchedules)


class DriverSchedule(EObject, metaclass=MetaEClass):

    shift = EAttribute(eType=Shift, unique=True, derived=False, changeable=True)
    driver = EReference(ordered=True, unique=True, containment=False, derived=False)
    assignment = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, shift=None, driver=None, assignment=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if shift is not None:
            self.shift = shift

        if driver is not None:
            self.driver = driver

        if assignment is not None:
            self.assignment = assignment
