from rest_framework import serializers

from .models import *

class AnswerSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Answer
        fields = (
            "id",
            "content",
            "group",
        )

class QuestionSerializer(serializers.ModelSerializer):
    """"""
    answers = AnswerSerializer()

    class Meta:
        model = Question
        fields = (
            "id",
            "content",
            "answers",
        )
    def create(self, validate_data):
        validateAnswers = validate_data.get("answers")
        validate_data.pop("answers")
        question = Question.objects.create(**validate_data)
        answers = []
        for answer in validateAnswers:
            serializer = AnswerSerializer(data = answer)
            serializer.is_valid(raise_exception=True)
            serializer.data.question.add(question, bulk = False)
            serializer.save()

        return Question.objects.get(id = question.id)
    
    """def update()"""

class TestSerializer(serializers.ModelSerializer):
    """"""

    questions = QuestionSerializer()
    
    class Meta:
        model = Test
        fields = (
            "id",
            "description",
            "questions",
        )
    def create(self, validate_data):
        validateQuestions = validate_data.get("questions")
        validate_data.pop("questions")
        test = Test.objects.create(**validate_data)
        questions = []
        for question in validateQuestions:
            serializer = QuestionSerializer(data = question)
            serializer.is_valid(raise_exception=True)
            serializer.data.test.add(test, bulk = False)
            serializer.save()

        return Test.objects.get(id = test.id)
    
    """def update()"""
