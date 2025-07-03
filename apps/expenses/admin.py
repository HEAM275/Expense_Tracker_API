from django.utils import timezone
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "amount",
        "description",
        "type",
        "user",
        "payment_date",
        "is_active",
        "created_by",
        "updated_by",
    )
    list_display_links = ("id", "amount")
    list_filter = ("type", "is_active", "payment_date", "created_date")
    search_fields = (
        "description",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-payment_date",)
    date_hierarchy = "payment_date"
    raw_id_fields = ("user",)
    readonly_fields = (
        "created_by",
        "created_date",
        "updated_by",
        "updated_date",
        "deleted_by",
        "deleted_date",
    )

    fieldsets = (
        (
            _("Información Básica"),
            {"fields": ("user", "amount", "description", "type", "payment_date")},
        ),
        (_("Estado"), {"fields": ("is_active",)}),
        (
            _("Auditoría"),
            {
                "fields": (
                    "created_by",
                    "created_date",
                    "updated_by",
                    "updated_date",
                    "deleted_by",
                    "deleted_date",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Vista de creación
            return (
                (
                    _("Información Básica"),
                    {
                        "fields": (
                            "user",
                            "amount",
                            "description",
                            "type",
                            "payment_date",
                        )
                    },
                ),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:  # Creación
            obj.created_by = request.user.get_full_name() or request.user.username
        else:  # Actualización
            obj.updated_by = request.user.get_full_name() or request.user.username

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):

        obj.is_active = False
        obj.deleted_by = request.user.get_full_name() or request.user.username
        obj.save()

    def has_delete_permission(self, request, obj=None):
        return True

    actions = ["soft_delete_selected", "activate_selected"]

    def soft_delete_selected(self, request, queryset):
        updated = queryset.update(
            is_active=False,
            deleted_by=request.user.get_full_name() or request.user.username,
            deleted_date=timezone.now(),
        )
        self.message_user(request, _("Se desactivaron {} gastos").format(updated))

    soft_delete_selected.short_description = _("Desactivar gastos seleccionados")

    def activate_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _("Se activaron {} gastos").format(updated))

    activate_selected.short_description = _("Activar gastos seleccionados")

    # class Media:
    #     css = {
    #         'all': ('css/admin/custom_admin.css',)
    #     }
