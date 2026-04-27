"""
URL configuration for ivhemms_project project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

from core.views import serve_html

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # Serve root-level HTML files
    path('index.html', serve_html, {'page_path': 'index.html'}, name='index'),
    path('login.html', serve_html, {'page_path': 'login.html'}, name='login_page'),
    path('register.html', serve_html, {'page_path': 'register.html'}, name='register_page'),
    path('forgot-password.html', serve_html, {'page_path': 'forgot-password.html'}, name='forgot_password_page'),
    path('reset-password.html', serve_html, {'page_path': 'reset-password.html'}, name='reset_password_page'),

    # Serve pages/**/*.html
    re_path(r'^(?P<page_path>pages/.+\.html)$', serve_html, name='pages'),

    # Serve /assets/ directory (CSS, JS, uploads)
    re_path(r'^assets/(?P<path>.*)$', static_serve, {'document_root': settings.BASE_DIR / 'assets'}),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Default: redirect bare "/" to index.html
urlpatterns.insert(0, path('', serve_html, {'page_path': 'index.html'}, name='root'))
