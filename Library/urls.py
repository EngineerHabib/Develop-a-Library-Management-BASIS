
from django.urls import path
from . import views


urlpatterns = [

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Book Management
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/update/<int:pk>/', views.update_book, name='update_book'),
    path('books/delete/<int:pk>/', views.delete_book, name='delete_book'),

    # Issue and Return Books
    path('books/issue/<int:pk>/', views.issue_book, name='issue_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),

    # Admin Issued Books
    path('issues/', views.issue_list, name='issue_list'),

]
