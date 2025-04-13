from django.urls import path

from tables import views


urlpatterns = [
    path("tables/", views.TableView.as_view(), name="tables_list_create"),
    path("tables/<int:pk>", views.TableDeleteView.as_view(), name="table_delete"),
    path("reservations/", views.ReservationView.as_view(), name="reservations_list_create"),
    path("reservations/<int:pk>", views.ReservationDeleteView.as_view(), name="reservation_delete"),
]
