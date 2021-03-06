from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('create', views.create),
    path('dashboard', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('items/new', views.new),
    path('items/create', views.itemCreate),
    path('items/<int:item_id>/remove', views.remove),
    path('items/<int:item_id>/edit', views.edit),
    path('items/<int:item_id>/update', views.update),
    path('items/<int:item_id>', views.items),
    path('items/<int:item_id>/comment', views.item_comment),
    path('blog', views.blog),
    path('blog/new', views.newBlog),
    path('blog/create', views.blogCreate),
    path('blog/<int:blog_id>', views.blogs),
    path('blog/<int:blog_id>/remove', views.removeBlog),
    path('blog/<int:blog_id>/edit', views.editBlog),
    path('blog/<int:blog_id>/update', views.updateBlog),
    path('upload', views.image_upload_view),
    ]
