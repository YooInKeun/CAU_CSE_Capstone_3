from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import re
from urllib import parse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *

urls = []

# 페이스/파운데이션
urls.append("https://www.bobbibrown.co.kr/products/14017/")

# 페이스/쿠션
urls.append("https://www.bobbibrown.co.kr/products/21888/")

# 페이스/프라이머
urls.append("https://www.bobbibrown.co.kr/products/22322/")

# 페이스/코렉터&컨실러
urls.append("https://www.bobbibrown.co.kr/products/14018/")

# 페이스/파우더
urls.append("https://www.bobbibrown.co.kr/products/14019/")

# 페이스/브러쉬&툴
urls.append("https://www.bobbibrown.co.kr/products/13995/")

# 립/립스틱
urls.append("https://www.bobbibrown.co.kr/products/2342/")

# 립/립케어
urls.append("https://www.bobbibrown.co.kr/products/2341/")

# 립/립글로스
urls.append("https://www.bobbibrown.co.kr/products/2340/")

# 립/립라이너
urls.append("https://www.bobbibrown.co.kr/products/2343/")

# 아이/아이섀도우
urls.append("https://www.bobbibrown.co.kr/products/2330/")

# 아이/아이라이너
urls.append("https://www.bobbibrown.co.kr/products/2328/")

# 아이/마스카라
urls.append("https://www.bobbibrown.co.kr/products/2332/")

# 아이/브라우
urls.append("https://www.bobbibrown.co.kr/products/2327/")

# 아이/브러쉬&툴
urls.append("https://www.bobbibrown.co.kr/products/13995/")

# 치크/블러쉬
urls.append("https://www.bobbibrown.co.kr/products/14021/")

# 치크/하이라이터
urls.append("https://www.bobbibrown.co.kr/products/14022/")

# 스킨케어/모이스춰라이저
urls.append("https://www.bobbibrown.co.kr/products/14007/")

# 스킨케어/아이케어
urls.append("https://www.bobbibrown.co.kr/products/14008/")

# 스킨케어/썬케어
urls.append("https://www.bobbibrown.co.kr/products/19142/")

# 스킨케어/클렌저&토너
urls.append("https://www.bobbibrown.co.kr/products/14013/")

# 스킨케어/마스크
urls.append("https://www.bobbibrown.co.kr/products/16155/")

# 스킨케어/메이크업리무버
urls.append("https://www.bobbibrown.co.kr/products/14011/")

cnt=0
for url in urls:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    main_html = urlopen(req).read()
    soup = BeautifulSoup(main_html, "html.parser")

    raws = soup.find_all("h4", {"class": "product-brief__short-desc"})
    product_additional_url = []
    product_names = []
    for raw in raws:
        j1 = str(raw).split('href=\"')
        j2 = j1[1]
        j3 = j2.split('\"')
        j4 = j3[0]
        product_additional_url.append(j4)
    
    for i in range(len(product_additional_url)):
        product_color_names = []
        product_color_values = []
        product_images = []

        product_url = 'https://www.bobbibrown.co.kr' + product_additional_url[i]
        req = Request(product_url, headers={'User-Agent': 'Mozilla/5.0'})
        main_html = urlopen(req).read()
        soup = BeautifulSoup(main_html, "html.parser")
        product_names.append(str(soup.find("div", {"class": "sticky-add-to-bag__name"}).text))

        product_color_name_tags = soup.findAll("span", {"class": "js-shade-select-label shade-picker__shade-item--label"})
        if product_color_name_tags:
            for tag_content in product_color_name_tags:
                product_color_names.append(tag_content.text)
        elif not product_color_name_tags:
            product_color_names.append("None")

        for j in range(len(product_color_names)):
            blank_pattern = re.compile(r'\s+')
            product_color_names[j] = re.sub(blank_pattern, '', product_color_names[j])
        product_color_names = product_color_names[int(len(product_color_names)/2):len(product_color_names)]

        product_color_value_tags = soup.findAll("div", {"class": "product-full-shades__shade-swatch"})
        if product_color_value_tags:
            for tag_content in product_color_value_tags:
                str_tag_content = str(tag_content)
                sharp_pos = str_tag_content.find("#")
                product_color_values.append(str_tag_content[sharp_pos:sharp_pos+7])
        elif not product_color_value_tags:
            product_color_values.append("None")

        for product_color_name in product_color_names:
            try:
                product_color_name = parse.quote(product_color_name)
                product_url = 'https://www.bobbibrown.co.kr' + product_additional_url[i] + '#/shade' + '/' + product_color_name
                req = Request(product_url, headers={'User-Agent': 'Mozilla/5.0'})
                main_html = urlopen(req).read()
                soup = BeautifulSoup(main_html, "html.parser")
                product_image = str(soup.find("img", {"class": "product-full-image__photo--thumb"}))
                src_pos = product_image.find('src')
                jpg_pos = product_image.find('jpg')
                product_image = product_image[src_pos+5:jpg_pos+3]
                product_images.append('https://www.bobbibrown.co.kr' + product_image)
                # print(product_url)
                # print(product_images)
            except:
                product_images.append("None")

        # 결과 확인
        for j in range(len(product_color_values)):
            cnt +=1
            try:
                stripped_product_name = product_names[i].strip()
                stripped_product_color_name = product_color_names[j].strip()
                print(Cosmetic.objects.get(product=Product.objects.get(brand=Brand.objects.get(brand_name="바비 브라운"), product_name=stripped_product_name),
                                           type_name=stripped_product_color_name))
                print("이미 존재하는 제품입니다.")
            except:
                try:
                    stripped_product_name = product_names[i].strip()
                    stripped_product_color_name = product_color_names[j].strip()
                    stripped_product_color_value = product_color_values[j].strip()
                    stripped_product_image = product_images[j].strip()
                    cosmetic = Cosmetic(product = Product.objects.get(brand=Brand.objects.get(brand_name="바비 브라운"), product_name=stripped_product_name),
                                        type_name = stripped_product_color_name,
                                        rgb_value = stripped_product_color_value, 
                                        image_link = stripped_product_image)
                    cosmetic.save()
                except:
                    print(stripped_product_name)
                    print("Error")
print(cnt)