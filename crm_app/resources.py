from import_export import resources
from .models import bank_cat

class ImportsResource(resources.ModelResource):
    class meta:
        model = bank_cat