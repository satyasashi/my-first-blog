from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
	# we are using 'forms.ModelForm' because if we use 'forms.Form' we
	# again need to write FormFields similar to fields in models.py
	# In order to get rid of that we use META class where we mention
	# we use fields from Model-Post
	class Meta:
		model = Post
		fields = ('title', 'text', )

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author', 'text')