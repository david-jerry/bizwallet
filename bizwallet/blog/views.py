try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

import datetime

from category.models import Tag
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Count, F, Q, Sum
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from .forms import EmailPostForm
from .models import Post  # , Comment

User = get_user_model()

# Create your views here.
class PostList(ListView):
    model = Post
    template_name = "blog/list.html"
    ordering = ["title", "-pub_date"]
    queryset = Post.objects.all_posts()
    context_object_name = "posts"
    allow_empty = True
    paginate_by = 5
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        tags = Tag.objects.all()
        recent_posts = Post.objects.recent_posts()[:5]
        context["tags"] = tags
        context["recent_posts"] = recent_posts
        return context


class SearchPostList(ListView):
    model = Post
    template_name = "blog/search_list.html"
    ordering = ["title", "-pub_date"]
    context_object_name = "posts"
    allow_empty = True
    paginate_by = 5
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        tags = Tag.objects.all()
        recent_posts = Post.objects.recent_posts()[:5]
        context["tags"] = tags
        context["recent_posts"] = recent_posts
        return context



def tag_posts(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag], status="published")
        print("tag object id = ", object_list)

    tags = Tag.objects.all()
    recent_posts = Post.objects.recent_posts()[:5]

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    data = {
        'page': page,
        'posts': posts,
        'tags': tags,
        'recent_posts': recent_posts,
        'tag': tag
    }        
    return render(request, 'blog/tags.html', data)




def post_share(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    if not request.method == "POST":
        HttpResponseForbidden

    tags = Tag.objects.all()
    recent_posts = Post.objects.recent_posts()[:5]

    form = EmailPostForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        post_url = request.build_absolute_url(post.get_absolute_url())
        subject = f"{cd['name']} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url} \n\n {cd['name']}\'s comments: {cd['comments']}"
        send_mail(
            subject,
            message,
            "info@bizwallet.com",
            [cd['to']],
            fail_silently=False
        )
        messages.success(request, f"You have successfully shared {post.title}")
        return HttpResponseRedirect(reverse_lazy('blogs:list'))
    else:
        form = EmailPostForm()

    data = {
        'tags': tags,
        'recent_posts': recent_posts,
        'post': post, 
        'form': form
    }
    
    return render(request, 'blog/share.html', data)




def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    tags = Tag.objects.all()
    recent_posts = Post.objects.recent_posts().exclude(id=post.id)[:5]
    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.objects.all_posts().filter(tags__in=post_tags_ids).exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-pub_date')[:5]




    data = {
        "post": post,
        'recent_posts': recent_posts,
        'related_posts': related_posts,
        "tags": tags
    }
    return render(request, "blog/detail.html", data)
