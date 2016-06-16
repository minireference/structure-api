from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from djstruct.views import DjangoBaseNodeDetailView, DjangoBaseNodeListView
from neomodelstruct.views import NeoBaseNodeDetailView as OldNeoBaseNodeDetailView
from neomodelstruct.views import NeoBaseNodeListView as OldNeoBaseNodeListView


from neolixirstruct.views import NeolixirBaseNodeDetailView, NeolixirBaseNodeListView

router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include(router.urls)),

    # DjangoBaseNode API
    url(r'^api/v1/nodes2/(?P<uuid>[a-zA-Z0-9_-]*)/$', 
        DjangoBaseNodeDetailView.as_view(), name='djangobasenode-detail'),
    url(r'^api/v1/nodes2/$',
        DjangoBaseNodeListView.as_view(), name='djangobasenode-list'),

    # NeoBaseNode API
    url(r'^api/v1/nodes3/(?P<uuid>[a-zA-Z0-9_-]*)/$', 
       OldNeoBaseNodeDetailView.as_view(), name='neobasenode-detail'),
    url(r'^api/v1/nodes3/$', 
       OldNeoBaseNodeListView.as_view(), name='neobasenode-list'),
    #
    # Neolixir-backed API
    url(r'^api/v1/nodes4/(?P<uuid>[a-zA-Z0-9_-]*)/$', 
       NeolixirBaseNodeDetailView.as_view(), name='neolixirbasenode-detail'),
    url(r'^api/v1/nodes4/$', 
       NeolixirBaseNodeListView.as_view(), name='neolixirbasenode-list'),
      
    
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    url(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
