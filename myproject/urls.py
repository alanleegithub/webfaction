from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', include('blog.urls')),
    url(r'^blogs/', include('blog.urls')),
    url(r'^login/$', 'blog.views.login'),
    url(r'^logout/$', 'blog.views.logout'),
    url(r'^post/$', 'blog.views.post'),
    url(r'^register/$', 'blog.views.register'),
    url(r'^about/$', 'blog.views.about'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
