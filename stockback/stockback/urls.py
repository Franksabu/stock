from django.contrib import admin
from django.urls import include, path
from stockApp.admin_dashboard import stock_admin 

urlpatterns = [
    #path('admin/dashboard/', stock_admin.urls),
    path('admin/', stock_admin.urls),
    #path('admin/', admin.site.urls),
   # path('stock/', include('stockApp.urls')),
]

