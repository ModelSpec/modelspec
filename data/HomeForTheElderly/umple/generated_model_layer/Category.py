# %% NEW FILE Category BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 11 "model.ump"
# line 107 "model.ump"

class Category():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Category Attributes
    #Category Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aPrice, aType):
        self._rooms = None
        self._type = None
        self._price = None
        self._price = aPrice
        self._type = aType
        self._rooms = []

    #------------------------
    # INTERFACE
    #------------------------
    def setPrice(self, aPrice):
        wasSet = False
        self._price = aPrice
        wasSet = True
        return wasSet

    def setType(self, aType):
        wasSet = False
        self._type = aType
        wasSet = True
        return wasSet

    def getPrice(self):
        return self._price

    def getType(self):
        return self._type

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

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRooms():
        return 0

    # Code from template association_AddManyToOne 
    def addRoom1(self, aRoomNumber, aDepartment):
        from .Room import Room
        return Room(aRoomNumber, aDepartment, self)

    def addRoom2(self, aRoom):
        wasAdded = False
        if (aRoom) in self._rooms :
            return False
        existingCategory = aRoom.getCategory()
        isNewCategory = not (existingCategory is None) and not self == existingCategory
        if isNewCategory :
            aRoom.setCategory(self)
        else :
            self._rooms.append(aRoom)
        wasAdded = True
        return wasAdded

    def removeRoom(self, aRoom):
        wasRemoved = False
        #Unable to remove aRoom, as it must always have a category
        if not self == aRoom.getCategory() :
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
        i = len(self._rooms)
        while i > 0 :
            aRoom = self._rooms[i - 1]
            aRoom.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "price" + ":" + str(self.getPrice()) + "," + "type" + ":" + str(self.getType()) + "]"

    def addRoom(self, *argv):
        from .Room import Room
        from .Department import Department
        if len(argv) == 2 and isinstance(argv[0], int) and isinstance(argv[1], Department) :
            return self.addRoom1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Room) :
            return self.addRoom2(argv[0])
        raise TypeError("No method matches provided parameters")
