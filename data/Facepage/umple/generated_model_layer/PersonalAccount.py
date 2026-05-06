# %% NEW FILE PersonalAccount BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 25 "model.ump"
# line 97 "model.ump"
from .Account import Account
from .Facepage import Facepage
class PersonalAccount(Account):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #PersonalAccount Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAccountNumber, aFacepage, aUser):
        self._receiverOf = None
        self._senderOf = None
        self._administrator = None
        self._privileges = None
        super().__init__(aAccountNumber, aFacepage, aUser)
        self._privileges = []
        self._administrator = []
        self._senderOf = []
        self._receiverOf = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getPrivilege(self, index):
        aPrivilege = self._privileges[index]
        return aPrivilege

    def getPrivileges(self):
        newPrivileges = tuple(self._privileges)
        return newPrivileges

    def numberOfPrivileges(self):
        number = len(self._privileges)
        return number

    def hasPrivileges(self):
        has = len(self._privileges) > 0
        return has

    def indexOfPrivilege(self, aPrivilege):
        index = (-1 if not aPrivilege in self._privileges else self._privileges.index(aPrivilege))
        return index

    # Code from template association_GetMany 
    def getAdministrator1(self, index):
        aAdministrator = self._administrator[index]
        return aAdministrator

    def getAdministrator2(self):
        newAdministrator = tuple(self._administrator)
        return newAdministrator

    def numberOfAdministrator(self):
        number = len(self._administrator)
        return number

    def hasAdministrator(self):
        has = len(self._administrator) > 0
        return has

    def indexOfAdministrator(self, aAdministrator):
        index = (-1 if not aAdministrator in self._administrator else self._administrator.index(aAdministrator))
        return index

    # Code from template association_GetMany 
    def getSenderOf1(self, index):
        aSenderOf = self._senderOf[index]
        return aSenderOf

    def getSenderOf2(self):
        newSenderOf = tuple(self._senderOf)
        return newSenderOf

    def numberOfSenderOf(self):
        number = len(self._senderOf)
        return number

    def hasSenderOf(self):
        has = len(self._senderOf) > 0
        return has

    def indexOfSenderOf(self, aSenderOf):
        index = (-1 if not aSenderOf in self._senderOf else self._senderOf.index(aSenderOf))
        return index

    # Code from template association_GetMany 
    def getReceiverOf1(self, index):
        aReceiverOf = self._receiverOf[index]
        return aReceiverOf

    def getReceiverOf2(self):
        newReceiverOf = tuple(self._receiverOf)
        return newReceiverOf

    def numberOfReceiverOf(self):
        number = len(self._receiverOf)
        return number

    def hasReceiverOf(self):
        has = len(self._receiverOf) > 0
        return has

    def indexOfReceiverOf(self, aReceiverOf):
        index = (-1 if not aReceiverOf in self._receiverOf else self._receiverOf.index(aReceiverOf))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfPrivileges():
        return 0

    # Code from template association_AddManyToOne 
    def addPrivilege1(self, aTypeOfPrivilege, aPersonalPage):
        from .Privilege import Privilege
        return Privilege(aTypeOfPrivilege, self, aPersonalPage)

    def addPrivilege2(self, aPrivilege):
        wasAdded = False
        if (aPrivilege) in self._privileges :
            return False
        existingPersonalAccount = aPrivilege.getPersonalAccount()
        isNewPersonalAccount = not (existingPersonalAccount is None) and not self == existingPersonalAccount
        if isNewPersonalAccount :
            aPrivilege.setPersonalAccount(self)
        else :
            self._privileges.append(aPrivilege)
        wasAdded = True
        return wasAdded

    def removePrivilege(self, aPrivilege):
        wasRemoved = False
        #Unable to remove aPrivilege, as it must always have a personalAccount
        if not self == aPrivilege.getPersonalAccount() :
            self._privileges.remove(aPrivilege)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addPrivilegeAt(self, aPrivilege, index):
        wasAdded = False
        if self.addPrivilege(aPrivilege) :
            if index < 0 :
                index = 0
            if index > self.numberOfPrivileges() :
                index = self.numberOfPrivileges() - 1
            self._privileges.remove(aPrivilege)
            self._privileges.insert(index, aPrivilege)
            wasAdded = True
        return wasAdded

    def addOrMovePrivilegeAt(self, aPrivilege, index):
        wasAdded = False
        if (aPrivilege) in self._privileges :
            if index < 0 :
                index = 0
            if index > self.numberOfPrivileges() :
                index = self.numberOfPrivileges() - 1
            self._privileges.remove(aPrivilege)
            self._privileges.insert(index, aPrivilege)
            wasAdded = True
        else :
            wasAdded = self.addPrivilegeAt(aPrivilege, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfAdministrator():
        return 0

    # Code from template association_AddManyToOne 
    def addAdministrator1(self, aPageName, aVisits, aFacepage):
        from .PersonalPage import PersonalPage
        return PersonalPage(aPageName, aVisits, aFacepage, self)

    def addAdministrator2(self, aAdministrator):
        wasAdded = False
        if (aAdministrator) in self._administrator :
            return False
        existingPersonalAccount = aAdministrator.getPersonalAccount()
        isNewPersonalAccount = not (existingPersonalAccount is None) and not self == existingPersonalAccount
        if isNewPersonalAccount :
            aAdministrator.setPersonalAccount(self)
        else :
            self._administrator.append(aAdministrator)
        wasAdded = True
        return wasAdded

    def removeAdministrator(self, aAdministrator):
        wasRemoved = False
        #Unable to remove aAdministrator, as it must always have a personalAccount
        if not self == aAdministrator.getPersonalAccount() :
            self._administrator.remove(aAdministrator)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addAdministratorAt(self, aAdministrator, index):
        wasAdded = False
        if self.addAdministrator(aAdministrator) :
            if index < 0 :
                index = 0
            if index > self.numberOfAdministrator() :
                index = self.numberOfAdministrator() - 1
            self._administrator.remove(aAdministrator)
            self._administrator.insert(index, aAdministrator)
            wasAdded = True
        return wasAdded

    def addOrMoveAdministratorAt(self, aAdministrator, index):
        wasAdded = False
        if (aAdministrator) in self._administrator :
            if index < 0 :
                index = 0
            if index > self.numberOfAdministrator() :
                index = self.numberOfAdministrator() - 1
            self._administrator.remove(aAdministrator)
            self._administrator.insert(index, aAdministrator)
            wasAdded = True
        else :
            wasAdded = self.addAdministratorAt(aAdministrator, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfSenderOf():
        return 0

    # Code from template association_AddManyToOne 
    def addSenderOf1(self, aReceiver):
        from .FriendRequest import FriendRequest
        return FriendRequest(self, aReceiver)

    def addSenderOf2(self, aSenderOf):
        wasAdded = False
        if (aSenderOf) in self._senderOf :
            return False
        existingSender = aSenderOf.getSender()
        isNewSender = not (existingSender is None) and not self == existingSender
        if isNewSender :
            aSenderOf.setSender(self)
        else :
            self._senderOf.append(aSenderOf)
        wasAdded = True
        return wasAdded

    def removeSenderOf(self, aSenderOf):
        wasRemoved = False
        #Unable to remove aSenderOf, as it must always have a sender
        if not self == aSenderOf.getSender() :
            self._senderOf.remove(aSenderOf)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addSenderOfAt(self, aSenderOf, index):
        wasAdded = False
        if self.addSenderOf(aSenderOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfSenderOf() :
                index = self.numberOfSenderOf() - 1
            self._senderOf.remove(aSenderOf)
            self._senderOf.insert(index, aSenderOf)
            wasAdded = True
        return wasAdded

    def addOrMoveSenderOfAt(self, aSenderOf, index):
        wasAdded = False
        if (aSenderOf) in self._senderOf :
            if index < 0 :
                index = 0
            if index > self.numberOfSenderOf() :
                index = self.numberOfSenderOf() - 1
            self._senderOf.remove(aSenderOf)
            self._senderOf.insert(index, aSenderOf)
            wasAdded = True
        else :
            wasAdded = self.addSenderOfAt(aSenderOf, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfReceiverOf():
        return 0

    # Code from template association_AddManyToOne 
    def addReceiverOf1(self, aSender):
        from .FriendRequest import FriendRequest
        return FriendRequest(aSender, self)

    def addReceiverOf2(self, aReceiverOf):
        wasAdded = False
        if (aReceiverOf) in self._receiverOf :
            return False
        existingReceiver = aReceiverOf.getReceiver()
        isNewReceiver = not (existingReceiver is None) and not self == existingReceiver
        if isNewReceiver :
            aReceiverOf.setReceiver(self)
        else :
            self._receiverOf.append(aReceiverOf)
        wasAdded = True
        return wasAdded

    def removeReceiverOf(self, aReceiverOf):
        wasRemoved = False
        #Unable to remove aReceiverOf, as it must always have a receiver
        if not self == aReceiverOf.getReceiver() :
            self._receiverOf.remove(aReceiverOf)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addReceiverOfAt(self, aReceiverOf, index):
        wasAdded = False
        if self.addReceiverOf(aReceiverOf) :
            if index < 0 :
                index = 0
            if index > self.numberOfReceiverOf() :
                index = self.numberOfReceiverOf() - 1
            self._receiverOf.remove(aReceiverOf)
            self._receiverOf.insert(index, aReceiverOf)
            wasAdded = True
        return wasAdded

    def addOrMoveReceiverOfAt(self, aReceiverOf, index):
        wasAdded = False
        if (aReceiverOf) in self._receiverOf :
            if index < 0 :
                index = 0
            if index > self.numberOfReceiverOf() :
                index = self.numberOfReceiverOf() - 1
            self._receiverOf.remove(aReceiverOf)
            self._receiverOf.insert(index, aReceiverOf)
            wasAdded = True
        else :
            wasAdded = self.addReceiverOfAt(aReceiverOf, index)
        return wasAdded

    def delete(self):
        i = len(self._privileges)
        while i > 0 :
            aPrivilege = self._privileges[i - 1]
            aPrivilege.delete()
            i -= 1

        i = len(self._administrator)
        while i > 0 :
            aAdministrator = self._administrator[i - 1]
            aAdministrator.delete()
            i -= 1

        i = len(self._senderOf)
        while i > 0 :
            aSenderOf = self._senderOf[i - 1]
            aSenderOf.delete()
            i -= 1

        i = len(self._receiverOf)
        while i > 0 :
            aReceiverOf = self._receiverOf[i - 1]
            aReceiverOf.delete()
            i -= 1

        super().delete()

    def getAdministrator(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getAdministrator1(argv[0])
        if len(argv) == 0 :
            return self.getAdministrator2()
        raise TypeError("No method matches provided parameters")

    def getSenderOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getSenderOf1(argv[0])
        if len(argv) == 0 :
            return self.getSenderOf2()
        raise TypeError("No method matches provided parameters")

    def getReceiverOf(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getReceiverOf1(argv[0])
        if len(argv) == 0 :
            return self.getReceiverOf2()
        raise TypeError("No method matches provided parameters")

    def addPrivilege(self, *argv):
        from .PersonalPage import PersonalPage
        from .Privilege import Privilege
        if len(argv) == 2 and isinstance(argv[0], str) and isinstance(argv[1], PersonalPage) :
            return self.addPrivilege1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], Privilege) :
            return self.addPrivilege2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addAdministrator(self, *argv):
        from .PersonalPage import PersonalPage
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], int) and isinstance(argv[2], Facepage) :
            return self.addAdministrator1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], PersonalPage) :
            return self.addAdministrator2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addSenderOf(self, *argv):
        from .FriendRequest import FriendRequest
        if len(argv) == 1 and isinstance(argv[0], PersonalAccount) :
            return self.addSenderOf1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], FriendRequest) :
            return self.addSenderOf2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addReceiverOf(self, *argv):
        from .FriendRequest import FriendRequest
        if len(argv) == 1 and isinstance(argv[0], PersonalAccount) :
            return self.addReceiverOf1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], FriendRequest) :
            return self.addReceiverOf2(argv[0])
        raise TypeError("No method matches provided parameters")
