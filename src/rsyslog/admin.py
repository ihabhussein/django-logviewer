from django.contrib import admin
from django.utils.translation import ugettext as _
from .models import Event


admin.site.disable_action('delete_selected')


class TagListFilter(admin.SimpleListFilter):
    title = _('Program')
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        return [(t, t) for t in Event.tags()]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        else:
            return queryset.filter(tag__startswith=self.value())


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['time_received', 'tag', 'facility', 'priority', 'message',]
    ordering = ['-id',]
    list_filter = ['time_received', TagListFilter, 'facility', 'priority',]
    search_fields = ['message',]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, extra_context=extra_context)
