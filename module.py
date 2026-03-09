from django.utils.translation import gettext_lazy as _

MODULE_ID = 'catalog'
MODULE_NAME = _('Catalog')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'book-outline'

MENU = {
    'label': _('Catalog'),
    'icon': 'book-outline',
    'order': 55,
}

NAVIGATION = [
    {'label': _('Preview'), 'icon': 'eye-outline', 'id': 'dashboard'},
    {'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

PERMISSIONS = [
    'catalog.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": ["manage_settings"],
    "employee": [],
}
