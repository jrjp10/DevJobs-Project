"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

app_name = 'account'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    
    path('api/account/', include(('account.api.urls', 'account'), namespace='account')),
    path('api/', include(('job.api.urls', 'job'), namespace='job')),
    path('api/candidate/', include(('experience.urls', 'expereince'), namespace='experience')),
    path('api/application/', include(('application.urls', 'application'), namespace='application')),
    path('api/payment/', include(('payment.urls', 'payment'), namespace='payment')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler500 = 'utils.error_views.handler500'
handler404 = 'utils.error_views.handler404'


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
