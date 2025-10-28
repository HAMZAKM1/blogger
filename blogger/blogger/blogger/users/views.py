from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import RegisterForm, ProfileForm
from .models import Notification
from blog.models import Post

User = get_user_model()


# -----------------------------
# 🔔 Notifications
# -----------------------------
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'users/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return HttpResponseRedirect(reverse('users:notifications'))


@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return HttpResponseRedirect(reverse('users:notifications'))


# -----------------------------
# 📝 Register View
# -----------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('blog:post_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# -----------------------------
# 🔐 Login View
# -----------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url or 'blog:post_list')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/login.html', {'form': form})


# -----------------------------
# 🚪 Logout View
# -----------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('users:login')


# -----------------------------
# ⚙️ Settings Page
# -----------------------------
@login_required
def settings_view(request):
    return render(request, 'users/settings.html')


# -----------------------------
# 👤 Profile Page
# -----------------------------
@login_required
def profile(request):
    return render(request, 'users/profile.html')


# -----------------------------
# ✏️ Edit Profile
# -----------------------------
@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated.")
        return redirect('users:profile')

    return render(request, 'users/edit_profile.html', {'form': form})


# -----------------------------
# 🧑‍💻 User's Posts Page
# -----------------------------
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/user_posts.html', {
        'author': user,
        'posts': page_obj,
    })
@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('users:login')  # Or any other route
    return render(request, 'users/delete_account_confirm.html')