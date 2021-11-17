from rest_framework import viewsets

from analytics.models import submission_analytics
from api.pagination import BasePagination
from api.permissions import TeacherAccessPermission
from api.serializers.submission_analytics import SubmissionAnalyticsSerializer


class SubmissionAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = submission_analytics.objects.all()
    serializer_class = SubmissionAnalyticsSerializer
    permission_classes = [TeacherAccessPermission]
    pagination_class = BasePagination
