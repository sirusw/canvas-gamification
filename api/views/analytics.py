from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from analytics.models.java import JavaQuestionAnalytics
from analytics.models.mcq import MCQQuestionAnalytics
from analytics.models.models import SubmissionAnalytics, QuestionAnalytics
from analytics.models.parsons import ParsonsQuestionAnalytics
from analytics.services.question_analytics import get_all_question_analytics, get_question_analytics, \
    get_question_analytics_by_event
from analytics.services.submission_analytics import get_submission_analytics, get_all_submission_analytics
from api.permissions import TeacherAccessPermission
from api.serializers.question_analytics import MCQQuestionAnalyticsSerializer, JavaQuestionAnalyticsSerializer, \
    ParsonsQuestionAnalyticsSerializer
from canvas.models import Event
from course.models.models import Submission, Question


class AnalyticsViewSet(viewsets.GenericViewSet):
    permission_classes = [TeacherAccessPermission]
    queryset = SubmissionAnalytics.objects.all()

    def list(self, request):
        return Response(get_all_submission_analytics())

    @action(detail=False, methods=['get'], url_path='submission')
    def submission(self, request):
        submission_id = request.GET.get('id', None)
        submission = get_object_or_404(Submission, pk=submission_id)
        return Response(get_submission_analytics(submission))


class QuestionAnalyticsViewSet(viewsets.GenericViewSet):
    permission_classes = [TeacherAccessPermission]
    queryset = QuestionAnalytics.objects.all()

    def get_serialized_data(self, question_analytics):
        if isinstance(question_analytics, MCQQuestionAnalytics):
            return MCQQuestionAnalyticsSerializer(question_analytics).data
        if isinstance(question_analytics, JavaQuestionAnalytics):
            return JavaQuestionAnalyticsSerializer(question_analytics).data
        if isinstance(question_analytics, ParsonsQuestionAnalytics):
            return ParsonsQuestionAnalyticsSerializer(question_analytics).data

    def list(self, request):
        get_all_question_analytics()
        query_set = QuestionAnalytics.objects.all()
        results = [
            self.get_serialized_data(analytics) for analytics in query_set
        ]
        return Response(results)

    @action(detail=False, methods=['get'], url_path='question')
    def question(self, request):
        question_id = request.GET.get('id', None)
        question = get_object_or_404(Question, pk=question_id)
        return Response(get_question_analytics(question))


class EventAnalyticsViewSet(viewsets.GenericViewSet):
    permission_classes = [TeacherAccessPermission]
    queryset = EventAnalytics.objects.all()

    def list(self, request):
        return Response("Please specify an event number.")

    @action(detail=False, methods=['get'], url_path='event')
    def question(self, request):
        event_id = request.GET.get('id', None)
        event = get_object_or_404(Event, pk=event_id)
        return Response(get_event_analytics(event))

    @action(detail=False, methods=['get'], url_path='event')
    def event(self, request):
        event_id = request.GET.get('id', None)
        event = get_object_or_404(Event, pk=event_id)
        analytics = get_question_analytics_by_event(event)
        results = [
            self.get_serialized_data(item) for item in analytics
        ]
        return Response(results)


