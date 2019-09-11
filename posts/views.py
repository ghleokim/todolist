from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# Create your views here.
def home(request):
    return redirect('posts:index')

def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)

def create(request):
    if request.method == 'POST':
        schedule = request.POST.get('schedule')
        due_date = request.POST.get('due-date')
        Post.objects.create(schedule=schedule, due_date=due_date)
        return redirect('posts:index')
    else:
        return render(request, 'posts/create.html')

def update(request, id):
    if request.method == 'POST':
        # post = Post.objects.get(id=id)
        post = get_object_or_404(Post, id=id)
        post.schedule = request.POST.get('schedule')
        post.due_date = request.POST.get('due-date')
        post.save()
        return redirect('posts:index')
    else:
        # post = Post.objects.get(id=id)
        post = get_object_or_404(Post, id=id)
        context = {
            'post': post,
        }
        return render(request, 'posts/update.html', context)

def delete(request, id):
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('posts:index')