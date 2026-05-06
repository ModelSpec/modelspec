from typing import Callable, Any, Optional
from ..shared import Middleware, split_first_keyword, camel_to_snake
from ..shared.errors import MWAttributeMissing, MWTypeError, GET_WITH_UNSUPPORTED_MESSAGE

class EcoreMiddleware(Middleware):
    def __init__(self, model, **kwargs):
        if model is None:
            self.model = None
            return
        if isinstance(model, type):
            self.model = model(**kwargs)
        else:
            self.model = model

    # ---------- helper resolution ----------

    def _resolve_attr_name(self, base: str) -> Optional[str]:
        """
        Try exact variants to locate an attribute/reference on the Ecore model:
          - camel (e.g., 'raisedOnDate')
          - snake (e.g., 'raised_on_date')
        Return the first existing name, else None.
        """

        candidates = [
            base,                   # Try exact camelCase first
            camel_to_snake(base),   # Then try snake_case fallback
        ]
        for name in candidates:
            try:
                if hasattr(self.model, name):
                    return name
            except:
                continue
        return None

    def _get_attr_value(self, base: str) -> Any:
        name = self._resolve_attr_name(base)
        if not name:
            raise MWAttributeMissing(attribute_name=base)
        return getattr(self.model, name)

    def _set_attr_value(self, base: str, value: Any) -> None:
        name = self._resolve_attr_name(base)
        if not name:
            raise MWAttributeMissing(attribute_name=base)
        setattr(self.model, name, value)

    def _resolve_list_attr(self, base: str, operation: str) -> Any:
        """
        Resolve a list-like attribute for add/remove/index operations.
        Tries `base` first, then plural candidates (e.g. `base + 's'`, and
        `...y -> ...ies`), taking whichever resolves to a list-like member.
        Raises MWAttributeMissing if no candidate attribute exists at all.
        Raises MWTypeError if an attribute exists but is not list-like.
        """
        plural_candidates = [base + "s"]
        if base.endswith("y") and len(base) > 1:
            plural_candidates.append(base[:-1] + "ies")

        found_any = False
        for candidate in (base, *plural_candidates):
            name = self._resolve_attr_name(candidate)
            if name is None:
                continue
            found_any = True
            coll = getattr(self.model, name)
            if hasattr(coll, "append"):
                return coll
        if not found_any:
            raise MWAttributeMissing(attribute_name=base)
        raise MWTypeError(operation=operation, expected_type="list-like reference")

    # ---------- verb handlers ----------

    def handle_get_attr(self, attr: str) -> Callable[[], Any]:
        _, tail = split_first_keyword(attr)

        if tail.startswith("with"):
            # two things may be happening here:
            # 1. there's an actual attribute named "withFoo". This is supported and we'll handle that as usual.
            # 2. "foo" is a unique ID, thus Umple exposes "getWithFoo".
            # This latter is not supported and the user is expected to use list lookup instead.
            if self._resolve_attr_name(tail) is None:
                raise MWAttributeMissing(message=GET_WITH_UNSUPPORTED_MESSAGE)

        def _getter(*args):
            # If an index argument was passed, resolve via list auto-pluralization
            if args:
                index = args[0]
                try:
                    coll = self._resolve_list_attr(tail, attr)
                except MWTypeError:
                    raise TypeError(f"'{tail}' is not a list; cannot index into it")
                return self._wrap(coll[index])  # raises IndexError naturally

            value = self._get_attr_value(tail)

            # Normalize pyecore ELists to plain lists for test predictability
            try:
                if hasattr(value, "__iter__") and not isinstance(value, (str, bytes, dict)):
                    if hasattr(value, "append") or hasattr(value, "__len__"):
                        value = list(value)
            except TypeError:
                pass

            return self._wrap(value)
        return _getter

    def handle_set_attr(self, attr: str) -> Callable[[Any], None]:
        # set_<tail>(v) -> assign attribute/reference
        _, tail = split_first_keyword(attr)
        def _setter(v):
            assigned = self._unwrap(v)
            self._set_attr_value(tail, assigned)
            return self._wrap(assigned)
        return _setter

    def handle_add_attr(self, attr: str) -> Callable:
        _, base = split_first_keyword(attr)

        # Detect add<Item>At pattern for positional inserts
        if base.endswith("At"):
            item_name = base[:-2]  # strip 'At'
            def _add_at(o, index):
                coll = self._resolve_list_attr(item_name, attr)
                if not hasattr(coll, "insert"):
                    raise MWTypeError(operation=attr, expected_type="list-like reference")
                added = self._unwrap(o)
                coll.insert(index, added)
                return self._wrap(added)
            return _add_at

        # Regular add<Item>(obj) -> append
        def _add(o):
            coll = self._resolve_list_attr(base, attr)
            added = self._unwrap(o)
            coll.append(added)
            return self._wrap(added)
        return _add

    def handle_remove_attr(self, attr: str) -> Callable[[Any], None]:
        _, base = split_first_keyword(attr)
        def _remove(o):
            coll = self._resolve_list_attr(base, attr)
            # Let ValueError propagate if the item is not in the collection
            removed = self._unwrap(o)
            coll.remove(removed)
            return self._wrap(removed)
        return _remove

    def handle_delete_attr(self, attr: str) -> Callable[[], None]:
        # delete() on Ecore: most generated classes won't have it; we no-op unless present.
        # If a model implements delete(), we delegate to it.
        def _delete():
            if hasattr(self.model, "delete") and callable(getattr(self.model, "delete")):
                return self._wrap(getattr(self.model, "delete")())
            # else: no-op
            return None
        return _delete

    def handle_number_of_attr(self, attr: str) -> Callable[[], int]:
        # numberOfItems() -> len(reference)
        _, tail = split_first_keyword(attr)
        def _count():
            coll = self._get_attr_value(tail)
            if hasattr(coll, "__len__"):
                return len(coll)
            raise MWTypeError(operation=attr, expected_type="sized/list-like reference")
        return _count

    def handle_has_attr(self, attr: str) -> Callable[[Any], bool]:
        # has_<item>(value) -> membership check when value provided; fall back to truthiness otherwise
        _, tail = split_first_keyword(attr)
        def _has(value=None):
            v = self._get_attr_value(tail)

            # When a value is provided, treat this as a membership query
            if value is not None:
                target = self._unwrap(value)
                try:
                    return target in v
                except TypeError:
                    # container does not support membership; fall back to truthiness check
                    return bool(v)

            # No value provided: preserve original semantics (truthiness/length check)
            try:
                if hasattr(v, "__len__") and not isinstance(v, (str, bytes, dict)):
                    return len(v) > 0
            except TypeError:
                pass
            return bool(v)
        return _has

    def handle_is_attr(self, attr: str) -> Callable[[], bool]:
        # is_<flag>() -> bool(flag)
        _, tail = split_first_keyword(attr)
        def _is():
            v = self._get_attr_value(tail)
            return bool(v)
        return _is

    def handle_index_of_attr(self, attr: str) -> Callable[[Any], int]:
        # indexOfItem(obj) -> list.index(obj) or -1
        _, base = split_first_keyword(attr)
        def _index(o):
            coll = self._resolve_list_attr(base, attr)
            try:
                return coll.index(self._unwrap(o))
            except ValueError:
                return -1
        return _index