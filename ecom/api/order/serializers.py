from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.HyperlinkedModelsSerializer):
    class Meta:
        model = Order
        fields  = ('user')
        #TODO:add product and quantity