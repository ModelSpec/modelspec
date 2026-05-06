# %% NEW FILE UserAccess BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
# line 245 "model.ump"

class UserAccess():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #UserAccess Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._userRegistrations = None
        self._users = None
        self._users = []
        self._userRegistrations = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getUser(self, index):
        aUser = self._users[index]
        return aUser

    def getUsers(self):
        newUsers = tuple(self._users)
        return newUsers

    def numberOfUsers(self):
        number = len(self._users)
        return number

    def hasUsers(self):
        has = len(self._users) > 0
        return has

    def indexOfUser(self, aUser):
        index = (-1 if not aUser in self._users else self._users.index(aUser))
        return index

    # Code from template association_GetMany
    def getUserRegistration(self, index):
        aUserRegistration = self._userRegistrations[index]
        return aUserRegistration

    def getUserRegistrations(self):
        newUserRegistrations = tuple(self._userRegistrations)
        return newUserRegistrations

    def numberOfUserRegistrations(self):
        number = len(self._userRegistrations)
        return number

    def hasUserRegistrations(self):
        has = len(self._userRegistrations) > 0
        return has

    def indexOfUserRegistration(self, aUserRegistration):
        index = (-1 if not aUserRegistration in self._userRegistrations else self._userRegistrations.index(aUserRegistration))
        return index

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfUsers():
        return 0

    # Code from template association_AddManyToOne
    def addUser1(self, aId, aLogin, aEmail, aFirstName, aLastName, aName):
        from .User import User
        return User(aId, aLogin, aEmail, aFirstName, aLastName, aName, self)

    def addUser2(self, aUser):
        wasAdded = False
        if (aUser) in self._users :
            return False
        existingUserAccess = aUser.getUserAccess()
        isNewUserAccess = not (existingUserAccess is None) and not self == existingUserAccess
        if isNewUserAccess :
            aUser.setUserAccess(self)
        else :
            self._users.append(aUser)
        wasAdded = True
        return wasAdded

    def removeUser(self, aUser):
        wasRemoved = False
        #Unable to remove aUser, as it must always have a userAccess
        if not self == aUser.getUserAccess() :
            self._users.remove(aUser)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addUserAt(self, aUser, index):
        wasAdded = False
        if self.addUser(aUser) :
            if index < 0 :
                index = 0
            if index > self.numberOfUsers() :
                index = self.numberOfUsers() - 1
            self._users.remove(aUser)
            self._users.insert(index, aUser)
            wasAdded = True
        return wasAdded

    def addOrMoveUserAt(self, aUser, index):
        wasAdded = False
        if (aUser) in self._users :
            if index < 0 :
                index = 0
            if index > self.numberOfUsers() :
                index = self.numberOfUsers() - 1
            self._users.remove(aUser)
            self._users.insert(index, aUser)
            wasAdded = True
        else :
            wasAdded = self.addUserAt(aUser, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfUserRegistrations():
        return 0

    # Code from template association_AddManyToOne
    def addUserRegistration1(self, aLogin, aEmail, aFirstName, aLastName):
        from .UserRegistration import UserRegistration
        return UserRegistration(aLogin, aEmail, aFirstName, aLastName, self)

    def addUserRegistration2(self, aUserRegistration):
        wasAdded = False
        if (aUserRegistration) in self._userRegistrations :
            return False
        existingUserAccess = aUserRegistration.getUserAccess()
        isNewUserAccess = not (existingUserAccess is None) and not self == existingUserAccess
        if isNewUserAccess :
            aUserRegistration.setUserAccess(self)
        else :
            self._userRegistrations.append(aUserRegistration)
        wasAdded = True
        return wasAdded

    def removeUserRegistration(self, aUserRegistration):
        wasRemoved = False
        #Unable to remove aUserRegistration, as it must always have a userAccess
        if not self == aUserRegistration.getUserAccess() :
            self._userRegistrations.remove(aUserRegistration)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addUserRegistrationAt(self, aUserRegistration, index):
        wasAdded = False
        if self.addUserRegistration(aUserRegistration) :
            if index < 0 :
                index = 0
            if index > self.numberOfUserRegistrations() :
                index = self.numberOfUserRegistrations() - 1
            self._userRegistrations.remove(aUserRegistration)
            self._userRegistrations.insert(index, aUserRegistration)
            wasAdded = True
        return wasAdded

    def addOrMoveUserRegistrationAt(self, aUserRegistration, index):
        wasAdded = False
        if (aUserRegistration) in self._userRegistrations :
            if index < 0 :
                index = 0
            if index > self.numberOfUserRegistrations() :
                index = self.numberOfUserRegistrations() - 1
            self._userRegistrations.remove(aUserRegistration)
            self._userRegistrations.insert(index, aUserRegistration)
            wasAdded = True
        else :
            wasAdded = self.addUserRegistrationAt(aUserRegistration, index)
        return wasAdded

    def delete(self):

        while len(self._users) > 0 :
            aUser = self._users[len(self._users) - 1]
            aUser.delete()
            self._users.remove(aUser)

        while len(self._userRegistrations) > 0 :
            aUserRegistration = self._userRegistrations[len(self._userRegistrations) - 1]
            aUserRegistration.delete()
            self._userRegistrations.remove(aUserRegistration)

    def addUser(self, *argv):
        from .User import User
        if len(argv) == 6 and isinstance(argv[0], int) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], str) :
            return self.addUser1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5])
        if len(argv) == 1 and isinstance(argv[0], User) :
            return self.addUser2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addUserRegistration(self, *argv):
        from .UserRegistration import UserRegistration
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) :
            return self.addUserRegistration1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], UserRegistration) :
            return self.addUserRegistration2(argv[0])
        raise TypeError("No method matches provided parameters")
