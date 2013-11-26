from django.shortcuts import render
from blog.models import Post, Comment

# Create your views here.


def encode_url(str):
    return str.replace(' ', '_')


def decode_url(str):
    return str.replace('_', ' ')


def index(request):
    post_list = Post.objects.order_by('-publish_date')[:5]
    for post in post_list:
        post.url = encode_url(post.title)
    context = {'posts': post_list}
    return render(request, 'blog/index.html', context)


def blogpost(request, post_url):
    post_title = decode_url(post_url)
    post_context = Post.objects.get(title__iexact=post_title)
    try:
        comments = Comment.objects.get(content__iexact=post_context)
    except:
        comments = {}
    context = {'post': post_context, 'comments': comments}
    return render(request, 'blog/blogpost.html', context)


def about(request):
    context = {}
    return render(request, 'blog/about.html')


def contact(request):
    context = {}
    return render(request, 'blog/contact.html')
