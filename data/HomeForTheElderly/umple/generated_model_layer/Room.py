# %% NEW FILE Room BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 16 "model.ump"
# line 112 "model.ump"
import os

class Room():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Room Attributes
    #Room Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRoomNumber, aDepartment, aCategory):
        self._beds = None
        self._category = None
        self._department = None
        self._roomNumber = None
        self._roomNumber = aRoomNumber
        didAddDepartment = self.setDepartment(aDepartment)
        if not didAddDepartment :
            raise RuntimeError ("Unable to create room due to department. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCategory = self.setCategory(aCategory)
        if not didAddCategory :
            raise RuntimeError ("Unable to create room due to category. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._beds = []

    #------------------------
    # INTERFACE
    #------------------------
    def setRoomNumber(self, aRoomNumber):
        wasSet = False
        self._roomNumber = aRoomNumber
        wasSet = True
        return wasSet

    def getRoomNumber(self):
        return self._roomNumber

    # Code from template association_GetOne 
    def getDepartment(self):
        return self._department

    # Code from template association_GetOne 
    def getCategory(self):
        return self._category

    # Code from template association_GetMany 
    def getBed(self, index):
        aBed = self._beds[index]
        return aBed

    def getBeds(self):
        newBeds = tuple(self._beds)
        return newBeds

    def numberOfBeds(self):
        number = len(self._beds)
        return number

    def hasBeds(self):
        has = len(self._beds) > 0
        return has

    def indexOfBed(self, aBed):
        index = (-1 if not aBed in self._beds else self._beds.index(aBed))
        return index

    # Code from template association_SetOneToMany 
    def setDepartment(self, aDepartment):
        wasSet = False
        if aDepartment is None :
            return wasSet
        existingDepartment = self._department
        self._department = aDepartment
        if not (existingDepartment is None) and not existingDepartment == aDepartment :
            existingDepartment.removeRoom(self)
        self._department.addRoom(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setCategory(self, aCategory):
        wasSet = False
        if aCategory is None :
            return wasSet
        existingCategory = self._category
        self._category = aCategory
        if not (existingCategory is None) and not existingCategory == aCategory :
            existingCategory.removeRoom(self)
        self._category.addRoom(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfBeds():
        return 0

    # Code from template association_AddManyToOne 
    def addBed1(self, aBedNumber):
        from .Bed import Bed
        return Bed(aBedNumber, self)

    def addBed2(self, aBed):
        wasAdded = False
        if (aBed) in self._beds :
            return False
        existingRoom = aBed.getRoom()
        isNewRoom = not (existingRoom is None) and not self == existingRoom
        if isNewRoom :
            aBed.setRoom(self)
        else :
            self._beds.append(aBed)
        wasAdded = True
        return wasAdded

    def removeBed(self, aBed):
        wasRemoved = False
        #Unable to remove aBed, as it must always have a room
        if not self == aBed.getRoom() :
            self._beds.remove(aBed)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addBedAt(self, aBed, index):
        wasAdded = False
        if self.addBed(aBed) :
            if index < 0 :
                index = 0
            if index > self.numberOfBeds() :
                index = self.numberOfBeds() - 1
            self._beds.remove(aBed)
            self._beds.insert(index, aBed)
            wasAdded = True
        return wasAdded

    def addOrMoveBedAt(self, aBed, index):
        wasAdded = False
        if (aBed) in self._beds :
            if index < 0 :
                index = 0
            if index > self.numberOfBeds() :
                index = self.numberOfBeds() - 1
            self._beds.remove(aBed)
            self._beds.insert(index, aBed)
            wasAdded = True
        else :
            wasAdded = self.addBedAt(aBed, index)
        return wasAdded

    def delete(self):
        placeholderDepartment = self._department
        self._department = None
        if not (placeholderDepartment is None) :
            placeholderDepartment.removeRoom(self)
        placeholderCategory = self._category
        self._category = None
        if not (placeholderCategory is None) :
            placeholderCategory.removeRoom(self)
        i = len(self._beds)
        while i > 0 :
            aBed = self._beds[i - 1]
            aBed.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "roomNumber" + ":" + str(self.getRoomNumber()) + "]" + str(os.linesep) + "  " + "department = " + str(((format(id(self.getDepartment()), "x")) if not (self.getDepartment() is None) else "null")) + str(os.linesep) + "  " + "category = " + ((format(id(self.getCategory()), "x")) if not (self.getCategory() is None) else "null")

    def addBed(self, *argv):
        from .Bed import Bed
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.addBed1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], Bed) :
            return self.addBed2(argv[0])
        raise TypeError("No method matches provided parameters")
