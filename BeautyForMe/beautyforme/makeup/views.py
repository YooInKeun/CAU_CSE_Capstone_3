from django.views.generic import TemplateView
from django.shortcuts import render
from django.core import serializers
from .models import *
from cosmetic.models import *
import json

class RecommendMakeupTV(TemplateView):
    template_name = 'makeup/recommend.html'

def recommend_result(request):
    raws = json.loads(request.POST.get('selected_cosmetics'))
    cosmetics = {}
    cosmetics['cosmetics'] = raws
    selected_cosmetic_ids = []
    for raw in raws:
        selected_cosmetic_ids.append(raw['id'])

    videos = Video.objects.all()
    video_scores = {}
    video_scores_contained_cosmetic_ids = []
    for video in videos:
        video_cosmetic_ids = []
        contained_cosmetic_ids = []
        raw = video.cosmetics
        raw = raw.replace("'", "\"")
        json_video_cosmetic_ids = json.loads(raw)
        for key in json_video_cosmetic_ids.keys():
            video_cosmetic_ids.append(int(json_video_cosmetic_ids[key]))

        score = 0
        for selected_cosmetic_id in selected_cosmetic_ids:
            for video_cosmetic_id in video_cosmetic_ids:
                if selected_cosmetic_id == video_cosmetic_id:
                    big_category = str(Cosmetic.objects.get(id=selected_cosmetic_id).product.category.big_category)
                    small_category = str(Cosmetic.objects.get(id=selected_cosmetic_id).product.category)
                    cosmetic_importance = json.loads(Cosmetic_Importance.objects.get(user=request.user).importance)
                    importance = Cosmetic_Importance.objects.get(user=request.user)
                    contained_cosmetic_ids.append(selected_cosmetic_id)
                    parenthesis_pos = small_category.find(']')
                    small_category = small_category[parenthesis_pos+2:]

                    if small_category == '아이브로우-마스카라&리퀴드' or small_category == '아이브로우-파우더' or small_category == '아이브로우-펜슬':
                        small_category = '아이브로우'
                    elif small_category == '아이라이너-리퀴드' or small_category == '아이라이너-펜슬&젤':
                        small_category = '아이라이너'
                    score += float(cosmetic_importance[big_category][small_category])
        if score != 0:
            video_scores[video.id] = score
            video_scores_contained_cosmetic_ids.append([score, contained_cosmetic_ids])
    
    video_queryset = Video.objects.filter(title="Fuck You")
    context = {}
    sorted_videos = sorted(video_scores.items(), key=lambda element:element[1], reverse=True)

    '''
    for sorted_video in sorted_videos:
        video_queryset |= Video.objects.filter(pk=sorted_video[0])
    context['cosmetics'] = cosmetics['cosmetics']
    context['videos'] = []
    video_list = json.loads(serializers.serialize('json', video_queryset))
    for video in video_list:
        youtuber = Youtuber.objects.get(pk=video['fields']['youtuber']).name
        video['fields']['youtuber'] = youtuber
        video['fields']['id'] = video['pk']
        context['videos'].append(video['fields'])
        # print(video['fields'])
    for idx, val in enumerate(sorted_videos):
        context['videos'][idx]['score'] = val[1]
    '''

    context['cosmetics'] = cosmetics['cosmetics']
    context['videos'] = []
    for sorted_video in sorted_videos:
        video_queryset = Video.objects.filter(pk=sorted_video[0])
        video= json.loads(serializers.serialize('json', video_queryset))
        youtuber = Youtuber.objects.get(pk=video[0]['fields']['youtuber']).name
        video[0]['fields']['youtuber'] = youtuber
        video[0]['fields']['id'] = video[0]['pk']
        context['videos'].append(video[0]['fields'])
    for idx, val in enumerate(sorted_videos):
        context['videos'][idx]['score'] = val[1]
    
    contained_cosmetics = []
    sorted_scores_cosmetic_ids = sorted(video_scores_contained_cosmetic_ids, key=lambda element:element[0], reverse=True)
    print(sorted_scores_cosmetic_ids)
    for idx, sorted_scores_cosmetic_id in enumerate(sorted_scores_cosmetic_ids):
        context['videos'][idx]['containedCosmetics'] = []
        cosmetic_queryset = Cosmetic.objects.filter(rgb_value="Fuck You")
        for cosmetic_id in sorted_scores_cosmetic_id[1]:
            cosmetic_queryset |= Cosmetic.objects.filter(pk=cosmetic_id)
        cosmetic_list = json.loads(serializers.serialize('json', cosmetic_queryset))
        for cosmetic in cosmetic_list:
            cosmetic_info = {}
            cosmetic_info['brandName'] = str(Product.objects.get(pk=cosmetic['fields']['product']).brand)
            product_name = str(Product.objects.get(pk=cosmetic['fields']['product']))
            parenthesis_pos = product_name.find(']')
            product_name = product_name[parenthesis_pos+2:]
            cosmetic_info['id'] = cosmetic['pk']
            cosmetic_info['productName'] = product_name
            cosmetic_info['typeName'] = cosmetic['fields']['type_name'].strip()
            context['videos'][idx]['containedCosmetics'].append(cosmetic_info)
    # print(context)
    return render(request, 'makeup/recommend_result.html', {'context':context})

# class RecommendResultTV(TemplateView):
#     template_name = 'makeup/recommend_result.html'

class VideoTV(TemplateView):
    template_name = 'makeup/video_list.html'

class VideoDetailTV(TemplateView):
    template_name = 'makeup/video_detail.html'