from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.sites.models import Site, RequestSite
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from registration import signals
from registration.models import RegistrationProfile
from registration.views import RegistrationView as BaseRegistrationView

from forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    """
    Overrides registration.backends.default.views.RegistrationView

    """
    form_class = RegistrationForm

    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(email, email, password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        return ('registration_complete', (), {})


class CustomLoginView(TemplateView):
    """
    Change template context name of form to login_form

    """
    template_name = 'course-intro.html'

    def post(self, *argz, **kwargs):
        ret = login(self.request, template_name=CustomLoginView.template_name)
        if type(ret) is TemplateResponse:
            ret.context_data['login_form'] = ret.context_data.pop('form')
        return ret