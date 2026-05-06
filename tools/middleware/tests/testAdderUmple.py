import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel
from ..core.shared.errors import *


@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw


def testUmpleAddItemToEmptyCollection(umple_middleware):
    # Act
    umple_middleware.addTag("Tag1")

    # Assert
    assert len(umple_middleware.model._tags) == 1
    assert umple_middleware.model._tags[0] == "Tag1"


def testUmpleAddItemToNonEmptyCollection(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")

    # Act
    umple_middleware.addTag("Tag2")

    # Assert
    assert len(umple_middleware.model._tags) == 2
    assert umple_middleware.model._tags[0] == "Tag1"
    assert umple_middleware.model._tags[1] == "Tag2"


def testUmpleAddDuplicateItem(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")

    # Act
    umple_middleware.addTag("Tag1")

    # Assert
    assert len(umple_middleware.model._tags) == 2
    assert umple_middleware.model._tags[0] == "Tag1"
    assert umple_middleware.model._tags[1] == "Tag1"


def testUmpleAddNone(umple_middleware): #Null?
    # Act
    umple_middleware.addTag(None)

    # Assert
    assert len(umple_middleware.model._tags) == 1
    assert umple_middleware.model._tags[0] is None


def testUmpleAddItemAtIndexZero(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    umple_middleware.addTagAt("Tag0", 0)

    # Assert
    assert umple_middleware.model._tags[0] == "Tag0"
    assert umple_middleware.model._tags[1] == "Tag1"
    assert len(umple_middleware.model._tags) == 3


def testUmpleAddItemAtLastIndex(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    umple_middleware.addTagAt("Tag3", 2)

    # Assert
    assert len(umple_middleware.model._tags) == 3
    assert umple_middleware.model._tags[2] == "Tag3"


def testUmpleAddItemAtNotLastIndex(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")
    umple_middleware.model.addTag("Tag3")

    # Act
    umple_middleware.addTagAt("Tag1.5", 1)

    # Assert
    assert len(umple_middleware.model._tags) == 4
    assert umple_middleware.model._tags[0] == "Tag1"
    assert umple_middleware.model._tags[1] == "Tag1.5"
    assert umple_middleware.model._tags[2] == "Tag2"
    assert umple_middleware.model._tags[3] == "Tag3"


def testUmpleAddItemToNonCollectionPropertyThrowsError(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.addName("Name")

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'name' not found on the model"


def testUmpleAddItemToNonExistentPropertyThrowsError(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.addNonexistent("Value")

    # Assert
    assert (
        str(errorInfo.value)
        == "Attribute or method 'nonexistent' not found on the model"
    )