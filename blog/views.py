from django.shortcuts import render

# Create your views here.
# View for list of posts

def post_list(request):
    return render(request, 'blog/post_list.html', {})
