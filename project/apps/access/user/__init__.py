import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy_utils import PasswordType

from core.db import BaseModel
from core.server import db

DEFAULT_USER_SETTINGS = {
    'procedure_delay': 0,
    'timezone': '',
    'tray_notifications': True,
    'automatic_logout': 0,
    'clean_deleted': False,
    'clean_drafts': 14,
    'tips': True,
    'auto_answer': {  # ??
        'type': AutoAnswerTypeSetting.DISABLED.value,
    },
    'new_procedure': {
        'flashing_icon': True,
        'notify_overlay': True,
        'notify_sound': True,
        'notify_to_my_email': True,
        'notify_to_custom_emails': False,
        'notify_custom_emails': [],
    },
    'complete_procedure': {
        'flashing_icon': True,
        'notify_overlay': True,
        'notify_sound': True,
        'notify_to_my_email': True,
        'notify_to_custom_emails': False,
        'notify_custom_emails': [],
        'report_to_my_email': True,
        'report_to_custom_emails': False,
        'report_custom_emails': [],
    }
}


class AbstractUser(BaseModel):
    __abstract__ = True

    password = db.Column(
        PasswordType(),
        unique=False,
        nullable=False,)
    last_login = db.Column(DateTime, default=datetime.datetime.utcnow)

    is_active = db.Column(Boolean, default=False)

    _password = None

    def __str__(self):
        return self.get_username()

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'
