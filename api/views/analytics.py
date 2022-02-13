from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from analytics.models import MCQSubmissionAnalytics, ParsonsSubmissionAnalytics, JavaSubmissionAnalytics
from analytics.models.models import SubmissionAnalytics
from analytics.services.submission_analytics import get_submission_analytics, get_all_submission_analytics
from api.permissions import TeacherAccessPermission
from api.serializers.submission_analytics import MCQSubmissionAnalyticsSerializer, JavaSubmissionAnalyticsSerializer, \
    ParsonsSubmissionAnalyticsSerializer
from course.models.models import Submission


class AnalyticsViewSet(viewsets.GenericViewSet):
    permission_classes = [TeacherAccessPermission]
    queryset = SubmissionAnalytics.objects.all()

    def get_serialized_data(self, submission_analytics):
        if isinstance(submission_analytics, MCQSubmissionAnalytics):
            return MCQSubmissionAnalyticsSerializer(submission_analytics).data
        if isinstance(submission_analytics, JavaSubmissionAnalytics):
            return JavaSubmissionAnalyticsSerializer(submission_analytics).data
        if isinstance(submission_analytics, ParsonsSubmissionAnalytics):
            return ParsonsSubmissionAnalyticsSerializer(submission_analytics).data

    def list(self, request):
        analytics = get_all_submission_analytics()
        results = [
            self.get_serialized_data(analytics) for analytics in analytics
        ]
        return Response(results)

    @action(detail=False, methods=['get'], url_path='submission')
    def submission(self, request):
        submission_id = request.GET.get('id', None)
        submission = get_object_or_404(Submission, pk=submission_id)
        return Response(self.get_serialized_data(get_submission_analytics(submission)))
