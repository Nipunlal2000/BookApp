from django.urls import path
from . import views

urlpatterns = [

    path('', views.listBook, name='listbook'),

    path('book/',views.createBook,name='createbook'),

    path('author/', views.Create_Author, name='author'),

    path('detailview/<int:book_id>/', views.detailView, name='detailview'),

    path('updateview/<int:book_id>/', views.updateView, name='updateview'),

    path('deleteview/<int:book_id>/', views.deleteView, name='deleteview'),

    path('adminbase/', views.base,name='adminbase'),

    path('search/', views.Search_Book,name='search'),

]
