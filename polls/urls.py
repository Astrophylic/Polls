from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('overview/', views.overview, name='overview'),
    path('orders/', views.orders, name='orders'),
    path('horario/', views.horario, name='horario'),
    #path('contadorhorario/', views.contadorhorario, name='contadorhorario'),
]