import pytest

from ..core.umple.umple_middleware import UmpleMiddleware
from ..core.ecore.ecore_middleware import EcoreMiddleware
from ..factory import get_middleware_class
from ..mock import MockUmpleModel, MockEcoreModel

def testFactoryCreatesUmpleMiddlewareSuccess():
    # Act
    MW = get_middleware_class("umple")

    # Assert
    assert MW == UmpleMiddleware

def testFactoryCreatesEcoreMiddlewareSuccess():
    # Act
    MW = get_middleware_class("ecore")

    # Assert
    assert MW == EcoreMiddleware

def testFactoryThrowsErrorForUnknownModelSuccess():
    # Act
    with pytest.raises(ValueError) as errorInfo:
        get_middleware_class("unknown")

    # Assert
    assert str(errorInfo.value) == "Unknown model_type 'unknown'. Supported types: 'umple', 'ecore'."


def testEcoreMiddlewareWrapsClassWithArgs():
    mw = get_middleware_class("ecore")(MockEcoreModel, id=0, name="Alice")
    assert isinstance(mw.model, MockEcoreModel)
    assert mw.getName() == "Alice"


def testEcoreMiddlewareWrapsExistingInstance():
    instance = MockEcoreModel(id=0, name="Alice")
    mw = get_middleware_class("ecore")(instance)
    assert mw.model is instance
    assert mw.getName() == "Alice"


def testUmpleMiddlewareWrapsClassWithArgs():
    mw = get_middleware_class("umple")(MockUmpleModel, id=0, name="Bob")
    assert isinstance(mw.model, MockUmpleModel)
    assert mw.getName() == "Bob"


def testUmpleMiddlewareWrapsExistingInstance():
    instance = MockUmpleModel(aId=0, aName="Bob")
    mw = get_middleware_class("umple")(instance)
    assert mw.model is instance
    assert mw.getName() == "Bob"