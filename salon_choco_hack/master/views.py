from master.models import Master
from django.contrib.auth.models import User
from master.serializers import UserModelSerializer, MasterModelSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from main.serializers import SalonModelSerializer
from main.models import Salon

class MasterList(ListCreateAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterModelSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = MasterModelSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=ValueError):
    #         serializer.create(validated_data=request.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.error_messages,
    #                     status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        telephone = request.data.get('telephone')
        serializer = UserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.data['password'])
        master = Master(user=user, telephone=telephone)
        master.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
        # serializer.save(user=self.request)


class MasterDetail(RetrieveUpdateDestroyAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterModelSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        Master = Master.objects.get(id=self.kwargs[self.lookup_field])
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.update(instance=Master, validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

        # Master = Master.objects.get(id=self.kwargs[self.lookup_field])
        # serializer = UserModelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # Master.user = serializer.save()
        # Master.save()
        # return super().update(request, *args, **kwargs)

    # lookup_field = 'pk'

    # def get_object(self):
    #     print(self.kwargs['pk'])
    #     user = User.objects.get(id=self.kwargs[self.lookup_field])
    #     Master = Master.objects.get(user = user)
    #     return Master


@api_view(['POST'])
def register(request):
    user_data = request.data.pop('user')
    user_serializer = UserModelSerializer(data=user_data)
    salon_data = request.data.pop('salon')
    salon_serializer = SalonModelSerializer(salon_data)
    salon_id = salon_serializer.data.get('salon_id')
    salon = Salon.objects.get(pk=int(salon_id))
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(user_data['password'])
        user.save()
        master = Master(user=user, salon=salon)
        master.save()
        token, _ = Token.objects.get_or_create(user=user)
        if user:
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'key': token.key, 'master_id': user.Master.pk})
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return Response({'error: Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'key': token.key, 'master_id': user.master.pk})

@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'detail': 'Succesfully logget out'})
