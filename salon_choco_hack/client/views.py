from client.models import Client
from django.contrib.auth.models import User
from client.serializers import UserModelSerializer, ClientModelSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token

class ClientList(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = ClientModelSerializer(data=request.data)
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
        client = Client(user=user, telephone=telephone)
        client.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
        # serializer.save(user=self.request)


class ClientDetail(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        client = Client.objects.get(id=self.kwargs[self.lookup_field])
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.update(instance=client, validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

        # client = Client.objects.get(id=self.kwargs[self.lookup_field])
        # serializer = UserModelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # client.user = serializer.save()
        # client.save()
        # return super().update(request, *args, **kwargs)

    # lookup_field = 'pk'

    # def get_object(self):
    #     print(self.kwargs['pk'])
    #     user = User.objects.get(id=self.kwargs[self.lookup_field])
    #     client = Client.objects.get(user = user)
    #     return client


@api_view(['POST'])
def register(request):
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()
        client = Client(user=user)
        client.save()
        token, _ = Token.objects.get_or_create(user=user)
        if user:
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'key': token.key, 'client_id': user.client.pk})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return Response({'error: Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'key': token.key, 'client_id': user.client.pk})

@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'detail': 'Succesfully logget out'})
