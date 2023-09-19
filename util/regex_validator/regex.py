from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
charValidator = RegexValidator(r'^[a-zA-Z]*$', message='Invalid characters provided .')
numericValidator = RegexValidator(r'^[0-9]*$', message='Invalid characters, numeric characters are allowed .')