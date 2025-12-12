from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockIn, StockOut, StockHistory


# --------------------------
# ENTRÉE STOCK (StockIn)
# --------------------------
@receiver(post_save, sender=StockIn)
def update_stock_after_stockin(sender, instance, created, **kwargs):
    if created:
        produit = instance.produit
        produit.stock += instance.quantite
        produit.save()

        # Enregistrer dans l'historique
        StockHistory.objects.create(
            produit=produit,
            quantite=instance.quantite,
            operation_type="IN",
            stock_apres_operation=produit.stock,
            fait_par=instance.created_by
        )


# --------------------------
# SORTIE STOCK (StockOut)
# --------------------------
@receiver(post_save, sender=StockOut)
def update_stock_after_stockout(sender, instance, created, **kwargs):
    if created:
        produit = instance.produit
        produit.stock -= instance.quantite
        if produit.stock < 0:
            produit.stock = 0  # empêche un stock négatif
        produit.save()

        # Historique
        StockHistory.objects.create(
            produit=produit,
            quantite=instance.quantite,
            operation_type="OUT",
            stock_apres_operation=produit.stock,
            fait_par=instance.done_by
        )
