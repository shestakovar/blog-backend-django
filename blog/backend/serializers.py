from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Comment, UserProfile


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
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
    author_id = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('origin', )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(
        source='userprofile.avatar', required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'last_login', 'email', 'date_joined', 'avatar')
        read_only_fields = ('last_login', 'date_joined')

    def create(self, validated_data):
        pswd = validated_data.pop('password')
        avatar = ''
        if 'userprofile' in validated_data:
            avatar = validated_data.pop('userprofile').pop('avatar')
        user = super().create(validated_data)
        user.set_password(pswd)

        if avatar:
            user.userprofile.avatar = avatar

        user.save()
        return user

    def update(self, instance, validated_data):
        pswd = ''
        avatar = ''
        if 'password' in validated_data:
            pswd = validated_data.pop('password')
        if 'userprofile' in validated_data:
            avatar = validated_data.pop('userprofile').pop('avatar')

        user = super().update(instance, validated_data)
        if pswd:
            user.set_password(pswd)
        if avatar or avatar is None:
            user.userprofile.avatar = avatar

        user.save()
        return user
