from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification

@login_required
def notification_list(request):
    """Show notifications for the logged-in user."""
    notifications = request.user.user_notifications.order_by('-timestamp')  # Use your related_name
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })

@login_required
def mark_read(request, pk):
    """Mark a specific notification as read."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True  # Correct field name
    notification.save()
    messages.success(request, 'Notification marked as read.')
    return redirect('notifications:list')

@login_required
def mark_all_read(request):
    """Mark all unread notifications as read."""
    notifications = request.user.user_notifications.filter(is_read=False)  # Correct field name and related_name
    notifications.update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications:list')

@login_required
def delete_notification(request, pk):
    """Optionally delete a notification."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted.')
    return redirect('notifications:list')
