from django.urls import path              

from .views import home, track_phone_view, input_view


urlpatterns = [
    path("", home, name="home"),
    path("track-phone-number/", track_phone_view, name='track_phone'),
    path("input-html/test/", input_view, name="input"),
]
