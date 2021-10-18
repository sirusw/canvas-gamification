from rest_framework import viewsets
from api.pagination import BasePagination
from api.permissions import TeacherAccessPermission
from api.serializers import ParsonsSubmissionSerializer
from course.models.parsons import ParsonsSubmission


class ParsonsSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParsonsSubmission.objects.all()
    serializer_class = ParsonsSubmissionSerializer
    permission_classes = [TeacherAccessPermission]
    pagination_class = BasePagination
