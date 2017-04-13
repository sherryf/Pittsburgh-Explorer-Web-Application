from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from planner import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'planner/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^search$', views.search, name='searchResult'),

    url(r'^itinerary$', views.itinerary, name='itinerary'),
    url(r'^add-item/(?P<itemid>\d+)$', views.add_item, name='add-item'),

    url(r'^get_attrList_json$', views.get_attrList_json),

    url(r'^get_list/(?P<itemid>[^/]+)$', views.get_list),
    url(r'^save$',views.save),

    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),
]