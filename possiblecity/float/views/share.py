# portfolio/views/share.py

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from possiblecity.float.models import Project, ProjectImage
from possiblecity.float.forms import ProjectForm, ProjectImageForm

class ProjectCreateView(CreateView):
    form_class = ProjectForm
    #success_url = 'success'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.agent = self.request.user
        self.object.slug = str(slugify(form.cleaned_data['title']))
        self.object.featured = False
        self.object.enable_comments = False
        self.object.moderate_comments = False
        self.object.status = Project.STATUS_PENDING
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(ProjectCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': True})
        return context_data

class ProjectUpdateView(UpdateView):
    form_class = ProjectForm
    template_name = 'float/create_project.html'
    success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        if self.project.user.id != request.user.id:
            return HttpResponseForbidden()
        return super(ProjectUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = Project.STATUS_PENDING
        self.object.save()
        if self.object.status == Project.STATUS_PUBLISHED:
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(ProjectCreateView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'create': False})
        return context_data


class ProjectImageCreateView(CreateView):
    form_class = ProjectImageForm
    template_name = 'float/create_image.html'
    success_url = 'success'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        return super(ProjectImageCreateView, self).dispatch(*args, **kwargs)

