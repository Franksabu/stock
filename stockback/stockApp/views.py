from django.shortcuts import render
from .models import Produit, StockIn, StockOut, StockHistory
from django.db.models import Sum

def stock_dashboard(request):
    # Totaux
    total_entrees = StockIn.objects.aggregate(total=Sum('quantite'))['total'] or 0
    total_sorties = StockOut.objects.aggregate(total=Sum('quantite'))['total'] or 0
    stock_total = Produit.objects.aggregate(total=Sum('stock'))['total'] or 0
    produits = Produit.objects.all()
    mouvements = StockHistory.objects.order_by('-created_at')[:10]  # 10 derniers mouvements

    context = {
        'total_entrees': total_entrees,
        'total_sorties': total_sorties,
        'stock_total': stock_total,
        'produits': produits,
        'mouvements': mouvements,
    }
    return render(request, "admin/stock_dashboard.html", context)
