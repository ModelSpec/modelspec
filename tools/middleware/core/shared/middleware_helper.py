import re

def is_snake_case(s: str) -> bool:
    """Return True if s is lowercase and contains an underscore."""
    return s == s.lower() and "_" in s

def is_camel_case(s: str) -> bool:
    """Return True if s looks like lowerCamelCase (no underscores, has at least one uppercase letter)."""
    return "_" not in s and s[0].islower() and s != s.lower()

def snake_to_camel(s: str) -> str:
    """Convert snake_case to lowerCamelCase (e.g., 'get_name' -> 'getName')."""
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def camel_to_snake(s: str) -> str:
    """
    Convert lowerCamelCase to snake_case.
    Examples:
      'getName'      -> 'get_name'
      'addTagAt'     -> 'add_tag_at'
      'numberOfTags' -> 'number_of_tags'
      'indexOfTag'   -> 'index_of_tag'
      'isIsActive'   -> 'is_is_active'
      'hasTags'      -> 'has_tags'
      'getWithId'    -> 'get_with_id'
    """
    # Insert underscore before each uppercase letter, then lowercase the whole thing.
    return re.sub(r'([A-Z])', r'_\1', s).lower()

def split_first_keyword(s: str) -> tuple[str, str]:
    """
    Split a camelCase verb+tail into ('verb', 'tail'). Also handles legacy snake_case.

    Examples (camelCase, primary):
      'getName'        -> ('get', 'name')
      'setAmount'      -> ('set', 'amount')
      'addTag'         -> ('add', 'tag')
      'addTagAt'       -> ('add', 'tagAt')
      'numberOfTags'   -> ('number', 'tags')   # 'Of' prefix stripped
      'indexOfTag'     -> ('index', 'tag')      # 'Of' prefix stripped
      'isActive'       -> ('is', 'active')
      'hasTags'        -> ('has', 'tags')
      'getWithId'      -> ('get', 'withId')

    Examples (snake_case, legacy):
      'get_name'        -> ('get', 'name')
      'number_of_items' -> ('number', 'items')
    """
    # Legacy snake_case path
    if "_" in s:
        first, rest = s.split("_", 1)
        if first in ("index", "number") and rest.startswith("of_"):
            rest = rest.split("_", 1)[1]
        return first, rest

    # camelCase path: split at the first uppercase letter
    for i, c in enumerate(s):
        if c.isupper():
            first = s[:i]                           # lowercase prefix, e.g. 'get', 'number'
            suffix = s[i:]                           # e.g. 'Name', 'OfTags', 'Active'
            rest = suffix[0].lower() + suffix[1:]   # lowercase first char: 'name', 'ofTags'
            # For 'number' and 'index', strip a leading 'of' segment
            if first in ("number", "index") and rest.startswith("of"):
                after_of = rest[2:]                 # e.g. 'Tags' or 'Tag'
                if after_of:
                    rest = after_of[0].lower() + after_of[1:]   # 'tags' or 'tag'
            return first, rest

    return s, ""
