# %% NEW FILE BusinessAccount BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 20 "model.ump"
# line 92 "model.ump"
from .Account import Account
from .Facepage import Facepage
class BusinessAccount(Account):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #BusinessAccount Attributes
    #BusinessAccount Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAccountNumber, aFacepage, aUser, aCompanyName):
        self._advertisementPages = None
        self._companyName = None
        super().__init__(aAccountNumber, aFacepage, aUser)
        self._companyName = aCompanyName
        self._advertisementPages = []

    #------------------------
    # INTERFACE
    #------------------------
    def setCompanyName(self, aCompanyName):
        wasSet = False
        self._companyName = aCompanyName
        wasSet = True
        return wasSet

    def getCompanyName(self):
        return self._companyName

    # Code from template association_GetMany 
    def getAdvertisementPage(self, index):
        aAdvertisementPage = self._advertisementPages[index]
        return aAdvertisementPage

    def getAdvertisementPages(self):
        newAdvertisementPages = tuple(self._advertisementPages)
        return newAdvertisementPages

    def numberOfAdvertisementPages(self):
        number = len(self._advertisementPages)
        return number

    def hasAdvertisementPages(self):
        has = len(self._advertisementPages) > 0
        return has

    def indexOfAdvertisementPage(self, aAdvertisementPage):
        index = (-1 if not aAdvertisementPage in self._advertisementPages else self._advertisementPages.index(aAdvertisementPage))
        return index

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfAdvertisementPages():
        return 0

    # Code from template association_AddManyToOne 
    def addAdvertisementPage1(self, aPageName, aVisits, aFacepage, aBounceRate, aClickThroughRate, aConversionRate):
        from .AdvertisementPage import AdvertisementPage
        return AdvertisementPage(aPageName, aVisits, aFacepage, aBounceRate, aClickThroughRate, aConversionRate, self)

    def addAdvertisementPage2(self, aAdvertisementPage):
        wasAdded = False
        if (aAdvertisementPage) in self._advertisementPages :
            return False
        existingBusinessAccount = aAdvertisementPage.getBusinessAccount()
        isNewBusinessAccount = not (existingBusinessAccount is None) and not self == existingBusinessAccount
        if isNewBusinessAccount :
            aAdvertisementPage.setBusinessAccount(self)
        else :
            self._advertisementPages.append(aAdvertisementPage)
        wasAdded = True
        return wasAdded

    def removeAdvertisementPage(self, aAdvertisementPage):
        wasRemoved = False
        #Unable to remove aAdvertisementPage, as it must always have a businessAccount
        if not self == aAdvertisementPage.getBusinessAccount() :
            self._advertisementPages.remove(aAdvertisementPage)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addAdvertisementPageAt(self, aAdvertisementPage, index):
        wasAdded = False
        if self.addAdvertisementPage(aAdvertisementPage) :
            if index < 0 :
                index = 0
            if index > self.numberOfAdvertisementPages() :
                index = self.numberOfAdvertisementPages() - 1
            self._advertisementPages.remove(aAdvertisementPage)
            self._advertisementPages.insert(index, aAdvertisementPage)
            wasAdded = True
        return wasAdded

    def addOrMoveAdvertisementPageAt(self, aAdvertisementPage, index):
        wasAdded = False
        if (aAdvertisementPage) in self._advertisementPages :
            if index < 0 :
                index = 0
            if index > self.numberOfAdvertisementPages() :
                index = self.numberOfAdvertisementPages() - 1
            self._advertisementPages.remove(aAdvertisementPage)
            self._advertisementPages.insert(index, aAdvertisementPage)
            wasAdded = True
        else :
            wasAdded = self.addAdvertisementPageAt(aAdvertisementPage, index)
        return wasAdded

    def delete(self):
        i = len(self._advertisementPages)
        while i > 0 :
            aAdvertisementPage = self._advertisementPages[i - 1]
            aAdvertisementPage.delete()
            i -= 1

        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "companyName" + ":" + str(self.getCompanyName()) + "]"

    def addAdvertisementPage(self, *argv):
        from .AdvertisementPage import AdvertisementPage
        if len(argv) == 6 and isinstance(argv[0], str) and isinstance(argv[1], int) and isinstance(argv[2], Facepage) and isinstance(argv[3], (float, int)) and isinstance(argv[4], (float, int)) and isinstance(argv[5], (float, int)) :
            return self.addAdvertisementPage1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5])
        if len(argv) == 1 and isinstance(argv[0], AdvertisementPage) :
            return self.addAdvertisementPage2(argv[0])
        raise TypeError("No method matches provided parameters")
