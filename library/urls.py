from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^save/$', views.save_product, name='save'),
    url(r'^saved/$', views.read_user_list, name='saved'),
    url(r'^legal-notice/$', views.legal_notice, name='legal_notice'),
]
