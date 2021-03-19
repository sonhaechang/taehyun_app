from django.contrib import admin
from accounts.models import (
	User, CrawlingDate,
	SearchAccountList, SearchAccountResult,
	SearchTagList, SearchTagResult,
)

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']

@admin.register(CrawlingDate)
class CrawlingDateAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'crawling_type', 'created_at']

@admin.register(SearchAccountList)
class SearchAccountListAdmin(admin.ModelAdmin):
	pass


@admin.register(SearchAccountResult)
class SearchAccountResultAdmin(admin.ModelAdmin):
	pass


@admin.register(SearchTagList)
class SearchTagListAdmin(admin.ModelAdmin):
	pass


@admin.register(SearchTagResult)
class SearchTagResultAdmin(admin.ModelAdmin):
	list_display = ['name', 'created_at']