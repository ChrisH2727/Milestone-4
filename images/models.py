from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Image(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254)
    title = models.CharField(max_length=254, blank=True, null=True)
    size = models.CharField(max_length=254, blank=True, null=True)
    dimensions = models.CharField(max_length=254, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    views = models.PositiveIntegerField(null=True, blank=True, default=1)
    downloads = models.PositiveIntegerField(null=True, blank=True, default=1)
    image = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

