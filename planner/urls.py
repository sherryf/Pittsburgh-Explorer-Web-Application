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
    url(r'^itinerary$', views.itinerary, name='itinerary'),

    # url(r'^add-post$', views.add_post),
    # Parses number from URL and uses it as the item_id argument to the action
    # url(r'^profile$', views.profile, name='profile'),
    #url(r'^profile/(\w+)$', views.profile, name='profile'),
    # url(r'^edit/(\d+)$', views.edit, name='edit'),
    # url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
    # url(r'^follow/(\d+)$', views.follow, name='follow'),
    # url(r'^unfollow/(\d+)$', views.unfollow, name='unfollow'),
    # url(r'^followerstream$', views.followerstream, name='followerstream'),
    # for HW6 add-in
    # url(r'^get-list-json$', views.get_list_json),
    # url(r'^get-comment-json$', views.get_comment_json),
    # url(r'^add-comment/(?P<post_id>\d+)$', views.add_comment,name='add-comment'),

    # url(r'^get-fellower-list-json$', views.get_fellower_list_json),
    # url(r'^get-profile-list-json$', views.get_profile_list_json),
    # The following URL should match any username valid in Django and
    # any token produced by the default_token_generator
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),
]