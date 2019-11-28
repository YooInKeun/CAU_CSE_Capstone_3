import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beautyforme.settings")
import django
django.setup()
from cosmetic.models import *
from makeup.models import *
import csv

youtuber = "Risabae"
file_name = "risabae_matched_001"

if __name__=='__main__':
    with open(f'db_insert_data/All Data/{file_name}.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        row=list(csv.reader(csvDataFile))

        all_cosmetics = []
        cosmetic_names = []
        for cosmetic_instance in Cosmetic.objects.all():
            splited_brand = cosmetic_instance.product.brand.brand_name.split(' ')
            splited_name = cosmetic_instance.product.product_name.split(' ')
            if cosmetic_instance.type_name == "":
                splited_type = ""
            else:
                splited_type = cosmetic_instance.type_name.split(' ')
            full_name = "".join(splited_brand) + "".join(splited_name) + "".join(splited_type)

            cosmetic = {
                'id' : cosmetic_instance.id,
                'brand' : splited_brand,
                'name' : splited_name,
                'type' : splited_type,
            }
            cosmetic_names.append({
                'id':cosmetic_instance.id,
                'full_name': full_name
            })
            all_cosmetics.append(cosmetic)
        print("all_cosmetics end!")

        matched_count = 0
        not_matched_count = 0

        for col in row:
            title = col[0]
            link = col[1]
            hits = col[3]
            upload_date = col[4].replace(".", "-").replace(" ", "")
            if upload_date[-1] == "-":
                upload_date = upload_date[:-1]
            thumbnail = col[5]

            try:
                Video.objects.get(link=link)
            except:
                cosmetic_list = []
                cosmetic_json = "{"
                cosmetic_count = 0
                for cosmetic in col[6:]:
                    if cosmetic == "":
                        break

                    for cosmetic_name in cosmetic_names:
                        if cosmetic.replace(" ", "") == cosmetic_name['full_name']:
                            matched_count += 1
                            cosmetic_id = cosmetic_name["id"]
                            if cosmetic_id in cosmetic_list:
                                break
                            cosmetic_list.append(cosmetic_id)
                            cosmetic_json += f"'{cosmetic_count}':'{cosmetic_id}', "
                            cosmetic_count += 1
                            break
                if cosmetic_count > 0:
                    cosmetic_json = cosmetic_json[:-2] + "}"
                    print(cosmetic_json)

                    video = Video(title = title, thumbnail=thumbnail, link=link, upload_date= upload_date, hits=hits, 
                    youtuber=Youtuber.objects.get(name=youtuber), cosmetics=cosmetic_json)
                    video.save()

               