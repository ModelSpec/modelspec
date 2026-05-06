from datetime import date
from ..generated_model_layer import BusTransportationManagementSystem


class BusTransportationManagementSystemController:
    def __init__(self):
        self.btms = BusTransportationManagementSystem()


    def createDriver(self, drivername: str):
        if not drivername:
            raise ValueError('The name of a driver cannot be empty.')

        self.btms.addDriver(drivername)


    def createRoute(self, number: int):
        if number <= 0:
            raise ValueError('The number of a route must be greater than zero.')

        if number > 9999:
            raise ValueError('The number of a route cannot be greater than 9999.')

        if any(route.getNumber() == number for route in self.btms.getRoutes()):
            raise ValueError('A route with this number already exists. Please use a different number.')

        self.btms.addRoute(number)


    def createRouteAssignment(self, licensePlate: str, route: int, _date: date):
        # Check bus existence
        if not any(vehicle.getLicencePlate() == licensePlate for vehicle in self.btms.getVehicles()):
            raise ValueError('A bus must be specified for the assignment.')

        # Check route existence
        if not any((_route.getNumber() == route) for _route in self.btms.getRoutes()):
            raise ValueError('A route must be specified for the assignment.')

        # Validate date (within one year from today)
        today = date.today()
        try:
            oneYearFromToday = today.replace(year=today.year + 1)
        except ValueError:
            # 29 February: fall back to 28 February of the next year
            oneYearFromToday = today.replace(year=today.year + 1, day=28)
        if not today <= _date <= oneYearFromToday:
            raise ValueError('The date must be within a year from today.')

        vehicle = next(vehicle for vehicle in self.btms.getVehicles() if vehicle.getLicencePlate() == licensePlate)
        route = next(_route for _route in self.btms.getRoutes() if _route.getNumber() == route)

        # Create the new assignment
        self.btms.addAssignment(_date, vehicle, route)