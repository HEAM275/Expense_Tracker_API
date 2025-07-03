from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator
from apps.common.models import AuditableMixins
from apps.manager.models import User

# Renombrado por convención
EXPENSE_TYPE_CHOICES = (
    ("comestibles", _("Comestibles")),
    ("ocio", _("Ocio")),
    ("electronica", _("Electrónica")),
    ("servicio públicos", _("Servicios públicos")),
    ("ropa", _("Ropa")),
    ("salud", _("Salud")),
    ("otros", _("Otros")),
)


class Expense(AuditableMixins):
    description = models.CharField(verbose_name=_("Description"), max_length=255)
    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    type = models.CharField(
        verbose_name=_("Type"), max_length=50, choices=EXPENSE_TYPE_CHOICES
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    payment_date = models.DateTimeField(
        verbose_name=_("Payment Date"), default=timezone.now
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.type})"
