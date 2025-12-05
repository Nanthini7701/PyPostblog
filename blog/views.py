from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Count
from .models import Post, Comment
from .forms import RegisterForm, PostForm, CommentForm
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, "blog/profile.html", {
        "profile": profile,
        "posts": posts,
    })
@login_required
def settings_view(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("blog:profile")

    return render(request, "blog/settings.html", {"form": form})
def post_list(request):
    q = request.GET.get("q", "")
    posts = Post.objects.filter(published=True)
    if q:
        posts = posts.filter(title__icontains=q)

    trending = (
        Post.objects.filter(published=True)
        .annotate(num_likes=Count("likes"))
        .order_by("-num_likes", "-created_at")[:5]
    )

    context = {
        "posts": posts,
        "trending": trending,
    }
    return render(request, "blog/home.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comment_form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.post = post
            c.user = request.user
            c.save()
            messages.success(request, "Comment added.")
            return redirect(post.get_absolute_url())

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comment_form": comment_form},
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Post created.")
        return redirect(post.get_absolute_url())
    return render(request, "blog/post_form.html", {"form": form, "title": "New Post"})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("Not allowed")
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated.")
        return redirect(post.get_absolute_url())
    return render(
        request, "blog/post_form.html", {"form": form, "post": post, "title": "Edit Post"}
    )


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("blog:post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})


@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "total_likes": post.total_likes()})
    return redirect(post.get_absolute_url())


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("blog:post_list")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
