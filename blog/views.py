from django.shortcuts import render
from django.utils import timezone # To get timestamp 
from .models import Post # Import Post model. That's where the data is.

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts,})