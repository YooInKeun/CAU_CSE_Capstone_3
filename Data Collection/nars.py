from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

# 페이스/파운데이션
url = "https://www.narscosmetics.co.kr/ko/foundation"
main_html = urlopen(url)
soup = BeautifulSoup(main_html, "html.parser")

raw = soup.find_all('script')
json_raw = str(raw[14])
j1 = json_raw.split('var productData = ')
j2 = j1[1]
j3 = j2.split('var searchItems =')
j4 = j3[0]
j5 = j4[0:len(j4)-2]
j6 = json.loads(j5)

foundation_info = j6['product']
foundation_id = []

for i in range(len(foundation_info)):
    foundation_id.append(foundation_info[i]['id'])

for i in range(len(foundation_id)):
    product_url = "https://www.narscosmetics.co.kr/ko/natural-radiant-longwear-cushion-foundation-spf50/" + \
                    str(foundation_id[i]) + ".html"
    product_html = urlopen(product_url)
    soup = BeautifulSoup(product_html, "html.parser")

    product_name = soup.find("h1", {"id": "products-name"}).text

    product_color_name_tags = soup.findAll("img", {"class": "hide"})
    product_color_names = []

    for tag_content in product_color_name_tags:
        str_tag_content = str(tag_content)
        alt_pos = str_tag_content.find("alt")
        class_pos = str_tag_content.find("class")
        print(product_name + str_tag_content[alt_pos+5:class_pos-2])