import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockEcoreChildModel
from ..core.shared.errors import *


@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw


def testEcoreNumberOfNonEmptyCollection(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")
    ecore_middleware.model.tags.append("Tag3")

    # Act
    value = ecore_middleware.numberOfTags()

    # Assert
    assert value == 3


def testEcoreNumberOfEmptyCollection(ecore_middleware):
    # Act
    value = ecore_middleware.numberOfTags()

    # Assert
    assert value == 0


def testEcoreNumberOfNonCollectionThrowsError(ecore_middleware):
    # Arrange
    ecore_middleware.model.child = MockEcoreChildModel(1)

    # Act
    with pytest.raises(MWTypeError) as errorInfo:
        ecore_middleware.numberOfChild()

    # Assert
    assert (
        str(errorInfo.value)
        == "Operation 'numberOfChild' expects sized/list-like reference"
    )


def testEcoreNumberOfNonExistentPropertyThrowsError(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.numberOfNonexistent()

    # Assert
    assert (
        str(errorInfo.value)
        == "Attribute or method 'nonexistent' not found on the model"
    )
