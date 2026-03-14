from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.db.models import Q
from django.forms.models import modelform_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import classonlymethod, method_decorator
from django.views.generic import TemplateView, View, RedirectView, CreateView, UpdateView, DeleteView, FormView, \
    DetailView, ListView

from posts.decorators import measure_execution_time
from posts.forms import PostForm, PostCreateForm, PostEditForm, PostDeleteForm, PostSearchForm, CommentFormSet
from posts.mixins import TimeRestrictedMixin
from posts.models import Post

class IndexView(TemplateView):
    # template_name = 'common/index-test.html'
    # extra_context = {
    #     'current_time': datetime.now(),
    # }
    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        kwargs.update({'current_time': datetime.now()})
        return kwargs

    template_name = 'common/index-test.html'
    # def get_template_names(self):
    #     if self.request.user.is_authenticated:
    #         return ['common/index-test.html']
    #     return ['index.html']

@method_decorator(measure_execution_time, name='dispatch')
class DashboardView(ListView):
    model = Post
    template_name = 'posts/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 4
    form_class = PostSearchForm

    def get_context_data(self, **kwargs):
        kwargs.update({'search_form': self.form_class()})
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_value = self.request.GET.get('query')
        if search_value:
            queryset = queryset.filter(
                Q(title__icontains=search_value) |
                Q(content__icontains=search_value) |
                Q(author__icontains=search_value)
            )
        return queryset

# def dashboard(request):
#     search_form = PostSearchForm(request.GET)
#     posts = Post.objects.all()
#     if request.method == 'GET' and search_form.is_valid():
#         query = search_form.cleaned_data.get('query')
#         posts = posts.filter(
#             Q(title__icontains=query) | Q(content__icontains=query) | Q(author__icontains=query)
#         )
#
#     context = {
#         'posts': posts,
#         'search_form': search_form,
#     }
#
#     return render(request, 'posts/dashboard.html', context)

#example of class-based view without using Django's built-in CBVs
# class MyView:
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             return self.get(request, *args, **kwargs)
#         elif request.method == 'POST':
#             return self.post(request, *args, **kwargs)
#         else:
#             return HttpResponse(status=405)
#
#     @classonlymethod
#     def as_view(cls):
#         def view(request, *args, **kwargs):
#             self = cls()
#             return self.dispatch(request, *args, **kwargs)
#         return view


def welcome_message(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('welcome')
    context = {'form': form}
    return render(request, 'index.html', context)


def navigation_view(request):
    return HttpResponse("This is the navigation view.")

#@login_required
class AddPostView(LoginRequiredMixin,TimeRestrictedMixin,CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('dashboard')
# def add_post(request):
#     form = PostCreateForm(request.POST or None, request.FILES or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('dashboard')
#     return render(request, 'posts/add-post.html', {'form': form})


class EditPostView(UpdateView):
    model = Post
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('dashboard')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return modelform_factory(Post, fields='__all__')
        return modelform_factory(Post, fields=('content',))

# def edit_post(request, post_id):
#     post = Post.objects.get(id=post_id)
#     form = PostEditForm(request.POST or None, instance=post)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('dashboard')
#     return render(request, 'posts/edit-post.html', {'form': form})


class DeletePostView(DeleteView, FormView):
    model = Post
    form_class = PostDeleteForm
    template_name = 'posts/delete-post.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = self.model.objects.get(pk=pk)
        return post.__dict__

# def delete_post(request, post_id):
#     post = Post.objects.get(id=post_id)
#     form = PostDeleteForm(instance=post)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('dashboard')
#     return render(request, 'posts/delete-post.html', {'form': form})

class MyRedirectView(RedirectView):
    #both static ways to specify the redirect URL
    #url = 'http://127.0.0.1:8000/'
    #pattern_name = 'dashboard'

    def get_redirect_url(self, *args, **kwargs):
        #dynamic way to specify the redirect URL
        if self.request.user.is_authenticated:
            return reverse('welcome')
        else:
            return reverse('dashboard')

class PostDetailsView(DetailView):
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_set'] = CommentFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form_set = CommentFormSet(request.POST)
        if comment_form_set.is_valid():
            for form in comment_form_set:
                comment = form.save(commit=False)
                comment.author = request.user.username
                comment.post = self.object
                comment.save()
            return redirect('post-details', pk=self.object.id)

# def post_details(request, pk):
#     post = Post.objects.get(id=pk)
#     comment_form_set = CommentFormSet(request.POST or None)
#     if request.method == 'POST' and comment_form_set.is_valid():
#         for form in comment_form_set:
#             comment = form.save(commit=False)
#             comment.author = request.user.username
#             comment.post = post
#             comment.save()
#             return redirect('post-details', pk=post.id)
#     context = {
#         'post': post,
#         'form_set': comment_form_set,
#     }
#     return render(request, 'posts/post-details.html', context)
from django.contrib.auth import get_user_model
User = get_user_model()

def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == 'POST':
        user = User.objects.create_user(username=username, password=password)






