# litellm_patch.py
import litellm

# These are the words that confuse Groq's API
UNSUPPORTED_KEYS = ["cache_breakpoint"]

# Save the original function
_original_completion = litellm.completion

def _patched_completion(*args, **kwargs):
    """
    This new function removes the confusing words
    before sending the message to Groq.
    """
    for key in UNSUPPORTED_KEYS:
        if key in kwargs:
            del kwargs[key]
    return _original_completion(*args, **kwargs)

def apply_patch():
    """
    This function turns on our filter.
    """
    litellm.completion = _patched_completion
