from rest_framework import serializers

from analytics.models import submission_analytics


class SubmissionAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = submission_analytics
        fields = '__all__'

        depth = 1
