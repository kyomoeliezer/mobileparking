from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.views.generic import TemplateView


class YouDontHavePermission(TemplateView):
    template_name = 'perm/nopermission.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['header']='No Permission!'
        return context

