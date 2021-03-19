import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pyvirtualdisplay import Display 
from selenium import webdriver

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from accounts.models import (
	CrawlingDate,
	SearchTagList, SearchTagResult,
	SearchAccountList, SearchAccountResult,
)

User = get_user_model()

@transaction.atomic
def tag_crawling(request):
	today = datetime.now()

	# 태그 목록
	search_tag_list = SearchTagList.objects.filter(user=request.user)

	try:
		# 인스타 주소
		url = "https://www.instagram.com/accounts/login/?source=auth_switcher"

		# 크롬드라이버 파일위치(사용중인 크롬 버전과 다를시 에러 발생)
		# DRIVER_DIR = "/Users/sonhaechang/Django_Web_Programming/taehyun_app/chromedriver"

		# selenium으로 크롬창 띄우기
		driver = webdriver.Chrome(settings.DRIVER_PATH)
		driver.implicitly_wait(3) 
		driver.get(url)

		time.sleep(2)

		# 아이디 비밀번호 입력 코드
		driver.find_elements_by_name("username")[0].send_keys(request.user.instagram_id)
		driver.find_elements_by_name("password")[0].send_keys(request.user.instagram_pw)

		# 제출버튼 클릭 코드
		driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button").submit()

		time.sleep(2)

		#정보저장 알림창 저장안함으로 닫기 코드
		driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()

		time.sleep(2)

		# 알림설정 알림창 설정안함으로 닫기 코드
		driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()

		time.sleep(2)

		# 마지막 크롤링한 데이터 가져와서 리스트로 만들기 
		last_crawling = CrawlingDate.objects.filter(user=request.user, crawling_type='tags').first()
		last_date = []

		for tag in last_crawling.searchtagresult_set.all():
			last_date.append(tag)

		# 오늘 현제 크롤링 테이터 생성 
		today_crawling = CrawlingDate.objects.create(
			user=request.user, crawling_type='tags', created_at=timezone.now()
		)
		
		# 개시글 수 저장할 빈 리스트
		total_count_list = []
		
		# 태그 목록만큼 반복시키는 코드
		for idx, tag in enumerate(search_tag_list):
			
			# 검색창에 태그입력 코드
			search_input = driver.find_element_by_xpath(
				"""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input"""
			).send_keys(f'#{tag.name}')
			
			time.sleep(2)
			
			# 검색시 나오는 개시글 수 가져오기 코드
			total_count = driver.find_element_by_xpath(
				"/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div/div[2]/div[2]/div/span/span"
			).text
			
			# 콤마제거 후 정수로 받음
			total_count = int(total_count.replace(',','')) 

			# 비교값 계산 
			compare = int(total_count) - int(last_date[idx].count)

			# 개시글 수 db에 저장
			name = SearchTagList.objects.get(id=tag.id)
			SearchTagResult.objects.create(
				name=name, crawling_at=today_crawling,
				compare=compare, count=int(total_count),
				created_at=timezone.now()
			)
			
			time.sleep(2)
			
			# 검색창 내용 지우기 코드
			driver.find_element_by_class_name("coreSpriteSearchClear").click()
			
			time.sleep(2) 
		
		return('success')
		
	except Exception as e:	
		print(e)
		driver.quit()
		return('error')

	finally:
		driver.quit()

@transaction.atomic
def account_crawling(request):
	# 계정 목록
	accounts_list = SearchAccountList.objects.filter(user=request.user)

	try:
		# 인스타 주소
		url = "https://www.instagram.com/accounts/login/?source=auth_switcher"

		# 크롬드라이버 파일위치(사용중인 크롬 버전과 다를시 에러 발생)
		# DRIVER_DIR = "/Users/sonhaechang/Django_Web_Programming/taehyun_app/chromedriver"

		# selenium으로 크롬창 띄우기
		driver = webdriver.Chrome(settings.DRIVER_PATH)
		driver.implicitly_wait(3) 
		driver.get(url)

		time.sleep(2)

		# 아이디 비밀번호 입력 코드
		driver.find_elements_by_name("username")[0].send_keys(request.user.instagram_id)
		driver.find_elements_by_name("password")[0].send_keys(request.user.instagram_pw)

		# 제출버튼 클릭 코드
		driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button").submit()

		time.sleep(2)

		#정보저장 알림창 저장안함으로 닫기 코드
		driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()

		time.sleep(2)

		# 알림설정 알림창 설정안함으로 닫기 코드
		driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()

		time.sleep(2)

		# 마지막 크롤링한 데이터 가져와서 리스트로 만들기 
		last_crawling = CrawlingDate.objects.filter(user=request.user, crawling_type='accounts').first()
		last_date = []

		for tag in last_crawling.searchaccountresult_set.all():
			last_date.append(tag)	

		# 개시글 수 저장할 빈 리스트
		total_count_list = []

		# 오늘 현제 크롤링 테이터 생성 
		today_crawling = CrawlingDate.objects.create(
			user=request.user, crawling_type='accounts', created_at=timezone.now()
		)
		
		# 태그 목록만큼 반복시키는 코드
		for idx, account in enumerate(accounts_list):

			# 검색창에 태그입력 코드
			search_input = driver.find_element_by_xpath(
				"""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input"""
			).send_keys(f'@{account.name}')
			
			time.sleep(2)

			# 검색창에 검색하는 코드
			driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a").click()

			time.sleep(2)

			# 팔로워 수 가져오기 코드
			total_count = driver.find_elements_by_class_name("g47SY")[1].text 
        
			if total_count[-1] == '천':
				value = int(total_count[:-1].replace('.', ''))
				value = str(value) + '000'
				total_count = int(value)
			elif total_count[-1] == '만':
				value = int(total_count[:-1].replace('.', ''))
				value = str(value) + '0000'
				total_count = int(value)
			else:
				# 콤마제거 후 정수로 받음
				total_count = int(total_count.replace(',', '')) 

			# 비교값 계산 
			compare = int(total_count) - int(last_date[idx].count)

			# 팔로워 수 db에 저장
			SearchAccountResult.objects.create(
				name=account, crawling_at=today_crawling,
				compare=compare, count=int(total_count),
				created_at=timezone.now()
			)

			time.sleep(2)

		return('success')
			
		
	except Exception as e:
		print(e)
		driver.quit()
		return('error')	

	finally:
		driver.quit()