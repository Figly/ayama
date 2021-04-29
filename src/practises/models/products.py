from clients.models import ClientDetail
from django.conf import settings
from django.db import models

from .advisor_detail import AdvisorDetail
from .base import BaseModel
from .practise_detail import PractiseDetail

types = (
    ("INS", "Insurance"),
    ("RA", "Retirement Annuity"),
    ("UT", "Unit Trust"),
)


class ProductDetail(BaseModel):
    """
    Class descriptor
    """

    product_name = models.CharField("Product Name", max_length=100)
    is_active = models.BooleanField("Is Active")

    def __str__(self):
        return f"{self.product_name}"


class ProductAdvisor(BaseModel):
    """
    Class descriptor
    """

    advisor_id_fk = models.ForeignKey("AdvisorDetail", on_delete=models.CASCADE)
    product_id_fk = models.ForeignKey("ProductDetail", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name}"


class ProductClient(BaseModel):
    """
    Class descriptor
    """

    client_id_fk = models.ForeignKey("clients.ClientDetail", on_delete=models.CASCADE)
    product_id_fk = models.ForeignKey("ProductDetail", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name}"
