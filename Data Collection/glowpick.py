from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
import csv


# from selenium.webdriver.common.Keys import Keys

driver = webdriver.Chrome('./chromedriver')
# driver.get(
#     'https://www.glowpick.com/search/result?query=%EB%A6%BD%EC%8A%A4%ED%8B%B1')

driver.get(
    'https://www.glowpick.com/brand/list')
sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# driver.execute_script("window.scrollTo(0, 200)")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

# 스킨 (회사이름 스킨 들어가는거 삭제)
# https://www.glowpick.com/search/result?query=%EC%8A%A4%ED%82%A8
# https://www.glowpick.com/search/result?query=%ED%86%A0%EB%84%88

# 로션(4570)
# https://www.glowpick.com/search/result?query=%EB%A1%9C%EC%85%98

# 에센스
# https://www.glowpick.com/search/result?query=에센스

# 크림
# https://www.glowpick.com/search/result?query=%ED%81%AC%EB%A6%BC

SCROLL_PAUSE_TIME = 10

# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
# i = 0
# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page
#     sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#     print(i)
#     i += 1
times=0;
skin = [2, 3, 4, 5, 1, 7, 6, 210]
skin_name = ["스킨","로션","에센스","크림","미스트","메이크업픽서","페이스오일","토너/필링패드"]
color = [68, 48, 50, 49, 47, 69, 204,
         70, 142, 71, 72, 202, 203, 73, 189, 74]
color_name=["립스틱","립글로스/락커","립틴트","립밤","립라이너","아이라이너-펜슬&젤","아이라이너-리퀴드","마스카라","픽서/영양제","아이섀도우","아이브로우-펜슬","아이브로우-파우더","아이브로우-마스카라&리퀴드","하이라이터","쉐딩","블러셔"]
base = [67, 201, 200, 40, 43, 42, 136, 140, 44, 46, 192, 45]
base_name=["메이크업베이스","톤업크림","베이스프라이머","포인트프라이머","파운데이션","비비크림","씨씨크림","쿠션타입","컨실러","팩트","파우더","트윈케익"]

notices = soup.select('ul.brand-list__result__wrap li meta')
print(len(notices))
for n in notices:
    if('https://' in(n.get('content'))):
        a = n.get('content')
        for w in range(len(skin)):
            driver.get(a+"&main_category_id=1&sub_category_id="+str(skin[w]))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            notices_twp = soup.select('ul.list-wrap li div meta')
            if(notices_twp != 0):
                for z in notices_twp:
                    if('https://' in(z.get('content'))):
                        b = z.get('content')
                        driver.get(b)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        print("스킨케어")
                        print(skin_name[w])
                        times=times+1;
                        if(len(soup.select('div.product-detail__color-type-list')) != 0):
                            print(('색감 : '+soup.select('div.product-detail__color-type-list')[0].text).strip())
                        print(('상표 : '+soup.select('div.section-wrap p.product-main-info__brand_name')[0].text))

                        print('이름 : '+(soup.select('h1.product-main-info__product_name span.product-main-info__product_name__text')[0].text).replace("[단종]", "").strip())
                        img = soup.select('img.product-image__dump')
                        print('사진 : 'img[0]["src"])
                        #print('사진 : '+ img.get('src'))
                        data = soup.select('span.product-detail__tags')
                        for c in range(len(data)):
                            print('태그 : '+data[c].text)

print("---------------------------------------------------------------------------------------------------------------------------------")

for n in notices:
    if('https://' in(n.get('content'))):
        a = n.get('content')
        for w in range(len(color)):
            driver.get(a+"&main_category_id=1&sub_category_id="+str(color[w]))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            notices_twp = soup.select('ul.list-wrap li div meta')
            if(notices_twp != 0):
                for z in notices_twp:
                    if('https://' in(z.get('content'))):
                        b = z.get('content')
                        driver.get(b)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        print("색조")
                        print(color_name[w])
                        times=times+1;
                        if(len(soup.select('div.product-detail__color-type-list')) != 0):
                            print(
                                ('색감 : '+soup.select('div.product-detail__color-type-list')[0].text).strip())
                        print(
                            ('상표 : '+soup.select('div.section-wrap p.product-main-info__brand_name')[0].text))
                        print('이름 : '+(soup.select(
                            'h1.product-main-info__product_name span.product-main-info__product_name__text')[0].text).replace("[단종]", "").strip())
                        img = soup.select('img.product-image__dump')
                        print('사진 : 'img[0]["src"])

                        data = soup.select('span.product-detail__tags')
                        for c in range(len(data)):
                            print('태그 : '+data[c].text)

print("---------------------------------------------------------------------------------------------------------------------------------")

for n in notices:
    if('https://' in(n.get('content'))):
        a = n.get('content')
        for w in range(len(base)):
            driver.get(a+"&main_category_id=1&sub_category_id="+str(base[w]))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            notices_twp = soup.select('ul.list-wrap li div meta')
            if(notices_twp != 0):
                for z in notices_twp:
                    if('https://' in(z.get('content'))):
                        b = z.get('content')
                        driver.get(b)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        print("베이스")
                        print(base_name[w])
                        times=times+1;
                        if(len(soup.select('div.product-detail__color-type-list')) != 0):
                            print(
                                ('색감 : '+soup.select('div.product-detail__color-type-list')[0].text).strip())
                        print(
                            ('상표 : '+soup.select('div.section-wrap p.product-main-info__brand_name')[0].text))
                        print('이름 : '+(soup.select(
                            'h1.product-main-info__product_name span.product-main-info__product_name__text')[0].text).replace("[단종]", "").strip())
                        img = soup.select('img.product-image__dump')
                        print('사진 : 'img[0]["src"])
                        data = soup.select('span.product-detail__tags')
                        for c in range(len(data)):
                            print('태그 : '+data[c].text)
        # html = driver.page_source
        # soup = BeautifulSoup(html, 'html.parser')

        # print(
        #                     (soup.select('div.product-detail__color-type-list')[0].text).strip())

        # print(
        #     (soup.select('div.section-wrap p.product-main-info__brand_name')[0].text))
        # print((soup.select(
        #     'h1.product-main-info__product_name span.product-main-info__product_name__text')[0].text).replace("[단종]", "").strip())
        # print(
        #     (soup.select('div.product-detail__color-type-list')[0].text).strip())
        # data = soup.select('span.product-detail__tags')
        # for c in range(len(data)):
        #     print(data[c].text)
# notices = soup.select('div.side-info')

# notices = soup.select('div.list-item meta')
# print(len(notices))
# for n in notices:
#     if('https://' in(n.get('content'))):
#         a = n.get('content')
#         driver.get(a)
#         html = driver.page_source
#         soup = BeautifulSoup(html, 'html.parser')

#         print(
#             (soup.select('div.section-wrap p.product-main-info__brand_name')[0].text))
#         print((soup.select(
#             'h1.product-main-info__product_name span.product-main-info__product_name__text')[0].text).replace("[단종]", "").strip())
#         print(
#             (soup.select('div.product-detail__color-type-list')[0].text).strip())
#         data = soup.select('span.product-detail__tags')
#         for c in range(len(data)):
#             print(data[c].text)


print(times)
driver.close()
