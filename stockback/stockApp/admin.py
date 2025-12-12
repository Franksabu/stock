from django.contrib import admin
from django.urls import reverse
from django.db.models import Sum
from django.utils.html import format_html

from .models import Produit, StockIn, StockOut, StockHistory
from .admin_dashboard import stock_admin


# ---------------------------
# Inlines
# ---------------------------

class StockInInline(admin.TabularInline):
    model = StockIn
    extra = 1
    readonly_fields = ('created_by', 'created_at')


class StockOutInline(admin.TabularInline):
    model = StockOut
    extra = 1
    readonly_fields = ('done_by', 'created_at')


# ---------------------------
# Action personnalisée
# ---------------------------

@admin.action(description='Créer une sortie pour le produit sélectionné')
def creer_sortie(modeladmin, request, queryset):
    for produit in queryset:
        StockOut.objects.create(
            produit=produit,
            quantite=1,
            done_by=request.user
        )
        produit.stock -= 1
        produit.save()


# ---------------------------
# Admin Produit
# ---------------------------

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'stock', 'prix')
    inlines = [StockInInline, StockOutInline]
    actions = [creer_sortie]
    search_fields = ('nom',)

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["dashboard_url"] = reverse("stock_admin:stock-dashboard")
        return super().changelist_view(request, extra_context=extra_context)


# ---------------------------
# Admin StockIn
# ---------------------------

class StockInAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite', 'prix_unitaire', 'created_by', 'created_at', 'stock_apres')
    autocomplete_fields = ('produit',)

    def stock_apres(self, obj):
        return obj.produit.stock
    stock_apres.short_description = "Stock après entrée"

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        total = StockIn.objects.aggregate(total=Sum('quantite'))['total'] or 0
        extra_context = extra_context or {"total_quantite": total}
        return super().changelist_view(request, extra_context=extra_context)


# ---------------------------
# Admin StockOut
# ---------------------------

class StockOutAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite', 'description', 'done_by', 'created_at', 'stock_apres')
    autocomplete_fields = ('produit',)

    def stock_apres(self, obj):
        return obj.produit.stock
    stock_apres.short_description = "Stock après sortie"

    def save_model(self, request, obj, form, change):
        if not obj.done_by:
            obj.done_by = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        total = StockOut.objects.aggregate(total=Sum('quantite'))['total'] or 0
        extra_context = extra_context or {"total_quantite": total}
        return super().changelist_view(request, extra_context=extra_context)


# ---------------------------
# Admin StockHistory
# ---------------------------

class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('produit', 'operation_type', 'quantite', 'stock_apres_operation', 'fait_par', 'created_at')
    autocomplete_fields = ('produit',)

    def save_model(self, request, obj, form, change):
        if not obj.fait_par:
            obj.fait_par = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        total = StockHistory.objects.aggregate(total=Sum('quantite'))['total'] or 0
        extra_context = extra_context or {"total_quantite": total}
        return super().changelist_view(request, extra_context=extra_context)


# ============================================================
#  CONNECTER LE NOUVEL ADMIN PERSONNALISÉ
# ============================================================

# 1️⃣ Désenregistrer du Django admin normal (évite AlreadyRegistered)
for model in [Produit, StockIn, StockOut, StockHistory]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# 2️⃣ Enregistrer dans ton admin customisé
stock_admin.register(Produit, ProduitAdmin)
stock_admin.register(StockIn, StockInAdmin)
stock_admin.register(StockOut, StockOutAdmin)
stock_admin.register(StockHistory, StockHistoryAdmin)
