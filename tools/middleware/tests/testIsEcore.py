import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel
from ..core.shared.errors import *

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreIsOnTrueBooleanPropertyWithIsPrefix(ecore_middleware):
    # Arrange
    ecore_middleware.model.isActive = True

    # Act
    value = ecore_middleware.isIsActive()

    # Assert
    assert value

def testEcoreIsOnFalseBooleanPropertyWithIsPrefix(ecore_middleware):
    # Arrange
    ecore_middleware.model.isActive = False

    # Act
    value = ecore_middleware.isIsActive()

    # Assert
    assert not value

def testEcoreIsOnNonExistentProperty(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.isNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testEcoreIsOnTrueBooleanProperty(ecore_middleware):
    # Arrange
    ecore_middleware.model.ongoing = True

    # Act
    value = ecore_middleware.isOngoing()

    # Assert
    assert value

def testEcoreIsOnFalseBooleanProperty(ecore_middleware):
    # Arrange
    ecore_middleware.model.ongoing = False

    # Act
    value = ecore_middleware.isOngoing()

    # Assert
    assert not value


