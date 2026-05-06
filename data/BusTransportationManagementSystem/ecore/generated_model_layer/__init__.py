
from .BusTransportationManagementSystem import getEClassifier, eClassifiers
from .BusTransportationManagementSystem import name, nsURI, nsPrefix, eClass
from .BusTransportationManagementSystem import BTMS, BusVehicle, Route, RouteAssignment, Driver, DriverSchedule, Shift


from . import BusTransportationManagementSystem

__all__ = ['BTMS', 'BusVehicle', 'Route', 'RouteAssignment', 'Driver', 'DriverSchedule', 'Shift']

eSubpackages = []
eSuperPackage = None
BusTransportationManagementSystem.eSubpackages = eSubpackages
BusTransportationManagementSystem.eSuperPackage = eSuperPackage

BTMS.vehicles.eType = BusVehicle
BTMS.routes.eType = Route
BTMS.assignments.eType = RouteAssignment
BTMS.drivers.eType = Driver
BTMS.schedules.eType = DriverSchedule
BusVehicle.routeAssignments.eType = RouteAssignment
Route.routeAssignments.eType = RouteAssignment
RouteAssignment.bus.eType = BusVehicle
RouteAssignment.bus.eOpposite = BusVehicle.routeAssignments
RouteAssignment.route.eType = Route
RouteAssignment.route.eOpposite = Route.routeAssignments
RouteAssignment.driverSchedules.eType = DriverSchedule
Driver.driverSchedules.eType = DriverSchedule
DriverSchedule.driver.eType = Driver
DriverSchedule.driver.eOpposite = Driver.driverSchedules
DriverSchedule.assignment.eType = RouteAssignment
DriverSchedule.assignment.eOpposite = RouteAssignment.driverSchedules

otherClassifiers = [Shift]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
