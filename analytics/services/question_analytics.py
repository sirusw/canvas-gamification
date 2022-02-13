import json
from datetime import datetime
from django.utils.timezone import utc

from analytics.models import JavaSubmissionAnalytics, MCQSubmissionAnalytics, ParsonsSubmissionAnalytics
from analytics.models.java import JavaQuestionAnalytics
from analytics.models.mcq import MCQQuestionAnalytics
from analytics.models.models import QuestionAnalytics, SubmissionAnalytics
import statistics

from analytics.models.parsons import ParsonsQuestionAnalytics
from analytics.services.submission_analytics import get_all_submission_analytics
from api.serializers.question_analytics import QuestionAnalyticsSerializer, JavaQuestionAnalyticsSerializer, \
    MCQQuestionAnalyticsSerializer, ParsonsQuestionAnalyticsSerializer
from canvas.models import Event
from course.models.models import Question
from course.models.java import JavaQuestion
from course.models.parsons import ParsonsQuestion
from course.models.multiple_choice import MultipleChoiceQuestion
from django.db.models import Avg, Max


def get_question_analytics(question):
    # try:
    #     if isinstance(question, JavaQuestion):
    #         analytics = JavaQuestionAnalytics.objects.get(question=question)
    #     if isinstance(question, ParsonsQuestion):
    #         analytics = ParsonsQuestionAnalytics.objects.get(question=question)
    #     if isinstance(question, MultipleChoiceQuestion):
    #         analytics = MCQQuestionAnalytics.objects.get(question=question)
    #
    # except QuestionAnalytics.DoesNotExist:
    return create_question_analytics(question)
    # else:
    #     now = datetime.utcnow().replace(tzinfo=utc)
    #     time_diff = now - analytics.time_created
    #     time_diff = time_diff.total_seconds()
    #     # the analytics expires after one day
    #     if time_diff < 86400:
    #         if isinstance(analytics, JavaQuestionAnalytics):
    #             return JavaQuestionAnalyticsSerializer(analytics).data
    #         if isinstance(analytics, ParsonsQuestionAnalytics):
    #             return ParsonsQuestionAnalyticsSerializer(analytics).data
    #         if isinstance(analytics, MCQQuestionAnalytics):
    #             return MCQQuestionAnalyticsSerializer(analytics).data
    #     else:
    #         return create_question_analytics(question)


def get_all_question_analytics():
    submission_analytics = get_all_submission_analytics()
    distinct_events = []
    analytics = []
    for item in submission_analytics:
        if item.event not in distinct_events:
            distinct_events.append(item.event)
    for event in distinct_events:
        question_list = []
        for item in submission_analytics:
            if item.event.id == event.id and item.question not in question_list:
                question_list.append(item.question)
        for question in question_list:
            analytics.append(create_question_analytics(question))
    return analytics


def get_question_analytics_by_event(event):
    analytics = get_all_question_analytics()
    if analytics is None:
        return {}
    analytics_by_event = []
    for item in analytics:
        if item.event == event:
            analytics_by_event.append(item)
    return analytics_by_event


def create_question_analytics(question):
    submission_analytics = get_all_submission_analytics()
    event = question.event
    course = question.course
    analytics_by_question = []
    for analytics in submission_analytics:
        if analytics.question.id == question.id:
            analytics_by_question.append(analytics)
    num_respondents = []
    for analytics in analytics_by_question:
        if analytics.user_id not in num_respondents:
            num_respondents.append(analytics.user_id)
    num_respondents = len(num_respondents)
    if num_respondents == 0:
        return 'No Submission Analytics are found.'
    total_attempts = 0
    attempts = []
    total_grade = 0
    grade = []
    time_spent = []
    distinct_user = []
    for item in analytics_by_question:
        total_grade += item.submission.grade
        grade.append(item.submission.grade)
        time_spent.append(item.time_spent)
        if item.user_id not in distinct_user:
            distinct_user.append(item.user_id)
    for user in distinct_user:
        max_attempt = 0
        for item in analytics_by_question:
            if item.user_id == user:
                if item.num_attempts > max_attempt:
                    max_attempt = item.num_attempts
        total_attempts += max_attempt
        attempts.append(max_attempt)

    avg_attempt = total_attempts / num_respondents
    attempt_std_dev = statistics.stdev(attempts) if len(attempts) > 1 else 0
    avg_grade = total_grade / num_respondents
    grade_std_dev = statistics.stdev(grade) if len(grade) > 1 else 0

    time_spent = [i for i in time_spent if i > 0]
    median_time_spent = statistics.median(time_spent) if len(time_spent) != 0 else 0

    lines = 0
    blank_lines = 0
    comment_lines = 0
    import_lines = 0
    cyclomatic_complexity = 0
    method = 0
    operator = 0
    operand = 0
    unique_operator = 0
    unique_operand = 0
    vocab = 0
    size = 0
    vol = 0
    difficulty = 0
    effort = 0
    error = 0
    test_time = 0
    count = 0
    if isinstance(analytics_by_question[0], JavaSubmissionAnalytics) or isinstance(analytics_by_question[0],
                                                                                   ParsonsSubmissionAnalytics):
        for item in analytics_by_question:
            lines += item.lines
            blank_lines += item.blank_lines
            comment_lines += item.comment_lines
            import_lines += item.import_lines
            cyclomatic_complexity += item.cyclomatic_complexity
            method += item.method
            operator += item.operator
            operand += item.operand
            unique_operator += item.unique_operator
            unique_operand += item.unique_operand
            vocab += item.vocab
            size += item.size
            vol += item.vol
            difficulty += item.difficulty
            effort += item.effort
            error += item.error
            test_time += item.test_time
            count += 1

    if isinstance(analytics_by_question[0], JavaSubmissionAnalytics):
        if count != 0:
            lines = item.lines / count
            blank_lines = item.blank_lines / count
            comment_lines = item.comment_lines / count
            import_lines = item.import_lines / count
            cyclomatic_complexity = item.cyclomatic_complexity / count
            method = item.method / count
            operator = item.operator / count
            operand = item.operand / count
            unique_operator = item.unique_operator / count
            unique_operand = item.unique_operand / count
            vocab = item.vocab / count
            size = item.size / count
            vol = item.vol / count
            difficulty = item.difficulty / count
            effort = item.effort / count
            error = item.error / count
            test_time = item.test_time / count

            question_analytics = JavaQuestionAnalytics(
                question=question,
                event=event,
                course=course,
                most_frequent_wrong_ans='',
                avg_grade=avg_grade,
                grade_std_dev=grade_std_dev,
                num_respondents=num_respondents,
                avg_attempt=avg_attempt,
                attempt_std_dev=attempt_std_dev,
                median_time_spent=median_time_spent,
                lines=lines,
                blank_lines=blank_lines,
                comment_lines=comment_lines,
                import_lines=import_lines,
                cyclomatic_complexity=cyclomatic_complexity,
                method=method,
                operator=operator,
                operand=operand,
                unique_operator=unique_operator,
                unique_operand=unique_operand,
                vocab=vocab,
                size=size,
                vol=vol,
                difficulty=difficulty,
                effort=effort,
                error=error,
                test_time=test_time

            )
        return question_analytics
    if isinstance(analytics_by_question[0], ParsonsSubmissionAnalytics):
        if count != 0:
            lines = item.lines / count
            blank_lines = item.blank_lines / count
            comment_lines = item.comment_lines / count
            import_lines = item.import_lines / count
            cyclomatic_complexity = item.cyclomatic_complexity / count
            method = item.method / count
            operator = item.operator / count
            operand = item.operand / count
            unique_operator = item.unique_operator / count
            unique_operand = item.unique_operand / count
            vocab = item.vocab / count
            size = item.size / count
            vol = item.vol / count
            difficulty = item.difficulty / count
            effort = item.effort / count
            error = item.error / count
            test_time = item.test_time / count
            question_analytics = ParsonsQuestionAnalytics.objects.create(
                question=question,
                event=event,
                course=course,
                most_frequent_wrong_ans='',
                avg_grade=avg_grade,
                grade_std_dev=grade_std_dev,
                num_respondents=num_respondents,
                avg_attempt=avg_attempt,
                attempt_std_dev=attempt_std_dev,
                median_time_spent=median_time_spent,
                lines=lines,
                blank_lines=blank_lines,
                comment_lines=comment_lines,
                import_lines=import_lines,
                cyclomatic_complexity=cyclomatic_complexity,
                method=method,
                operator=operator,
                operand=operand,
                unique_operator=unique_operator,
                unique_operand=unique_operand,
                vocab=vocab,
                size=size,
                vol=vol,
                difficulty=difficulty,
                effort=effort,
                error=error,
                test_time=test_time

            )
        return question_analytics
    if isinstance(analytics_by_question[0], MCQSubmissionAnalytics):
        most_frequent_wrong_ans = [{"a": 0, "b": 0, "c": 0, "d": 0}]
        for item in analytics_by_question:
            most_frequent_wrong_ans[0][item.answer] += 1
        answers = MCQSubmissionAnalytics.objects \
            .filter(question=question).values_list('answer', flat=True)
        distinct_ans = answers.distinct()
        # correct_ans = question.answer
        # answers = list(answers)
        # for ans in distinct_ans:
        #     if ans != correct_ans:
        #         most_frequent_wrong_ans.append({ans: answers.count(ans)})
        question_analytics = MCQQuestionAnalytics(
            question=question,
            event=event,
            course=course,
            most_frequent_wrong_ans=most_frequent_wrong_ans,
            avg_grade=avg_grade,
            grade_std_dev=grade_std_dev,
            num_respondents=num_respondents,
            avg_attempt=avg_attempt,
            attempt_std_dev=attempt_std_dev,
            median_time_spent=median_time_spent,
        )
        return question_analytics
