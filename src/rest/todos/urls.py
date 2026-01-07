from django.urls import path
from todos.views import TodoCreateView, TodoListView

urlpatterns = [
    path('', TodoListView.as_view(), name='list'),
    path('create/', TodoCreateView.as_view(), name='create'),
]