"""Definition of meta model 'mock'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'mock'
nsURI = 'mock'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)

class MockEcoreModel(EObject, metaclass=MetaEClass):
    # Ecore-style: direct attribute
    child = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, name=None):
        self.id = id
        self.tags = []
        self.items = []
        self.isActive = False
        self.ongoing = False
        self.child = None
        if name is not None:
            self.name = name

class MockEcoreChildModel(EObject, metaclass=MetaEClass):
    tinies = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    parent = EReference(ordered=True, unique=True, containment=False, derived=False)
    
    def __init__(self, value=None, pids = []):
        self.parent = None
        self.value = value
        self.pids = pids
        self.tinies = []

class MockTinyEcoreModel(EObject, metaclass=MetaEClass):
    parent = EReference(ordered=True, unique=True, containment=False, derived=False)
    
    def __init__(self, name):
        self.name = name
        self.parent = None