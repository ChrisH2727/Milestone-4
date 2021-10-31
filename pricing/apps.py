from django.apps import AppConfig

class PricingConfig(AppConfig):
    """
    Required to get signals to work
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pricing'

    #def ready(self):
    #    import pricing.signals