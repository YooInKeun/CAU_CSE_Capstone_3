from accounts.models import *
from cosmetic.models import *
from .serializer import *
from django.core import serializers

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User



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
        try:
            queryset = Cosmetic.objects.filter(product__in=Product.objects.filter(product_name__contains=request.data['query_cosmetic']))
            serializer = CosmeticSerializer(queryset, many=True)
            # queryset = Product.objects.filter(product_name__contains=request.data['query_cosmetic'])
            # serializer = ProductSerializer(queryset, many=True)
        except:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)