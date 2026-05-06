from typing import Callable, Any
from ..shared import Middleware, split_first_keyword
from ..shared.errors import (
    MWAttributeMissing,
    GET_WITH_UNSUPPORTED_MESSAGE,
)


class UmpleMiddleware(Middleware):
    def __init__(self, model, **kwargs):
        if model is None:
            self.model = None
            return
        if isinstance(model, type):
            model_kwargs = {
                f"a{key[0].upper()}{key[1:]}": value
                for key, value in kwargs.items()
            }
            self.model = model(**model_kwargs)
        else:
            self.model = model

    def _umple_handle_attr(self, attr: str) -> Callable:
        """
        This private function handles retrieving an attr (function) from the internal Umple model.
        Since Umple already generates many getters and setters, we can directly map them.
        :param attr: the attribute name in camelCase (e.g. 'getName', 'addTag').
        :return: a wrapped callable whose return value is passed through ``self._wrap``.
        :raises MWAttributeMissing: if the resolved method doesn't exist on the Umple model.
        """
        if not hasattr(self.model, attr):
            # Extract the tail (attribute name) for a cleaner error message
            _, tail = split_first_keyword(attr)
            raise MWAttributeMissing(attribute_name=tail or attr)

        method = getattr(self.model, attr)
        def _wrapped(*args, **kwargs):
            return self._wrap(method(*args, **kwargs))
        return _wrapped

    def handle_get_attr(self, attr: str) -> Callable[[], Any]:
        _, tail = split_first_keyword(attr)
        if tail.startswith("with"):
            # two things may be happening here:
            # 1. there's an actual attribute named "withFoo". This is supported and we'll handle that as usual.
            # 2. "foo" is a unique ID, thus Umple exposes "getWithFoo".
            # This latter is not supported and the user is expected to use list lookup instead.
            if not hasattr(self.model, f"_{tail}"):
                raise MWAttributeMissing(message=GET_WITH_UNSUPPORTED_MESSAGE)
        return self._umple_handle_attr(attr)

    def handle_set_attr(self, attr: str) -> Callable[[Any], None]:
        try:
            return self._umple_handle_attr(attr)
        except Exception:
            # If set{Tail} doesn't exist, there is a chance that {tail} is an autounique attribute,
            # in which case Umple does not expose a setter. However, the _{tail} field is still settable and we can use that as a workaround.
            _, tail = split_first_keyword(attr)
            
            if hasattr(self.model, f"_{tail}"):
                def _setter(value):
                    setattr(self.model, f"_{tail}", value)
                return _setter
            
            raise

    def handle_add_attr(self, attr: str) -> Callable[[Any], None]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.addName -> umple_model.addName
        return self._umple_handle_attr(attr)

    def handle_remove_attr(self, attr: str) -> Callable[[Any], None]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.removeName -> umple_model.removeName
        return self._umple_handle_attr(attr)

    def handle_delete_attr(self, attr: str) -> Callable[[], None]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.delete -> umple_model.delete
        return self._umple_handle_attr(attr)

    def handle_is_attr(self, attr: str) -> Callable[[Any], bool]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.isActive -> umple_model.isActive
        return self._umple_handle_attr(attr)

    def handle_has_attr(self, attr: str) -> Callable[[Any], bool]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.hasTags -> umple_model.hasTags
        return self._umple_handle_attr(attr)

    def handle_number_of_attr(self, attr: str) -> Callable[[Any], int]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.numberOfTags -> umple_model.numberOfTags
        return self._umple_handle_attr(attr)

    def handle_index_of_attr(self, attr: str) -> Callable[[Any], int]:
        # for Umple, most function calls can be routed directly.
        # e.g., middleware.indexOfTag -> umple_model.indexOfTag
        return self._umple_handle_attr(attr)
