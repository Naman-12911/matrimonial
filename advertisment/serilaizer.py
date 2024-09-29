
from .models import Advertisment
from rest_framework import serializers


class AdvertismentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Advertisment
        fields = "__all__"