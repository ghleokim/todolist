from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from decouple import config
import requests

token = config("telegramTOKEN")
chat_ids = set()

# Create your views here.
def home(request):
    getId(request)
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

        for chid in chat_ids:
            txt = f'added to-do list\n    schedule:[{schedule}] due:[{due_date}].'#🗓 
            url = f'https://api.telegram.org/bot{token}/sendMessage?text={txt}&chat_id={chid}'
            requests.get(url)

        return redirect('posts:index')
    else:
        
        return render(request, 'posts/create.html')

def update(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        print(post)
        fpost = post
        post.schedule = request.POST.get('schedule')
        post.due_date = request.POST.get('due-date')
        post.save()

        for chid in chat_ids:
            txt = f'updated to-do list\n    from schedule:[{fpost.schedule}] due:[{fpost.due_date}]\n    to schedule:[{post.schedule}] due:[{post.due_date}].'#🛠 
            url = f'https://api.telegram.org/bot{token}/sendMessage?text={txt}&chat_id={chid}'
            requests.get(url)

        return redirect('posts:index')
    else:
        post = get_object_or_404(Post, id=id)
        context = {
            'post': post,
        }
        return render(request, 'posts/update.html', context)

def delete(request, id):
    post = get_object_or_404(Post, id=id)
    fpost = post
    post.delete()

    for chid in chat_ids:
            txt = f'deleted to-do list\n    schedule:[{fpost.schedule}] due:[{fpost.due_date}]'#🗑 
            url = f'https://api.telegram.org/bot{token}/sendMessage?text={txt}&chat_id={chid}'
            print(url+txt)
            requests.get(url)

    return redirect('posts:index')

def getId(request):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    getUpdates = requests.get(url)
    for res in getUpdates.json().get('result'):
        chat_ids.add(res.get('message').get('from').get('id'))
    print(chat_ids)
