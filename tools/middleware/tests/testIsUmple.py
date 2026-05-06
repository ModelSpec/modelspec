import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel
from ..core.shared.errors import *


@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw

def testUmpleIsOnTrueBooleanPropertyWithIsPrefix(umple_middleware):
    # Arrange
    umple_middleware.model.setIsActive(True)

    # Act
    value=umple_middleware.model.isIsActive()

    # Assert
    assert value

def testUmpleIsOnFalseBooleanPropertyWithIsPrefix(umple_middleware):
    # Arrange
    umple_middleware.model.setIsActive(False)

    # Act
    value = umple_middleware.model.isIsActive()

    # Assert
    assert not value

def testUmpleIsOnNonExistentProperty(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.isNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"


def testUmpleIsOnTrueBooleanProperty(umple_middleware):
    # Arrange
    umple_middleware.model.setOngoing(True)

    # Act
    value = umple_middleware.model.isOngoing()

    # Assert
    assert value

def testUmpleIsOnFalseBooleanProperty(umple_middleware):
    # Arrange
    umple_middleware.model.setOngoing(False)

    # Act
    value = umple_middleware.model.isOngoing()

    # Assert
    assert not value