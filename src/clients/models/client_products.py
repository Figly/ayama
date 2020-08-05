from django.conf import settings
from django.db import models

from .base import BaseModel


class ClientProduct(BaseModel):
    """
    Class descriptor
    """

    client_id_fk = models.ForeignKey("ClientDetail", on_delete=models.CASCADE)
    product_id_fk = models.ForeignKey(
        "practises.ProductDetail", on_delete=models.CASCADE
    )
