import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel
from ..core.shared.errors import MWAttributeMissing, GET_WITH_UNSUPPORTED_MESSAGE

@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw

def testUmpleGetExistingPropertyWithValue(umple_middleware):
    # Act
    value = umple_middleware.getName()

    # Assert
    assert value == umple_middleware.model._name

def testUmpleGetExistingPropertyWithNullValue(umple_middleware):
    # Act
    value = umple_middleware.getChild()

    # Assert
    assert value == umple_middleware.model._child
    assert value is None

def testUmpleGetNonExistentProperty(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.getNonexistent()

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testUmpleGetPropertyAfterSetterUpdate(umple_middleware):
    # Arrange
    umple_middleware.model.setName("UpdatedUmpleName")

    # Act
    value = umple_middleware.getName()

    # Assert via middleware
    assert value == umple_middleware.model._name
    assert value == "UpdatedUmpleName"

def testUmpleGetExistingListPropertyWithValue(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    value = umple_middleware.getTags()

    # Assert
    assert value == umple_middleware.model._tags
    assert len(value) == 2

def testUmpleGetExistingEmptyListPropertyWithValue(umple_middleware):
    # Act
    value = umple_middleware.getTags()

    # Assert
    assert value == umple_middleware.model._tags
    assert len(value) == 0

def testUmpleGetExistingListPropertyWithIndex(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    value = umple_middleware.getTag(1)

    # Assert
    assert value == umple_middleware.model._tags[1]
    assert value == "Tag2"

def testUmpleGetExistingListPropertyWithIndexOutOfBoundsThrowIndexError(umple_middleware):
    # Arrange
    umple_middleware.model.addTag("Tag1")
    umple_middleware.model.addTag("Tag2")

    # Act
    with pytest.raises(IndexError) as errorInfo:
        umple_middleware.getTag(5)

    # Assert
    assert str(errorInfo.value) == "list index out of range"

def testUmpleGetEmptyListPropertyWithIndexOutOfBoundsThrowIndexError(umple_middleware):
    # Act
    with pytest.raises(IndexError) as errorInfo:
        umple_middleware.getTag(0)

    # Assert
    assert str(errorInfo.value) == "list index out of range"

def testUmpleGetNonExistentPropertyIndexThrowsMWAttributeMissing(umple_middleware):
    # Act
    with pytest.raises(MWAttributeMissing) as errorInfo:
        umple_middleware.getNonexistent(1)

    # Assert
    assert str(errorInfo.value) == "Attribute or method 'nonexistent' not found on the model"

def testUmpleGetPropertyIndexOnNonCollectionThrowsTypeError(umple_middleware):
    # Act
    with pytest.raises(TypeError) as _:
        umple_middleware.getName(1)

def testUmpleGetWithIdRaisesUnsupported(umple_middleware):
    # getWith(Attribute) is not supported by the middleware (ecore-friendly approach: iterate parent collection).
    with pytest.raises(MWAttributeMissing) as exc_info:
        umple_middleware.getWithId(0)
    assert GET_WITH_UNSUPPORTED_MESSAGE in str(exc_info.value)
