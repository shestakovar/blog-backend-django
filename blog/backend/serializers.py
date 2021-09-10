from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comment_count = serializers.IntegerField(
        source='comment_set.count',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('origin', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('origin', )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'last_login', 'email', 'date_joined', )
        read_only_fields = ('last_login', 'date_joined')

    def create(self, validated_data):
        pswd = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(pswd)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            pswd = validated_data.pop('password')

        user = super().update(instance, validated_data)
        if pswd:
            user.set_password(pswd)
        user.save()
        return user
