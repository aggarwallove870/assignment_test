
from django.urls import path
from app import views


urlpatterns = [
    path("home",views.home_page,name="home"),
    path("",views.login_page,name="login_page"),
    path("register/",views.register,name="register"),
    path("blogs",views.all_blogs,name="all_blogs"),
    path('blog/<int:id>/', views.show_blog, name='show_blog'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('blog/<int:pk>/share/', views.share_blog_post, name='share_blog_post'),
    path('like_comment/', views.like_comment, name='like_comment'),
 
]
