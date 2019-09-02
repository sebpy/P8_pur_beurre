from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    #url(r'^$', views.index, name="library"),  # "/library" will call the method "index" in "views.py"
    url(r'^$', views.index),
    #url(r'^$', views.listing),
]
