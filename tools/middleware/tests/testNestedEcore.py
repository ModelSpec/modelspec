import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockEcoreChildModel
from ..core.shared.errors import *

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreNestedGetPropertyWithValue(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel("Value")

    # Act
    child = ecore_middleware.getChild()
    # Directly read the nested child's value via __getattr__ fallback
    value = child.value

    # Assert
    assert value == "Value"
    assert value == ecore_middleware.model.child.value

def testEcoreNestedSetNestedPropertyWithValue(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel("Value")

    # Act — use the middleware setter so the underlying model is updated
    child = ecore_middleware.getChild()
    child.setValue("NEW")
    value = child.getValue()

    # Assert
    assert value == "NEW"
    assert "NEW" == ecore_middleware.model.child.value

def testEcoreNestedGetOnCollectionProperty(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel("Value")
    ecore_middleware.model.child.pids.append(1)
    ecore_middleware.model.child.pids.append(3)
    ecore_middleware.model.child.pids.append(2)

    # Act
    child = ecore_middleware.getChild()
    value = child.pids

    # Assert
    assert len(value) == 3
    assert sorted(value) == [1, 2, 3]
    assert ecore_middleware.model.child.pids

def testEcoreNestedAssociationIsNoneReturnNoneException(ecore_middleware):
    # When association is None, getChild should return None without raising.
    child = ecore_middleware.getChild()
    assert child is None

def testEcoreNestedAssociationIsNoneExistentThrowsAttributeMissing(ecore_middleware):
    # Arrange
    with pytest.raises(MWAttributeMissing) as errorInfo:
        nonexistent = ecore_middleware.getNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testEcoreNestedGetChildReturnsMiddlewareWrappedEntity(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel("Value")

    # Act
    child = ecore_middleware.getChild()

    # Assert — child should be a middleware wrapper around MockEcoreChildModel
    assert isinstance(child, MockEcoreChildModel)
    assert child.model is ecore_middleware.model.child

def testEcoreNestedChainingGetChildThenGetValue(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel("ChainValue")

    # Act — chain middleware calls
    value = ecore_middleware.getChild().getValue()

    # Assert
    assert value == "ChainValue"
