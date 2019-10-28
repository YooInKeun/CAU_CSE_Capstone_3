from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

from .forms import CreateUserForm, ProfileForm
from django.urls import reverse_lazy

class CreateUserView(CreateView):
    template_name = 'signup.html'
    form_class =  CreateUserForm
    success_url = 'done/'

class RegisteredView(TemplateView):
    template_name = 'signup_done.html'

class ConfirmIsValidUserView(LoginView):
    template_name = 'registration/login.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        http_method = str(self.request).split()[1] 

        if http_method == 'POST' and self.content_type is None:
            context.update({
                'form_invalid_message': '입력 정보가 잘못되었습니다',
            })

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

class UserProfileView(TemplateView):
    template_name = 'profile.html'
    