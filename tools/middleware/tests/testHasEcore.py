import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockEcoreChildModel
from ..core.shared.errors import *

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreHasOnNonEmptyCollectionReturnsTrue(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    value = ecore_middleware.hasTags()

    # Assert
    assert value

def testEcoreHasOnEmptyCollectionReturnsFalse(ecore_middleware):
    # Act
    value = ecore_middleware.hasTags()

    # Assert
    assert not value

def testEcoreHasOnNonNoneAssociationReturnsTrue(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel(1)

    # Act
    value = ecore_middleware.hasChild()

    # Assert
    assert value

def testEcoreHasOnNoneAssociationReturnsFalse(ecore_middleware):
    # Act
    value = ecore_middleware.hasChild()

    # Assert
    assert not value

def testEcoreOnNonExistentAssociationThrowsError(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.hasNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"