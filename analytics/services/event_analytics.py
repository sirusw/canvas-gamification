from datetime import datetime
from django.utils.timezone import utc

from accounts.models import MyUser
from analytics.models.models import EventAnalytics
from analytics.services.question_analytics import get_all_question_analytics
from api.serializers.event_analytics import EventAnalyticsSerializer
from canvas.models import Event
from canvas.utils.utils import get_total_event_grade
from course.models.models import Submission, UserQuestionJunction


def get_event_analytics(event):
    return create_event_analytics(event)


def get_all_event_analytics():
    events = Event.objects.all()
    event_analytics = []
    for event in events:
        event_analytics.append(get_event_analytics(event))
    return event_analytics


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
        print(grades)
        import statistics
        avg_score_st_dev = statistics.pstdev(grades)
        print(avg_score_st_dev)
        num_participants = len(grades)
    else:
        high_score = 0
        low_score = 0
        avg_score = 0
        avg_score_st_dev = 0
        num_participants = 0

    grades = [{'grades': grades}]
    analytics = EventAnalytics(event=event, course=course, high_score=high_score,
                               lowest_score=low_score,
                               avg_score=avg_score, avg_score_st_dev=avg_score_st_dev,
                               num_participants=num_participants, grades=grades)
    return analytics
