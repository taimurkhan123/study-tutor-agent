
# litellm_patch.py
import litellm

# Save the original function
_original_completion = litellm.completion

def _sanitize_messages(messages):
    """Remove cache_breakpoint from every message object."""
    if not messages:
        return messages
    for msg in messages:
        if isinstance(msg, dict):
            msg.pop("cache_breakpoint", None)
    return messages

def _patched_completion(*args, **kwargs):
    # Strip cache_breakpoint from messages if present
    if "messages" in kwargs:
        kwargs["messages"] = _sanitize_messages(kwargs["messages"])
    return _original_completion(*args, **kwargs)

def apply_patch():
    """Monkey-patch litellm.completion to strip cache_breakpoint."""
    litellm.completion = _patched_completion
