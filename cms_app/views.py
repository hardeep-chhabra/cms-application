from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.http import HttpResponseNotAllowed
from .models import Author, Post, Like
from .serializers import *
from .permissions import IsOwner


class BlogGetPutDeleteCustomURL(APIView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            view = BlogDetail.as_view()
        elif request.method == 'PUT':
            view = BlogUpdate.as_view()
        elif request.method == 'DELETE':
            view = BlogUpdate.as_view()
        else:
            return HttpResponseNotAllowed(['GET','PUT','DELETE'])
        return view(request, *args, **kwargs)
    

class AuthorCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AuthorLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # WE CAN SET COOKIES HERE IF WE WANT TO, BUT NOT REQUIRED
            # login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user':user.email})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

class AuthorUpdateDeleteAPI(APIView):

    def put(self, request):
        user = request.user
        serializer = AuthorGetUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AuthorDetail(APIView):

    def get(self, request):
        user = request.user
        serializer = AuthorGetUpdateSerializer(user)
        return Response(serializer.data)
    

class BlogCreateFetchAll(APIView):

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = BlogSerializer(posts, many=True)
        return Response(serializer.data)
    

class BlogDetail(APIView):

    def get(self, request, pk):

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(data={'error':'post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if post.author == request.user or post.is_public:
            serializer = BlogSerializer(post)
        else:
            return Response(data={'message':'private post / not authorized'}, status=status.HTTP_403_FORBIDDEN)
            
        return Response(serializer.data)
    
class BlogUpdate(APIView):
    permission_classes = (IsAuthenticated, IsOwner, )

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(data={'error':'post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.author != request.user:
            return Response({'error': 'You do not have permission to edit this post'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BlogSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(data={'error':'post not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.author != request.user:
            return Response({'error': 'You do not have permission to delete this post'}, status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class LikeUnlikePost(APIView):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        Like.objects.create(author=request.user, post=post)
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        like_qs = Like.objects.filter(author=request.user, post=post)
        if not like_qs:
            return Response({'message': 'no likes found'}, status=status.HTTP_404_NOT_FOUND)
        
        like_qs.last().delete()
        return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)
    

