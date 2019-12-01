from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rango import views
from registration.backends.simple.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_succes_url(self, request, user):
        return '/rango/add_profile/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('rango/', include('rango.urls')),
    # above maps any URLs starting
    # with rango/ to be handled by
    # the rango application  
    path('accounts/register', MyRegistrationView.as_view(),
        name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
]
