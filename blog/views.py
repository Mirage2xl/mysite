from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from blog.models import Post
from blog.forms import ContactForm, SubscribeForm, PostSearchForm
from mysite.utils import get_mailchimp_api
import mailchimp

# Create your views here.


def encode_url(str):
    return str.replace(' ', '_')


def decode_url(str):
    return str.replace('_', ' ')


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    for post in posts:
        post.url = encode_url(post.title)
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def blogpost(request, post_url):
    post_title = decode_url(post_url)
    post = Post.objects.get(title__iexact=post_title)
    context = {'post': post}
    return render(request, 'blog/blogpost.html', context)


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
                      ['andrey.zalomskiy@gmail.com'])
        return HttpResponseRedirect('/blog/about/')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                m = get_mailchimp_api()
                m.lists.subscribe('54069483af', {'email': cd['email']})
            except mailchimp.ListAlreadySubscribedError:
                messages.error(request, "You already subscribed")
                return HttpResponseRedirect('/blog/subscribe/')
            except mailchimp.Error, e:
                messages.error(request, "An error occurred: %s - %s" % (e.__class__, e))
                return HttpResponseRedirect('/blog/subscribe/')
            return HttpResponseRedirect('/blog/')
    else:
        form = SubscribeForm()
    return render(request, 'blog/subscribe.html', {'form': form})


def search(request):
    form = PostSearchForm(request.GET)
    posts = form.search()
    context = {'posts': posts}
    return render(request, 'search/search.html', context)
