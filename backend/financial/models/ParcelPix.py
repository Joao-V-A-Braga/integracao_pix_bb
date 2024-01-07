from django.db import models
from .Parcel import Parcel
from .PixCharge import PixCharge

class ParcelPix(Parcel):
    pixCharge = models.ForeignKey(PixCharge, on_delete=models.PROTECT)