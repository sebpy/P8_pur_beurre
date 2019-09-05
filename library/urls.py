from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    #url(r'^$', views.index, name="library"),  # "/library" will call the method "index" in "views.py"
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^detail/$', views.search, name='detail'),
]
