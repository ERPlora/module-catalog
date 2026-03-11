"""
AI context for the Catalog module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Catalog

### Models

**CatalogSettings** (singleton per hub)
- `is_active` (BooleanField, default False) — whether the public catalog page is enabled
- `title` (CharField, blank) — custom catalog title; defaults to business name if blank
- `description` (TextField, blank) — short description shown below the title
- Content toggles: `show_products` (default True), `show_services` (default True), `show_prices` (default True)
- Contact toggles: `show_phone` (default True), `show_email` (default True), `show_whatsapp` (default True)
- Use `CatalogSettings.get_settings(hub_id)` to get or create the singleton

### Key flows

1. **Enable catalog**: Get or create CatalogSettings → set `is_active=True` → optionally set `title` and `description`.
2. **Configure visibility**: Toggle `show_products`, `show_services`, `show_prices` to control what customers see.
3. **Contact info**: Toggle `show_phone`, `show_email`, `show_whatsapp` to control which contact methods are visible.
4. **Disable catalog**: Set `is_active=False` to take the public page offline without deleting settings.

### Relationships
- No FK relationships — CatalogSettings is a standalone singleton configuration model
- The actual products and services displayed come from the `inventory` and `services` modules respectively; this module only controls the public-facing catalog page settings
"""
