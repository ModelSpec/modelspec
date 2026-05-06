from .mock_umple_model import MockUmpleModel, MockChildUmpleModel, MockTinyUmpleModel
from .mock_ecore_model import MockEcoreModel, MockEcoreChildModel, MockTinyEcoreModel
from .mock_ecore_model import getEClassifier, eClassifiers
from .mock_ecore_model import name, nsURI, nsPrefix, eClass

__all__ = ["MockUmpleModel", "MockEcoreModel", "MockController", "MockEcoreChildModel", "MockChildUmpleModel", "MockTinyUmpleModel", "MockTinyEcoreModel"]

eSubpackages = []
eSuperPackage = None
mock_ecore_model.eSubpackages = eSubpackages
mock_ecore_model.eSuperPackage = eSuperPackage

MockEcoreModel.child.eType = MockEcoreChildModel
MockEcoreChildModel.parent.eType = MockEcoreModel
MockEcoreChildModel.tinies.eType = MockTinyEcoreModel
MockTinyEcoreModel.parent.eType = MockEcoreChildModel

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)