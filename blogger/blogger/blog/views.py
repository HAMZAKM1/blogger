from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import NewsletterSubscriber
from django.shortcuts import render, get_object_or_404
from .models import Category, Post  # make sure Category & Post exist
from .models import Post, Comment, Notification
from .forms import PostForm, CommentForm

# Use your CustomUser
User = get_user_model()


# --------------------------------------
# 📄 Home / Post List
# --------------------------------------
def post_list(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})


# --------------------------------------
# 📄 Post Detail + Comments
# --------------------------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    related_posts = Post.objects.exclude(pk=post.pk).order_by('?')[:3]
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('users:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment was posted.")
            return redirect('blog:post_detail', pk=pk)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'related_posts': related_posts,
    })


# --------------------------------------
# 📝 Create a Post
# --------------------------------------
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully.")
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# --------------------------------------
# ✏️ Edit a Post
# --------------------------------------
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('blog:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'edit_mode': True})


# --------------------------------------
# ❌ Delete a Post
# --------------------------------------
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('blog:post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# Optional class-based delete view
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')


# --------------------------------------
# 🔍 Search Posts
# --------------------------------------
def post_search(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query).order_by('-created_at') if query else []
    return render(request, 'blog/post_search.html', {'query': query, 'results': results})


# --------------------------------------
# 🔔 Notifications for the logged-in user
# --------------------------------------
@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-timestamp')
    unread_count = user_notifications.filter(read=False).count()
    return render(request, 'notifications/notification_list.html', {
        'notifications': user_notifications,
        'unread_count': unread_count
    })


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.read = True
    notif.save()
    messages.success(request, "Marked as read.")
    return redirect('blog:notifications')


@login_required
def mark_all_read(request):
    request.user.notifications.filter(read=False).update(read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('blog:notifications')


# --------------------------------------
# 👤 Posts by Specific User
# --------------------------------------
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/user_posts.html', {'author': user, 'posts': posts})

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, '✅ You have successfully subscribed to our newsletter!')
    return redirect('blog:home')

def categories_view(request):
    """Display all blog categories."""
    categories = Category.objects.all().order_by('name')
    return render(request, 'blog/categories.html', {'categories': categories})


def category_posts_view(request, slug):
    """Display all posts under a specific category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts,
    })
