from datetime import datetime

from django.utils.timezone import utc

from accounts.models import MyUser
from analytics.models.models import UserAnalytics
from api.serializers.user_analytics import UserAnalyticsSerializer
from canvas.models import Event, CanvasCourseRegistration
from canvas.utils.utils import get_total_event_grade
from course.models.models import Submission, Question, UserQuestionJunction
from general.models.action import Action, ActionVerb, ActionObjectType
from django.utils import timezone
from datetime import timedelta


def create_user_analytics(user, course):
    events = Event.objects.filter(course=course)
    submission_count = 0
    missing_submission = 0
    total_event_grade = 0
    event_participated = 0
    for event in events:
        if event.is_closed():
            total_event_grade += get_total_event_grade(event, user)
            event_participated += 1
            questions = Question.objects.filter(event=event)
            for question in questions:
                try:
                    uqj = UserQuestionJunction.objects.get(question=question, user=user)
                    submission = Submission.objects.filter(uqj=uqj).exists()
                except Submission.DoesNotExist or UserQuestionJunction.DoesNotExist:
                    missing_submission += 1
                else:
                    if submission:
                        submission_count += 1
                    else:
                        missing_submission += 1

    current_score = total_event_grade / event_participated if event_participated != 0 else 0
    now = timezone.now()
    seven_days = now - timedelta(days=7)
    past_week_question_views = Action.objects.filter(time_created__gte=seven_days, actor=user, verb=ActionVerb.OPENED,
                                                     object_type=ActionObjectType.QUESTION).count()
    try:
        last_active = Action.objects.filter(actor=user, verb=ActionVerb.LOGGED_IN,
                                            object_type=ActionObjectType.USER).order_by(
            '-time_created').first()
    except Action.DoesNotExist or AttributeError:
        last_active = course.start_date
    if last_active:
        last_active = last_active.time_created
    else:
        last_active = course.start_date
    return UserAnalytics.objects.create(course=course, user=user, submissions=submission_count,
                                        missing_submissions=missing_submission, current_score=current_score,
                                        past_week_question_views=past_week_question_views, last_active=last_active)


def get_user_analytics(user, course):
    try:
        analytics = UserAnalytics.objects.get(user=user, course=course)
    except UserAnalytics.DoesNotExist:
        return create_user_analytics(user, course)
    else:
        now = datetime.utcnow().replace(tzinfo=utc)
        time_diff = now - analytics.time_created
        time_diff = time_diff.total_seconds()
        # the analytics expires after one day
        if time_diff < 86400:
            return UserAnalyticsSerializer(analytics).data
        else:
            return create_user_analytics(user, course)


def get_all_user_analytics(course):
    users = CanvasCourseRegistration.objects.filter(course=course)
    for user in users:
        get_user_analytics(user.user, course)
    user_analytics = UserAnalytics.objects.filter(course=course)
    return UserAnalyticsSerializer(user_analytics, many=True).data
