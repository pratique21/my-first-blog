from django import forms
from .models import Post

# django provides the basic form structure and we create a PostForm object
# that uses a specific type of form called ModelForm
# A ModelForm converts the data from the form into a model object, which in this case is the Post object
class PostForm(forms.ModelForm):
    # I do not know what the meta means, but it is part of the syntax for the form
    class Meta:
        # Later on, we can access the Post.title and Post.text in the html for displaying purposes
        model = Post
        fields = ('title','text',)
