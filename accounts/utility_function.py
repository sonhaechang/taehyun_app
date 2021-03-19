from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import (
	CrawlingDate, 
	SearchTagList, SearchAccountList, 
	SearchTagResult, SearchAccountResult
)

def page_range_pagination(qs, page, num):
    paginator = Paginator(qs, int(num))

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = None

    page_numbers_range = 5  # Display only 5 page numbers
    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
        end_index = max_index

    page_range = paginator.page_range[start_index:end_index]

    context = {
        'qs': qs,
        'page_range': page_range
    }

    return context

def bulk_create_tag_results(request, id):
	name = SearchTagList.objects.get(id=id)
	crawling_date = CrawlingDate.objects.filter(user=request.user, crawling_type='tags')
	tag_result_list = []

	if crawling_date is not None:
		for date in crawling_date:
			SearchTagResult.objects.create(
				name=name, crawling_at=date,
				count=0, compare=0, created_at=date.created_at
			)

def bulk_create_account_results(request, id):
	name = SearchAccountList.objects.get(id=id)
	crawling_date = CrawlingDate.objects.filter(user=request.user, crawling_type='accounts')
	account_result_list = []

	if crawling_date is not None:
		for date in crawling_date:
			SearchAccountResult.objects.create(
				name=name, crawling_at=date, 
				count=0, compare=0, created_at=date.created_at
			)