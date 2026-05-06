import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel, MockChildUmpleModel
from ..core.shared.errors import *

@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw

def testUmpleHasOnNonEmptyCollectionReturnsTrue(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    value = umple_middleware.hasTags()

    # Assert
    assert value

def testUmpleHasOnEmptyCollectionReturnsFalse(umple_middleware):
    # Act
    value = umple_middleware.hasTags()

    # Assert
    assert not value

def testUmpleHasOnNonNoneAssociationReturnsTrue(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel(1))

    # Act
    value = umple_middleware.hasChild()

    # Assert
    assert value

def testUmpleHasOnNoneAssociationReturnsFalse(umple_middleware):
    # Act
    value = umple_middleware.hasChild()

    # Assert
    assert not value

def testUmpleOnNonExistentAssociationThrowsError(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.hasNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"