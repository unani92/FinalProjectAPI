from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieArticleSerializer, ArticleSerializer, ArticleListSerializer, CommentSerializer
from .models import Movie, Article, Comment
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.

# pagination config default class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

# all movies, specific movie view
class MovieListPaginate(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieArticleSerializer
    pagination_class = StandardResultsSetPagination

class MovieBest3(APIView):
    def get(self, request):
        movies = Movie.objects.order_by('-popularity')[:3]
        serializer = MovieArticleSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetail(APIView):
    def get(self, request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieArticleSerializer(movie)
        return Response(serializer.data)

# all articles, specific article CRUD
class ArticleList(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    pagination_class = StandardResultsSetPagination

class ArticleBest3(APIView):
    def get(self,request):
        articles = Article.objects.annotate(count=Count('like_users')).order_by('-count')[:3]
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetail(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data)
        else:
            print(serializer.data)
            return Response({"msg": "error"})

    @permission_classes([IsAuthenticated])
    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else :
            return Response({"msg":"error"})

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({"msg":"deleted"})

# all comments, specific comment CRD
class CommentList(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response({"msg":"deleted"})