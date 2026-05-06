import os

class CourseSection():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #CourseSection Attributes
    #CourseSection Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aCode, aProfessor, aDays, aTime, aMaxCapacity, aRegistered, aOpen):
        self._registrations = None
        self._open = None
        self._registered = None
        self._maxCapacity = None
        self._time = None
        self._days = None
        self._professor = None
        self._code = None
        self._name = None
        self._name = aName
        self._code = aCode
        self._professor = aProfessor
        self._days = aDays
        self._time = aTime
        self._maxCapacity = aMaxCapacity
        self._registered = aRegistered
        self._open = aOpen
        self._registrations = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setCode(self, aCode):
        wasSet = False
        self._code = aCode
        wasSet = True
        return wasSet

    def setProfessor(self, aProfessor):
        wasSet = False
        self._professor = aProfessor
        wasSet = True
        return wasSet

    def setDays(self, aDays):
        wasSet = False
        self._days = aDays
        wasSet = True
        return wasSet

    def setTime(self, aTime):
        wasSet = False
        self._time = aTime
        wasSet = True
        return wasSet

    def setMaxCapacity(self, aMaxCapacity):
        wasSet = False
        self._maxCapacity = aMaxCapacity
        wasSet = True
        return wasSet

    def setRegistered(self, aRegistered):
        wasSet = False
        self._registered = aRegistered
        wasSet = True
        return wasSet

    def setOpen(self, aOpen):
        wasSet = False
        self._open = aOpen
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getCode(self):
        return self._code

    def getProfessor(self):
        return self._professor

    def getDays(self):
        return self._days

    def getTime(self):
        return self._time

    def getMaxCapacity(self):
        return self._maxCapacity

    def getRegistered(self):
        return self._registered

    def getOpen(self):
        return self._open

    # Code from template association_GetMany 
    def getRegistration(self, index):
        aRegistration = self._registrations[index]
        return aRegistration

    def getRegistrations(self):
        newRegistrations = tuple(self._registrations)
        return newRegistrations

    def numberOfRegistrations(self):
        number = len(self._registrations)
        return number

    def hasRegistrations(self):
        has = len(self._registrations) > 0
        return has

    def indexOfRegistration(self, aRegistration):
        index = (-1 if not aRegistration in self._registrations else self._registrations.index(aRegistration))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRegistrations():
        return 0

    # Code from template association_AddManyToOne 
    def addRegistration1(self, aRegistrationId, aGrade, aPassed, aStudent):
        return Registration(aRegistrationId, aGrade, aPassed, aStudent, self)

    def addRegistration2(self, aRegistration):
        wasAdded = False
        if (aRegistration) in self._registrations :
            return False
        existingCourseSection = aRegistration.getCourseSection()
        isNewCourseSection = not (existingCourseSection is None) and not self == existingCourseSection
        if isNewCourseSection :
            aRegistration.setCourseSection(self)
        else :
            self._registrations.append(aRegistration)
        wasAdded = True
        return wasAdded

    def removeRegistration(self, aRegistration):
        wasRemoved = False
        #Unable to remove aRegistration, as it must always have a courseSection
        if not self == aRegistration.getCourseSection() :
            self._registrations.remove(aRegistration)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addRegistrationAt(self, aRegistration, index):
        wasAdded = False
        if self.addRegistration(aRegistration) :
            if index < 0 :
                index = 0
            if index > self.numberOfRegistrations() :
                index = self.numberOfRegistrations() - 1
            self._registrations.remove(aRegistration)
            self._registrations.insert(index, aRegistration)
            wasAdded = True
        return wasAdded

    def addOrMoveRegistrationAt(self, aRegistration, index):
        wasAdded = False
        if (aRegistration) in self._registrations :
            if index < 0 :
                index = 0
            if index > self.numberOfRegistrations() :
                index = self.numberOfRegistrations() - 1
            self._registrations.remove(aRegistration)
            self._registrations.insert(index, aRegistration)
            wasAdded = True
        else :
            wasAdded = self.addRegistrationAt(aRegistration, index)
        return wasAdded

    def delete(self):
        i = len(self._registrations)
        while i > 0 :
            aRegistration = self._registrations[i - 1]
            aRegistration.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "code" + ":" + str(self.getCode()) + "," + "professor" + ":" + str(self.getProfessor()) + "," + "days" + ":" + str(self.getDays()) + "," + "time" + ":" + str(self.getTime()) + "," + "maxCapacity" + ":" + str(self.getMaxCapacity()) + "," + "registered" + ":" + str(self.getRegistered()) + "," + "open" + ":" + str(self.getOpen()) + "]"

    def addRegistration(self, *argv):
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], (float, int)) and isinstance(argv[2], bool) and isinstance(argv[3], Student) :
            return self.addRegistration1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], Registration) :
            return self.addRegistration2(argv[0])
        raise TypeError("No method matches provided parameters")

class Registration():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Registration Attributes
    #Registration Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRegistrationId, aGrade, aPassed, aStudent, aCourseSection):
        self._courseSection = None
        self._student = None
        self._passed = None
        self._grade = None
        self._registrationId = None
        self._registrationId = aRegistrationId
        self._grade = aGrade
        self._passed = aPassed
        didAddStudent = self.setStudent(aStudent)
        if not didAddStudent :
            raise RuntimeError ("Unable to create registration due to student. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCourseSection = self.setCourseSection(aCourseSection)
        if not didAddCourseSection :
            raise RuntimeError ("Unable to create registration due to courseSection. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setRegistrationId(self, aRegistrationId):
        wasSet = False
        self._registrationId = aRegistrationId
        wasSet = True
        return wasSet

    def setGrade(self, aGrade):
        wasSet = False
        self._grade = aGrade
        wasSet = True
        return wasSet

    def setPassed(self, aPassed):
        wasSet = False
        self._passed = aPassed
        wasSet = True
        return wasSet

    def getRegistrationId(self):
        return self._registrationId

    def getGrade(self):
        return self._grade

    def getPassed(self):
        return self._passed

    # Code from template association_GetOne 
    def getStudent(self):
        return self._student

    # Code from template association_GetOne 
    def getCourseSection(self):
        return self._courseSection

    # Code from template association_SetOneToMany 
    def setStudent(self, aStudent):
        wasSet = False
        if aStudent is None :
            return wasSet
        existingStudent = self._student
        self._student = aStudent
        if not (existingStudent is None) and not existingStudent == aStudent :
            existingStudent.removeRegistration(self)
        self._student.addRegistration(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setCourseSection(self, aCourseSection):
        wasSet = False
        if aCourseSection is None :
            return wasSet
        existingCourseSection = self._courseSection
        self._courseSection = aCourseSection
        if not (existingCourseSection is None) and not existingCourseSection == aCourseSection :
            existingCourseSection.removeRegistration(self)
        self._courseSection.addRegistration(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderStudent = self._student
        self._student = None
        if not (placeholderStudent is None) :
            placeholderStudent.removeRegistration(self)
        placeholderCourseSection = self._courseSection
        self._courseSection = None
        if not (placeholderCourseSection is None) :
            placeholderCourseSection.removeRegistration(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "registrationId" + ":" + str(self.getRegistrationId()) + "," + "grade" + ":" + str(self.getGrade()) + "," + "passed" + ":" + str(self.getPassed()) + "]" + str(os.linesep) + "  " + "student = " + str(((format(id(self.getStudent()), "x")) if not (self.getStudent() is None) else "null")) + str(os.linesep) + "  " + "courseSection = " + ((format(id(self.getCourseSection()), "x")) if not (self.getCourseSection() is None) else "null")

class Student():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Student Attributes
    #Student Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aBirthday, aName, aGpa):
        self._registrations = None
        self._gpa = None
        self._name = None
        self._birthday = None
        self._id = None
        self._id = aId
        self._birthday = aBirthday
        self._name = aName
        self._gpa = aGpa
        self._registrations = []

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        self._id = aId
        wasSet = True
        return wasSet

    def setBirthday(self, aBirthday):
        wasSet = False
        self._birthday = aBirthday
        wasSet = True
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setGpa(self, aGpa):
        wasSet = False
        self._gpa = aGpa
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    def getBirthday(self):
        return self._birthday

    def getName(self):
        return self._name

    def getGpa(self):
        return self._gpa

    # Code from template association_GetMany 
    def getRegistration(self, index):
        aRegistration = self._registrations[index]
        return aRegistration

    def getRegistrations(self):
        newRegistrations = tuple(self._registrations)
        return newRegistrations

    def numberOfRegistrations(self):
        number = len(self._registrations)
        return number

    def hasRegistrations(self):
        has = len(self._registrations) > 0
        return has

    def indexOfRegistration(self, aRegistration):
        index = (-1 if not aRegistration in self._registrations else self._registrations.index(aRegistration))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfRegistrations():
        return 0

    # Code from template association_AddManyToOne 
    def addRegistration1(self, aRegistrationId, aGrade, aPassed, aCourseSection):
        return Registration(aRegistrationId, aGrade, aPassed, self, aCourseSection)

    def addRegistration2(self, aRegistration):
        wasAdded = False
        if (aRegistration) in self._registrations :
            return False
        existingStudent = aRegistration.getStudent()
        isNewStudent = not (existingStudent is None) and not self == existingStudent
        if isNewStudent :
            aRegistration.setStudent(self)
        else :
            self._registrations.append(aRegistration)
        wasAdded = True
        return wasAdded

    def removeRegistration(self, aRegistration):
        wasRemoved = False
        #Unable to remove aRegistration, as it must always have a student
        if not self == aRegistration.getStudent() :
            self._registrations.remove(aRegistration)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addRegistrationAt(self, aRegistration, index):
        wasAdded = False
        if self.addRegistration(aRegistration) :
            if index < 0 :
                index = 0
            if index > self.numberOfRegistrations() :
                index = self.numberOfRegistrations() - 1
            self._registrations.remove(aRegistration)
            self._registrations.insert(index, aRegistration)
            wasAdded = True
        return wasAdded

    def addOrMoveRegistrationAt(self, aRegistration, index):
        wasAdded = False
        if (aRegistration) in self._registrations :
            if index < 0 :
                index = 0
            if index > self.numberOfRegistrations() :
                index = self.numberOfRegistrations() - 1
            self._registrations.remove(aRegistration)
            self._registrations.insert(index, aRegistration)
            wasAdded = True
        else :
            wasAdded = self.addRegistrationAt(aRegistration, index)
        return wasAdded

    def delete(self):
        i = len(self._registrations)
        while i > 0 :
            aRegistration = self._registrations[i - 1]
            aRegistration.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "name" + ":" + str(self.getName()) + "," + "gpa" + ":" + str(self.getGpa()) + "]" + str(os.linesep) + "  " + "birthday" + "=" + (((self.getBirthday().__str__().replaceAll("  ", "    ")) if not self.getBirthday() == self else "this") if not (self.getBirthday() is None) else "null")

    def addRegistration(self, *argv):
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], (float, int)) and isinstance(argv[2], bool) and isinstance(argv[3], CourseSection) :
            return self.addRegistration1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], Registration) :
            return self.addRegistration2(argv[0])
        raise TypeError("No method matches provided parameters")