import debug_toolbar

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.models import Group

from config import settings, yasg


admin.site.unregister(Group)
admin.site.site_header = "Social Network administration"
admin.site.site_title = "Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    # Oauth2 
    re_path(r'^oauth/', include('social_django.urls')),

    #Apps
    path('', include('src.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += yasg.urlpatterns
