from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import re

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

        # 결과 확인
        for j in range(len(product_color_values)):
            print(product_names[i] + '\n' + product_color_names[j] + '\n' + product_color_values[j] + '\n')