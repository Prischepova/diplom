from typing import List, Optional, Type

from django.contrib.auth.decorators import login_required
# from bootstrap_modal_forms.generic import BSModalCreateView
from django.forms import ModelForm, formset_factory
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django_filters.views import FilterView

# from bootstrap_datepicker_plus.widgets import (
#     DatePickerInput,
# )
#
# from main.forms import (
#     EventFilter,
# )

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.contrib import messages

from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsOwnerOrReadOnlyUser
from .serializers import *
from .utils import *


def newsimage(request, news_id):
    # slug = request.args
    newsimage = get_object_or_404(News, slug=news_id)
    newsimage.images.all()
    NewsImage.objects.filter(news=newsimage)

    return render(request, 'main/newsimage.html', {'newsimage': newsimage, 'menu': menu, 'title': 'Новости'})


def schedule(request, schedule_id):
    # slug = request.args
    schedule = get_object_or_404(Schedule, slug=schedule_id)

    return render(request, 'main/schedule.html', {'schedule': schedule, 'menu': menu, 'title': 'Расписание'})


def indiv(request):
    indiv = Indiv.objects.all()
    return render(request, 'main/indiv.html', {'indiv': indiv, 'menu': menu, 'title': 'Индив'})


class IndivDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Indiv
    context_object_name = 'indiv_detail'
    template_name = 'main/indiv_detail.html'
    queryset = model.objects.all().select_related('user')

    # success_message = "Вы успешно записались на индивидуальную тренировку"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class IndivUpdateView(LoginRequiredMixin, CreateView):
    """
    Представление для редактирования профиля
    """
    model = Indiv
    form_class = IndivUpdateForm
    template_name = 'main/indiv_create.html'
    succes_url = '/success/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('indiv')


def payment(request):
    return render(request, 'main/payment.html', {'menu': menu, 'title': 'Оплата'})


def documents(request):
    return render(request, 'main/documents.html', {'menu': menu, 'title': 'Документы'})


class DocumentsUpdateView(SuccessMessageMixin, UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Documents
    form_class = DocumentsUpdateForm
    template_name = 'main/documents.html'
    success_message = "Успешная загрузка страховки"

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         calculated_field=self.object.calculated_field,
    #     )

    def get_object(self, queryset=None):
        return self.request.user.documents

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
            if all([form.is_valid()]):
                form.save()
            else:
                # context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(DocumentsUpdateView, self).form_valid(form)


def attendance(request):
    return render(request, 'main/attendance.html', {'menu': menu, 'title': 'Посещаемость'})


def notifications(request):
    notifications = Notifications.objects.all()
    return render(request, 'main/notifications.html',
                  {'notifications': notifications, 'menu': menu, 'title': 'Уведомления'})



def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'main/profile_detail.html'
    queryset = model.objects.all().select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'main/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class SuccessRedirectMixin:
    request: HttpRequest

    def get_success_url(self) -> str:
        return self.request.META.get("HTTP_REFERER", "/")


class NamespaceTemplateMixin:
    request: HttpRequest

    def get_template_names(self) -> List[str]:
        template_names: List[str] = super().get_template_names()  # type: ignore
        if self.request.resolver_match:
            template_names = [
                name.format(namespace=self.request.resolver_match.namespace)
                for name in template_names
            ]
        return template_names


class EventListView(NamespaceTemplateMixin, FilterView):  # type: ignore
    news = News.objects.all()
    template_name = "main/{namespace}/index.html"
    filterset_class = EventFilter
    extra_context = {
        "news": news,
        "title_text": "ListView with django-filter",
        "submit_text": "Показать",
    }


class UserAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsOwnerOrReadOnlyUser, )


class UserAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProfileAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

# class UserViewSet(viewsets.
#                   # mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   # mixins.DestroyModelMixin,
#                   mixins.ListModelMixin,
#                   GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated, )
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return User.objects.all()[:3]
#
#         return User.objects.filter(pk=pk)
#
#     @action(methods=['get'],detail=True)
#     def profile(self, request, pk=None):
#         prof = Profile.objects.get(pk=pk)
#         return Response({'prof': [prof.slug]})

# class ProfileAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ProfileAPIView(generics.ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


# class UserAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
