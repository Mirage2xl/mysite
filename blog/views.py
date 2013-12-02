from datetime import datetime
# from django.template import RequestContext
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from blog.models import Post, Comment
from blog.forms import ContactForm, CommentForm

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
    form = CommentForm()
    post_title = decode_url(post_url)
    post_context = Post.objects.get(title__iexact=post_title)
    try:
        comments = Comment.objects.get(content__iexact=post_context)
    except:
        comments = {}
    context = {'post': post_context, 'comments': comments, 'form': form}
    return render(request, 'blog/blogpost.html', context)


def addcomment(request, post_url):
    post_title = decode_url(post_url)
#    context = RequestContext(request)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment = cd.save(commit=False)
            post = Post.objects.get(title=post_title)
            comment.post = post
            comment.comment_date = datetime.date
            comment.save()
            return blogpost(request, post_url)
        else:
            form.errors
    else:
        form = CommentForm()
    return blogpost(request, post_url)


def about(request):
#    context = {}
    return render(request, 'blog/about.html')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(cd['subject'],
                      cd['message'] + cd['name'],
                      cd.get('email', 'noreply@mysite.com'),
                      ['azalomskiy@icloud.com'])
        return HttpResponseRedirect('/blog/about/')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})
