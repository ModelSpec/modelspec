import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel
from ..core.shared.errors import MWAttributeMissing, GET_WITH_UNSUPPORTED_MESSAGE

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreGetExistingPropertyWithValue(ecore_middleware):
    # Act
    value = ecore_middleware.getName()
    print(ecore_middleware.model.id)

    # Assert
    assert value == ecore_middleware.model.name

def testEcoreGetExistingPropertyWithNullValue(ecore_middleware):
    # Act
    value = ecore_middleware.getChild()

    # Assert
    assert value == ecore_middleware.model.child
    assert value is None

def testEcoreGetNonExistentProperty(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.getNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testEcoreGetPropertyAfterSetterUpdate(ecore_middleware):
    # Arrange
    ecore_middleware.model.name = "UpdatedEcoreName"

    # Act
    value = ecore_middleware.getName()

    # Assert via middleware
    assert value == ecore_middleware.model.name
    assert value == "UpdatedEcoreName"

def testEcoreGetExistingListPropertyWithValue(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    value = ecore_middleware.getTags()

    # Assert
    assert value == ecore_middleware.model.tags
    assert len(value) == 2

def testEcoreGetExistingEmptyListPropertyWithValue(ecore_middleware):
    # Act
    value = ecore_middleware.getTags()

    # Assert
    assert value == ecore_middleware.model.tags
    assert len(value) == 0

def testEcoreGetExistingListPropertyWithIndex(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    value = ecore_middleware.getTag(1)

    # Assert
    assert value == ecore_middleware.model.tags[1]
    assert value == "Tag2"

def testEcoreGetExistingListPropertyWithIndexOutOfBoundsThrowIndexError(ecore_middleware):
    # Arrange
    ecore_middleware.model.tags.append("Tag1")
    ecore_middleware.model.tags.append("Tag2")

    # Act
    with pytest.raises(IndexError) as errorInfo:
        ecore_middleware.getTag(5)

    # Assert
    assert str(errorInfo.value) == "list index out of range"

def testEcoreGetEmptyListPropertyWithIndexOutOfBoundsThrowIndexError(ecore_middleware):
    # Act
    with pytest.raises(IndexError) as errorInfo:
        ecore_middleware.getTag(0)

    # Assert
    assert str(errorInfo.value) == "list index out of range"

def testEcoreGetNonExistentPropertyIndexThrowsMWAttributeMissing(ecore_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        ecore_middleware.getNonexistent(1)

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testEcoreGetPropertyIndexOnNonCollectionThrowsTypeError(ecore_middleware):
    # Act
    with pytest.raises(TypeError) as _:
        ecore_middleware.getName(1)

def testEcoreGetWithIdRaisesUnsupported(ecore_middleware):
    # getWith(Attribute) is not supported by the middleware (ecore-friendly approach: iterate parent collection).
    with pytest.raises(MWAttributeMissing) as exc_info:
        ecore_middleware.getWithId(0)
    assert GET_WITH_UNSUPPORTED_MESSAGE in str(exc_info.value)

