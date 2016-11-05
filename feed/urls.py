from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all$', views.feed_all),
    url(r'^filter$', views.feed_filter),
    url(r'^add_ical_source$', views.feed_add_ical),
    url(r'^force_update_icals$', views.force_update_icals),
]
