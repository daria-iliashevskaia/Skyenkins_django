
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('users.urls')),
    # path('profile/', include('filechecker.urls'))
]
