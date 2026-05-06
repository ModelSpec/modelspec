from datetime import date
from pyecore.ecore import EDate
from ..generated_model_layer import BTMS, Driver, Route, RouteAssignment, BusVehicle


class BusTransportationManagementSystemController:
    def __init__(self):
        self.btms = BTMS()

    def createDriver(self, drivername: str):
        if not drivername:
            raise ValueError("The name of a driver cannot be empty.")
        self.btms.drivers.append(Driver(name=drivername))

    def createRoute(self, number: int):
        if number <= 0:
            raise ValueError("The number of a route must be greater than zero.")
        if number > 9999:
            raise ValueError("The number of a route cannot be greater than 9999.")
        if any(route.number == number for route in self.btms.routes):
            raise ValueError(
                "A route with this number already exists. Please use a different number."
            )
        self.btms.routes.append(Route(number=number))

    def createRouteAssignment(self, licensePlate: str, route: int, _date: date):
        if not any(vehicle.licencePlate == licensePlate for vehicle in self.btms.vehicles):
            raise ValueError("A bus must be specified for the assignment.")
        if not any((_route.number == route) for _route in self.btms.routes):
            raise ValueError("A route must be specified for the assignment.")
        today = date.today()
        try:
            one_year_from_today = today.replace(year=today.year + 1)
        except ValueError:
            # 29 February: fall back to 28 February of the next year
            one_year_from_today = today.replace(year=today.year + 1, day=28)
        if not today <= _date <= one_year_from_today:
            raise ValueError("The date must be within a year from today.")

        vehicle = next(v for v in self.btms.vehicles if v.licencePlate == licensePlate)
        route_obj = next(r for r in self.btms.routes if r.number == route)

        edate = EDate.from_string(_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"))
        route_assignment = RouteAssignment(date=edate, route=route_obj, bus=vehicle)
        self.btms.assignments.append(route_assignment)
        vehicle.routeAssignments.append(route_assignment)
