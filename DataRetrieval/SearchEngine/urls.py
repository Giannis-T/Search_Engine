from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("view_history", views.view_history, name="view_history"),
    path("advanced_search", views.advanced_search, name="advanced_search"),
    path("view_results", views.view_results, name="view_results"),


]