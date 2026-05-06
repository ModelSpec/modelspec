import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel
from ..core.shared.errors import *

@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw

def testUmpleSetPropertyWithValue(umple_middleware):
    # Act
    umple_middleware.setName("NewName")

    # Assert
    assert umple_middleware.model._name == "NewName"

def testUmpleSetPropertyWithEmptyString(umple_middleware):
    # Act
    umple_middleware.setName("")

    # Assert
    assert umple_middleware.model._name == ""

def testUmpleSetPropertyWithNone(umple_middleware):
    # Act
    umple_middleware.setName(None)

    # Assert
    assert umple_middleware.model._name == None

def testUmpleSetAutoUniqueProperty(umple_middleware):
    # Id is auto-unique, meaning setId actually doesn't exist.
    # Act
    umple_middleware.setId(123)

    # Assert
    assert umple_middleware.model._id == 123

def testUmpleSetNonExistentProperty(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.setNonexistent("NotSet")

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"
