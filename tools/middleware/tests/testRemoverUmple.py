import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel
from ..core.shared.errors import *


@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw


def testUmpleRemoveItemFromCollection(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")
    umple_middleware.model.addTag("Tag3")

    # Act
    umple_middleware.removeTag("Tag2")

    # Assert
    assert "Tag2" not in umple_middleware.model._tags
    assert len(umple_middleware.model._tags) == 2


def testUmpleRemoveLastItemFromCollection(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("OnlyTag")

    # Act
    umple_middleware.removeTag("OnlyTag")

    # Assert
    assert "OnlyTag" not in umple_middleware.model._tags
    assert len(umple_middleware.model._tags) == 0


def testUmpleRemoveNonExistentItemFromCollectionThrowsError(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("ExistingTag")

    # Act & Assert
    with pytest.raises(ValueError) as _:
        umple_middleware.removeTag("AnyTag")

def testUmpleRemoveItemFromEmptyCollectionThrowsError(umple_middleware):

    # Act & Assert
    with pytest.raises(ValueError) as _:
        umple_middleware.removeTag("AnyTag")

def testUmpleRemoveItemFromNonExistentPropertyThrowsError(umple_middleware):
    
    #Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.removeNonexistent("Tag1")

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

