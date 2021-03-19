from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    instagram_id = models.CharField(
        max_length=60, 
        verbose_name=_('인스타그램 아이디'),
        help_text=_('인스타그램 아이디를 입력해주세요.')
    )
    instagram_pw = models.CharField(
        max_length=60, 
        verbose_name=_('인스타그램 비밀번호'),
        help_text=_('인스타그램 비밀번호를 입력해주세요.')
    )

    class Meta:
        db_table = 'users_tb'
        verbose_name = _('사용자')
        verbose_name_plural = _('사용자')

    def __str__(self):
        return f'{self.username}'


class CrawlingDate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crawling_type = models.CharField(
        verbose_name=_('크롤링 유형'),
        max_length=10,
        choices=(
            ('tags', '태그'),
            ('accounts', '계정')
        ),
    )
    created_at = models.DateTimeField(verbose_name= _('크롤링한 날짜'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('크롤링한 날짜')
        verbose_name_plural = _('크롤링한 날짜')

    def __str__(self):
        return f'{self.user}'


class BaseResult(models.Model):
    count = models.IntegerField(default=0)
    compare = models.IntegerField(default=0)
    created_at = models.DateTimeField(verbose_name= _('생성일'))
   