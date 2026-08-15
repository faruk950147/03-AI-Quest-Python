from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from queryset.models import Author, Post, Comment
from django.db import connection

# ==============================
# 1. Forward relation: Post → Author
# ==============================
class PostListWithoutSelectRelatedView(View):
    def get(self, request):
        posts = Post.objects.all()  # N+1 query problem
        for post in posts:
            print(post.author.name)  # Each access triggers a query
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("Without select_related optimization")


class PostListWithSelectRelatedView(View):
    def get(self, request):
        posts = Post.objects.select_related('author')  # single query
        for post in posts:
            print(post.author.name)
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("With select_related optimization")


# ==============================
# 2. Reverse / ManyToMany relation: Post → Tag
# ==============================
class PostListWithoutPrefetchRelatedView(View):
    def get(self, request):
        posts = Post.objects.all()  # N+1 query on tags
        for post in posts:
            print(post.title)
            for tag in post.tags.all():
                print(tag.name)
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("Without prefetch_related optimization")


class PostListWithPrefetchRelatedView(View):
    def get(self, request):
        posts = Post.objects.prefetch_related('tags', 'comments')  # efficient prefetch
        for post in posts:
            print(post.title)
            for tag in post.tags.all():
                print(tag.name)
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("With prefetch_related optimization")


# ==============================
# 3. Combined optimization: Author + Tags + Comments
# ==============================
class PostListOptimizedView(View):
    def get(self, request):
        posts = Post.objects.select_related('author').prefetch_related('tags', 'comments')
        for post in posts:
            print(post.title, post.author.name)
            for tag in post.tags.all():
                print(tag.name)
            for comment in post.comments.all():
                print(comment.content)
        for query in connection.queries:
            print(query['sql'])
        print(f"Total Number of queries: {len(connection.queries)}")
        return HttpResponse("Fully optimized view")
    

class ShowView(View):
    def get(self, request):
        # forword query for author
        author = Author.objects.first()
        # reverse query for posts
        posts = author.posts.all()
        return render(request, 'queryset/show.html', {'author': author, 'posts': posts})
    
