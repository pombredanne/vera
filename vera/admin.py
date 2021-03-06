from django.contrib import admin
from wq.db.patterns import admin as patterns
from wq.db.patterns.models import Authority, RelationshipType
import swapper


class ResultInline(admin.TabularInline):
    model = swapper.load_model('vera', 'Result')
    extra = 0


class ReportInline(admin.TabularInline):
    model = swapper.load_model('vera', 'Report')
    extra = 0


class ParameterAdmin(patterns.IdentifiedModelAdmin):
    list_display = ('name', 'units')
    list_filter = ('units', 'is_numeric')


class ReportAdmin(admin.ModelAdmin):
    inlines = [ResultInline]


class EventAdmin(admin.ModelAdmin):
    inlines = [ReportInline]

# Register models with admin, but only if they haven't been swapped
default_admin = {
    'Site': patterns.IdentifiedRelatedModelAdmin,
    'Event': EventAdmin,
    'Report': ReportAdmin,
    'ReportStatus': admin.ModelAdmin,
    'Parameter': ParameterAdmin,
}
for model in default_admin:
    if swapper.is_swapped('vera', model):
        continue
    admin.site.register(
        swapper.load_model('vera', model),
        default_admin[model]
    )

# Auto-register relevant patterns' type models
admin.site.register(Authority, patterns.AuthorityAdmin)
admin.site.register(RelationshipType)
