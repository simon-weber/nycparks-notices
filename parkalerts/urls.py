from django.urls import path

from django.contrib import admin

from parkalerts.core import views

admin.autodiscover()


urlpatterns = [
    path("", views.index, name="index"),
    path("browserconfig.xml", views.browserconfig, name="browserconfig"),
    path("site.webmanifest", views.webmanifest, name="webmanifest"),

    path("statuses/", views.statuses, name="statuses"),
    path("privacy/", views.privacy, name="privacy"),
    path("subscriber/", views.subscriber, name="subscriber"),
    path("subscriber/<uuid:key>/", views.subscriber, name="subscriber"),

    path("admin/", admin.site.urls),
]
