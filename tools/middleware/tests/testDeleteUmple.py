import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel, MockChildUmpleModel, MockTinyUmpleModel

@pytest.fixture
def umple_middleware():
    umple_mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")
    yield umple_mw

def testUmpleDeleteObjectWithNoAssociations(umple_middleware):
    # Arrange
    child_mw = get_middleware_class("umple")(MockChildUmpleModel(value="Value1"))
    umple_middleware.model.setChild(child_mw.model)

    # Act
    child_mw.delete()

    # Assert
    assert child_mw.model.getParent() == None
    assert not umple_middleware.model.hasChild()


def testUmpleDeleteObjectWithAssociations(umple_middleware):
    # Arrange
    child_mw = get_middleware_class("umple")(MockChildUmpleModel(value="Value1"))
    umple_middleware.model.setChild(child_mw.model)
    tiny_mw1 = get_middleware_class("umple")(MockTinyUmpleModel(name="Name1"))
    child_mw.model.addTiny1(tiny_mw1.model)
    tiny_mw2 = get_middleware_class("umple")(MockTinyUmpleModel(name="Name2"))
    child_mw.model.addTiny1(tiny_mw2.model)

    # Act
    child_mw.delete()

    # Assert
    assert child_mw.model.getParent() == None
    assert len(child_mw.model.getTinies()) == 0
    assert not umple_middleware.model.hasChild()
    assert tiny_mw1.model.getParent() == None
    assert tiny_mw2.model.getParent() == None

def testUmpleDeleteObjectWithIdDictionary(umple_middleware):
    # Arrange
    child_mw = get_middleware_class("umple")(MockChildUmpleModel(value="Value1"))
    umple_middleware.model.setChild(child_mw.model)
    tiny_mw1 = get_middleware_class("umple")(MockTinyUmpleModel(name="Name1"))
    child_mw.model.addTiny1(tiny_mw1.model)
    tiny_mw2 = get_middleware_class("umple")(MockTinyUmpleModel(name="Name2"))
    child_mw.model.addTiny1(tiny_mw2.model)

    # Act
    umple_middleware.delete()

    # Assert
    assert umple_middleware.model.getChild() == None
    assert len(umple_middleware.model.mockUmpleModelsById) == 0
    assert child_mw.model.getParent() == None
    assert len(child_mw.model.getTinies()) == 0
    assert not umple_middleware.model.hasChild()
    assert tiny_mw1.model.getParent() == None
    assert tiny_mw2.model.getParent() == None
