from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^bulletinboard/', include('bulletinboard.urls', namespace="bulletinboard")),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^markdown/', include('django_markdown.urls')),
    url(r'^accounts/login/$', 'bulletinboard.views.login_user'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}),
    url(r'^accounts/newUser/$', 'bulletinboard.views.new_user'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
