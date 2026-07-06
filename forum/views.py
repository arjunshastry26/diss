from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .models import Discussion, Category, Comment, UserProfile
from .forms import SignUpForm, DiscussionForm, CommentForm, ProfileForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to the forum! Your account was created successfully.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'forum/signup.html', {'form': form})


def home_view(request):
    discussions = Discussion.objects.select_related('author', 'category').annotate(
        num_comments=Count('comments')
    )

    query = request.GET.get('q')
    category_id = request.GET.get('category')
    status = request.GET.get('status')

    if query:
        discussions = discussions.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    if category_id:
        discussions = discussions.filter(category_id=category_id)
    if status == 'resolved':
        discussions = discussions.filter(is_resolved=True)
    elif status == 'open':
        discussions = discussions.filter(is_resolved=False)

    paginator = Paginator(discussions, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(num_discussions=Count('discussions'))

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query or '',
        'selected_category': int(category_id) if category_id else None,
        'status': status or '',
        'total_discussions': Discussion.objects.count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'forum/home.html', context)


def discussion_detail_view(request, pk):
    discussion = get_object_or_404(
        Discussion.objects.select_related('author', 'category'), pk=pk
    )
    discussion.views += 1
    discussion.save(update_fields=['views'])

    comments = discussion.comments.select_related('author').all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to reply.')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your reply was posted.')
            return redirect('discussion_detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'discussion': discussion,
        'comments': comments,
        'form': form,
    }
    return render(request, 'forum/discussion_detail.html', context)


@login_required
def create_discussion_view(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            messages.success(request, 'Your discussion has been posted!')
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = DiscussionForm()
    return render(request, 'forum/discussion_form.html', {'form': form, 'title': 'Start a New Discussion'})


@login_required
def edit_discussion_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if discussion.author != request.user:
        messages.error(request, "You can't edit someone else's discussion.")
        return redirect('discussion_detail', pk=pk)

    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discussion updated.')
            return redirect('discussion_detail', pk=pk)
    else:
        form = DiscussionForm(instance=discussion)
    return render(request, 'forum/discussion_form.html', {'form': form, 'title': 'Edit Discussion'})


@login_required
def delete_discussion_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if discussion.author != request.user:
        messages.error(request, "You can't delete someone else's discussion.")
        return redirect('discussion_detail', pk=pk)
    if request.method == 'POST':
        discussion.delete()
        messages.success(request, 'Discussion deleted.')
        return redirect('home')
    return render(request, 'forum/discussion_confirm_delete.html', {'discussion': discussion})


@login_required
def toggle_resolved_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if discussion.author == request.user:
        discussion.is_resolved = not discussion.is_resolved
        discussion.save(update_fields=['is_resolved'])
    return redirect('discussion_detail', pk=pk)


@login_required
def toggle_like_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.user in discussion.likes.all():
        discussion.likes.remove(request.user)
    else:
        discussion.likes.add(request.user)
    return redirect('discussion_detail', pk=pk)


@login_required
def mark_solution_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.discussion.author == request.user:
        comment.is_solution = True
        comment.save(update_fields=['is_solution'])
        comment.discussion.is_resolved = True
        comment.discussion.save(update_fields=['is_resolved'])
        messages.success(request, 'Marked as the solution.')
    return redirect('discussion_detail', pk=comment.discussion.pk)


@login_required
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    discussion_pk = comment.discussion.pk
    if comment.author == request.user or comment.discussion.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    return redirect('discussion_detail', pk=discussion_pk)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    discussions = Discussion.objects.filter(author=user)
    return render(request, 'forum/profile.html', {
        'profile_user': user,
        'profile': profile,
        'discussions': discussions,
    })


@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'forum/edit_profile.html', {'form': form})


def category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    discussions = Discussion.objects.filter(category=category)
    return render(request, 'forum/category.html', {'category': category, 'discussions': discussions})
