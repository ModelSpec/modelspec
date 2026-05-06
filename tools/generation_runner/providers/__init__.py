from .openai import submit as submit_openai, check as check_openai
from .anthropic import submit as submit_anthropic, check as check_anthropic
from .google import submit as submit_google, check as check_google
from .google_direct import submit as submit_google_direct, check as check_google_direct
from .openrouter_direct import submit as submit_openrouter_direct, check as check_openrouter_direct
from .misc import *

PROVIDERS = {
    "openai": (submit_openai, check_openai),
    "anthropic": (submit_anthropic, check_anthropic),
    "google": (submit_google, check_google),
    "google_direct": (submit_google_direct, check_google_direct),
    "openrouter_direct": (submit_openrouter_direct, check_openrouter_direct),
}
