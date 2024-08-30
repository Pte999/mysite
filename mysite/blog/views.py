from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from .forms import PostForm
from .models import Post
from .signals import my_signal

# def get_info(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             print(form.data)
#             return HttpResponseRedirect('/blog/')
#     else:
#         form = PostForm()
#
#     return render(request, 'blog/post/form.html', {'form': form})

# class PostList(View):
#     template_name = 'blog/post/list.html'
#
#     def get(self, request):
#         post_list = Post.objects.all()
#         paginator = Paginator(post_list, 3)
#         page_number = request.GET.get('page', 1)
#         page_obj = paginator.page(page_number)
#         context = {'page_obj': page_obj}
#
#         return render(request, self.template_name, context)



# class PostDetail(View):
#     templates_name = 'blog/post/detail.html'
#
#     def get(self, request, year, month, day, post):
#         post = get_object_or_404(Post,
#                                  slug=post,
#                                  publish__year=year,
#                                  publish__month=month,
#                                  publish__day=day)
#
#         context = {'post': post}
#         return render(request, self.templates_name, context)


# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                    'blog/post/list.html',
#                    {'posts':posts})



# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post,
#                              slug=post,
#                              publish__year=year,
#                              publish__month=month,
#                              publish__day=day)
#
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})

# def form_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             print(form.changed_data)
#             user = User.objects.get(id=1)
#             form.cleaned_data['author'] = user
#             Post.objects.create(**form.cleaned_data)
#             return HttpResponseRedirect('/blog/')
#     else:
#         form = PostForm()
#     return render(request, 'blog/post/form.html', {'form': form})



@login_required
def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    my_signal.send(sender=None, param1=1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                   'blog/post/list.html',
                   {'page_obj':posts, 'num_visits':num_visits})



class UserListBoolView(ListView):

    def get(self, request, username):
        permission_code = 'blog.add_post'
        if request.user.is_authenticated and request.user.has_perm(permission_code):
            user = User.objects.get(username=request.user.username)
            qs = Post.objects.filter(author=user)

            paginator = Paginator(qs, 3)
            page_number = request.GET.get('page', 1)
            try:
                qs = paginator.page(page_number)
            except PageNotAnInteger:
                qs = paginator.page(1)
            except EmptyPage:
                qs = paginator.page(paginator.num_pages)
            return render(request,
                          'blog/post/user_list.html',
                          {'page_obj':qs})
        else:
            return HttpResponse("Залогинься!")

class PostForm(FormView):
    template_name = 'blog/post/form.html'
    form_class = PostForm
    success_url = '/blog'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PostList(ListView):
    queryset = Post.published_posts.all()
    template_name = 'blog/post/list.html'
    paginate_by = 3



class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post1'
    slug_url_kwarg = 'post'

