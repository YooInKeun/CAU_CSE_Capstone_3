from accounts.models import *
from cosmetic.models import *
from .serializer import *
from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

import operator
from functools import reduce
from django.db.models import Q
import difflib
import json

class UserInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        queryset = User.objects.filter(pk=request.user.pk)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = User.objects.get(pk=request.user.pk)
        serializer = UserSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        queryset = Profile.objects.filter(user=request.user)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = Profile.objects.get(user=pk)
        serializer = ProfileSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CosmeticInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # queryset = Cosmetic.objects.filter(product__category__small_category="픽서/영양제")
        # print(queryset)
        # queryset = Cosmetic.objects.filter(product__category=21)
        # for a in queryset:
        #     if a.similar_cosmetics is not "":
        #         print('item명: ' + str(a) + str(a.rgb_value))
        #         print('id: ' + str(a.id))
        #         print('대체화장품: ' + str(a.similar_cosmetics))

        # print(queryset)
        # queryset = Cosmetic.objects.exclude(rgb_value="None")
        # print("Start!")
        # for a in queryset:
        #     if a.product.category.id == 21:
        #         print(a.rgb_value)
        queryset = Cosmetic.objects.filter(rgb_value="Fuck You!")
        serializer = CosmeticSerializer(queryset, many=True)
        size = 0

        try:
            if request.query_params['is_keyuped'] == "true":
                queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])).order_by('id')
                queryset = queryset[0:7]
                serializer = CosmeticSerializer(queryset, many=True)
                return Response(serializer.data)
            elif request.query_params['is_clicked'] == "true":
                page_num = int(request.query_params['page_num'])
                queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])).order_by('id')[30*(page_num-1):30*page_num]
                size = len(Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])))
        except:
            try:
                small_category_id = request.query_params['small_category_id']
                page_num = int(request.query_params['page_num'])
                queryset = Cosmetic.objects.filter(product__category__pk=small_category_id).order_by('id')[20*(page_num-1):20*page_num]
                size = len(Cosmetic.objects.filter(product__category__pk=small_category_id))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        #     속도가 너무 느림
        #     cosmetics = Cosmetic.objects.all()
        #     selected_cosmetic_ids = []
        #     for cosmetic in cosmetics.iterator():
        #         if difflib.SequenceMatcher(None, cosmetic.product.product_name, request.query_params['query_cosmetic']).ratio() > 0.5:
        #             selected_cosmetic_ids.append(cosmetic.id)
                    
        #     queryset = Cosmetic.objects.filter(pk__in=selected_cosmetic_ids)
        
        # if request.query_params['is_clicked'] == "true":
        serializer = CosmeticSerializer(queryset, many=True)

        return Response({
            'cosmetics': serializer.data,
            'cosmetic_size': size
        })


class UserCosmeticInfo(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            user_cosmetic = User_Cosmetic()
            user_cosmetic.user = request.user
            user_cosmetic.cosmetic = Cosmetic.objects.get(pk=request.data['cosmetic_id'])
            user_cosmetic.expiration_date = request.data['expiration_data']
            user_cosmetic.alarm_cycle = request.data['alarm_cycle']
            user_cosmetic.is_consent_alarm = request.data['is_consent_alarm']
            user_cosmetic.save()
            # queryset= User_Cosmetic.objects.filter(user=request.user)
            queryset= User_Cosmetic.objects.filter(pk=user_cosmetic.id)
            serializer = UserCosmeticSerializer(queryset, many=True)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        queryset = User_Cosmetic.objects.filter(user=request.user)
        serializer = UserCosmeticSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        try:
            user_cosmetic = User_Cosmetic.objects.get(pk=request.data['user_cosmetic_id'])
            user_cosmetic.is_consent_alarm = request.data['is_consent_alarm']
            user_cosmetic.alarm_cycle = request.data['alarm_cycle']
            user_cosmetic.save()
            queryset= User_Cosmetic.objects.filter(pk=user_cosmetic.id)
            serializer = UserCosmeticSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        queryset = request.data
        cosmetic_ids = queryset['user_cosmetic_id']
        try:
            for cosmetic_id in cosmetic_ids:
                user_cosmetic = User_Cosmetic.objects.get(pk=cosmetic_id)
                user_cosmetic.delete()
            cosmetic_id = {}
            cosmetic_id['user_cosmetic_id'] = cosmetic_ids
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(cosmetic_id)


class UserInterestedCosmeticInfo(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        queryset = User_Interested_Cosmetic.objects.filter(cosmetic=9999999999999)
        if len(User_Interested_Cosmetic.objects.filter(user=request.user, cosmetic=request.data['cosmetic_id'])) is not 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if isinstance(request.data['cosmetic_id'], list):
            try:
                cosmetic_ids = request.data['cosmetic_id']
                for cosmetic_id in cosmetic_ids:
                    user_interested_cosmetic = User_Interested_Cosmetic()
                    user_interested_cosmetic.user = request.user
                    user_interested_cosmetic.cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
                    user_interested_cosmetic.save()
                    queryset |= User_Interested_Cosmetic.objects.filter(pk=user_interested_cosmetic.id)
                serializer = UserInterestedCosmeticSerializer(queryset, many=True)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_interested_cosmetic = User_Interested_Cosmetic()
                user_interested_cosmetic.user = request.user
                user_interested_cosmetic.cosmetic = Cosmetic.objects.get(pk=request.data['cosmetic_id'])
                user_interested_cosmetic.save()
                queryset= User_Interested_Cosmetic.objects.filter(pk=user_interested_cosmetic.id)
                serializer = UserInterestedCosmeticSerializer(queryset, many=True)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        queryset = User_Interested_Cosmetic.objects.filter(user=request.user)
        serializer = UserInterestedCosmeticSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        queryset = request.data
        cosmetic_ids = queryset['user_interested_cosmetic_id']
        try:
            for cosmetic_id in cosmetic_ids:
                user_interested_cosmetic = User_Interested_Cosmetic.objects.get(pk=cosmetic_id)
                user_interested_cosmetic.delete()
            cosmetic_id = {}
            cosmetic_id['user_interested_cosmetic_id'] = cosmetic_ids
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(cosmetic_id)

class BigCategoryInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        queryset = Big_Category.objects.all()
        serializer = BigCategorySerializer(queryset, many=True)
        return Response(serializer.data)

class SmallCategoryInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # big_category_id = request.data['big_category_id']
        big_category_id = request.query_params['big_category_id']
        queryset = Small_Category.objects.filter(big_category__pk=big_category_id)
        serializer = SmallCategorySerializer(queryset, many=True)
        return Response(serializer.data)

class CosmeticImportanceInfo(APIView):

    def get(self, request, format=None):
        cosmetic_importance = {}
        try:
            queryset = Cosmetic_Importance.objects.filter(user=request.user)
            cosmetic_importance['importance'] = json.loads(queryset[0].importance)
            # serializer = CosmeticImportanceSerializer(queryset, many=True)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(cosmetic_importance)

    def put(self, request, format=None):
        cosmetic_importance = {}
        try:
            queryset = Cosmetic_Importance.objects.filter(user=request.user)
            cosmetic_importance = json.loads(queryset[0].importance)
            for i in range(len(request.data['importance'])):
                big_category = request.data['importance'][i]['big_category']
                for j in range(len(request.data['importance'][i]['small_categories'])):
                    small_category = request.data['importance'][i]['small_categories'][j][0]
                    value = request.data['importance'][i]['small_categories'][j][1]
                    cosmetic_importance[big_category][small_category] = value
            cosmetic_importance_obj = Cosmetic_Importance.objects.get(user=request.user)
            cosmetic_importance_obj.importance = json.dumps(cosmetic_importance)
            cosmetic_importance_obj.save()
            queryset = Cosmetic_Importance.objects.filter(user=request.user)
            cosmetic_importance = {}
            cosmetic_importance['importance'] = json.loads(queryset[0].importance)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(cosmetic_importance)

class AllVideoInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # page_num = request.data['page_num']
        page_num = request.query_params['page_num']
        page_num = int(page_num)
        queryset = Video.objects.all().order_by('id')[10*(page_num-1):10*page_num]
        serializer = VideoSerializer(queryset, many=True)

        videos_info = {}
        videos_info['video'] = serializer.data
        videos_info['video_size'] = len(Video.objects.all())
        for i in range(len(videos_info['video'])):
            raw = videos_info['video'][i]['cosmetics']
            raw = raw.replace("'", "\"")
            cosmetic_ids = json.loads(raw)
            cosmetics = []
            for key in cosmetic_ids.keys():
                cosmetic_info = {}
                cosmetic = Cosmetic.objects.get(id=cosmetic_ids[key])
                cosmetic_info['id'] = cosmetic_ids[key]
                cosmetic_info['brandName'] = cosmetic.product.brand.brand_name
                cosmetic_info['productName'] = cosmetic.product.product_name
                cosmetic_info['typeName'] = str(cosmetic.type_name).strip()
                cosmetic_info['bigCategory'] = cosmetic.product.category.big_category.big_category
                cosmetic_info['smallCategory'] = cosmetic.product.category.small_category 
                cosmetic_info['imageLink'] = cosmetic.image_link
                cosmetic_info['rgbValue'] = cosmetic.rgb_value
                tag_names = json.loads(serializers.serialize('json', cosmetic.product.tag_names.all()))
                cosmetic_info['tagNames'] = tag_names
                cosmetics.append(cosmetic_info)
        
            videos_info['video'][i]['cosmetics'] = cosmetics

        youtuber_list = Youtuber.objects.all()
        serializer = YoutuberSerializer(youtuber_list, many=True)
        videos_info['youtuber_list'] = serializer.data
        return Response(videos_info)

class VideoDetailInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, pk, format=None):
        queryset = Video.objects.filter(pk=pk)
        serializer = VideoSerializer(queryset, many=True)

        video_info = {}
        video_info['video'] = serializer.data[0]

        raw = video_info['video']['cosmetics']
        raw = raw.replace("'", "\"")
        cosmetic_ids = json.loads(raw)
        cosmetics = []
        for key in cosmetic_ids.keys():
            cosmetic_info = {}
            cosmetic = Cosmetic.objects.get(id=cosmetic_ids[key])
            cosmetic_info['id'] = cosmetic_ids[key]
            cosmetic_info['brandName'] = cosmetic.product.brand.brand_name
            cosmetic_info['productName'] = cosmetic.product.product_name
            cosmetic_info['typeName'] = str(cosmetic.type_name).strip()
            cosmetic_info['bigCategory'] = cosmetic.product.category.big_category.big_category
            cosmetic_info['smallCategory'] = cosmetic.product.category.small_category 
            cosmetic_info['imageLink'] = cosmetic.image_link
            cosmetic_info['rgbValue'] = cosmetic.rgb_value
            tag_names = json.loads(serializers.serialize('json', cosmetic.product.tag_names.all()))
            cosmetic_info['tagNames'] = tag_names
            cosmetics.append(cosmetic_info)
        
        video_info['video']['cosmetics'] = cosmetics
        return Response(video_info)

class FilteredVideoInfo(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # page_num = int(request.data['page_num'])
        # youtuber_ids = request.data['youtuber_ids']
        page_num = int(request.query_params['page_num'])
        youtuber_ids = request.query_params['youtuber_ids'].split(',')
        youtuber_ids = map(int, youtuber_ids)
        queryset = Video.objects.filter(youtuber__id__in=youtuber_ids).order_by('id')[10*(page_num-1):10*page_num]
        serializer = VideoSerializer(queryset, many=True)

        videos_info = {}
        videos_info['video'] = serializer.data
        videos_info['video_size'] = len(Video.objects.filter(youtuber__id__in=youtuber_ids))
        for i in range(len(videos_info['video'])):
            raw = videos_info['video'][i]['cosmetics']
            raw = raw.replace("'", "\"")
            cosmetic_ids = json.loads(raw)
            cosmetics = []
            for key in cosmetic_ids.keys():
                cosmetic_info = {}
                cosmetic = Cosmetic.objects.get(id=cosmetic_ids[key])
                cosmetic_info['id'] = cosmetic_ids[key]
                cosmetic_info['brandName'] = cosmetic.product.brand.brand_name
                cosmetic_info['productName'] = cosmetic.product.product_name
                cosmetic_info['typeName'] = str(cosmetic.type_name).strip()
                cosmetic_info['bigCategory'] = cosmetic.product.category.big_category.big_category
                cosmetic_info['smallCategory'] = cosmetic.product.category.small_category 
                cosmetic_info['imageLink'] = cosmetic.image_link
                cosmetic_info['rgbValue'] = cosmetic.rgb_value
                tag_names = json.loads(serializers.serialize('json', cosmetic.product.tag_names.all()))
                cosmetic_info['tagNames'] = tag_names
                cosmetics.append(cosmetic_info)
        
            videos_info['video'][i]['cosmetics'] = cosmetics
        return Response(videos_info)