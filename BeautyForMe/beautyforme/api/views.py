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
        queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.query_params['query_cosmetic'])).order_by('id')
        entries = request.query_params['query_cosmetic'].split(" ")

        if len(queryset) < 5:
            queryset |= Cosmetic.objects.filter(
                product__in=Product.objects.filter(reduce(operator.and_, (Q(product_name__contains=item) for item in entries[0:len(entries)-2]))),
                type_name__contains=entries[len(entries)-1])
        queryset = queryset[0:5]
        serializer = CosmeticSerializer(queryset, many=True)
        return Response(serializer.data)


class UserCosmeticInfo(APIView):
    # permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = UserCosmeticSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = User_Cosmetic.objects.filter(user=request.user)
        serializer = UserCosmeticSerializer(queryset, many=True)
        return Response(serializer.data)