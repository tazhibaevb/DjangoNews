from django.db.models import F
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegistrationForm, UserLoginForm, ContactForm
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegistrationForm()
    return render(request, 'news/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = UserLoginForm()
        return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['content'],
                             'bahatoktobekov7@gmail.com',
                             ['kulbarakovich@gmail.com', 'bektur1902@gmail.com'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/contact.html', {'form': form})

# def test(request):
#     objects = ['baha', 'janarbek', 'amina', 'dilmurat', 'ajar', 'baystan', 'beka']
#     paginator = Paginator(objects, 3)
#     page_num = request.GET.get('page', 1)
#     page_objects = paginator.get_page(page_num)
#     return render(request, 'news/test.html', {'page_obj': page_objects})

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'

    # extra_context = {'title': 'Это то что я хотел'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')
# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id']).select_related('category')
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'

    def get_context_data(self, **kwargs):
        context = super(ViewNews, self).get_context_data()
        self.object.views = F('views') +1
        self.object.save()
        self.object.refresh_from_db()
        return context
# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})

class CreateViews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect('/')
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

