from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Suggestion, Profile, Tag, Type, Category
from .forms import *
import random

paginate = 3

# Create your views here.
class Index(ListView):
    model = Suggestion
    template_name = "index.html"
    paginate_by = paginate
    #queryset = Suggestion.objects.filter(status = True).order_by('ranking')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_image'] = "https://via.placeholder.com/1900x1200?text=Index+View"
        context['subpage_title'] = ""
        context['button_filter'] = "all"
        context['button_slug'] = "all"
        return context  
    
    def get_queryset(self):
        srch = self.request.GET.get("search")
        if srch:
            queryset = Suggestion.objects.filter(Q(title__icontains=srch)|Q(content__icontains=srch), status= True).distinct().order_by('-ranking')
        else:
            queryset = Suggestion.objects.filter(status = True).order_by('-ranking')
        return queryset

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog:index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

class EditProfile(UpdateView):
    model = Profile
    template_name = 'accounts/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('blog:index')

    #to avoid users edit other users profiles.
    def dispatch(self, request, *args, **kwargs):
        self_object = self.get_object()
        if not request.user == self_object.user:
            return redirect('blog:index')
        return super(EditProfile, self).dispatch(request, *args, **kwargs)
    

class MyPosts(ListView):
    model = Suggestion
    template_name = 'index.html'
    paginate_by = paginate

    def get_queryset(self):
        srch = self.request.GET.get("search")
        if srch:
            queryset = Suggestion.objects.filter(Q(title__icontains=srch)|Q(content__icontains=srch), Q(author=self.request.user), status= True).distinct().order_by('-ranking')
        else:
            queryset = Suggestion.objects.filter(Q(status=True), Q(author=self.request.user)).order_by('-ranking')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_image'] = "https://via.placeholder.com/1900x1200?text=My+Posts+View"
        context['subpage_title'] = " | My suggestions"
        context['button_filter'] = "my-posts"
        context['button_slug'] = "all"
        return context  

class PostDetail(DetailView):
    model = Suggestion
    template_name = 'post.html'

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        suggest = self.get_object()
        old_rank = suggest.ranking
        new_rank = old_rank+1
        suggest.ranking = new_rank
        suggest.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    
class authorSuggestionList(ListView):
    model = Suggestion
    template_name = 'index.html'
    paginate_by = paginate

    def get_queryset(self):
        srch = self.request.GET.get("search")
        if srch:
            queryset = Suggestion.objects.filter(Q(title__icontains=srch)|Q(content__icontains=srch), Q( author__profile__slug = self.kwargs['slug']), status= True).distinct().order_by('-ranking')
        else:
            queryset = Suggestion.objects.filter(Q( status = True ), Q( author__profile__slug = self.kwargs['slug'])).order_by('-ranking')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_image'] = "https://via.placeholder.com/1900x1200?text=author+Suggestion+List+View"
        context['subpage_title'] = " | Suggested by"
        context['button_filter'] = "posted-by"
        context['button_slug'] = self.kwargs['slug']
        return context  




class ContributionList(ListView):
    model = Profile
    template_name = 'contributor.html'
    paginate_by = paginate

    def get_queryset(self):
        return Profile.objects.filter(status = True).order_by('-contribution')

class SuggestionCreateView(CreateView):
    form_class = SuggestionForm
    template_name = 'newpost.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        prof = Profile.objects.get(id=self.request.user.id)
        old_cont = prof.contribution
        new_cont = old_cont+1
        prof.contribution = new_cont
        prof.save()
        return super().form_valid(form)

class SuggestionUpdateView(UpdateView):
    model = Suggestion
    form_class = SuggestionForm
    template_name = 'newpost.html'
    success_url = reverse_lazy('blog:index')

    #to avoid users edit other user's suggestions.
    def dispatch(self, request, *args, **kwargs):
        self_object = self.get_object()
        if not request.user == self_object.author:
            return redirect('blog:index')
        return super(SuggestionUpdateView, self).dispatch(request, *args, **kwargs)

class SuggestionDeleteView(DeleteView):
    model = Suggestion
    success_url = reverse_lazy('blog:index')
    template_name='confirm_delete.html'

    #to avoid users edit other user's suggestions.
    def dispatch(self, request, *args, **kwargs):
        self_object = self.get_object()
        if not request.user == self_object.author:
            return redirect('blog:index')
        return super(SuggestionDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        suggestion_to_delete = Suggestion.objects.get(slug=self.kwargs['slug'])
        suggestion_to_delete.status = False
        suggestion_to_delete.save()
        return redirect('blog:index')


class SlugSuggestionList(ListView):
    model = Suggestion
    template_name = 'index.html'
    paginate_by = paginate

    def get_queryset(self):
        srch = self.request.GET.get("search")
        filter_param = self.kwargs['filter']
        if filter_param == 'tag':
            if srch:
                queryset = Suggestion.objects.filter(Q(title__icontains=srch)|Q(content__icontains=srch), Q( tag__slug = self.kwargs['slug']), status= True).distinct().order_by('-ranking')
            else:
                queryset = Suggestion.objects.filter(Q( status = True ), Q( tag__slug = self.kwargs['slug'])).order_by('-ranking')
        elif filter_param == 'type':
            if srch:
                queryset = Suggestion.objects.filter(Q(title__icontains=srch)|Q(content__icontains=srch), Q( type__slug = self.kwargs['slug']), status= True).distinct().order_by('-ranking')
            else:
                queryset = Suggestion.objects.filter(Q( status = True ), Q( type__slug = self.kwargs['slug'])).order_by('-ranking')
        elif filter_param == 'category':
            if srch:
                queryset = Suggestion.objects.filter(Q(title__icontains=srch)|Q(content__icontains=srch), Q( category__slug = self.kwargs['slug']), status= True).distinct().order_by('-ranking')
            else:
                queryset = Suggestion.objects.filter(Q( status = True ), Q( category__slug = self.kwargs['slug'])).order_by('-ranking')
        else:
            queryset = Suggestion.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_param = self.kwargs['filter']
        if filter_param == 'tag':
            tag_slug = self.kwargs['slug']
            used_tag = Tag.objects.get(slug=tag_slug)
            context['header_image'] = used_tag.image
            context['subpage_title'] = " | Tag | "+str(used_tag.name)
            context['button_filter'] = "tag"
            context['button_slug'] = tag_slug
        elif filter_param == 'type':
            type_slug = self.kwargs['slug']
            used_type = Type.objects.get(slug=type_slug)
            context['header_image'] = used_type.image
            context['subpage_title'] = " | Types | "+str(used_type.name)
            context['button_filter'] = "type"
            context['button_slug'] = type_slug
        elif filter_param == 'category':
            category_slug = self.kwargs['slug']
            used_category = Category.objects.get(slug=category_slug)
            context['header_image'] = used_category.image
            context['subpage_title'] = " | Categories | "+str(used_category.name)
            context['button_filter'] = "category"
            context['button_slug'] = category_slug
        else:
            context['header_image'] = "https://via.placeholder.com/1900x1200?text=Undefined+Suggestion+List+View"
            context['subpage_title'] = " | Undefined Filter | "+str(self.kwargs['filter'])
        return context  


def random_post(request,filter_slug,secondary_slug):
    suggestion_count = Suggestion.objects.all().count()
    random_val = random.randint(0,suggestion_count-1)
    suggestion_slug = Suggestion.objects.values_list('slug', flat=True)[random_val]
    
    if filter_slug == 'all':
        suggestion_filter = Suggestion.objects.filter(status=True)
        if(suggestion_filter):
            suggestion_count = suggestion_filter.count()
            random_val = random.randint(0,suggestion_count-1)
            suggestion_slug = suggestion_filter.values_list('slug', flat=True)[random_val]
        else:
            return redirect('blog:index')

    elif filter_slug == 'tag':
        suggestion_filter = Suggestion.objects.filter(Q( status = True ), Q( tag__slug = secondary_slug))
        if(suggestion_filter):
            suggestion_count = suggestion_filter.count()
            random_val = random.randint(0,suggestion_count-1)
            suggestion_slug = suggestion_filter.values_list('slug', flat=True)[random_val]
        else:
            return redirect('blog:index')
    elif filter_slug == 'type':
        suggestion_filter = Suggestion.objects.filter(Q( status = True ), Q( type__slug = secondary_slug))
        if(suggestion_filter):
            suggestion_count = suggestion_filter.count()
            random_val = random.randint(0,suggestion_count-1)
            suggestion_slug = suggestion_filter.values_list('slug', flat=True)[random_val]
        else:
            return redirect('blog:index')
    elif filter_slug == 'category':
        suggestion_filter = Suggestion.objects.filter(Q( status = True ), Q( category__slug = secondary_slug))
        if(suggestion_filter):
            suggestion_count = suggestion_filter.count()
            random_val = random.randint(0,suggestion_count-1)
            suggestion_slug = suggestion_filter.values_list('slug', flat=True)[random_val]
        else:
            return redirect('blog:index')
    elif filter_slug == 'my-posts':
        suggestion_filter = Suggestion.objects.filter(Q(status=True), Q(author=request.user))
        if(suggestion_filter):
            suggestion_count = suggestion_filter.count()
            random_val = random.randint(0,suggestion_count-1)
            suggestion_slug = suggestion_filter.values_list('slug', flat=True)[random_val]
        else:
            return redirect('blog:index')
    elif filter_slug == 'posted-by':
        suggestion_filter = Suggestion.objects.filter(Q( status = True ), Q( author__profile__slug = secondary_slug))
        if(suggestion_filter):
            suggestion_count = suggestion_filter.count()
            random_val = random.randint(0,suggestion_count-1)
            suggestion_slug = suggestion_filter.values_list('slug', flat=True)[random_val]
        else:
            return redirect('blog:index')
    else:
        return redirect('blog:index')

    return redirect('blog:post-detail', slug=suggestion_slug)

