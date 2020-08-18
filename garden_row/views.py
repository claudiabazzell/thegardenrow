from .forms import ImageForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Item
from .models import Blog
from .models import Image
from .models import ItemComment

import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def create(request):

    errors = User.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    new_user = User.objects.register(request.POST)
    request.session['user_id'] = new_user.id
    request.session['first_name'] = new_user.first_name
    return redirect('/dashboard')


def login(request):
    result = User.objects.authenticate(
        request.POST['email'], request.POST['password'])
    if result == False:
        messages.error(request, "Invalid Email/Password", extra_tags='login')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name

        return redirect('/dashboard')
    return redirect('/')


def success(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    items = user.item_set.all()
    for item in items:
        item.item_name = item.item_name
        item.quantity = item.quantity
    context = {
        'user': user,
        'items': Item.objects.all(),
        'images': Image.objects.all(),
        'form': ImageForm()
    }
    return render(request, 'hello_dash.html', context)


def signUp(request):
    request.session.clear()

    return redirect('/register')


def logout(request):
    request.session.clear()

    return redirect('/')


def new(request):
    return render(request, 'new.html')


def itemCreate(request):
    errors = Item.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='new')
            return redirect('/items/new')
    user = User.objects.get(id=request.session['user_id'])
    n = request.POST.copy()
    n['user'] = user
    item = Item.objects.createItem(n)
    return redirect('/dashboard')


def blogCreate(request):
    errors = Blog.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='new')
            return redirect('/blog/new')
    user = User.objects.get(id=request.session['user_id'])
    n = request.POST.copy()
    n['user'] = user

    blog = Blog.objects.createBlog(n)
    return redirect('/blog')


def newBlog(request):
    return render(request, 'new_blog.html')

def blog(request):
    context = {
        'blogs': Blog.objects.all()
    }
    return render(request, 'blogs.html', context)


def blogs(request, blog_id):
    one_blog = Blog.objects.get(id=blog_id)
    context = {
        'blog': one_blog
    }
    return render(request, 'blog_details.html', context)


def removeBlog(request, blog_id):
    to_delete = Blog.objects.get(id=blog_id)
    to_delete.delete()
    return redirect('/blog')


def editBlog(request, blog_id):
    one_blog = Blog.objects.get(id=blog_id)
    context = {
        'blog': one_blog
    }
    return render(request, 'edit_blog.html', context)


def updateBlog(request, blog_id):
    errors = Blog.objects.validate(request.POST)
    if errors:
        for field, value in errors.blogs():
            messages.error(request, value, extra_tags='edit')
            return redirect('/blog/' + str(title) + '/edit')
    to_update = Blog.objects.get(id=blog_id)
    to_update.tite = request.POST['title']
    to_update.description = request.POST['description']
    to_update.save()
    return redirect('/blog')


def remove(request, item_id):
    to_delete = Item.objects.get(id=item_id)
    to_delete.delete()
    return redirect('/dashboard')


def edit(request, item_id):
    one_item = Item.objects.get(id=item_id)
    context = {
        'item': one_item
    }
    return render(request, 'edit.html', context)


def update(request, item_id):
    errors = Item.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='edit')
            return redirect('/items/' + str(item_id) + '/edit')
    to_update = Item.objects.get(id=item_id)
    to_update.item_name = request.POST['item_name']
    to_update.quantity = request.POST['quantity']
    to_update.description = request.POST['description']
    to_update.save()
    return redirect('/dashboard')


def items(request, item_id):
    one_item = Item.objects.get(id=item_id)
    comments = ItemComment.objects.filter(item=one_item)
    context = {
        'item': one_item,
        'comments': comments
    }
    return render(request, 'details.html', context)


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            img = Image.objects.createImg(img_obj)
            return redirect('/dashboard')


def item_comment(request, item_id):
    errors = ItemComment.objects.validate(request.POST)
    if errors:
        for field, value in errors.items():
            messages.error(request, value, extra_tags='new')
            return redirect('/item/comment')
    user = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=item_id)
    n = request.POST.copy()
    n['user'] = user
    n['item'] = item
    comment = ItemComment.objects.createComment(n)
    return redirect('/items/' + str(item_id))
