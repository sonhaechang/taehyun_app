from django.contrib.auth.views import LogoutView
from django.urls import path
from accounts import views

urlpatterns = [
	path('login/', views.login, name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
	path('change/password', views.change_password, name='change_password'),
	path('edit/insta/accounts/', views.edit_insta_accounts_info, name='edit_insta_accounts_info'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('tag/list/', views.TagListView.as_view(), name='tag_list'),
	path('tag/delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
	path('tag/result/', views.tag_result, name='tag_result'),
	path('tag/crawling/', views.crawling_tag_list, name='crawling_tag_list'),
	path('account/list/', views.AccountListView.as_view(), name='account_list'),
	path('account/delete/<int:pk>/', views.AccountDeleteView.as_view(), name='account_delete'),
	path('account/follower/result/', views.account_follower_result, name='account_follower_result'),
	path('account/crawling/', views.crawling_account_list, name='crawling_account_list'),
	path('db/data/save/', views.db_data_save, name='db_data_save'),
]