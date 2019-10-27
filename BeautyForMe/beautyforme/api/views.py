from accounts.models import *
from .serializer import ProfileSerializer

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework import status


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
<<<<<<< HEAD
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
>>>>>>> [UPDATE] 프로필 생성 코드 제거
