from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required as auth
from django.contrib import admin
admin.autodiscover()

from links.views import LinkListView
from links.views import aboutus, participate, detailnews, sharenews, thanksharing, voteup, votedown
from links.views import UserProfileDetailView
from links.views import UserProfileEditView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', LinkListView.as_view(), name='home'),

    url(r"^aboutus/$", aboutus, name="aboutus"),
    url(r"^participate/$", participate, name="participate"),
    url(r"^detailnews/(.+)/$", detailnews, name="detailnews"),
    url(r"^sharenews/(.+)/$", sharenews, name="sharenews"),
    url(r"^thanksharing/(.+)/$", thanksharing, name="thanksharing"),
    url(r"^vote/up/(.+)/$", voteup, name="voteup"),
    url(r"^vote/down/(.+)/$", votedown, name="votedown"),


    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login",
        name="logout"),

    url(r"^accounts/", include("registration.backends.simple.urls")),
    url(r"^users/(?P<slug>\w+)/$", UserProfileDetailView.as_view(),
        name="profile"),
    url(r"edit_profile/$", auth(UserProfileEditView.as_view()),
        name="edit_profile")
)
