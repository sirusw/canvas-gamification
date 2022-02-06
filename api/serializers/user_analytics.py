from rest_framework import serializers

from analytics.models.models import UserAnalytics


class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytics
        fields = '__all__'

        depth = 1
