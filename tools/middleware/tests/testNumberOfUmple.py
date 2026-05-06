import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel, MockChildUmpleModel
from ..core.shared.errors import *


@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw


def testUmpleNumberOfNonEmptyCollection(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")
    umple_middleware.model.addTag("Tag3")

    # Act
    value = umple_middleware.numberOfTags()

    # Assert
    assert value == 3


def testUmpleNumberOfEmptyCollection(umple_middleware):
    # Act
    value = umple_middleware.numberOfTags()

    # Assert
    assert value == 0


def testUmpleNumberOfNonCollectionThrowsError(umple_middleware):
    # Arrange
    umple_middleware.model.setChild(MockChildUmpleModel(1))

    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.numberOfChild()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'child' not found on the model"

def testUmpleNumberOfNonExistentPropertyThrowsError(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.numberOfNonexistent()

    # Assert
    assert (
        str(errorInfo.value)
        == "Attribute or method 'nonexistent' not found on the model"
    )
