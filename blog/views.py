from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # To get timestamp 
from .models import Post, Comment # Import Post model. That's where the data is.
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts,})

# for detailed post
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post,})

# for adding new Post
# login_required is Special Django Decorator used
# such that, to access this method/page, user must login.
# This is a Special Django Decorator from 'auth'
@login_required
def post_new(request):

	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			#post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()

	return render(request, 'blog/post_edit.html', {'form': form,})

# login_required is Special Django Decorator used
# such that, to access this method/page, user must login.
# This is a Special Django Decorator from 'auth'
@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			#post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})


# function to show the list of draft posts which are not submitted.
# login_required is Special Django Decorator used
# such that, to access this method/page, user must login.
# This is a Special Django Decorator from 'auth'
@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
	return render(request, 'blog/post_draft_list.html', {'posts': posts,})


# Now in post_detail page there will be button to publish instantly
# login_required is Special Django Decorator used
# such that, to access this method/page, user must login.
# This is a Special Django Decorator from 'auth'
@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

# To remove the post or delete it
# get the Post object for particular pk.
# now using 'post object' use '.delete()' method
# Django Models have special method which can be used to delete.
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')

# Add comment to post
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST) # request.POST holds the form data
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form,})

# Approve the comments
@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

# Remove the comments
@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)