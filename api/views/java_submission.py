from rest_framework import viewsets
from api.pagination import BasePagination
from api.permissions import TeacherAccessPermission
from api.serializers import JavaSubmissionSerializer
from course.models.java import JavaSubmission


class JavaSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JavaSubmission.objects.all()
    serializer_class = JavaSubmissionSerializer
    permission_classes = [TeacherAccessPermission]
    pagination_class = BasePagination
