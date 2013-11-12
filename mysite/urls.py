from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

# from youtubetomp3 import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^', include('youtubetomp3.urls', namespace="youtubetomp3")),

    # url(r'^accounts/profile/$', views.profile, name="profile_detail"),
    url(r'^accounts/', include('registration.backends.default.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
