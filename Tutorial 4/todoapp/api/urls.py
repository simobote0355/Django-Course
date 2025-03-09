from django.urls import path
from .views import *

urlpatterns = [
    path('todos/', ToDoListCreate.as_view(), name='list'),
    path('todos/<int:pk>', ToDoRetrieveUpdateDestroy.as_view(), name='todo_RUD'),
    path('todos/<int:pk>/complete', ToDoToggleComplete.as_view()),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]