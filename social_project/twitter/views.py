from django.shortcuts import render, redirect
from . models import Profile, Post
from . forms import UserRegisterForm, PostForm


def home(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        # guardar el post del twitt

        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
        
    else:
        form = PostForm()

    return render(request, 'twitter/newsfeed.html', {
        'posts': posts,
        'form': form
    })


def register(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        return render(request, 'twitter/register.html', {
            'form': UserRegisterForm()
        })
