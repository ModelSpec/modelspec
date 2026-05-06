import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel
from ..core.shared.errors import *


@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw


def testEcoreIndexOfExistingItemInCollection(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")
    ecore_middleware.model.tags.append("Tag3")

    # Act
    value = ecore_middleware.indexOfTag("Tag2")

    # Assert
    assert value == 1


def testEcoreIndexOfNonExistentItemInCollection(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    value = ecore_middleware.indexOfTag("Tag3")

    # Assert
    assert value == -1


def testEcoreIndexOfNonExistentProperty(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.indexOfNonexistent("Tag")

    # Assert
    assert (
        str(errorInfo.value)
        == "Attribute or method 'nonexistent' not found on the model"
    )
