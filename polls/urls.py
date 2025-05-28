from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('signin/', views.signin, name='signin'), #inicio de sesion
    path('signup/', views.signup, name='signup'), #registro
    path('overview/', views.overview, name='overview'), #perfil
    path('orders/', views.orders, name='orders'), # encuestas
    path('horario/', views.horario, name='horario'), #control de horario
    path('horario/checkin/', views.check_in, name='check_in'),
    path('horario/checkout/', views.check_out, name='check_out'),
]