from django.shortcuts import render, get_object_or_404
from django.utils import timezone # To get timestamp 
from .models import Post # Import Post model. That's where the data is.

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts,})

# for detailed post
def post_detail(request, pk):
	# post = Post.objects.get(pk=pk)
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post,})