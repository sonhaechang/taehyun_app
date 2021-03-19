from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import BaseResult

class SearchTagList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('검색할 태그 목록')
        verbose_name_plural = _('검색할 태그 목록')

    def __str__(self):
        return f'{self.name}'


class SearchTagResult(BaseResult):
    name = models.ForeignKey('accounts.SearchTagList', on_delete=models.CASCADE)
    crawling_at = models.ForeignKey('accounts.CrawlingDate', on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('태그 검색 결과')
        verbose_name_plural = _('태그 검색 결과')

    def __str__(self):
        return f'{self.name.name}'