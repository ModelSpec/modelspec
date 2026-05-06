import pytest

from ..factory import get_middleware_class
from ..mock import MockUmpleModel, MockChildUmpleModel


@pytest.fixture
def umple_middleware():
    return get_middleware_class("umple")(MockUmpleModel, id=0, name="InitialName")

def testUmpleMiddlewareEqualsItsOwnUnderlyingModel(umple_middleware):
    assert umple_middleware == umple_middleware.model

def testUmpleMiddlewareEqualsAnotherMiddlewareWrappingTheSameModel(umple_middleware):
    MW = get_middleware_class("umple")
    second_wrapper = MW(umple_middleware.model)
    assert umple_middleware == second_wrapper

def testUmpleMiddlewareDoesNotEqualADifferentModel(umple_middleware):
    other_model = MockUmpleModel(aId=99, aName="Other")
    assert not (umple_middleware == other_model)

def testUmpleMiddlewareDoesNotEqualADifferentMiddlewareWrappingADifferentModel(umple_middleware):
    MW = get_middleware_class("umple")
    other = MW(MockUmpleModel, id=99, name="Other")
    assert not (umple_middleware == other)

def testUmpleMiddlewareEqualityIsSymmetricWithPlainModel(umple_middleware):
    # plain_model == middleware should also hold via model.__eq__
    assert umple_middleware.model == umple_middleware

def testUmpleMiddlewareIsInstanceOfUnderlyingModelClass(umple_middleware):
    assert isinstance(umple_middleware, MockUmpleModel)

def testUmpleMiddlewareIsNotInstanceOfUnrelatedClass(umple_middleware):
    assert not isinstance(umple_middleware, MockChildUmpleModel)

def testUmpleMiddlewareClassPropertyReturnsUnderlyingModelType(umple_middleware):
    assert umple_middleware.__class__ is MockUmpleModel
