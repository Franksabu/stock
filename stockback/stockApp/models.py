from django.db import models
from django.conf import settings

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField(blank=True, null=True)
      
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom
    
    
class StockIn(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)   
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entrée: {self.produit.nom} ({self.quantite})"
    
    
class StockOut(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='stock_sortie')
    quantite = models.PositiveIntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    
    done_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Sortie: {self.produit.nom} ({self.quantite})"
    
    
class StockHistory(models.Model):
    OPERATION_TYPES = (
        ('IN', 'Entrée'),
        ('OUT', 'Sortie'),
    )
     
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    operation_type = models.CharField(max_length=3, choices=OPERATION_TYPES)
    stock_apres_operation = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    fait_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Historique: {self.operation_type} {self.produit.nom}"
