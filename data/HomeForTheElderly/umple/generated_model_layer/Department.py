# %% NEW FILE Department BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 7 "model.ump"
# line 102 "model.ump"
import os

class Department():
    departmentsById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Department Attributes
    #Department Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aHomeForTheElderly):
        self._rooms = None
        self._homeForTheElderly = None
        self._id = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddHomeForTheElderly = self.setHomeForTheElderly(aHomeForTheElderly)
        if not didAddHomeForTheElderly :
            raise RuntimeError ("Unable to create department due to homeForTheElderly. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._rooms = []

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Department.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Department.departmentsById.pop(anOldId, None)
        Department.departmentsById[aId] = self
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithId(aId):
        return Department.departmentsById.get(aId)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithId(aId):
        return not (Department.getWithId(aId) is None)

    # Code from template association_GetOne 
    def getHomeForTheElderly(self):
        return self._homeForTheElderly

    # Code from template association_GetMany 
    def getRoom(self, index):
        aRoom = self._rooms[index]
        return aRoom

    def getRooms(self):
        newRooms = tuple(self._rooms)
        return newRooms

    def numberOfRooms(self):
        number = len(self._rooms)
        return number

    def hasRooms(self):
        has = len(self._rooms) > 0
        return has

    def indexOfRoom(self, aRoom):
        index = (-1 if not aRoom in self._rooms else self._rooms.index(aRoom))
        return index

    # Code from template association_SetOneToMany 
    def setHomeForTheElderly(self, aHomeForTheElderly):
        wasSet = False
        if aHomeForTheElderly is None :
            return wasSet
        existingHomeForTheElderly = self._homeForTheElderly
        self._homeForTheElderly = aHomeForTheElderly
        if not (existingHomeForTheElderly is None) and not existingHomeForTheElderly == aHomeForTheElderly :
            existingHomeForTheElderly.removeDepartment(self)
        self._homeForTheElderly.addDepartment(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRooms():
        return 0

    # Code from template association_AddManyToOne 
    def addRoom1(self, aRoomNumber, aCategory):
        from .Room import Room
        return Room(aRoomNumber, self, aCategory)

    def addRoom2(self, aRoom):
        wasAdded = False
        if (aRoom) in self._rooms :
            return False
        existingDepartment = aRoom.getDepartment()
        isNewDepartment = not (existingDepartment is None) and not self == existingDepartment
        if isNewDepartment :
            aRoom.setDepartment(self)
        else :
            self._rooms.append(aRoom)
        wasAdded = True
        return wasAdded

    def removeRoom(self, aRoom):
        wasRemoved = False
        #Unable to remove aRoom, as it must always have a department
        if not self == aRoom.getDepartment() :
            self._rooms.remove(aRoom)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addRoomAt(self, aRoom, index):
        wasAdded = False
        if self.addRoom(aRoom) :
            if index < 0 :
                index = 0
            if index > self.numberOfRooms() :
                index = self.numberOfRooms() - 1
            self._rooms.remove(aRoom)
            self._rooms.insert(index, aRoom)
            wasAdded = True
        return wasAdded

    def addOrMoveRoomAt(self, aRoom, index):
        wasAdded = False
        if (aRoom) in self._rooms :
            if index < 0 :
                index = 0
            if index > self.numberOfRooms() :
                index = self.numberOfRooms() - 1
            self._rooms.remove(aRoom)
            self._rooms.insert(index, aRoom)
            wasAdded = True
        else :
            wasAdded = self.addRoomAt(aRoom, index)
        return wasAdded

    def delete(self):
        Department.departmentsById.pop(self.getId(), None)
        placeholderHomeForTheElderly = self._homeForTheElderly
        self._homeForTheElderly = None
        if not (placeholderHomeForTheElderly is None) :
            placeholderHomeForTheElderly.removeDepartment(self)
        i = len(self._rooms)
        while i > 0 :
            aRoom = self._rooms[i - 1]
            aRoom.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]" + str(os.linesep) + "  " + "homeForTheElderly = " + ((format(id(self.getHomeForTheElderly()), "x")) if not (self.getHomeForTheElderly() is None) else "null")

    def addRoom(self, *argv):
        from .Room import Room
        from .Category import Category
        if len(argv) == 2 and isinstance(argv[0], int) and isinstance(argv[1], Category) :
            return self.addRoom1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Room) :
            return self.addRoom2(argv[0])
        raise TypeError("No method matches provided parameters")
