import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel
from ..core.shared.errors import *


@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw


def testUmpleIndexOfExistingItemInCollection(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")
    umple_middleware.model.addTag("Tag3")

    # Act
    value = umple_middleware.indexOfTag("Tag2")

    # Assert
    assert value == 1


def testUmpleIndexOfNonExistentItemInCollection(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    value = umple_middleware.indexOfTag("Tag3")

    # Assert
    assert value == -1


def testUmpleIndexOfNonExistentProperty(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.indexOfNonexistent()

    # Assert
    assert (
        str(errorInfo.value)
        == "Attribute or method 'nonexistent' not found on the model"
    )
