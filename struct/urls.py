from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
# from djstruct.views import BaseNodeDetailView, BaseNodeListView
from neostruct.views import NeoBaseNodeDetailView, NeoBaseNodeListView

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include(router.urls)),

    # BaseNode API
    # url(r'^api/v1/nodes2/(?P<uuid>[a-zA-Z0-9_-]*)/$', 
    #    BaseNodeDetailView.as_view(), name='basenode-detail'),
    #url(r'^api/v1/nodes2/$', 
    #    BaseNodeListView.as_view(), name='basenode-list'),

    # NeoBaseNode API
    url(r'^api/v1/nodes3/(?P<uuid>[a-zA-Z0-9_-]*)/$', 
       NeoBaseNodeDetailView.as_view(), name='neobasenode-detail'),
    url(r'^api/v1/nodes3/$', 
       NeoBaseNodeListView.as_view(), name='neobasenode-list'),
    
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    url(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
