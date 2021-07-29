from django import urls
from django.contrib import admin
from django.urls import path, include

#Static files config
from django.conf import settings
from django.conf.urls.static import static

from posts.views import PostViewSet
from users.views import users as users_views
from users.views.users import ProfileDataViewSet
from users.views.login import UserLoginAPIView as login

#Django REST framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'profile', ProfileDataViewSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', users_views.UserListView.as_view(), name='users'),
    path('users/login/', login.as_view(), name='login'), 
    path('users/signup/', users_views.signup, name='signup'),
    path('users/verification', users_views.account_verification, name='verification'),
    path('', include(router.urls))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
