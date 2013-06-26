from django.views.generic import ListView, DetailView
from .models import Link, UserProfile, Vote
from .forms import UserProfileForm
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404


# class Vote(models.Model):
#     voter = models.ForeignKey(User)
#     link = models.ForeignKey(Link)


class LinkListView(ListView):
    model = Link
    queryset = Link.with_votes.all()
    paginate_by = 5



def voteup(request, id):
    # request.session['karma'] = request.session['karma'] + 1
    objlink = Link.objects.get(pk=id)
    newvote = Vote.objects.create(link_id=id, voter=request.user)
    return HttpResponseRedirect('/')


def votedown(request, id):
    # request.session['karma'] = request.session['karma'] + 1
    objlink = Link.objects.get(pk=id)
    if objlink:
        votelist = Vote.objects.filter(link_id=id, voter=request.user)
        if votelist:
            votelist.delete()
        # vote = Vote.objects.get(link_id=id, voter=request.user)
    return HttpResponseRedirect('/')



def thanksharing(request, id):
    template = 'thanksharing.html'
    try:
        request.session['karma'] = request.session['karma'] + 1
    except:
        request.session['karma'] = 1
    obj = Link.objects.get(pk=id)
    data = {
        'newsobj': obj
    }
    return render_to_response(template, data,
                              context_instance=RequestContext(request))


def sharenews(request, id):
    template = 'sharenews.html'

    obj = Link.objects.get(pk=id)
    data = {
        'newsobj': obj
    }
    return render_to_response(template, data,
                              context_instance=RequestContext(request))


def detailnews(request, id):
    template = 'detailnews.html'
    obj = Link.objects.get(pk=id)
    data = {
        'newsobj': obj
    }
    return render_to_response(template, data,
                              context_instance=RequestContext(request))


def aboutus(request):
    template = 'aboutus.html'
    data = {
    }
    return render_to_response(template, data,
                              context_instance=RequestContext(request))


def participate(request):
    template = 'participate.html'
    data = {
    }
    return render_to_response(template, data,
                              context_instance=RequestContext(request))


class SimplePageView(ListView):
    model = Link


class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})
