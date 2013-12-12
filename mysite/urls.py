from django.conf.urls import patterns, include, url
from blog import views
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    #url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
