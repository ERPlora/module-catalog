from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models.base import HubBaseModel


class CatalogSettings(HubBaseModel):
    """Per-hub catalog settings."""

    # Content visibility
    show_products = models.BooleanField(default=True, help_text=_('Show products from inventory'))
    show_services = models.BooleanField(default=True, help_text=_('Show services'))
    show_prices = models.BooleanField(default=True, help_text=_('Show prices in catalog'))

    # Contact visibility
    show_phone = models.BooleanField(default=True, help_text=_('Show phone number'))
    show_email = models.BooleanField(default=True, help_text=_('Show email address'))
    show_whatsapp = models.BooleanField(default=True, help_text=_('Show WhatsApp link'))

    # Customization
    title = models.CharField(max_length=255, blank=True, help_text=_('Custom catalog title (defaults to business name)'))
    description = models.TextField(blank=True, help_text=_('Short description shown below title'))

    # Status
    is_active = models.BooleanField(default=False, help_text=_('Enable public catalog'))

    class Meta(HubBaseModel.Meta):
        db_table = 'catalog_settings'
        unique_together = [('hub_id',)]
        verbose_name = _('Catalog Settings')
        verbose_name_plural = _('Catalog Settings')

    def __str__(self):
        return f"CatalogSettings (hub={self.hub_id})"

    @classmethod
    def get_settings(cls, hub_id):
        settings, _ = cls.all_objects.get_or_create(hub_id=hub_id)
        return settings
