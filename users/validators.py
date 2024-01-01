from django.core.exceptions import ValidationError
import re
import phonenumbers
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


def validate_email(value):
    """Validate email"""

    pattern = r"[\w-]{1,20}@gmail\.com"
    if not re.match(pattern, value):
        raise ValidationError(_("Enter a valid email address."), params={"value": value})


@deconstructible
class PhoneValidator:
    requires_context = False

    @staticmethod
    def clean(value):
        return re.sub('[^0-9+]+', '', value)

    @staticmethod
    def validate(value):
        try:
            z = phonenumbers.parse(value)  # 998944009080
            if not phonenumbers.is_valid_number(z):
                return False
        except:
            return False

        return True

    def __call__(self, value):
        if not PhoneValidator.validate(value):
            raise ValidationError(_("The value entered is not a phone number."))
