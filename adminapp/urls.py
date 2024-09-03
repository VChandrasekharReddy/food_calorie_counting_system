from django.urls import path
from adminapp import views
urlpatterns=[
    path('adminlogin',views.adminlogin),
    path('LogAction',views.LogAction),
    path('adminhome',views.adminhome),
    path('AddFoodCalories',views.AddFoodCalories),
    path('AddFoodCaloriesAction',views.AddFoodCaloriesAction),
    path('ViewFoodCalories',views.ViewFoodCalories),
    ]
