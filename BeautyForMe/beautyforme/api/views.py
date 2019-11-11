from accounts.models import *
from cosmetic.models import *
from .serializer import *
from django.core import serializers

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

import operator
from functools import reduce
from django.db.models import Q
import difflib

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
        queryset = Cosmetic.objects.filter(rgb_value="Fuck You!")
        serializer = CosmeticSerializer(queryset, many=True)

        if request.query_params['is_keyuped'] == "true":
            queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])).order_by('id')
            queryset = queryset[0:4]
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
    # permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        request.data['user_id'] = request.user
        serializer = UserCosmeticSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = User_Cosmetic.objects.filter(user=request.user)
        serializer = UserCosmeticSerializer(queryset, many=True)
        return Response(serializer.data)