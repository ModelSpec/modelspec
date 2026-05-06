import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockEcoreChildModel, MockTinyEcoreModel

@pytest.fixture
def ecore_middleware():
    ecore_mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")
    yield ecore_mw

def testEcoreDeleteObjectWithNoAssociations(ecore_middleware):
    # Arrange
    child_mw = get_middleware_class("ecore")(MockEcoreChildModel(value="Value1"))
    ecore_middleware.model.child = child_mw.model

    # Act
    child_mw.delete()

    # Assert
    assert child_mw.model.parent == None
    assert ecore_middleware.model.child is None


def testEcoreDeleteObjectWithAssociations(ecore_middleware):
    # Arrange
    child_mw = get_middleware_class("ecore")(MockEcoreChildModel(value="Value1"))
    ecore_middleware.model.child = child_mw.model
    tiny_mw1 = get_middleware_class("ecore")(MockTinyEcoreModel(name="Name1"))
    child_mw.model.tinies.append(tiny_mw1.model)
    tiny_mw2 = get_middleware_class("ecore")(MockTinyEcoreModel(name="Name2"))
    child_mw.model.tinies.append(tiny_mw2.model)

    # Act
    child_mw.delete()

    # Assert
    assert child_mw.model.parent == None
    assert len(child_mw.model.tinies) == 0
    assert ecore_middleware.model.child is None
    assert tiny_mw1.model.parent == None
    assert tiny_mw2.model.parent == None


def testEcoreDeleteWithoutDeleteMethodReturnsNone(ecore_middleware):
    # MockEcoreModel does not define delete(), middleware should no-op and return None
    assert ecore_middleware.delete() is None


def testEcoreDeleteReturnsWrappedDeleteResult():
    class _DeleteReturnModel:
        def __init__(self):
            self.child = MockTinyEcoreModel("DeletedChild")

        def delete(self):
            return self.child

    model_mw = get_middleware_class("ecore")(_DeleteReturnModel)

    deleted = model_mw.delete()

    assert isinstance(deleted, MockTinyEcoreModel)
    assert deleted.model is model_mw.model.child
