from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include(('authentication.urls', 'auth'))),
    path('env/', include(('user_environment.urls', 'env'))),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
