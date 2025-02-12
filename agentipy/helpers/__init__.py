import asyncio
import platform


def fix_asyncio_for_windows():
    """
    Ensures proper asyncio event loop policy on Windows platforms.
    This is a fix for the 'aiodns needs a SelectorEventLoop on Windows' issue.
    """
    if platform.system() in ["Windows", "win32"]:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def validate_input (data:dict,schema:dict) -> None:
    """
    Validates the input against the schema.

    Schema format:{
    "field_name":{
        "type":type,
        "required":bool,
        "min_length":int,
        "min":int,
        "max":int,
        "choices":list ,# optional for enums
        }
    }
    """
    for field, rules in schema.items():
        # this will check for the required fields
        if rules.get("required", True) and field not in data:
            raise ValueError(f"Missing required field: {field}")
            
        if field in data:
            value = data[field]
            
            # Type checking
            if not isinstance(value, rules["type"]):
                raise ValueError(f"{field} must be of type {rules['type'].__name__}")
            
            # Length validation for strings/lists
            if rules.get("min_length") is not None and len(value) < rules["min_length"]:
                raise ValueError(f"{field} must have minimum length of {rules['min_length']}")
            
            # Range validation for numbers
            if isinstance(value, (int, float)):
                if rules.get("min") is not None and value < rules["min"]:
                    raise ValueError(f"{field} must be greater than {rules['min']}")
                if rules.get("max") is not None and value > rules["max"]:
                    raise ValueError(f"{field} must be less than {rules['max']}")
            
            # Choices validation
            if rules.get("choices") and value not in rules["choices"]:
                raise ValueError(f"{field} must be one of {rules['choices']}")
    
