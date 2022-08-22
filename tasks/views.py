from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.utils.timezone import make_aware
from django.views.generic import DeleteView, ListView, UpdateView
from unidecode import unidecode

from .forms import DateRangeForm, TaskForm
from .models import *


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.slug = slugify(unidecode(form.cleaned_data.get('title')))
            slug_legnth = Task.objects.filter(slug__startswith=task.slug).count()
            if slug_legnth >=1: 
                task.slug += f"-{slug_legnth}"
            task.save()
        return redirect('/')
        

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        start_date = make_aware(datetime.strptime(self.request.GET.get('start_date', '01-01-1997'), '%d-%m-%Y'))
        end_date = make_aware(datetime.strptime(self.request.GET.get('end_date', '01-01-2100'), '%d-%m-%Y'))
        tasks = Task.objects.filter(
            user=self.request.user, title__iregex=q, created__range=(start_date, end_date)).order_by('-created')
        return tasks

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = TaskForm()
        data['date_form'] = DateRangeForm()
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        data['parameters'] = "&" + parameters if parameters != '' else ''
        return data

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'complete']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.user:
            return True
        return False
