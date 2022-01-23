from django.contrib import admin


class HideModelAdmin(admin.ModelAdmin):

    def log_addition(self, *args):
        return

    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return


class HideTabularInline(admin.TabularInline):

    def log_addition(self, *args):
        return

    def log_change(self, *args):
        return

    def log_deletion(self, *args):
        return


class ReadOnlyAdmin(admin.ModelAdmin):
    """Provides a read-only view of a model in Django admin."""
    readonly_fields = []

    def change_view(self, request, object_id, extra_context=None, **kwargs):
        """ customize add/edit form to remove save / save and continue """
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(ReadOnlyAdmin, self).change_view(
            request, object_id, extra_context=extra_context
        )

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
           [field.name for field in obj._meta.fields] + \
           [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
