from django.urls import path

from . import views

urlpatterns = [
    path("mailings/", views.MailingsListView.as_view()),
    path("mailing/<int:pk>/", views.MailingDetailView.as_view()),
    path("create_mailing/", views.MailingCreateView.as_view()),
    path("delete_mailing/<int:pk>/", views.MailingDeleteView.as_view()),
    path("users/", views.UsersListView.as_view()),
    path("messages/", views.MessageListView.as_view()),
    path("create_user/", views.UserCreateView.as_view()),
    path("update_user/<int:pk>/", views.UserUpdateView.as_view()),
    path("delete_user/<int:pk>/", views.UserDeleteView.as_view()),
]
