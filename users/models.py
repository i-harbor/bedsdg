from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    """
    自定义用户模型
    """
    telephone = models.CharField(verbose_name=_('电话'), max_length=11, blank=True, default='')
    company = models.CharField(verbose_name=_('公司/单位'), max_length=255, blank=True, default='')

    def get_full_name(self):
        if self.last_name.encode('UTF-8').isalpha() and self.first_name.encode('UTF-8').isalpha():
            return f'{self.first_name} {self.last_name}'

        return f'{self.last_name}{self.first_name}'
