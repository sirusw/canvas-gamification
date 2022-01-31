from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from analytics.models.models import SubmissionAnalytics, QuestionAnalytics, EventAnalytics
from analytics.services.event_analytics import get_event_analytics, get_all_event_analytics
from analytics.services.question_analytics import get_all_question_analytics, get_question_analytics
from analytics.services.submission_analytics import get_submission_analytics, get_all_submission_analytics
from api.permissions import TeacherAccessPermission
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

    def list(self, request):
        return Response(get_all_question_analytics())

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
