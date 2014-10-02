#from django.shortcuts import render
# Create your views here.

from django.shortcuts import render_to_response
from blog.models import Post, Comment
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from forms import MyRegistrationForm
from forms import PostForm, CommentForm
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from calendar import HTMLCalendar
from datetime import date

def blogs(request):
    if not(request.user.is_authenticated()):
       request.user.username = 'None'

    return render_to_response('blogs.html',
           {'blogs': Post.objects.all().order_by('-published_date'),
            'user': request.user,
            'calendar': HTMLCalendar(6).formatmonth(date.today().year, date.today().month), }, context_instance=RequestContext(request))

def blog(request, post_id = 1):
    if not(request.user.is_authenticated()):
       request.user.username = 'None'

    return render_to_response('blog.html',
           {'post': Post.objects.get(id = post_id),
            'user': request.user,
            'calendar': HTMLCalendar(6).formatmonth(date.today().year, date.today().month), })

def tagpage(request, tag):
    posts = Post.objects.filter(tags__name = tag)
    return render_to_response('tagpage.html',
        {'posts': posts, 'tag': tag})

from django.contrib.auth.forms import UserCreationForm

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/blogs/')
    return HttpResponseRedirect('/register/')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        f = form.save(commit = False)
        f.author = request.user
        if request.FILES:
            f.docfile = request.FILES['docfile']
        f.save()
        return HttpResponseRedirect('/blogs/')
    return render_to_response('post.html',
        {'user': request.user,
         'form': form},  context_instance=RequestContext(request))

def register(request):
    # 2nd time around
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
           form.save()
           return HttpResponseRedirect('/blogs/')
        return render(request, 'register.html', {'form': form})

    # 1st time visit
    args = {}
    args.update(csrf(request))
    # form with no input
    args['form'] = MyRegistrationForm()
    return render_to_response('register.html', args)

def register_success(request):
    return render_to_response('register_success.html')

def about(request):
    return render_to_response('about.html', {'calendar': HTMLCalendar(6).formatmonth(date.today().year, date.today().month)})

def comment(request, post_id = 1):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id = post_id)
    if form.is_valid():
        f = form.save(commit = False)
        f.author = request.user
        f.post = post
        f.save()
        return HttpResponseRedirect('/blogs/')

    if not(request.user.is_authenticated()):
        request.user.username = 'None'
    post = Post.objects.get(id = post_id)
    return render_to_response('comment.html',
           {'comments': post.comment_set.all(),
            'user': request.user,
            'form': form,
            'blog_id': post_id},  context_instance=RequestContext(request))
