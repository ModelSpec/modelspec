# %% NEW FILE HomeForTheElderly BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
# line 97 "model.ump"

class HomeForTheElderly():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #HomeForTheElderly Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._people = None
        self._departments = None
        self._departments = []
        self._people = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getDepartment(self, index):
        aDepartment = self._departments[index]
        return aDepartment

    def getDepartments(self):
        newDepartments = tuple(self._departments)
        return newDepartments

    def numberOfDepartments(self):
        number = len(self._departments)
        return number

    def hasDepartments(self):
        has = len(self._departments) > 0
        return has

    def indexOfDepartment(self, aDepartment):
        index = (-1 if not aDepartment in self._departments else self._departments.index(aDepartment))
        return index

    # Code from template association_GetMany 
    def getPeople1(self, index):
        aPeople = self._people[index]
        return aPeople

    def getPeople2(self):
        newPeople = tuple(self._people)
        return newPeople

    def numberOfPeople(self):
        number = len(self._people)
        return number

    def hasPeople(self):
        has = len(self._people) > 0
        return has

    def indexOfPeople(self, aPeople):
        index = (-1 if not aPeople in self._people else self._people.index(aPeople))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfDepartments():
        return 0

    # Code from template association_AddManyToOne 
    def addDepartment1(self, aId):
        from .Department import Department
        return Department(aId, self)

    def addDepartment2(self, aDepartment):
        wasAdded = False
        if (aDepartment) in self._departments :
            return False
        existingHomeForTheElderly = aDepartment.getHomeForTheElderly()
        isNewHomeForTheElderly = not (existingHomeForTheElderly is None) and not self == existingHomeForTheElderly
        if isNewHomeForTheElderly :
            aDepartment.setHomeForTheElderly(self)
        else :
            self._departments.append(aDepartment)
        wasAdded = True
        return wasAdded

    def removeDepartment(self, aDepartment):
        wasRemoved = False
        #Unable to remove aDepartment, as it must always have a homeForTheElderly
        if not self == aDepartment.getHomeForTheElderly() :
            self._departments.remove(aDepartment)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addDepartmentAt(self, aDepartment, index):
        wasAdded = False
        if self.addDepartment(aDepartment) :
            if index < 0 :
                index = 0
            if index > self.numberOfDepartments() :
                index = self.numberOfDepartments() - 1
            self._departments.remove(aDepartment)
            self._departments.insert(index, aDepartment)
            wasAdded = True
        return wasAdded

    def addOrMoveDepartmentAt(self, aDepartment, index):
        wasAdded = False
        if (aDepartment) in self._departments :
            if index < 0 :
                index = 0
            if index > self.numberOfDepartments() :
                index = self.numberOfDepartments() - 1
            self._departments.remove(aDepartment)
            self._departments.insert(index, aDepartment)
            wasAdded = True
        else :
            wasAdded = self.addDepartmentAt(aDepartment, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfPeople():
        return 0

    # Code from template association_AddManyToOne 
    def addPeople1(self, aId, aName, aBirthdate):
        from .Person import Person
        return Person(aId, aName, aBirthdate, self)

    def addPeople2(self, aPeople):
        wasAdded = False
        if (aPeople) in self._people :
            return False
        existingHomeForTheElderly = aPeople.getHomeForTheElderly()
        isNewHomeForTheElderly = not (existingHomeForTheElderly is None) and not self == existingHomeForTheElderly
        if isNewHomeForTheElderly :
            aPeople.setHomeForTheElderly(self)
        else :
            self._people.append(aPeople)
        wasAdded = True
        return wasAdded

    def removePeople(self, aPeople):
        wasRemoved = False
        #Unable to remove aPeople, as it must always have a homeForTheElderly
        if not self == aPeople.getHomeForTheElderly() :
            self._people.remove(aPeople)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addPeopleAt(self, aPeople, index):
        wasAdded = False
        if self.addPeople(aPeople) :
            if index < 0 :
                index = 0
            if index > self.numberOfPeople() :
                index = self.numberOfPeople() - 1
            self._people.remove(aPeople)
            self._people.insert(index, aPeople)
            wasAdded = True
        return wasAdded

    def addOrMovePeopleAt(self, aPeople, index):
        wasAdded = False
        if (aPeople) in self._people :
            if index < 0 :
                index = 0
            if index > self.numberOfPeople() :
                index = self.numberOfPeople() - 1
            self._people.remove(aPeople)
            self._people.insert(index, aPeople)
            wasAdded = True
        else :
            wasAdded = self.addPeopleAt(aPeople, index)
        return wasAdded

    def delete(self):

        while len(self._departments) > 0 :
            aDepartment = self._departments[len(self._departments) - 1]
            aDepartment.delete()
            self._departments.remove(aDepartment)

        while len(self._people) > 0 :
            aPeople = self._people[len(self._people) - 1]
            aPeople.delete()
            self._people.remove(aPeople)

    def getPeople(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getPeople1(argv[0])
        if len(argv) == 0 :
            return self.getPeople2()
        raise TypeError("No method matches provided parameters")

    def addDepartment(self, *argv):
        from .Department import Department
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addDepartment1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Department) :
            return self.addDepartment2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addPeople(self, *argv):
        from .Person import Person
        from datetime import date
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], date) :
            return self.addPeople1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Person) :
            return self.addPeople2(argv[0])
        raise TypeError("No method matches provided parameters")
