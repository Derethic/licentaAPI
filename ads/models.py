import os
import time
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class UserAdManager(models.Manager):

    def get_queryset(self, user_id):
        return super(UserAdManager, self).get_query_set().filter(user=user_id)


class User(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(_('email address'), max_length=254, unique=True)
        first_name = models.CharField(_('first name'), max_length=30, blank=True)
        last_name = models.CharField(_('last name'), max_length=30, blank=True)
        is_staff = models.BooleanField(_('staff status'), default=False,
                                       help_text=_('Designates whether the user can log into this admin '
                                                   'site.'))
        is_active = models.BooleanField(_('active'), default=True,
                                        help_text=_('Designates whether this user should be treated as '
                                                    'active. Unselect this instead of deleting accounts.'))

        location = models.CharField(max_length=50)
        phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                     message="Phone number must be entered in the format: '+999999999'."
                                             " Up to 15 digits allowed.")
        phone_number = models.CharField(validators=[phone_regex], max_length=15)
        date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
        last_login = models.DateTimeField(_('date joined'), default=timezone.now)

        USERNAME_FIELD = 'email'

        REQUIRED_FIELDS = ['first_name', 'last_name', 'location', 'phone_number']

        objects = MyUserManager()

        def __str__(self):
            return self.first_name + ' ; ' + self.last_name + ' ; ' + self.phone_number

        class Meta:
            verbose_name = _('user')
            verbose_name_plural = _('users')

        def get_absolute_url(self):
            return "/users/%s/" % urlquote(self.email)

        def get_full_name(self):
            """
            Returns the first_name plus the last_name, with a space in between.
            """
            full_name = '%s %s' % (self.first_name, self.last_name)
            return full_name.strip()

        def get_short_name(self):
            "Returns the short name for the user."
            return self.first_name

        def email_user(self, subject, message, from_email=None):
            """
            Sends an email to this User.
            """
            send_mail(subject, message, from_email, [self.email])


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Message(models.Model):
    message_sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name="%(app_label)s_%(class)s_senders")
    message_receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name="%(app_label)s_%(class)s_receivers")
    content = models.CharField(max_length=3000)
    read_time = models.DateTimeField(blank=True, null=True)
    message_created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.content


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subcategory_name


class MCateg(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return str(self.category.category_name) + ' -> ' + str(self.subcategory.subcategory_name)


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        currentTime = time.strftime("%Y%m%d-%H%M%S")

        filename = '{}.{}'.format(currentTime + "_" + uuid4().hex, ext)

        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class Ad(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(max_length=15)
    currency = models.CharField(max_length=10)
    condition = models.CharField(max_length=10)
    description = models.CharField(max_length=3000)
    view_count = models.IntegerField(blank=True, default=0, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mapcategory = models.ForeignKey(MCateg, on_delete=models.CASCADE)
    picture1 = models.ImageField(
        upload_to=UploadToPathAndRename('pictures'),
        default='',
        null=True,
        blank=True,
        editable=True,
        help_text="Ad Pictures",
        verbose_name="Ad Pictures")
    picture2 = models.ImageField(
        upload_to=UploadToPathAndRename('pictures'),
        default='',
        null=True,
        blank=True,
        editable=True,
        help_text="Ad Pictures",
        verbose_name="Ad Pictures")
    picture3 = models.ImageField(
        upload_to=UploadToPathAndRename('pictures'),
        default='',
        null=True,
        blank=True,
        editable=True,
        help_text="Ad Pictures",
        verbose_name="Ad Pictures")
    picture4 = models.ImageField(
        upload_to=UploadToPathAndRename('pictures'),
        default='',
        null=True,
        blank=True,
        editable=True,
        help_text="Ad Pictures",
        verbose_name="Ad Pictures")
    ad_created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.title + ' ; ' + str(self.price) + ' ' + self.currency + ' ; ' \
               + ' ; ' + str(self.ad_created_at)
