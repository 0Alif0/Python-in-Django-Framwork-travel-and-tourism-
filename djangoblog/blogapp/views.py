from django.shortcuts import render, Http404, get_object_or_404, redirect
from .models import author, category, article, comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import createForm, registerUser, createAuthor, categoryForm, commentForm
from django.contrib import messages
from django.views import View


# Create your views here.
class index(View):
    template_name = "index.html"
    def get(self, request):
        post = article.objects.all()
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        paginator = Paginator(post, 8)  # Show 25 contacts per page

        page = request.GET.get('page')
        total_article = paginator.get_page(page)
        context = {
            "post": total_article
        }
        return render(request,self.template_name, context)


class getauthor(View):
    template = "profile.html"

    def get(self, request, name):
        post_author = get_object_or_404(User, username=name)
        auth = get_object_or_404(author, name=post_author.id)
        post = article.objects.filter(article_author=auth.id)
        context = {
            "auth": auth,
            "post": post
        }
        return render(request, self.template, context)


class getsingle(View):
    def get(self, request, id):
        post = get_object_or_404(article, pk=id)
        first = article.objects.first()
        last = article.objects.last()
        getComment = comment.objects.filter(post=id)
        related = article.objects.filter(category=post.category).exclude(id=id)[:4]
        form = commentForm
        context = {
            "post": post,
            "first": first,
            "last": last,
            "related": related,
            "form": form,
            "comment": getComment
        }
        return render(request, "single.html", context)

    def post(self, request, id):
        post = get_object_or_404(article, pk=id)
        form = commentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            return redirect('blog:single_post', id=id)


def getTopic(request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category=cat.id)
    paginator = Paginator(post, 4)  # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    return render(request, "category.html", {"post": total_article, "cat": cat})


class getLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:index')
        else:
            return render(request, "login.html")

    def post(self, request):
        user = request.POST.get('user')
        password = request.POST.get('pass')
        auth = authenticate(request, username=user, password=password)
        if auth is not None:
            login(request, auth)
            return redirect('blog:index')
        else:
            messages.add_message(request, messages.ERROR, 'Username or password mismatch')
            return redirect('blog:login')


def getlogout(request):
    logout(request)
    return redirect('blog:index')


def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            return redirect('blog:index')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('blog:login')


def getUpdate(request, pid):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=pid)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Article is updated successfully')
            return redirect('blog:profile')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('blog:login')


def getDelete(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pid)
        post.delete()
        messages.warning(request, 'Article is deleted successfully')
        return redirect('blog:profile')
    else:
        return redirect('blog:login')


def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            return render(request, 'logged_in_profile.html', {"post": post, "user": authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                messages.success(request, 'Author profile is created successfully')
                return redirect('blog:profile')
            return render(request, 'createauthor.html', {"form": form})

    else:
        return redirect('blog:login')


def getRegister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration successfully completed')
        return redirect('blog:login')
    return render(request, 'register.html', {"form": form})


def getCategory(request):
    query = category.objects.all()
    return render(request, 'topics.html', {"topic": query})


def createTopic(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = categoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'topic is created!')
                return redirect('blog:category')
            return render(request, 'create_topics.html', {"form": form})
        else:
            raise Http404('You are not authorized to access this page')
    else:
        return redirect('blog:login')
