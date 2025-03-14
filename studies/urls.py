from django.urls import path
from. import views

urlpatterns=[
    path('home',views.home,name='home'),
    path('',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register,name='register'),
    path('room_add', views.create_room,name='room_add'),
    path('room/<str:pk>', views.room,name='room'),
    path('update/<int:pk>',views.update_record,name='update'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('delete_message/<int:pk>',views.delete_message,name='delete_message'),
    path('profile/<int:pk>',views.profile ,name='profile'),
    path('update-user', views.update_user,name='update-user'),
    path('topics', views.topics,name='topics'),
    path('activity', views.activities,name='activity')
] 