from abc import ABC, abstractmethod
from typing import Callable, Any
from .middleware_helper import split_first_keyword, is_snake_case, is_camel_case, snake_to_camel

# Scalar and collection types that are never model entities.
# Shared by all middleware implementations; subclasses use these to decide
# what to pass through vs. what to wrap.
# Not meant to be exhaustive on Python's built-in types, just the common ones we expect to encounter in models,
# so add more as needed.
MW_PRIMITIVES = (str, int, float, bool, bytes, complex)
MW_COLLECTIONS = (list, tuple, set, frozenset)

class Middleware(ABC):

    """
    This is the base class for all middleware implementations.
    """

    @abstractmethod
    def __init__(self, model, **kwargs):
        """
        Wrap a model in the middleware.
        :param model: either a model *class* (constructed with **kwargs) or an
                       already-instantiated model object (kwargs are ignored).
        :param kwargs: keyword constructor arguments when *model* is a class.
        """
        pass

    @property
    def __class__(self):
        """
        Make isinstance(middlewared_instance, SomeClass) transparent:
        Python's isinstance() consults obj.__class__, so returning the
        underlying model's type lets callers treat the wrapper as if it
        were the model itself.
        """
        return type(self.model)

    def __eq__(self, other: Any) -> bool:
        """
        Delegate equality to the underlying model.
        Both plain model instances and other middleware-wrapped instances
        are handled by unwrapping before comparison.
        """
        return self.model == self._unwrap(other)

    def __hash__(self) -> int:
        return hash(self.model)

    def _wrap(self, value: Any) -> Any:
        """
        Wrap a getter return value in middleware if it is a model entity.
        MW_PRIMITIVES, MW_COLLECTIONS, None, and lists are handled directly;
        everything else is assumed to be a model entity and wrapped via type(self).
        """
        if value is None:
            return None
        if isinstance(value, MW_PRIMITIVES):
            return value
        if isinstance(value, dict):
            return {k: self._wrap(v) for k, v in value.items()}
        if isinstance(value, MW_COLLECTIONS):
            return type(value)(self._wrap(v) for v in value)
        return type(self)(value)

    def _unwrap(self, obj: Any) -> Any:
        """
        If tests passed another middleware-wrapped instance, unwrap to the concrete model.
        This allows middleware objects to be composed and passed to each other.
        :param obj: The object to unwrap (could be a middleware instance or a regular object)
        :return: The unwrapped model instance, or obj itself if it's not a middleware instance
        """
        return getattr(obj, "model", obj)

    def __getattr__(self, attr):
        """
        This is a built-in method in Python that is called when an attribute is not found in the usual places.
        For example, when calling middleware.some_attr, Python will first look for some_attr in the middleware instance.
        If none is found, __getattr__ is called with attr="some_attr".
        :param attr: the attribute name being accessed.
        :return: the corresponding attribute from the internal model.
        """
        # In Python, functions are actually just a special type (callable) of attribute.
        # When you call middleware.some_function(), what happens is:
        # 1. Python looks for the some_function attribute in the middleware instance, i.e., middleware.some_function
        # 2. We expect this returned attribute to be callable, so the () operator can be applied to it, optionally with arguments.
        # This is the intuition behind why this works for functions as well as regular attributes.

        # If the caller used snake_case (e.g., get_name, add_tag), convert to
        # camelCase first so that a single code-path handles both conventions.
        if is_snake_case(attr):
            attr = snake_to_camel(attr)

        # Special-case plain delete() which has no tail and therefore is not
        # considered camelCase by is_camel_case.
        if attr == 'delete':
            return self.handle_delete_attr(attr)

        if is_camel_case(attr):
            # get the first keyword to determine the type of calls.
            # The keywords would be things like "get", "set", "is", "add", "remove", etc.
            first_keyword, _rest = split_first_keyword(attr)

            # call to the handler function, which will be implemented in subclasses.
            # split_first_keyword returns (first, rest) where `first` is a string like 'get' or 'set'.
            if first_keyword == 'get':
                return self.handle_get_attr(attr)
            elif first_keyword == 'set':
                return self.handle_set_attr(attr)
            elif first_keyword == 'add':
                return self.handle_add_attr(attr)
            elif first_keyword == 'remove':
                return self.handle_remove_attr(attr)
            elif first_keyword == 'delete':
                return self.handle_delete_attr(attr)
            elif first_keyword == 'number':
                # expecting 'number_of' prefix, handler will parse the rest
                return self.handle_number_of_attr(attr)
            elif first_keyword == 'has':
                return self.handle_has_attr(attr)
            elif first_keyword == 'is':
                return self.handle_is_attr(attr)
            elif first_keyword == 'index':
                # expecting 'index_of' prefix
                return self.handle_index_of_attr(attr)
            else:
                # handle more cases here
                raise AttributeError(f"Method {attr} not found in model.")

        # fallback to directly attempting to get the attribute from the model.
        return getattr(self.model, attr)


    # Marks the following functions as abstract, meaning subclasses must implement them.
    @abstractmethod
    def handle_get_attr(self, attr: str) -> Callable[[], Any]:
        """
        Handles "get" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "get_some_attribute"
        :return: a callable that retrieves the corresponding attribute from the internal model.
        """
        pass


    @abstractmethod
    def handle_set_attr(self, attr: str) -> Callable[[Any], None]:
        """
        Handles "set" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "set_some_attribute"
        :return: a callable that sets the corresponding attribute on the internal model.
        """
        pass

    @abstractmethod
    def handle_add_attr(self, attr: str) -> Callable[[Any], None]:
        """
        Handles "add" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "add_some_element"
        :return: a callable that adds an element to the corresponding collection attribute on the internal model.
        """
        pass

    @abstractmethod
    def handle_remove_attr(self, attr: str) -> Callable[[Any], None]:
        """
        Handles "remove" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "remove_some_element"
        :return: a callable that removes an element from the corresponding collection attribute on the internal model.
        """
        pass

    @abstractmethod
    def handle_delete_attr(self, attr: str) -> Callable[[], None]:
        """
        Handles "delete" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "deleteSomeAttribute"
        :return: a callable that deletes the corresponding attribute from the internal model.
        """
        pass

    @abstractmethod
    def handle_number_of_attr(self, attr: str) -> Callable[[], int]:
        """
        Handles "number_of" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "number_of_some_elements"
        :return: a callable that returns the number of elements in the corresponding collection attribute on the internal model.
        """
        pass

    @abstractmethod
    def handle_has_attr(self, attr: str) -> Callable[[Any], bool]:
        """
        Handles "has" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "has_some_element"
        :return: a callable that checks if an element exists in the corresponding collection attribute on the internal model.
        """
        pass

    @abstractmethod
    def handle_is_attr(self, attr: str) -> Callable[[], bool]:
        """
        Handles "is" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "is_some_condition"
        :return: a callable that returns the boolean value of the corresponding attribute on the internal model.
        """
        pass

    @abstractmethod
    def handle_index_of_attr(self, attr: str) -> Callable[[Any], int]:
        """
        Handles "index_of" attribute calls.
        :param attr: the full attribute name being accessed, e.g., "index_of_some_element"
        :return: a callable that returns the index of an element in the corresponding collection attribute on the internal model.
        """
        pass