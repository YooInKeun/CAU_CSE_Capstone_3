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

        if request.query_params['is_keyuped'] == "true":
            queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])).order_by('id')
            queryset = queryset[0:7]
        elif request.query_params['is_clicked'] == "true":
            queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])).order_by('id')
        #     속도가 너무 느림
        #     cosmetics = Cosmetic.objects.all()
        #     selected_cosmetic_ids = []
        #     for cosmetic in cosmetics.iterator():
        #         if difflib.SequenceMatcher(None, cosmetic.product.product_name, request.query_params['query_cosmetic']).ratio() > 0.5:
        #             selected_cosmetic_ids.append(cosmetic.id)
                    
        #     queryset = Cosmetic.objects.filter(pk__in=selected_cosmetic_ids)
        
        # if request.query_params['is_clicked'] == "true":
        serializer = CosmeticSerializer(queryset, many=True)
        return Response(serializer.data)


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

    def delete(self, request, format=None):
        queryset = request.data
        for json_ids in queryset:
            dict_ids = json.loads(json_ids)
            cosmetic_ids = dict_ids['user_cosmetic_id']
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
        for json_ids in queryset:
            dict_ids = json.loads(json_ids)
            cosmetic_ids = dict_ids['user_interested_cosmetic_id']
        try:
            for cosmetic_id in cosmetic_ids:
                user_interested_cosmetic = User_Interested_Cosmetic.objects.get(pk=cosmetic_id)
                user_interested_cosmetic.delete()
            cosmetic_id = {}
            cosmetic_id['user_interested_cosmetic_id'] = cosmetic_ids
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(cosmetic_id)