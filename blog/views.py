from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from .forms import AddUserCreatingForm, AddUserLoginForm, UserProfileEditForm
from .models import AddUser
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def index(request):
    return render(request, 'index.html')

class Register(generic.CreateView):
    template_name = 'catalog/register.html'
    form_class = AddUserCreatingForm
    success_url = reverse_lazy('login')

class Login(FormView):
    template_name = 'catalog/login.html'
    form_class = AddUserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверное имя пользователя или пароль.")
            return self.form_invalid(form)  # возвращаем форму с ошибками


class UserProfileListView(generic.ListView):
    model = AddUser
    template_name = 'catalog/profile.html'

def logout_user(request):
    logout(request)
    return render(request, 'catalog/logout.html')

def create_user(request):
    if request.method == 'POST':
        form = AddUserCreatingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return render(request, 'catalog/login.html')
    else:
        form = AddUserCreatingForm()
    return render(request, 'catalog/register.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserProfileEditView(generic.UpdateView):
    model = AddUser
    form_class = UserProfileEditForm
    template_name = 'catalog/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user  # получаем текущего пользователя

@login_required
def delete_user(request):
    user = request.user
    user.delete() # удаляем профиль пользователя
    return redirect('index') # перенаправление на главную страницу после удаления