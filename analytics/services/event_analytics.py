from datetime import datetime
from django.utils.timezone import utc

from accounts.models import MyUser
from analytics.models.models import EventAnalytics
from api.serializers.event_analytics import EventAnalyticsSerializer
from canvas.models import Event
from canvas.utils.utils import get_total_event_grade
from course.models.models import Submission, UserQuestionJunction


def get_event_analytics(event):
    try:
        analytics = EventAnalytics.objects.get(event=event)

    except EventAnalytics.DoesNotExist:
        return create_event_analytics(event)
    else:
        now = datetime.utcnow().replace(tzinfo=utc)
        time_diff = now - analytics.time_created
        time_diff = time_diff.total_seconds()
        # the analytics expires after one day
        if time_diff < 86400:
            return EventAnalyticsSerializer(analytics).data
        else:
            return create_event_analytics(event)


def get_all_event_analytics():
    events = Event.objects.all()
    event_analytics = EventAnalytics.objects.all()
    if events.count() == event_analytics.count():
        return EventAnalyticsSerializer(event_analytics).data
    for event in events:
        get_event_analytics(event)
    event_analytics = EventAnalytics.objects.all()
    return EventAnalyticsSerializer(event_analytics).data


def create_event_analytics(event):
    course = event.course
    distinct_uqj = Submission.objects.values('uqj').distinct()
    users = []
    grades = []
    for item in distinct_uqj:
        uqj = UserQuestionJunction.objects.get(pk=item['uqj'])
        uqj_event = uqj.question.event
        if uqj_event == event:
            if uqj.user not in users:
                users.append(uqj.user)
    for user in users:
        grades.append(get_total_event_grade(event, user))

    if len(grades) != 0:
        high_score = max(grades)
        low_score = min(grades)
        avg_score = sum(grades) / len(grades)
        import statistics
        avg_score_st_dev = statistics.stdev(grades)
        num_participants = len(grades)
    else:
        high_score = 0
        low_score = 0
        avg_score = 0
        avg_score_st_dev = 0
        num_participants = 0

    analytics = None
    try:
        analytics = EventAnalytics.objects.get(event=event)
    except EventAnalytics.DoesNotExist:
        analytics = EventAnalytics.objects.create(event=event, course=course, high_score=high_score, lowest_score=low_score,
                                      avg_score=avg_score, avg_score_st_dev=avg_score_st_dev,
                                      num_participants=num_participants)
        return EventAnalyticsSerializer(analytics).data
    else:
        analytics.high_score = high_score
        analytics.lowest_score = low_score
        analytics.avg_score = avg_score
        analytics.avg_score_st_dev = avg_score_st_dev
        analytics.num_participants = num_participants
        analytics.save()
        return EventAnalyticsSerializer(analytics).data

