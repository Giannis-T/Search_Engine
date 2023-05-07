from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("search/<int:history_query_id>", views.search, name="search"),
    path("search/<str:rec_query>/<str:rec_field>", views.search, name="search"),
    path("view_history", views.view_history, name="view_history"),
    path("advanced_search", views.advanced_search, name="advanced_search"),
    path("view_results", views.search, name="view_results"),
    path("next_ten", views.next_ten, name="next_ten"),
    path("prev_ten", views.prev_ten, name="prev_ten"),
    path("delete_history", views.delete_history, name="delete_history")

]