from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

import accounts.urls
import clients.urls
import practises.urls
import profiles.urls
import calculator.urls

from . import views

# Personalized admin site settings like title and header
admin.site.site_title = "Ayama Site Admin"
admin.site.site_header = "Ayama Administration"

urlpatterns = [
    re_path(r"^healthz/", views.healthz, name="healthz"),
    path("", views.HomePage.as_view(), name="home"),
    path("about/", views.AboutPage.as_view(), name="about"),
    path("users/", include(profiles.urls)),
    path("admin/", admin.site.urls),
    path("", include(accounts.urls)),
    path("", include(practises.urls)),
    path("", include(clients.urls)),
    path("calcs/", include(calculator.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    # Dev ref for profile pics -- should probably redo this at some point
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
