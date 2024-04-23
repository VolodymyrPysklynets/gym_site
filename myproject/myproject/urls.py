from django.contrib import admin
from django.urls import path, include
from gymsite.views import articleId
from users.views import account, login_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainpage/', include('gymsite.urls')),
    path('trainers/', include('gymsite.urls')),
    path('mainpage/article/<int:id>/', articleId),
    path('users/', include('users.urls')),
    path('users/register/account/', account),
    path('users/login/', login_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
