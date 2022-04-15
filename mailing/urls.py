from django.urls import path

from . import views

urlpatterns = [
    path("mailings/", views.MailingsListView.as_view()),
    path("mailing/<int:pk>", views.MailingDetailView.as_view()),
    path("create_mailing/", views.MailingCreateView.as_view()),
    path("users/", views.UsersListView.as_view()),
    path("messages/", views.MessageListView.as_view()),
    path("cr_up_user/", views.UserCreateUpdateView.as_view()),
    path("cr_up_user/<int:pk>/", views.UserCreateUpdateView.as_view()),

]
