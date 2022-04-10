from django.urls import path

from . import views

urlpatterns = [
    path("mailings/", views.MailingsListView.as_view()),
    path("mailings/<int:pk>", views.MailingDetailListView.as_view()),
    path("users/", views.UsersListView.as_view()),
    path("messages/", views.MessageListView.as_view())
]
