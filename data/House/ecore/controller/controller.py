from ..generated_model_layer import *

class HouseController:
    def __init__(self):
        self.houses = []
        self.companies = []

    def createHouse(self, address: str, material: BMType, basementType: str, basementName: str, basementSize: float, basementQuality: float, basementHumidity: float) -> None:
        if address == "":
            raise ValueError("The address of a house cannot be empty.")

        if material is None:
            raise ValueError("The building material cannot be empty.")

        if basementType not in ["", "concrete", "earth"]:
            raise ValueError('The type of a basement must be either "concrete", "earth" or empty.')

        if basementType != "":
            if basementName == "":
                raise ValueError("The name of a basement cannot be empty.")

            if basementSize <= 0:
                raise ValueError("The size of a basement must be greater than 0.")

            if basementType == "concrete":
                if basementQuality < 0 or basementQuality > 1:
                    raise ValueError("The quality of a concrete basement must be between 0 and 1.")

                if basementHumidity != 0:
                    raise ValueError("The humidity of a concrete basement must be 0.")

            if basementType == "earth":
                if basementHumidity < 0 or basementHumidity > 1:
                    raise ValueError("The humidity of an earth basement must be between 0 and 1.")

                if basementQuality != 0:
                    raise ValueError("The quality of an earth basement must be 0.")

        house = House(address=address, buildingMaterial=material)

        if basementType == "concrete":
            ConcreteBasement(size=basementSize, name=basementName, house=house, quality=basementQuality)

        if basementType == "earth":
            EarthBasement(size=basementSize, name=basementName, house=house, humidity=basementHumidity)

        self.houses.append(house)

    def createCompany(self, name: str, address: str) -> None:
        if name == "":
            raise ValueError("The name of a company cannot be empty.")

        if address == "":
            raise ValueError("The address of a company cannot be empty.")

        company = Company(name=name, address=address)
        self.companies.append(company)

    def createJobLog(self, hours: int, price: float, houseAddress: str, companyName: str) -> None:
        if hours <= 0:
            raise ValueError("The number of hours must be greater than 0.")

        if price < 0:
            raise ValueError("The price must be at least 0.")

        house = None
        for h in self.houses:
            if h.address == houseAddress:
                house = h
                break

        if house is None:
            raise ValueError("The house does not exist.")

        company = None
        for c in self.companies:
            if c.name == companyName:
                company = c
                break

        if company is None:
            raise ValueError("The company does not exist.")

        JobLog(hours=hours, price=price, house=house, company=company)

    def createSemiDetachedWithCarport(self, address: str, buildingMaterial: BMType, windows: int, garden: bool, dp1: bool, fr1: bool, dp2: bool, fr2: bool, basementType: str, basementName: str, basementSize: float, basementQuality: float, basementHumidity: float) -> None:
        if address == "":
            raise ValueError("The address of a house cannot be empty.")

        if buildingMaterial is None:
            raise ValueError("The building material cannot be empty.")

        if windows < 0:
            raise ValueError("The number of windows must be non-negative.")

        if basementType not in ["", "concrete", "earth"]:
            raise ValueError('The type of a basement must be either "concrete", "earth" or empty.')

        if basementType != "":
            if basementName == "":
                raise ValueError("The name of a basement cannot be empty.")

            if basementSize <= 0:
                raise ValueError("The size of a basement must be greater than 0.")

            if basementType == "concrete":
                if basementQuality < 0 or basementQuality > 1:
                    raise ValueError("The quality of a concrete basement must be between 0 and 1.")

                if basementHumidity != 0:
                    raise ValueError("The humidity of a concrete basement must be 0.")

            if basementType == "earth":
                if basementHumidity < 0 or basementHumidity > 1:
                    raise ValueError("The humidity of an earth basement must be between 0 and 1.")

                if basementQuality != 0:
                    raise ValueError("The quality of an earth basement must be 0.")

        house = SemiDetachedWithCarport(address=address, buildingMaterial=buildingMaterial, garden=garden, windows=windows)
        Carport(doublePort=dp1, flatRoof=fr1, semiDetachedWithCarport=house)
        Carport(doublePort=dp2, flatRoof=fr2, semiDetachedWithCarport=house)

        if basementType == "concrete":
            ConcreteBasement(size=basementSize, name=basementName, house=house, quality=basementQuality)

        if basementType == "earth":
            EarthBasement(size=basementSize, name=basementName, house=house, humidity=basementHumidity)

        self.houses.append(house)

    def createSemiDetachedWithGarage(self, address: str, buildingMaterial: BMType, windows: int, garden: bool, automatic: bool, basementType: str, basementName: str, basementSize: float, basementQuality: float, basementHumidity: float) -> None:
        if address == "":
            raise ValueError("The address of a house cannot be empty.")

        if buildingMaterial is None:
            raise ValueError("The building material cannot be empty.")

        if windows < 0:
            raise ValueError("The number of windows must be non-negative.")

        if basementType not in ["", "concrete", "earth"]:
            raise ValueError('The type of a basement must be either "concrete", "earth" or empty.')

        if basementType != "":
            if basementName == "":
                raise ValueError("The name of a basement cannot be empty.")

            if basementSize <= 0:
                raise ValueError("The size of a basement must be greater than 0.")

            if basementType == "concrete":
                if basementQuality < 0 or basementQuality > 1:
                    raise ValueError("The quality of a concrete basement must be between 0 and 1.")

                if basementHumidity != 0:
                    raise ValueError("The humidity of a concrete basement must be 0.")

            if basementType == "earth":
                if basementHumidity < 0 or basementHumidity > 1:
                    raise ValueError("The humidity of an earth basement must be between 0 and 1.")

                if basementQuality != 0:
                    raise ValueError("The quality of an earth basement must be 0.")

        garage = Garage(automatic=automatic)
        house = SemiDetachedWithGarage(address=address, buildingMaterial=buildingMaterial, garden=garden, windows=windows, garage=garage)

        if basementType == "concrete":
            ConcreteBasement(size=basementSize, name=basementName, house=house, quality=basementQuality)

        if basementType == "earth":
            EarthBasement(size=basementSize, name=basementName, house=house, humidity=basementHumidity)
        self.houses.append(house)