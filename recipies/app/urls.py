from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('recipes/<int:recipe_id>/add_comment/', add_comment, name='add_comment'),
    path('recipes/<int:recipe_id>/add_rating/', add_rating, name='add_rating'),
    path('recipes/add/', add_recipe, name='add_recipe'),
    path('recipes/<int:recipe_id>/edit/', edit_recipe, name='edit_recipe'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
]
    


