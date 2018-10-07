__all__ = ['ValidationError', 'FieldValidationError', 'FieldsetValidationError',
           'FormValidationError']


class ValidationError(ValueError):
    pass


class FieldValidationError(ValidationError):
    pass


class FieldsetValidationError(ValidationError):
    pass


class FormValidationError(ValidationError):
    pass
