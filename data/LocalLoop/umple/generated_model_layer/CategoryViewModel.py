# %% NEW FILE CategoryViewModel BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 97 "model.ump"
# line 232 "model.ump"

class CategoryViewModel():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #CategoryViewModel Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aManageCategoriesActivity, aManageEventActivity):
        self._manageEventActivity = None
        self._manageCategoriesActivity = None
        self._categories = None
        self._categories = []
        didAddManageCategoriesActivity = self.setManageCategoriesActivity(aManageCategoriesActivity)
        if not didAddManageCategoriesActivity :
            raise RuntimeError ("Unable to create categoryViewModel due to manageCategoriesActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddManageEventActivity = self.setManageEventActivity(aManageEventActivity)
        if not didAddManageEventActivity :
            raise RuntimeError ("Unable to create categoryViewModel due to manageEventActivity. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getCategory(self, index):
        aCategory = self._categories[index]
        return aCategory

    def getCategories(self):
        newCategories = tuple(self._categories)
        return newCategories

    def numberOfCategories(self):
        number = len(self._categories)
        return number

    def hasCategories(self):
        has = len(self._categories) > 0
        return has

    def indexOfCategory(self, aCategory):
        index = (-1 if not aCategory in self._categories else self._categories.index(aCategory))
        return index

    # Code from template association_GetOne 
    def getManageCategoriesActivity(self):
        return self._manageCategoriesActivity

    # Code from template association_GetOne 
    def getManageEventActivity(self):
        return self._manageEventActivity

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfCategories():
        return 0

    # Code from template association_AddManyToOne 
    def addCategory1(self, aCategoryId, aName, aDescription):
        from .Category import Category
        return Category(aCategoryId, aName, aDescription, self)

    def addCategory2(self, aCategory):
        wasAdded = False
        if (aCategory) in self._categories :
            return False
        existingCategoryViewModel = aCategory.getCategoryViewModel()
        isNewCategoryViewModel = not (existingCategoryViewModel is None) and not self == existingCategoryViewModel
        if isNewCategoryViewModel :
            aCategory.setCategoryViewModel(self)
        else :
            self._categories.append(aCategory)
        wasAdded = True
        return wasAdded

    def removeCategory(self, aCategory):
        wasRemoved = False
        #Unable to remove aCategory, as it must always have a categoryViewModel
        if not self == aCategory.getCategoryViewModel() :
            self._categories.remove(aCategory)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addCategoryAt(self, aCategory, index):
        wasAdded = False
        if self.addCategory(aCategory) :
            if index < 0 :
                index = 0
            if index > self.numberOfCategories() :
                index = self.numberOfCategories() - 1
            self._categories.remove(aCategory)
            self._categories.insert(index, aCategory)
            wasAdded = True
        return wasAdded

    def addOrMoveCategoryAt(self, aCategory, index):
        wasAdded = False
        if (aCategory) in self._categories :
            if index < 0 :
                index = 0
            if index > self.numberOfCategories() :
                index = self.numberOfCategories() - 1
            self._categories.remove(aCategory)
            self._categories.insert(index, aCategory)
            wasAdded = True
        else :
            wasAdded = self.addCategoryAt(aCategory, index)
        return wasAdded

    # Code from template association_SetOneToOptionalOne 
    def setManageCategoriesActivity(self, aNewManageCategoriesActivity):
        wasSet = False
        if aNewManageCategoriesActivity is None :
            #Unable to setManageCategoriesActivity to null, as categoryViewModel must always be associated to a manageCategoriesActivity
            return wasSet
        existingCategoryViewModel = aNewManageCategoriesActivity.getCategoryViewModel()
        if not (existingCategoryViewModel is None) and not self == existingCategoryViewModel :
            #Unable to setManageCategoriesActivity, the current manageCategoriesActivity already has a categoryViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldManageCategoriesActivity = self._manageCategoriesActivity
        self._manageCategoriesActivity = aNewManageCategoriesActivity
        self._manageCategoriesActivity.setCategoryViewModel(self)
        if not (anOldManageCategoriesActivity is None) :
            anOldManageCategoriesActivity.setCategoryViewModel(None)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToOptionalOne 
    def setManageEventActivity(self, aNewManageEventActivity):
        wasSet = False
        if aNewManageEventActivity is None :
            #Unable to setManageEventActivity to null, as categoryViewModel must always be associated to a manageEventActivity
            return wasSet
        existingCategoryViewModel = aNewManageEventActivity.getCategoryViewModel()
        if not (existingCategoryViewModel is None) and not self == existingCategoryViewModel :
            #Unable to setManageEventActivity, the current manageEventActivity already has a categoryViewModel, which would be orphaned if it were re-assigned
            return wasSet
        anOldManageEventActivity = self._manageEventActivity
        self._manageEventActivity = aNewManageEventActivity
        self._manageEventActivity.setCategoryViewModel(self)
        if not (anOldManageEventActivity is None) :
            anOldManageEventActivity.setCategoryViewModel(None)
        wasSet = True
        return wasSet

    def delete(self):
        i = len(self._categories)
        while i > 0 :
            aCategory = self._categories[i - 1]
            aCategory.delete()
            i -= 1

        existingManageCategoriesActivity = self._manageCategoriesActivity
        self._manageCategoriesActivity = None
        if not (existingManageCategoriesActivity is None) :
            existingManageCategoriesActivity.setCategoryViewModel(None)
        existingManageEventActivity = self._manageEventActivity
        self._manageEventActivity = None
        if not (existingManageEventActivity is None) :
            existingManageEventActivity.setCategoryViewModel(None)

    def addCategory(self, *argv):
        from .Category import Category
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) :
            return self.addCategory1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], Category) :
            return self.addCategory2(argv[0])
        raise TypeError("No method matches provided parameters")
