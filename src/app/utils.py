from enum import Enum
from datetime import datetime
from app.errors import ValidationError

DATE_FORMAT = "%d/%m/%Y"

class utils:
    def validate_request_json(request_json, required_fields, missing_message=""):
        if not request_json:
            raise ValidationError("Request body must be JSON")

        missing = [f for f in required_fields if f not in request_json]
        if missing_message != "": 
            missing_message = " " + missing_message
        if missing:
            raise ValidationError(f"Missing fields{missing_message}: {', '.join(missing)}")


    def validate_string_to_enum(enum_class: type[Enum], value, field_name: str = "value"):
        try:
            return enum_class(value)
        except ValueError:
            valid = [e.value for e in enum_class]
            raise ValidationError(f"Invalid {field_name}. Must be one of: {valid}")

    def validate_date_string(value, field_name: str = "date"):
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string in dd/MM/yyyy format")
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValidationError(f"Invalid {field_name}. Must be a real date in dd/MM/yyyy format")