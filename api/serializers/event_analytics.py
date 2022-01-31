from analytics.models.models import EventAnalytics
from rest_framework import serializers


class EventAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAnalytics
        fields = '__all__'

        depth = 1
