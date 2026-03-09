from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from apps.accounts.decorators import login_required, permission_required, public_view
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav
from apps.configuration.models import HubConfig, StoreConfig

from .models import CatalogSettings


# =============================================================================
# Admin views
# =============================================================================

@login_required
@permission_required('catalog.manage_settings')
@with_module_nav('catalog', 'dashboard')
@htmx_view('catalog/pages/dashboard.html', 'catalog/partials/dashboard_content.html')
def dashboard(request):
    """Preview of the public catalog and QR code."""
    hub_id = request.session.get('hub_id')
    config = CatalogSettings.get_settings(hub_id)
    store = StoreConfig.get_solo()

    # Build public catalog URL
    catalog_url = request.build_absolute_uri('/public/catalog/')

    return {
        'config': config,
        'store': store,
        'catalog_url': catalog_url,
    }


@login_required
@permission_required('catalog.manage_settings')
@with_module_nav('catalog', 'settings')
@htmx_view('catalog/pages/settings.html', 'catalog/partials/settings_content.html')
def settings_view(request):
    """Catalog settings with toggle buttons."""
    hub_id = request.session.get('hub_id')
    config = CatalogSettings.get_settings(hub_id)

    if request.method == 'POST':
        config.is_active = request.POST.get('is_active') == 'on'
        config.show_products = request.POST.get('show_products') == 'on'
        config.show_services = request.POST.get('show_services') == 'on'
        config.show_prices = request.POST.get('show_prices') == 'on'
        config.show_phone = request.POST.get('show_phone') == 'on'
        config.show_email = request.POST.get('show_email') == 'on'
        config.show_whatsapp = request.POST.get('show_whatsapp') == 'on'
        config.title = request.POST.get('title', '').strip()
        config.description = request.POST.get('description', '').strip()
        config.save()

    store = StoreConfig.get_solo()

    return {
        'config': config,
        'store': store,
    }


# =============================================================================
# Public views (no authentication)
# =============================================================================

@public_view
def public_catalog(request):
    """Public catalog page — no authentication required."""
    hub_config = HubConfig.get_solo()
    hub_id = hub_config.hub_id
    store = StoreConfig.get_solo()
    config = CatalogSettings.get_settings(hub_id)

    # If catalog is disabled, return a simple message
    if not config.is_active:
        return render(request, 'catalog/public/inactive.html', {
            'store': store,
        })

    # Collect products and services
    products_by_category = {}
    services_by_category = {}

    if config.show_products:
        try:
            from inventory.models import Product, Category
            categories = Category.objects.filter(
                hub_id=hub_id, is_active=True
            ).order_by('sort_order', 'name')

            for category in categories:
                items = Product.objects.filter(
                    hub_id=hub_id,
                    is_active=True,
                    categories=category,
                ).order_by('name')
                if items.exists():
                    products_by_category[category] = items

            # Uncategorized products
            uncategorized = Product.objects.filter(
                hub_id=hub_id,
                is_active=True,
                categories__isnull=True,
            ).order_by('name')
            if uncategorized.exists():
                products_by_category[None] = uncategorized
        except (ImportError, Exception):
            pass

    if config.show_services:
        try:
            from services.models import Service, ServiceCategory
            categories = ServiceCategory.objects.filter(
                hub_id=hub_id, is_active=True
            ).order_by('sort_order', 'name')

            for category in categories:
                items = Service.objects.filter(
                    hub_id=hub_id,
                    is_active=True,
                    category=category,
                ).order_by('sort_order', 'name')
                if items.exists():
                    services_by_category[category] = items

            # Uncategorized services
            uncategorized = Service.objects.filter(
                hub_id=hub_id,
                is_active=True,
                category__isnull=True,
            ).order_by('sort_order', 'name')
            if uncategorized.exists():
                services_by_category[None] = uncategorized
        except (ImportError, Exception):
            pass

    # Build WhatsApp URL
    whatsapp_url = ''
    if config.show_whatsapp and store.phone:
        phone_clean = store.phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not phone_clean.startswith('+'):
            phone_clean = '+34' + phone_clean
        whatsapp_url = f'https://wa.me/{phone_clean.replace("+", "")}'

    catalog_title = config.title or store.business_name or 'Catalog'

    return render(request, 'catalog/public/catalog.html', {
        'store': store,
        'config': config,
        'catalog_title': catalog_title,
        'products_by_category': products_by_category,
        'services_by_category': services_by_category,
        'whatsapp_url': whatsapp_url,
    })
