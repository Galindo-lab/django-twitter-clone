from django.shortcuts import render, redirect
from . models import Profile, Post, Relationship
from . forms import UserRegisterForm, PostForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


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


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')


def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all()

    return render(request, 'twitter/profile.html', {
        'user': user,
        'posts': posts
    })


def editar(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()

    return render(request, 'twitter/editar.html', {
        'u_form': u_form,
        'p_form': p_form
    })

def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user

    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()

    return redirect('home')

