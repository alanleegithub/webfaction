from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'blogs'),
    url(r'^all/$', 'blogs'),
    url(r'^get/(?P<post_id>\d+)/$', 'blog'),
    url(r'^get/(?P<post_id>\d+)/comment/$', 'comment'),
    #url(r'^tag/(?P<tag>\w+)/$', 'tagpage'),
)
