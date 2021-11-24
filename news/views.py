from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import *
from .filters import SearchFilter 
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
 
class NewsList(ListView):
    model = Post  
    template_name = 'news_list.html' 
    context_object_name = 'news_list'
    ordering = ['-date']
    paginate_by = 10
    queryset = Post.objects.order_by('-date') 

class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.add_post', )

class NewsDetailView(DetailView):
    model = Post  
    template_name = 'news_detail.html' 
    context_object_name = 'news'

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.change_post', )
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'news'
    permission_required = ('news.delete_post', )

class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        return context
