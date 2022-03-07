import json

from accounts.models import MyUser
from analytics.models import JavaSubmissionAnalytics, ParsonsSubmissionAnalytics, MCQSubmissionAnalytics
from analytics.models.models import SubmissionAnalytics
from analytics.utils.init_analytics import SubmissionAnalyticsObj
from api.serializers.submission_analytics import JavaSubmissionAnalyticsSerializer, \
    ParsonsSubmissionAnalyticsSerializer, MCQSubmissionAnalyticsSerializer, SubmissionAnalyticsSerializer
from course.models.java import JavaSubmission
from course.models.models import Submission
from course.models.multiple_choice import MultipleChoiceSubmission
from course.models.parsons import ParsonsSubmission
from general.models.action import Action, ActionVerb


def get_submission_analytics(submission):
    return create_submission_analytics(submission)


def get_all_submission_analytics():
    submissions = Submission.objects.all()
    analytics = []
    for submission in submissions:
        analytics.append(create_submission_analytics(submission))
    return analytics


def get_submission_analytics_by_question(question):
    submissions = Submission.objects.all()
    analytics = []
    for submission in submissions:
        if submission.question.id == question.id:
            analytics.append(create_submission_analytics(submission))
    return analytics


def create_submission_analytics(submission):
    curr_uqj_submissions = Submission.objects.filter(uqj=submission.uqj.id)
    num_attempts = curr_uqj_submissions.count()
    user_obj = MyUser.objects.get(pk=submission.user.pk)
    time_spent = 0

    try:
        submission_time = Action.objects.get(object_id=submission.pk, verb=ActionVerb.SUBMITTED).time_created
        question_last_access_time = Action.objects \
            .filter(actor=user_obj, object_id=submission.question.id, verb=ActionVerb.OPENED,
                    time_created__lt=submission_time) \
            .order_by('-time_created').first()
    except Action.DoesNotExist:
        pass
    else:
        if question_last_access_time:

            question_last_access_time = question_last_access_time.time_created
            time_diff = submission_time - question_last_access_time
            time_spent = time_diff.total_seconds()

    # is_correct = False
    # for item in curr_uqj_submissions:
    #     if item.is_correct is True:
    #         is_correct = True
    #         break

    if isinstance(submission, JavaSubmission):
        ans = submission.answer_files
        sub_analytics_dict = SubmissionAnalyticsObj(ans)
        decoded_results = submission.get_decoded_results()

        submission_analytics_obj = JavaSubmissionAnalytics(decoded_results=decoded_results,
                                                           uqj=submission.uqj, submission=submission,
                                                           question=submission.question,
                                                           event=submission.question.event,
                                                           user_id=submission.user,
                                                           first_name=user_obj.first_name,
                                                           last_name=user_obj.last_name,
                                                           ans_file=ans, time_spent=time_spent,
                                                           num_attempts=num_attempts,
                                                           is_correct=submission.is_correct,
                                                           lines=sub_analytics_dict.lines,
                                                           blank_lines=sub_analytics_dict.blank_lines,
                                                           comment_lines=sub_analytics_dict.comment_lines,
                                                           import_lines=sub_analytics_dict.imported_lines,
                                                           cyclomatic_complexity=sub_analytics_dict.cc,
                                                           method=sub_analytics_dict.method,
                                                           operator=sub_analytics_dict.operator,
                                                           operand=sub_analytics_dict.operand,
                                                           unique_operator=sub_analytics_dict.unique_operator,
                                                           unique_operand=sub_analytics_dict.unique_operand,
                                                           vocab=sub_analytics_dict.vocab,
                                                           size=sub_analytics_dict.size,
                                                           vol=sub_analytics_dict.vol,
                                                           difficulty=sub_analytics_dict.difficulty,
                                                           effort=sub_analytics_dict.effort,
                                                           error=sub_analytics_dict.error,
                                                           test_time=submission.results[0]['time'],
                                                           space=submission.results[0]['memory'])
        return submission_analytics_obj
    if isinstance(submission, ParsonsSubmission):
        ans = submission.answer_files
        input_files = submission.question.get_input_files()
        missing_lines = [{}]
        for item in input_files:
            missing_lines[0][item["name"]] = []
            lines = item["lines"]
            num = len(lines)
            ans_line_by_line = ans[item["name"]].split('\n')
            for line in lines:
                has_line = False
                if len(ans_line_by_line) <= 1:
                    break
                for ans_line in ans_line_by_line:
                    if line in ans_line:
                        has_line = True
                        break
                if not has_line:
                    missing_lines[0][item["name"]].append(line)
                    num -= 1
            if num == 0:
                missing_lines[0][item["name"]] = []

        sub_analytics_dict = SubmissionAnalyticsObj(ans)
        decoded_results = submission.get_decoded_results()
        submission_analytics_obj = ParsonsSubmissionAnalytics(decoded_results=decoded_results,
                                                              missing_lines=missing_lines,
                                                              uqj=submission.uqj, submission=submission,
                                                              question=submission.question,
                                                              event=submission.question.event,
                                                              user_id=submission.user,
                                                              first_name=user_obj.first_name,
                                                              last_name=user_obj.last_name,
                                                              ans_file=ans, time_spent=time_spent,
                                                              num_attempts=num_attempts,
                                                              is_correct=submission.is_correct,
                                                              lines=sub_analytics_dict.lines,
                                                              blank_lines=sub_analytics_dict.blank_lines,
                                                              comment_lines=sub_analytics_dict.comment_lines,
                                                              import_lines=sub_analytics_dict.imported_lines,
                                                              cyclomatic_complexity=sub_analytics_dict.cc,
                                                              method=sub_analytics_dict.method,
                                                              operator=sub_analytics_dict.operator,
                                                              operand=sub_analytics_dict.operand,
                                                              unique_operator=sub_analytics_dict.unique_operator,
                                                              unique_operand=sub_analytics_dict.unique_operand,
                                                              vocab=sub_analytics_dict.vocab,
                                                              size=sub_analytics_dict.size,
                                                              vol=sub_analytics_dict.vol,
                                                              difficulty=sub_analytics_dict.difficulty,
                                                              effort=sub_analytics_dict.effort,
                                                              error=sub_analytics_dict.error,
                                                              test_time=submission.results[0]['time'],
                                                              space=submission.results[0]['memory'])
        return submission_analytics_obj
    if isinstance(submission, MultipleChoiceSubmission):
        submission_analytics_obj = MCQSubmissionAnalytics(uqj=submission.uqj, submission=submission,
                                                          question=submission.question,
                                                          event=submission.question.event,
                                                          user_id=submission.user,
                                                          first_name=user_obj.first_name,
                                                          last_name=user_obj.last_name,
                                                          answer=submission.answer,
                                                          time_spent=time_spent,
                                                          num_attempts=num_attempts,
                                                          is_correct=submission.is_correct, )
        return submission_analytics_obj
