from enum import Enum

class EInputFieldContentType(str, Enum):
    Standard = "Standard"
    Autocorrected = "Autocorrected"
    IntegerNumber = "IntegerNumber"
    DecimalNumber = "DecimalNumber"
    Alphanumeric = "Alphanumeric"
    Name = "Name"
    EmailAddress = "EmailAddress"
    Password = "Password"
    Pin = "Pin"
    Custom = "Custom"
