from django.core.validators import RegexValidator
from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        return super().normalize_email(email).lower()

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Super user must have is_staff=True."))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Super user must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    STAFF = 'STAFF'
    ADMIN = 'ADMIN'
    SUPER_ADMIN = 'SUPER ADMIN'
    CUSTOMER = 'CUSTOMER'

    ROLES = (
        (STAFF, STAFF),
        (ADMIN, ADMIN),
        (SUPER_ADMIN, SUPER_ADMIN),
        (CUSTOMER, CUSTOMER)
    )

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')

    username = models.CharField(_('User Name'), default='', max_length=150, validators=[alphanumeric])
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=125, blank=True, default='', validators=[alphanumeric])
    last_name = models.CharField(_('last name'), max_length=125, blank=True, default='', validators=[alphanumeric])
    phone = models.CharField(_('Phone number'), max_length=20, blank=True, default='', validators=[alphanumeric])
    is_staff = models.BooleanField(_('Staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin site.')
                                   )
    is_active = models.BooleanField(_('Active'),
                                    default=True,
                                    help_text=_('Designates whether this user should be treated as active. \
                                                    Unselect this instead of deleting accounts.'
                                                ), )
    is_superuser = models.BooleanField(_('Super staff status'),
                                       default=False,
                                       help_text='Grants the all system privileges to the user'
                                       )

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    role = models.CharField(_("User role"), max_length=20, choices=ROLES, default='')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'password']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['date_joined']

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        """
            Returns the first_name + the last_name, with a space in between.
        """
        fullname = f'{self.first_name} {self.last_name}'
        return fullname.strip()

    def get_email(self):
        """Returns user's email"""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sending email to this user"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_user_admin(self):
        user = Group.objects.get(name=self.ADMIN)
        return user in self.groups.all()

    def is_super_admin(self):
        user = Group.objects.get(name=self.SUPER_ADMIN)
        return user in self.groups.all()

    def user_roles(self):
        if self.is_user_admin:
            return _(self.ADMIN)
        if self.is_super_admin:
            return _(self.SUPER_ADMIN)
        if self.is_staff:
            return _(self.STAFF)
