from django.contrib.admin import AdminSite
from django.db.models import Sum
from django.shortcuts import render
from django.urls import path
from .models import Produit, StockIn, StockOut, StockHistory

class StockAdminSite(AdminSite):
    site_header = "STOCK ADMIN"
    site_title = "Stock Admin"
    index_title = "Tableau de Bord"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', self.admin_view(self.stock_dashboard), name='stock-dashboard'),
        ]
        return my_urls + urls

    def stock_dashboard(self, request):
        total_entrees = StockIn.objects.aggregate(total=Sum('quantite'))['total'] or 0
        total_sorties = StockOut.objects.aggregate(total=Sum('quantite'))['total'] or 0
        stock_restant = total_entrees - total_sorties

        produits = Produit.objects.all()

        # 10 derniers mouvements
        mouvements = StockHistory.objects.order_by('-created_at')[:10]

        context = {
            'total_entrees': total_entrees,
            'total_sorties': total_sorties,
            'stock_restant': stock_restant,
            'produits': produits,
            'mouvements': mouvements,
        }

        return render(request, "admin/stock_dashboard.html", context)


# Instance de ton admin personnalisé
stock_admin = StockAdminSite(name='stock_admin')
