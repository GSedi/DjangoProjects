from rest_framework import serializers
from client.models import Client
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', )


class ClientModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    class Meta:
        model = Client
        fields = ('user', 'telephone',)

    def update(self, instance, validated_data):
        instance.user = validated_data.pop('user')
        instance.telephone =  validated_data.pop('telephone')
        instance.save()
        # user_data = validated_data.pop('user')
        # user = User.objects.get(username=user_data['username'])
        # user = UserModelSerializer.update(instance = self.user, validated_data=user_data)
        # client, created = Client.objects.update_or_create(user=user,
        #                     telephone=validated_data.pop('telephone'))
        return instance
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserModelSerializer.create(UserModelSerializer(), validated_data=user_data)
        client, created = Client.objects.update_or_create(user=user,
                            telephone=validated_data.pop('telephone'))
        return client
