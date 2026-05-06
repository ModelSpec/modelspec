import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockTinyEcoreModel
from ..core.shared.errors import *


@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw


def testEcoreAddItemToEmptyCollection(ecore_middleware):
    # Act
    ecore_middleware.addTag("Tag1")

    # Assert
    assert len(ecore_middleware.model.tags) == 1
    assert ecore_middleware.model.tags[0] == "Tag1"


def testEcoreAddItemToNonEmptyCollection(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")

    # Act
    ecore_middleware.addTag("Tag2")

    # Assert
    assert len(ecore_middleware.model.tags) == 2
    assert ecore_middleware.model.tags[0] == "Tag1"
    assert ecore_middleware.model.tags[1] == "Tag2"


def testEcoreAddDuplicateItem(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")

    # Act
    ecore_middleware.addTag("Tag1")

    # Assert
    assert len(ecore_middleware.model.tags) == 2
    assert ecore_middleware.model.tags[0] == "Tag1"
    assert ecore_middleware.model.tags[1] == "Tag1"


def testEcoreAddNull(ecore_middleware):
    # Act
    ecore_middleware.addTag(None)

    # Assert
    assert len(ecore_middleware.model.tags) == 1
    assert ecore_middleware.model.tags[0] is None


def testEcoreAddItemAtIndexZero(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    ecore_middleware.addTagAt("Tag0", 0)

    # Assert
    assert ecore_middleware.model.tags[0] == "Tag0"
    assert ecore_middleware.model.tags[1] == "Tag1"
    assert len(ecore_middleware.model.tags) == 3


def testEcoreAddItemAtLastIndex(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    ecore_middleware.addTagAt("Tag3", 2)

    # Assert
    assert len(ecore_middleware.model.tags) == 3
    assert ecore_middleware.model.tags[2] == "Tag3"


def testEcoreAddItemAtNotLastIndex(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")
    ecore_middleware.model.tags.append("Tag3")

    # Act
    ecore_middleware.addTagAt("Tag1.5", 1)

    # Assert
    assert len(ecore_middleware.model.tags) == 4
    assert ecore_middleware.model.tags[0] == "Tag1"
    assert ecore_middleware.model.tags[1] == "Tag1.5"
    assert ecore_middleware.model.tags[2] == "Tag2"
    assert ecore_middleware.model.tags[3] == "Tag3"
    

def testEcoreAddItemAutoPluralization(ecore_middleware):
    # Verify case 1: model only has plural 'items', but addItem (singular) is called
    ecore_middleware.addItem("Item1")
    item2 = ecore_middleware.addItem("Item2")

    assert len(ecore_middleware.model.items) == 2
    assert ecore_middleware.model.items[0] == "Item1"
    assert ecore_middleware.model.items[1] == "Item2"
    assert item2 == "Item2"
    assert item2 is not None


def testEcoreAddItemAtAutoPluralization(ecore_middleware):
    # Verify addItemAt also auto-pluralizes correctly
    ecore_middleware.addItem("Item1")
    ecore_middleware.addItem("Item2")

    item0 = ecore_middleware.addItemAt("Item0", 0)

    assert ecore_middleware.model.items[0] == "Item0"
    assert ecore_middleware.model.items[1] == "Item1"
    assert len(ecore_middleware.model.items) == 3
    assert item0 == "Item0"
    assert item0 is not None


def testEcoreAddEntityReturnsMiddlewareWrappedObject():
    tiny_middleware = get_middleware_class("ecore")(MockTinyEcoreModel, name="Tiny")

    ecore_middleware = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")

    added = ecore_middleware.addItem(tiny_middleware)

    assert isinstance(added, MockTinyEcoreModel)
    assert added.model is tiny_middleware.model
    assert ecore_middleware.model.items[0] is tiny_middleware.model


def testEcoreAddItemToNonCollectionPropertyThrowsError(ecore_middleware):
    # Act
    with pytest.raises(MWTypeError) as errorInfo:
        ecore_middleware.addName("Name")

    # Assert
    assert (
        str(errorInfo.value)
        == "Operation 'addName' expects list-like reference"
    )


def testEcoreAddItemToNonExistentPropertyThrowsError(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.addNonexistent("Value")

    # Assert
    assert (
        str(errorInfo.value)
        == "Attribute or method 'nonexistent' not found on the model"
    )