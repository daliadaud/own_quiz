from quiz.models import Quiz, QuizQuestion, QuestionChoiceAnswer, QuizChoiceResult, QuizInstance, QuizInstanceAnswer
from rest_framework import serializers
"""
class CreateImportJobSerializer(serializers.Serializer):
    import_file = serializers.FileField()


class ImportJobSerializer(serializers.ModelSerializer):
    mappings = serializers.SerializerMethodField()
    headers = serializers.SerializerMethodField()
    system_fields = serializers.SerializerMethodField()
    rejected = serializers.SerializerMethodField()

    class Meta:
        model = ImportJob
        fields = ('id', 'import_file', 'rejected', 'headers', 'summary', 'is_completed', 'duplicate_handling', 'system_fields', 'mappings')
        read_only_fields = ('import_file', 'rejected', 'headers', 'summary', 'is_completed', 'mappings')

    def get_mappings(self, obj):
        return ImportMappingField.get_job_mappings(import_job=obj)

    def get_headers(self, obj):
        return obj.get_file_headers()

    def get_system_fields(self, obj):
        return ImportSystemField.get_system_fields()

    def get_rejected(self, obj):
        request = self.context['request']
        if obj.is_job_completed() and obj.is_rejected_entries():
            return request.build_absolute_uri(obj.rejected.url)
        return ""
"""


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz