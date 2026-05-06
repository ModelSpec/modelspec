from typing import Literal, Type
from .core.umple.umple_middleware import UmpleMiddleware
from .core.ecore.ecore_middleware import EcoreMiddleware
from .core.shared.middleware import Middleware

ModelType = Literal["umple", "ecore"]

def get_middleware_class(model_type: ModelType) -> Type[Middleware]:
    """
    Return the middleware class to use for a run.
    How to use in tests/controllers:
        MW = get_middleware_class("umple" or "ecore")
        wrapped = MW(GeneratedModelClass, *constructor_args)
    """
    if model_type == "umple":
        return UmpleMiddleware
    elif model_type == "ecore":
        return EcoreMiddleware
    else:
        raise ValueError(f"Unknown model_type '{model_type}'. Supported types: 'umple', 'ecore'.")