from rest_framework import serializers

from .models import *

class AnswerSerializer(serializers.ModelSerializer):
    """Сериализация ответа"""
    class Meta:
        model = Answer
        fields = (
            "id",
            "content",
            "group",
        )

class QuestionSerializer(serializers.ModelSerializer):
    """Сериализация вопроса"""
    answers = AnswerSerializer(many = True)

    class Meta:
        model = Question
        fields = (
            "id",
            "content",
            "answers",
        )
    # def create(self, validate_data):
    #     validateAnswers = validate_data.get("answers")
    #     validate_data.pop("answers")
    #     question = Question.objects.create(**validate_data)
    #     answers = []
    #     for answer in validateAnswers:
    #         serializer = AnswerSerializer(data = answer)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.data.question.add(question, bulk = False)
    #         serializer.save()

    #     return Question.objects.get(id = question.id)

    """def update()"""

class TestSerializer(serializers.ModelSerializer):
    """Сериализация теста"""

    questions = QuestionSerializer(many = True)

    class Meta:
        model = Test
        fields = (
            "id",
            "description",
            "questions",
        )
        depth = 5
    #def create(self, validate_data):
    #    validateQuestions = validate_data.get("questions")
    #    validate_data.pop("questions")
    #    test = Test.objects.create(**validate_data)
    #    questions = []
    #    for question in validateQuestions:
    #        serializer = QuestionSerializer(data = question)
    #        serializer.is_valid(raise_exception=True)
    #        test.questions.add(serializer.data)

    #    return Test.objects.get(id = test.id)

    """def update()"""


class ResultOfTestSerializer(serializers.ModelSerializer):
    """Сериализация результата"""

    test = TestSerializer()

    class Meta:
        model = ResultOfTest
        fields = (
            "id",
            "competence",
            "test"
        )

    def create(self,validate_data):
        validateTest = validate_data.get("test")
        validate_data.pop("test")
        test = TestSerializer(data = validateTest)
        res = ResultOfTest.objects.create(test = test, **validate_data)
        res["competence"] = eval(res["competence"])
        return res