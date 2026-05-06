import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel, MockChildUmpleModel
from ..core.shared.errors import *

@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw

def testUmpleNestedGetPropertyWithValue(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel("Value"))

    # Act
    child = umple_middleware.getChild()
    value = child.getValue()

    # Assert
    assert value == "Value"
    assert value == umple_middleware.model.getChild().getValue()

def testUmpleNestedSetNestedPropertyWithValue(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel("Value"))

    # Act
    child = umple_middleware.getChild()
    value = child.setValue("NEW")

    # Assert
    assert value
    assert "NEW" == umple_middleware.model.getChild().getValue()

def testUmpleNestedGetOnCollectionProperty(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel("Value"))
    umple_middleware.model.getChild().addPid(1)
    umple_middleware.model.getChild().addPid(2)
    umple_middleware.model.getChild().addPid(3)

    # Act — child is already middleware-wrapped; no manual wrapping needed
    child = umple_middleware.getChild()
    value = child.getPids()

    # Assert
    assert len(value) == 3
    assert value == [1, 2, 3]
    assert umple_middleware.getChild().getPids()

def testUmpleNestedAssociationIsNoneReturnNoneException(umple_middleware):
    # When association is None, getChild should return None without raising.
    child = umple_middleware.getChild()
    assert child is None


def testUmpleNestedAssociationIsNoneExistentThrowsAttributeMissing(umple_middleware):
    # Arrange
    with pytest.raises(MWAttributeMissing) as errorInfo:
        nonexistent = umple_middleware.getNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testUmpleNestedGetChildReturnsMiddlewareWrappedEntity(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel("Value"))

    # Act
    child = umple_middleware.getChild()

    # Assert — child should be a middleware wrapper around MockChildUmpleModel
    assert isinstance(child, MockChildUmpleModel)
    assert child.model is umple_middleware.model.getChild()

def testUmpleNestedChainingGetChildThenGetValue(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel("ChainValue"))

    # Act — chain middleware calls
    value = umple_middleware.getChild().getValue()

    # Assert
    assert value == "ChainValue"
