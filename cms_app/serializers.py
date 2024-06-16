from rest_framework import serializers
from .models import Author, Post, Like



class AuthorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Author(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class AuthorGetUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['username', 'first_name', 'last_name','email','is_active']
        read_only_fields = ['email', 'password']


class LikeNestedSerializer(serializers.ModelSerializer):
    post = serializers.CharField(source='post.title', read_only=True)
    author = serializers.EmailField(source='author.email', read_only=True)
    like_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Like
        fields = ['like_id', 'author', 'post']


class BlogSerializer(serializers.ModelSerializer):
    likes = LikeNestedSerializer(many=True, read_only=True)
    post_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'is_public', 'post_id', 'author', 'likes']
        read_only_fields = ['id','author','likes']


    