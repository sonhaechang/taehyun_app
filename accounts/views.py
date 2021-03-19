from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    login as django_login, get_user_model,
	update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.forms import (
	LoginForm, SignupForm, 
	PasswordChangeForm, EditInstaAccountsInfoForm,
	SearchAccountForm, SearchTagForm,
)

from accounts.models import (
	CrawlingDate,
	SearchTagList, SearchTagResult,
	SearchAccountList, SearchAccountResult,
)

from accounts.serializers import TagListSerializer, AccountListSerializer

from accounts import sample
from accounts.crawling import tag_crawling, account_crawling
from accounts.utility_function import (
	page_range_pagination, bulk_create_tag_results, bulk_create_account_results
)

User = get_user_model()

# Create your views here.
def login(request):
	if request.method == 'POST':
		form = LoginForm(request=request, data=request.POST)

		if form.is_valid():
			user = form.get_user()
			django_login(request, user)
			messages.success(request, f'환영합니다. {user.username}님')
			return redirect('/')
	else:
		form = LoginForm()

	return render(request, 'accounts/login.html', {'form': form})

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, '성곡적으로 가입되었습니다. 로그인해주세요.')
			return redirect(settings.LOGIN_URL)
	else:
		form = SignupForm()

	return render(request, 'accounts/signup.html', {'form': form,})

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, '비밀번호가 변경되었습니다.')
			return JsonResponse(data={'redirect_url': reverse_lazy('dashboard')})
		else:
			errMsg = form.errors.get_json_data()
			data = {'errors': errMsg,}
			return JsonResponse(data)

@login_required
def edit_insta_accounts_info(request):
	if request.method == 'POST':
		form = EditInstaAccountsInfoForm(request.POST, instance=request.user)
		
		if form.is_valid():
			form.save()
			messages.success(request, '인스타그램 계정정보가 수정되었습니다.')
			return JsonResponse(data={'redirect_url': reverse_lazy('dashboard')})
		else:
			errMsg = form.errors.get_json_data()
			data = {'errors': errMsg,}
			return JsonResponse(data)

@login_required
def dashboard(request):
	change_password_form = PasswordChangeForm(request.user, request.POST)
	edit_insta_accounts_info_form = EditInstaAccountsInfoForm(request.POST)
	search_account_form = SearchAccountForm(request.POST)
	tag_list = SearchTagList.objects.all()
	account_list = SearchAccountList.objects.all()

	return render(request, 'accounts/dashboard.html', {
		'change_password_form': change_password_form,
		'edit_insta_accounts_info_form': edit_insta_accounts_info_form,
		'tag_list': tag_list,
		'account_list': account_list,
	})


class TagListView(APIView):
	def get(self, request):
		qs = SearchTagList.objects.filter(user=request.user)
		serializer = TagListSerializer(qs, many=True)
		return Response(serializer.data, status=201)

	@transaction.atomic
	def post(self, request):
		serializer = TagListSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(user=request.user)

			bulk_create_tag_results(request, serializer.data['id'])

			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)


class TagDeleteView(APIView):
	def delete(self, request, pk):
		qs = get_object_or_404(SearchTagList, pk=pk)
		qs.delete()
		return Response(status=204)


@login_required
def tag_result(request):
	tag_list = SearchTagList.objects.filter(user=request.user)
	crawling_date = CrawlingDate.objects.filter(user=request.user, crawling_type='tags')

	page = request.GET.get('page', 1)
	context = page_range_pagination(crawling_date, page, 20)
	crawling_date = context.pop('qs')
	page_range = context.pop('page_range')

	return render(request, 'accounts/tag_reslut.html', {
		'tag_list': tag_list,
		'crawling_date': crawling_date,
		'page_range': page_range
	})

@login_required
@transaction.atomic
def crawling_tag_list(request):
	crawling = tag_crawling(request)

	if crawling == 'success':
		messages.success(request, '크롤링을 성공적으로 완료하였습니다.')
		return JsonResponse(data={'success': 'success'})

	else:
		messages.error(request, '예기치 못한 문제발생, 다시 시도해주세요.')
		return JsonResponse(data={'error': 'error'})


class AccountListView(APIView):
	def get(self, request):
		qs = SearchAccountList.objects.filter(user=request.user)
		serializer = AccountListSerializer(qs, many=True)
		return Response(serializer.data, status=201)

	@transaction.atomic
	def post(self, request):
		serializer = AccountListSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(user=request.user)

			bulk_create_account_results(request, serializer.data['id'])

			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)


class AccountDeleteView(APIView):
	def delete(self, request, pk):
		qs = get_object_or_404(SearchAccountList, pk=pk)
		qs.delete()
		return Response(status=204)


@login_required
def account_follower_result(request):
	account_list = SearchAccountList.objects.filter(user=request.user)
	crawling_date = CrawlingDate.objects.filter(
		user=request.user, crawling_type='accounts'
	)

	page = request.GET.get('page', 1)
	context = page_range_pagination(crawling_date, page, 20)
	crawling_date = context.pop('qs')
	page_range = context.pop('page_range')

	return render(request, 'accounts/account_follower_reslut.html', {
		'account_list': account_list,
		'crawling_date': crawling_date,
		'page_range': page_range
	})

@login_required
@transaction.atomic
def crawling_account_list(request):
	crawling = account_crawling(request)

	if crawling == 'success':
		messages.success(request, '크롤링을 성공적으로 완료하였습니다.')
		return JsonResponse(data={'success': 'success'})

	else:
		messages.error(request, '예기치 못한 문제발생, 다시 시도해주세요.')
		return JsonResponse(data={'error': 'error'})

@login_required
@transaction.atomic
def db_data_save(request):
	tag_list = SearchTagList.objects.all()
	tag_result = SearchTagResult.objects.all()
	account_list = SearchAccountList.objects.all()
	accounts_result = SearchAccountResult.objects.all()

	if len(tag_list) == 0:
		sample.get_and_create_tags()
	if len(tag_result) == 0:
		sample.get_and_create_accounts()
	if len(tag_result) == 0:
		sample.save_tag_result()
	if len(accounts_result) == 0:
		sample.save_account_result()

	return JsonResponse(data={}, status=200)