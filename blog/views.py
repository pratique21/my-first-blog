from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm, RegisterForm
from django.contrib.auth.decorators import login_required
import pdb

# Create your views here.
# View for list of posts

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #This returns a QuerySet that is used by Django to display the data on the actual page

    #posts = Post.objects.order_by('-published_date')

    # This one will only show those entries which have a published time associated with them
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    # request is the address that the user types in. To this we append the name in second argument and the last part
    # says what the contents are, in this case, multiple posts or list of posts.

    return render(request, 'blog/post_list.html', {'posts':posts})

# view for post detail page

def post_detail(request, pk):
    #Using this function, we will be dirceted to a 404 not found page if the particular address does not correspond to a
    #primary key in the DB for the entries of the blog post

    post = get_object_or_404(Post, pk=pk)
    #pdb.set_trace()
    #Here the content is a singular post so that makes the last argument different from the one before.

    return render(request, 'blog/post_detail.html', {'post': post})

# view for add new post page

@login_required
def post_new(request):
    # POST is one of the methods in html for the data received from user on the page.

    if request.method == "POST":

        # request is where the information entered in the form is stored. Here we create a PostForm object
        # using the data from the form

        form = PostForm(request.POST)

        # Django has its own set of validations that makes sure the fields are not empty etc

        if form.is_valid():

            # We save but do not commit here because there are two attributes of post object that the user does not provide
            # in the form. We provide those in next two lines and then save again in the end.

            post = form.save(commit=False)
            post.author = request.user
            # Commenting the line below to implement save as draft by removing the published date attribute temporarily
            # until it is to be published
            # post.published_date = timezone.now()
            post.save()

            # redirect is a function that will, upon saving of the entered information, redirect to a different link
            # which in this case is the post_detail page that lists all the blog entries.

            return redirect('post_detail', pk=post.pk)
    else:

        # This is the default view, an empty form, if the user goes to the page for the first time.
        # Note: this page has two views: the empty one and then the one after pressing submit.

        form = PostForm()

        # Here the content we are dealing with is an object of form form and not post, therefore the change in last argument

    return render(request, 'blog/post_edit.html', {'form': form})

# view for blog edit

@login_required
def post_edit(request, pk):

    # This view is mostly the same as creating a new post with the difference that in case no changes are made
    # we use instance=post to mean that we re-create the object with the existing data so that it is not lost.

    post = get_object_or_404(Post, pk=pk)
    if request.method=="POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# View for the page that shows the unpublished drafts

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# This is the view for the publish page for drafts

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #pdb.set_trace()
    post.publish()
    #return render(request,'blog/post_detail.html', {'post': post})
    return redirect('post_detail', pk=pk)

# Delete post view

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    #No need pk for redirect to list of post because it is all of the posts
    return redirect('post_list')

# Add a comment on a post

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})

# for comment approval and deletion

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

#View for register page

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        else:
            form = RegisterForm()
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})