from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *

urls = []
# 페이스/파운데이션
urls.append("https://www.narscosmetics.co.kr/ko/foundation")

# 페이스/컨실러
urls.append("https://www.narscosmetics.co.kr/ko/concealers")

# 페이스/프라이머
urls.append("https://www.narscosmetics.co.kr/ko/primers")

# 페이스/파우더
urls.append("https://www.narscosmetics.co.kr/ko/powders")

# 치크/블러쉬
urls.append("https://www.narscosmetics.co.kr/ko/blush")

# 치크/하이라이터
urls.append("https://www.narscosmetics.co.kr/ko/highlighter")

# 치크/브론저
urls.append("https://www.narscosmetics.co.kr/ko/bronzer")

# 치크/멀티유즈
urls.append("https://www.narscosmetics.co.kr/ko/cheeks-multi-use")

# 립/립스틱
urls.append("https://www.narscosmetics.co.kr/ko/lipstick")

# 립/리퀴드 립스틱
urls.append("https://www.narscosmetics.co.kr/ko/liquid-lipstick")

# 립/글로스
urls.append("https://www.narscosmetics.co.kr/ko/lip-gloss")

# 립/펜슬
urls.append("https://www.narscosmetics.co.kr/ko/lip-pencils")

# 아이/아이섀도우
urls.append("https://www.narscosmetics.co.kr/ko/eyeshadow")

# 아이/아이라이너
urls.append("https://www.narscosmetics.co.kr/ko/eyeliners")

# 아이/마스카라
urls.append("https://www.narscosmetics.co.kr/ko/mascara")

# 아이/브로우
urls.append("https://www.narscosmetics.co.kr/ko/brow")

# 아이/아이팔레트
urls.append("https://www.narscosmetics.co.kr/ko/palettes-eye-palettes")

# 팔레트&기프트/치크팔레트
urls.append("https://www.narscosmetics.co.kr/ko/palettes-cheek-palettes")

# 팔레트&기프트/아이팔레트
urls.append("https://www.narscosmetics.co.kr/ko/palettes-eye-palettes")

# 멀티유즈/멀티플
urls.append("https://www.narscosmetics.co.kr/ko/multiple")

cnt = 0
for url in urls:
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
    product_names = []
    product_color_names = []
    product_color_values = []
    product_images = []

    for i in range(len(foundation_info)):
        foundation_id.append(foundation_info[i]['id'])

    foundation_id = set(foundation_id)
    foundation_id = list(foundation_id)

    for i in range(len(foundation_id)):
        product_url = "https://www.narscosmetics.co.kr/ko/natural-radiant-longwear-cushion-foundation-spf50/" + \
                        str(foundation_id[i]) + ".html"
        product_html = urlopen(product_url)
        soup = BeautifulSoup(product_html, "html.parser")
        if soup.find("h1", {"id": "products-name"}) is not None:
            product_names.append(soup.find("h1", {"id": "products-name"}).text)

        product_color_name_tags = soup.findAll("img", {"class": "hide"})

        for tag_content in product_color_name_tags:
            str_tag_content = str(tag_content)
            alt_pos = str_tag_content.find("alt")
            class_pos = str_tag_content.find("class")
            product_color_names.append(str_tag_content[alt_pos+5:class_pos-2])

        product_color_value_tags = soup.findAll("div", {"class": "swatch-block"})
        
        for tag_content in product_color_value_tags:
            str_tag_content = str(tag_content)
            sharp_pos = str_tag_content.find("#")
            product_color_values.append(str_tag_content[sharp_pos:sharp_pos+7])

        product_image_tags = soup.findAll("a", {"class": "swatchanchor"})

        for tag_content in product_image_tags:
            str_tag_content = str(tag_content)
            url_pos = str_tag_content.find("url")
            title_pos = str_tag_content.find("title")
            product_images.append(str_tag_content[url_pos+6:title_pos-3])

    # DB Insert
    for i in range(len(product_names)):
        for j in range(len(product_color_names)):
            cnt +=1
            try:
                stripped_product_name = product_names[i].strip()
                stripped_product_color_name = product_color_names[j].strip()
                print(Cosmetic.objects.get(product=Product.objects.get(brand=Brand.objects.get(brand_name="나스 (NARS)"), product_name=stripped_product_name),
                                           type_name=stripped_product_color_name))
                print("이미 존재하는 제품입니다.")
            except:
                try:
                    stripped_product_name = product_names[i].strip()
                    stripped_product_color_name = product_color_names[j].strip()
                    stripped_product_color_value = product_color_values[j].strip()
                    stripped_product_image = product_images[j].strip()
                    cosmetic = Cosmetic(product = Product.objects.get(brand=Brand.objects.get(brand_name="나스 (NARS)"), product_name=stripped_product_name),
                                        type_name = stripped_product_color_name,
                                        rgb_value = stripped_product_color_value, 
                                        image_link = stripped_product_image)
                    cosmetic.save()
                except:
                    print(stripped_product_name)
                    print("Error")
print(cnt)