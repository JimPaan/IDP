from django.urls import path, reverse_lazy
from . import views
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.index, name='index'),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('login', views.login, name='login'),
    path('admin/', admin.site.urls),
    path('selection', views.route, name='route'),
    path('stops/<str:pk>', views.bus_stop, name='stops'),
    path('rtbl/<str:pk>/<str:pt>', views.rtbl, name='rtbl'),
    path('get_buslocation/<str:pk>/<str:pt>', views.get_buslocation, name='get_buslocation'),
    path('tablet_displayer/<str:pk>/<str:pt>', views.tablet, name='tablet_displayer'),
]
