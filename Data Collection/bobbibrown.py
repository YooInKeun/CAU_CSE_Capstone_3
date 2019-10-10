from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import re

urls = []

# 페이스/파운데이션
urls.append("https://www.bobbibrown.co.kr/products/14017/")

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