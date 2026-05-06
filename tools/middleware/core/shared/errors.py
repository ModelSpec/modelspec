class MiddlewareError(Exception):
    """Base middleware error for unified, friendly messages."""
    
    def __init__(self, message: str = ""):
        """
        :param message: Custom error message. If empty, default template will be used.
        """
        super().__init__(message)
        self.message = message


# Message when tests/code use getWithX (e.g. getWithId, getWithEmail), which the middleware does not support.
# Use the ecore-friendly approach: get the parent's collection and iterate to find by attribute.
GET_WITH_UNSUPPORTED_MESSAGE = (
    "getWith(Attribute) is not supported by the middleware. "
    "Use the ecore-friendly approach: get the parent's collection and iterate to find the instance by attribute."
)


class MWAttributeMissing(MiddlewareError):
    """Raised when an expected attribute or method is not present on the model."""
    
    def __init__(self, attribute_name: str = None, operation: str = None, message: str = None):
        if message:
            super().__init__(message)
        elif attribute_name and operation:
            super().__init__(f"Attribute '{attribute_name}' not found. Cannot perform operation: {operation}")
        elif attribute_name:
            super().__init__(f"Attribute or method '{attribute_name}' not found on the model")
        else:
            super().__init__("Required attribute or method is missing on the model")


class MWTypeError(MiddlewareError):
    """Raised when an operation is invoked with the wrong type or arity."""
    
    def __init__(self, operation: str = None, expected_type: str = None, actual_type: str = None, message: str = None):
        if message:
            super().__init__(message)
        elif operation and expected_type:
            if actual_type:
                super().__init__(f"Operation '{operation}' expects {expected_type}, but got {actual_type}")
            else:
                super().__init__(f"Operation '{operation}' expects {expected_type}")
        elif operation:
            super().__init__(f"Operation '{operation}' called with wrong type or arity")
        else:
            super().__init__("Operation called with wrong type or arity")


class MWMultiplicityError(MiddlewareError):
    """Raised when a multiplicity rule is violated."""
    
    def __init__(self, constraint: str = None, entity: str = None, message: str = None):
        if message:
            super().__init__(message)
        elif constraint and entity:
            super().__init__(f"Multiplicity constraint '{constraint}' violated for {entity}")
        elif constraint:
            super().__init__(f"Multiplicity constraint '{constraint}' violated")
        else:
            super().__init__("Multiplicity constraint violated")


class MWNotFound(MiddlewareError):
    """Raised when an entity looked up by id/name cannot be found."""
    
    def __init__(self, entity_type: str = None, identifier: str = None, message: str = None):
        if message:
            super().__init__(message)
        elif entity_type and identifier:
            super().__init__(f"{entity_type} with identifier '{identifier}' not found")
        elif entity_type:
            super().__init__(f"{entity_type} not found")
        else:
            super().__init__("Requested entity not found")


class MWIllegalState(MiddlewareError):
    """Raised on inconsistent state transitions."""
    
    def __init__(self, current_state: str = None, attempted_transition: str = None, message: str = None):
        if message:
            super().__init__(message)
        elif current_state and attempted_transition:
            super().__init__(f"Cannot transition from '{current_state}' via '{attempted_transition}'")
        elif attempted_transition:
            super().__init__(f"Illegal state transition: '{attempted_transition}'")
        else:
            super().__init__("Invalid state transition")