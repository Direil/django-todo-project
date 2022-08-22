from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(
        template_name='tasks/list.html'), name='list'),
    path('update_task/<slug:slug>', views.TaskUpdateView.as_view(), name='update_task'),
    path('delete_task/<slug:slug>', views.TaskDeleteView.as_view(), name='delete_task'),
]
