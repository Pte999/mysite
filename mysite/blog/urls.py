from django.urls import path
from .views import PostList, PostDetail, PostForm, post_list, UserListBoolView

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', PostDetail.as_view(), name='post_detail'),
    path('form/', PostForm.as_view(), name='post_form'),
    path('<str:username>/', UserListBoolView.as_view()),

]