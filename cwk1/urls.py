
from django.contrib import admin
from django.urls import path , include

from api.views import Login_view, Logout_view,PostStory,GetStory,DeleteStory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/',Login_view),
    path('api/logout/',Logout_view),
    path('api/poststory/',PostStory),
    path('api/getstories/',GetStory),
    path('api/deletestory/',DeleteStory),
]
