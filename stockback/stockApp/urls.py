from django.urls import path
from . import views

app_name = "stock_admin"

urlpatterns = [
    path('dashboard/', self.admin_view(self.stock_dashboard), name='stock-dashboard') 
    
]

