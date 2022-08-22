from django.contrib import admin
from .models import Scan,Shelf
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class BarcodeResource(resources.ModelResource):

    class Meta:
        model = Scan
        import_id_fields = ('code')
        fields = ('shelf','code','qty')

class BarcodeAdmin(ImportExportModelAdmin):
    resource_class = BarcodeResource

# class ShelfResource(resources.ModelResource):
#
#     class Meta:
#         model = Shelf
#         import_id_fields = ('shelf')
#         fields = ('shelf')
#
# class ShelfAdmin(ImportExportModelAdmin):
#     resource_class = ShelfResource

admin.site.register(Scan,BarcodeAdmin)
admin.site.register(Shelf)
admin.site.site_header  =  "Barcode Scanner"
admin.site.index_title  =  "Database"
