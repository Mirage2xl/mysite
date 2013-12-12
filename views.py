from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from blog.models import Post, Comment

def index(request):
    post_list = Post.objects.order_by('-publish_date')[:5]
    for post in post_list:
        post.url = encode_url(post.title)
    context = {'posts': post_list}
    return render(request, 'blog/index.html', context)
