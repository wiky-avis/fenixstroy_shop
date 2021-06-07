from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = 'about/about.html'


class ContactView(TemplateView):
    template_name = 'about/contact.html'
