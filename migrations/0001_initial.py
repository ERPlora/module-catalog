import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CatalogSettings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('hub_id', models.UUIDField(db_index=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('show_products', models.BooleanField(default=True, help_text='Show products from inventory')),
                ('show_services', models.BooleanField(default=True, help_text='Show services')),
                ('show_prices', models.BooleanField(default=True, help_text='Show prices in catalog')),
                ('show_phone', models.BooleanField(default=True, help_text='Show phone number')),
                ('show_email', models.BooleanField(default=True, help_text='Show email address')),
                ('show_whatsapp', models.BooleanField(default=True, help_text='Show WhatsApp link')),
                ('title', models.CharField(blank=True, help_text='Custom catalog title (defaults to business name)', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Short description shown below title')),
                ('is_active', models.BooleanField(default=False, help_text='Enable public catalog')),
            ],
            options={
                'verbose_name': 'Catalog Settings',
                'verbose_name_plural': 'Catalog Settings',
                'db_table': 'catalog_settings',
                'unique_together': {('hub_id',)},
            },
        ),
    ]
