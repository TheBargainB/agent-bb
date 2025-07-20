"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    # Handle model names that might not include provider prefix
    parts = fully_specified_name.split("/", maxsplit=1)
    
    if len(parts) == 2:
        # Normal case: "provider/model"
        provider, model = parts
    elif len(parts) == 1:
        # Fallback case: just "model" - assume openai as default provider
        model = parts[0]
        provider = "openai"
        print(f"Warning: Model name '{fully_specified_name}' doesn't include provider. Defaulting to '{provider}/{model}'")
    else:
        # Should never happen, but handle gracefully
        raise ValueError(f"Invalid model name format: '{fully_specified_name}'. Expected 'provider/model' or 'model'")
    
    return init_chat_model(model, model_provider=provider)
