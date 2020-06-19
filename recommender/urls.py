from django.conf.urls import url
from django.urls import re_path
from recommender import views

urlpatterns = [
    re_path(r'^sim/user/(?P<user_id>\w+)/(?P<sim_method>\w+)/$',
        views.similar_users, name='similar_users'),
    re_path(r'^cf/user/(?P<user_id>\w+)/$',
        views.recs_cf, name='recs_cb'),
]
