from ..generated_model_layer import *

class HouseController:
    def __init__(self):
        self.houses = []
        self.companies = []
    
    def createHouse(self, address: str, material: House.BMType, basementType: str, basementName: str, basementSize: float, basementQuality: float, basementHumidity: float) -> None:
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

        house = House(address, material)

        if basementType == "concrete":
            ConcreteBasement(basementSize, basementName, house, basementQuality)

        if basementType == "earth":
            EarthBasement(basementSize, basementName, house, basementHumidity)

        self.houses.append(house)

    def createCompany(self, name: str, address: str) -> None:
        if name == "":
            raise ValueError("The name of a company cannot be empty.")

        if address == "":
            raise ValueError("The address of a company cannot be empty.")

        company = Company(name, address)
        self.companies.append(company)

    def createJobLog(self, hours: int, price: float, houseAddress: str, companyName: str) -> None:
        if hours <= 0:
            raise ValueError("The number of hours must be greater than 0.")

        if price < 0:
            raise ValueError("The price must be at least 0.")

        house = None
        for h in self.houses:
            if h.getAddress() == houseAddress:
                house = h
                break

        if house is None:
            raise ValueError("The house does not exist.")

        company = None
        for c in self.companies:
            if c.getName() == companyName:
                company = c
                break

        if company is None:
            raise ValueError("The company does not exist.")

        house.addJobLog(hours, price, company)

    def createSemiDetachedWithCarport(self, address: str, buildingMaterial: House.BMType, windows: int, garden: bool, dp1: bool, fr1: bool, dp2: bool, fr2: bool, basementType: str, basementName: str, basementSize: float, basementQuality: float, basementHumidity: float) -> None:
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

        house = SemiDetachedWithCarport(address, buildingMaterial, garden, windows)
        Carport(dp1, fr1, house)
        Carport(dp2, fr2, house)

        if basementType == "concrete":
            ConcreteBasement(basementSize, basementName, house, basementQuality)

        if basementType == "earth":
            EarthBasement(basementSize, basementName, house, basementHumidity)

        self.houses.append(house)

    def createSemiDetachedWithGarage(self, address: str, buildingMaterial: House.BMType, windows: int, garden: bool, automatic: bool, basementType: str, basementName: str, basementSize: float, basementQuality: float, basementHumidity: float) -> None:
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

        house = SemiDetachedWithGarage(address, buildingMaterial, garden, windows, automatic)

        if basementType == "concrete":
            ConcreteBasement(basementSize, basementName, house, basementQuality)

        if basementType == "earth":
            EarthBasement(basementSize, basementName, house, basementHumidity)

        self.houses.append(house)