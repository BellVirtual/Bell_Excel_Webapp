from django.urls import path
#from .views import home  #MainView
from . import views
from django.conf.urls.static import static
#from django.conf.urls import url
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    #url('', views.MainView.as_view()),
    path('', views.home),
    path('upload', views.upload),

    path('remove_colums', views.remove_colums),
    path('clear', views.clear),
    #url('',views.home),
    #url('/file_upload', views.upload)
    #url(r'^$',views.home),
    #url(r'^file_upload$', views.upload)
    #path('',views.home,name="home"),
    #path('/upload', views.upload)
    #path('',MainView.as_view(template_name='index.html'), name='homepage'),
    #path('upload/', views.file_upload_view, name='upload-view')

    #path('^$', views.activate,name="script"),
    #url(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
