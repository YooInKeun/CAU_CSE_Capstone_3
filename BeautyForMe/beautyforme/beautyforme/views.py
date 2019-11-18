from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from cosmetic.models import *
import datetime


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        try:
            print('유저 로그인 시간: ', self.request.user.last_login)
            print('현재 시간: ', timezone.now())
            if((timezone.now() - self.request.user.last_login).seconds < 0.2):
                context['is_alarm_time'] = True
            queryset = User_Cosmetic.objects.filter(alarm_cycle=9999999)
            alarm_candidates = User_Cosmetic.objects.filter(user=self.request.user, is_consent_alarm=True)
            for alarm_candidate in alarm_candidates:
                expiration_date = datetime.datetime.strptime(str(alarm_candidate.expiration_date), '%Y-%m-%d')
                if (expiration_date-timezone.now()).days + 1 < alarm_candidate.alarm_cycle:
                    user_cosmetic = User_Cosmetic.objects.filter(user=self.request.user, pk=alarm_candidate.id)
                    user_cosmetic.expiration_date= datetime.datetime.strptime(str(alarm_candidate.expiration_date), '%Y-%m-%d').date()
                    queryset |= user_cosmetic
            context['alarm_cosmetics'] = queryset
            if queryset.exists() is False:
                context['is_alarm_time'] = False
        except:
            print("유저는 아직 로그인 하지 않았습니다")
        return context


class PreparationView(TemplateView):
    template_name = 'preparation.html'