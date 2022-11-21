from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """ユーザマネージャー"""
    use_in_migrations = True

    def _create_user(self, username, email, nickname, password, **extra_fields):
        """
        ユーザ名，メールアドレス，パスワードからユーザを作成して保存する．
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not nickname:
            raise ValueError('The given nickname must be set')

        user = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            nickname=nickname,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザモデル"""
    """
    ユーザ名，メールアドレス，ニックネーム，パスワードは必須．その他のフィールドはオプション．
    ユーザ名，メールアドレスはユニークでなければならない．
    """
    username = models.CharField(
        verbose_name=_('username'),
        max_length=25,
        unique=True,
        validators=[MinLengthValidator(6), UnicodeUsernameValidator()],
        help_text=_('Required. 6~25 characters. Letters, digits and @/./+/-/_ only.')
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True,
    )
    nickname = models.CharField(
        verbose_name=_('nickname'),
        max_length=25,
        blank=False,
        null=False,
    )
    image = models.ImageField(
        verbose_name=_('profile image'),
        blank=True,
        null=True,
    )
    introduction = models.TextField(
        verbose_name=_('introduction'),
        blank=True,
        null=True
    )
    url = models.URLField(
        verbose_name=_('url'),
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
        help_text=_(
           'Designates whether this user should be treated as active. '
           'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        verbose_name=_('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD = ['email', 'nickname']

    class Meta:
        verbose_name = _('ユーザ')
        verbose_name_plural = _('ユーザ群')


