from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
import uuid
from .validators import validate_email, PhoneValidator


class BaseUserManager(DjangoBaseUserManager):
    """
    Define a model manager for User model with no username field.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_("The given email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class CustomUserModel(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(_("email address"), unique=True,
                              help_text=_("Required. Your gmail address."),
                              error_messages={"unique": _("A user with that email already exists")},
                              validators=[validate_email])

    phone_number = models.CharField(max_length=15, blank=True, null=True,
                                    unique=True, help_text=_('Enter phone number'
                                                             ' e.g: +998123456789'),
                                    verbose_name='phone number',
                                    error_messages={'unique': _('A user with that phone number already exists'),
                                                    'invalid': _('Please enter a valid phone')},
                                    validators=[PhoneValidator()])

    CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    site_ranking = models.PositiveSmallIntegerField(choices=CHOICES, null=True, blank=True)

    password = models.CharField(max_length=100, validators=[validate_password])
    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ()

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        db_table = 'users'
        verbose_name = "user"
        verbose_name_plural = "users"


class ClientDetails(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='client_details')
    first_name = models.CharField(max_length=100, verbose_name='first name', help_text=_('your first name'))
    last_name = models.CharField(max_length=100, verbose_name='last name', help_text=_('your last name'))
    region = models.CharField(max_length=100, verbose_name='region', help_text=_('region'))
    city = models.CharField(max_length=100, verbose_name='city', help_text=_('city'))
    street = models.TextField(verbose_name='street', help_text=_('street'))
    flat_number = models.IntegerField(null=True, blank=True, verbose_name='flat number', help_text=_('flat number'))

    def __str__(self):
        return f'client: {self.first_name} {self.last_name}'

    class Meta:
        db_table = 'client_details'
        verbose_name = "client detail"
        verbose_name_plural = "client details"
