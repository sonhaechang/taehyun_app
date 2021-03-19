from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import BaseResult

class SearchAccountList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('검색할 계정 목록')
        verbose_name_plural = _('검색할 계정 목록')

    def __str__(self):
        return f'{self.name}'


class SearchAccountResult(BaseResult):
    name = models.ForeignKey('accounts.SearchAccountList', on_delete=models.CASCADE)
    crawling_at = models.ForeignKey('accounts.CrawlingDate', on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('계정별 팔로워 검색 결과')
        verbose_name_plural = _('계정별 팔로워 검색 결과')

    def __str__(self):
        return f'{self.name.name}'