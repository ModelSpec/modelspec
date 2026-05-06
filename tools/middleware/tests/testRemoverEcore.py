import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockTinyEcoreModel
from ..core.shared.errors import *

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreRemoveItemFromCollection(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")
    ecore_middleware.model.tags.append("Tag3")

    # Act
    removed = ecore_middleware.removeTag("Tag2")

    # Assert
    assert "Tag2" not in ecore_middleware.model.tags
    assert len(ecore_middleware.model.tags) == 2
    assert removed == "Tag2"


def testEcoreRemoveEntityReturnsMiddlewareWrappedObject(ecore_middleware):
    tiny_mw = get_middleware_class("ecore")(MockTinyEcoreModel, name="Tiny")
    ecore_middleware.model.items.append(tiny_mw.model)

    removed = ecore_middleware.removeItem(tiny_mw)

    assert isinstance(removed, MockTinyEcoreModel)
    assert removed.model is tiny_mw.model
    assert tiny_mw.model not in ecore_middleware.model.items


def testEcoreRemoveLastItemFromCollection(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("OnlyTag")

    # Act
    ecore_middleware.removeTag("OnlyTag")

    # Assert
    assert "OnlyTag" not in ecore_middleware.model.tags
    assert len(ecore_middleware.model.tags) == 0


def testEcoreRemoveNonExistentItemFromCollectionThrowsError(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("ExistingTag")

    # Act & Assert
    with pytest.raises(ValueError) as _:
        ecore_middleware.removeTag("NonExistentTag")


def testEcoreRemoveItemFromEmptyCollectionThrowsError(ecore_middleware):
    # Act & Assert
    with pytest.raises(ValueError) as _:
        ecore_middleware.removeTag("AnyTag")

def testEcoreRemoveItemFromNonCollectionPropertyThrowsError(ecore_middleware):
    # Act & Assert
    with pytest.raises(ValueError) as _:
        ecore_middleware.removeTag("InitialName")

def testEcoreRemoveItemFromNonExistentPropertyThrowsError(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.removeNonexistent("Value")

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"
