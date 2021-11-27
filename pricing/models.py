import uuid
from django.db import models
from django.conf import settings
from profiles.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
#from phonenumber_field.modelfields import PhoneNumberField

class Pricing(models.Model):
    """
    Provides the pricing for all the
    subscription options
    """

    sku = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    def get_display_name(self):
        return self.display_name


class Order(models.Model):
    """
    Provides the pricing for all the
    subscription options
    """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    mobile_phone_number = models.CharField(max_length=20, null=False, blank=False)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    address_line_1 = models.CharField(max_length=80, null=True, blank=True)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    sales_tax_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, default= settings.SALES_TAX_RATE)
    sales_tax = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    completed = models.BooleanField(default=False)
    
    
    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Calculate sales tax and generate grand total
        """

        self.sales_tax = self.order_total * (settings.SALES_TAX_RATE / 100)
        self.grand_total = self.order_total + self.sales_tax
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class Subscription(models.Model):
    """
    Defines the types of subscriptions on offer
    """
    sku = models.CharField(max_length=254, blank=True, null=True)
    sub_type = models.PositiveIntegerField(null=True, blank=True)
    sub_name = models.CharField(max_length=254, blank=True, null=True)
    sub_display_name = models.CharField(max_length=254, blank=True, null=True)
    sub_display_description = models.CharField(max_length=254, blank=True, null=True)
    sub_duration = models.PositiveIntegerField(null=True, blank=True)
    sub_images = models.PositiveIntegerField(null=True, blank=True)
    sub_price = models.DecimalField(max_digits=6, decimal_places=2)
    sub_display_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.sub_name

    def get_display_name(self):
        return self.sub_display_name

class Trolly (models.Model):
    """
    Provides the on-line store shopping trolly
    """
    sku = models.CharField(max_length=254, blank=True, null=True)
    sub_name = models.CharField(max_length=254, blank=True, null=True)
    sub_display_name = models.CharField(max_length=254, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sub_count = models.PositiveIntegerField(null=True, blank=True)
    credits = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.sub_name
