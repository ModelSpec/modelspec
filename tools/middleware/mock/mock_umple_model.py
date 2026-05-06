class MockUmpleModel:
    mockUmpleModelsById = dict()
    def __init__(self, aId, aName):
        self._id = aId
        self._name = None
        self._name = aName
        MockUmpleModel.mockUmpleModelsById[aId] = self
        self._tags = []
        self._child = None
        self._isActive = False
        self._ongoing = False

    def getId(self):
        return self._id

    @staticmethod
    def getWithId(aId):
        return MockUmpleModel.mockUmpleModelsById.get(aId)

    def setName(self, aName):
        self._name = aName
        return True

    def getName(self):
        return self._name
    
    def addTag(self, t):
        self._tags.append(t)

    def addTagAt(self, t, index):
        self._tags.insert(index, t)

    def removeTag(self, t):
        self._tags.remove(t)

    def setIsActive(self, isActive):
        self._isActive = isActive

    def isIsActive(self):
        return self._isActive

    def setOngoing(self, ongoing):
        self._ongoing = ongoing

    def isOngoing(self):
        return self._ongoing
    
    def numberOfTags(self):
        return len(self._tags)

    def indexOfTag(self, t):
        try:
            return self._tags.index(t)
        except ValueError:
            return -1

    def hasTags(self):
        return len(self._tags) > 0

    def hasTag(self, t):
        return t in self._tags
    
    def getTags(self):
        return self._tags
    
    def getTag(self, index):
        return self._tags[index]
    
    def getChild(self):
        return self._child
    
    def setChild(self, child):
        self._child = child
        child.setParent(self)

    def hasChild(self):
        return not (self._child is None)
    
    def removeChild(self):
        self._child = None

    def delete(self):
        # When the root model is deleted, the id dictionary should no longer
        # contain any live instances. For the purposes of the middleware tests,
        # we clear the entire registry rather than just this instance.
        MockUmpleModel.mockUmpleModelsById.clear()
        placeholderChild = self._child
        self._child = None
        if placeholderChild is not None:
            placeholderChild.delete()


class MockChildUmpleModel:
    def __init__(self, value, pids = []):
        self._value = value
        self._pids = pids
        self._tinies = []
        self._parent = None

    def setParent(self, parent):
        self._parent = parent

    def getParent(self):
        return self._parent

    def getValue(self):
        return self._value
    
    def setValue(self, value):
        self._value = value
        return True
    
    def addPid(self, pid):
        self._pids.append(pid)

    def getPids(self):
        return self._pids
    
    def addTiny(self, name):
        tiny = MockTinyUmpleModel(name, self)
        tiny.setParent(self)
        self._tinies.append(tiny)
        return True
    
    def addTiny1(self, tiny):
        self._tinies.append(tiny)
    
    def getTinies(self):
        return self._tinies
    
    def delete(self):
        placeholderParent = self._parent
        self._parent = None
        placeholderParent.removeChild()
        i = len(self._tinies)
        while i > 0:
            aTiny = self._tinies[i - 1]
            aTiny.delete()
            self._tinies.remove(aTiny)
            i -= 1

    
class MockTinyUmpleModel:
    def __init__(self, name):
        self._name = name
        self._parent = None

    def setParent(self, parent):
        self._parent = parent
        self._parent.addTiny1(self)

    def getParent(self):
        return self._parent
    
    def delete(self):
        self._parent = None