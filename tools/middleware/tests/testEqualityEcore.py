import pytest

from ..factory import get_middleware_class
from ..mock import MockEcoreModel, MockEcoreChildModel


@pytest.fixture
def ecore_middleware():
    return get_middleware_class("ecore")(MockEcoreModel, id=0, name="InitialName")

def testEcoreMiddlewareEqualsItsOwnUnderlyingModel(ecore_middleware):
    assert ecore_middleware == ecore_middleware.model

def testEcoreMiddlewareEqualsAnotherMiddlewareWrappingTheSameModel(ecore_middleware):
    MW = get_middleware_class("ecore")
    second_wrapper = MW(ecore_middleware.model)
    assert ecore_middleware == second_wrapper

def testEcoreMiddlewareDoesNotEqualADifferentModel(ecore_middleware):
    other_model = MockEcoreModel(id=99, name="Other")
    assert not (ecore_middleware == other_model)

def testEcoreMiddlewareDoesNotEqualADifferentMiddlewareWrappingADifferentModel(ecore_middleware):
    MW = get_middleware_class("ecore")
    other = MW(MockEcoreModel, id=99, name="Other")
    assert not (ecore_middleware == other)

def testEcoreMiddlewareEqualityIsSymmetricWithPlainModel(ecore_middleware):
    # plain_model == middleware should also hold via model.__eq__
    assert ecore_middleware.model == ecore_middleware

def testEcoreMiddlewareIsInstanceOfUnderlyingModelClass(ecore_middleware):
    assert isinstance(ecore_middleware, MockEcoreModel)

def testEcoreMiddlewareIsNotInstanceOfUnrelatedClass(ecore_middleware):
    assert not isinstance(ecore_middleware, MockEcoreChildModel)

def testEcoreMiddlewareClassPropertyReturnsUnderlyingModelType(ecore_middleware):
    assert ecore_middleware.__class__ is MockEcoreModel
