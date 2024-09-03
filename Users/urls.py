from django.urls import path
from Users import views
urlpatterns=[
    path('',views.index),
    path('Users',views.userlogin),
    path('register',views.register),
    path('RegAction',views.RegAction),
    path('LogAction',views.LogAction),
    path('userhome',views.userhome),
    path('CaloryLimit',views.CaloryLimit),
    path('CaloryLimitSetAction',views.CaloryLimitSetAction),
    path('SugarAction',views.SugarAction),
    path('CaloryLimitAction',views.CaloryLimitAction),
    path('ConfirmCalory',views.ConfirmCalory),
    path('AddItems',views.AddItems),
    path('AddItemAction',views.AddItemAction),
    path('ViewItems',views.ViewItems),
    path('DeleteItem',views.DeleteItem),
    path('AddExercise',views.AddExercise),
    path('AddExerciseAction',views.AddExerciseAction),
    path('ViewExercise',views.ViewExercise),
    path('DeleteExercise',views.DeleteExercise),
    path('ViewResult',views.ViewResult),
        
	]
