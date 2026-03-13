from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import User, Post, Follow, Comment

def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    for post in posts:
        post.liked_by_user = request.user.is_authenticated and post.likes.filter(pk=request.user.pk).exists()

    return render(request, "network/index.html", {"posts": posts})

@login_required
def following(request):
    following_users = request.user.following.values_list('following', flat=True)
    posts_list = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    for post in posts:
        post.liked_by_user = post.likes.filter(pk=request.user.pk).exists()

    return render(request, "network/index.html", {"posts": posts})

def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(user=user_profile).order_by('-timestamp')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    is_following = False
    if request.user.is_authenticated and request.user != user_profile:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    for post in posts:
        post.liked_by_user = request.user.is_authenticated and post.likes.filter(pk=request.user.pk).exists()

    return render(request, "network/profile.html", {
        "profile_user": user_profile,
        "posts": posts,
        "is_following": is_following,
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        return render(request, "network/login.html", {"message": "Invalid username or password"})
    return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match"})
        if User.objects.filter(username=username).exists():
            return render(request, "network/register.html", {"message": "Username already taken"})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("index")
    return render(request, "network/register.html")

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Post.objects.create(user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({"liked": liked, "count": post.likes.count()})
    return JsonResponse({"error": "POST request required."}, status=400)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        if new_content:
            post.content = new_content
            post.save()
            return JsonResponse({"success": True, "content": post.content})
        return JsonResponse({"error": "Content cannot be empty"}, status=400)

@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    follow_relation = Follow.objects.filter(follower=request.user, following=user_to_follow)
    if follow_relation.exists():
        follow_relation.delete()
    elif user_to_follow != request.user:
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect("profile", username=username)

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        content = request.POST.get("content", "").strip()
        if content:
            comment = Comment.objects.create(user=request.user, post=post, content=content)
            return JsonResponse({
                "success": True,
                "username": comment.user.username,
                "content": comment.content,
                "timestamp": comment.timestamp.strftime("%Y-%m-%d %H:%M")
            })
        return JsonResponse({"error": "Content cannot be empty."}, status=400)
    return JsonResponse({"error": "POST request required."}, status=400)