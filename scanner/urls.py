from django.urls import path
from . import views
app_name = 'scanner'
urlpatterns = [
    path('test/', views.readBarcode, name = 'readBarcode'),
    path('scan/', views.scan_now, name = 'scan_now'),
    path('upload/', views.read_image, name = 'upload'),
    path('add_shelf/',views.AddShelf.as_view(), name = 'shelf'),
    path('',views.Shelves.as_view(), name = 'home'),
    path('<pk>/',views.ShelfDetailAdd.as_view(), name = 'shelf_details')
]
