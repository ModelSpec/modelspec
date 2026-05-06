import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockEcoreChildModel
from ..core.shared.errors import *

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreSetPropertyWithValue(ecore_middleware):
    # Act
    new_name = ecore_middleware.setName("NewName")

    # Assert
    assert ecore_middleware.model.name == "NewName"
    assert new_name == "NewName"


def testEcoreSetAssociationReturnsMiddlewareWrappedObject(ecore_middleware):
    child_mw = get_middleware_class("ecore")(MockEcoreChildModel, value="Value1")

    assigned = ecore_middleware.setChild(child_mw)

    assert ecore_middleware.model.child is child_mw.model
    assert isinstance(assigned, MockEcoreChildModel)
    assert assigned.model is child_mw.model

def testEcoreSetPropertyWithEmptyString(ecore_middleware):
    # Act
    ecore_middleware.setName("")

    # Assert
    assert ecore_middleware.model.name == ""

def testEcoreSetPropertyWithNone(ecore_middleware):
    # Act
    ecore_middleware.setName(None)

    # Assert
    assert ecore_middleware.model.name == None

def testEcoreSetAutoUniqueProperty(ecore_middleware):
    # Actually, there's no concept of autounique in Ecore, but have this test for consistency.
    # Act
    ecore_middleware.setId(123)

    # Assert
    assert ecore_middleware.model.id == 123

def testEcoreSetNonExistentProperty(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.setNonexistent("NotSet")

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"


