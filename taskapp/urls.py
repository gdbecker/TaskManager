from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'taskapp'

urlpatterns = [
    path('items/', views.ListItems.as_view(), name='items'),
    path('additem/', views.CreateItem.as_view(), name='add_item'),
    path('edititem/<int:pk>/', views.EditItem, name='edit_item'),
    path('deleteitem/<int:pk>/', views.DeleteItem.as_view(), name='delete_item'),
    path('addcategory', views.CreateCategory.as_view(), name='add_category'),
]
