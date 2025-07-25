import pytest

from quiz_project.quiz.models import Question, Choice

pytestmark = pytest.mark.django_db


def test_question_str_representation():
    question = Question.objects.create(text="Sample question?")
    assert str(question) == "Sample question?"


def test_question_default_points():
    question = Question.objects.create(text="Another question?")
    assert question.points == 1


def test_choice_str_representation():
    question = Question.objects.create(text="Select one")
    choice = Choice.objects.create(question=question, text="Option A", is_correct=True)
    assert str(choice) == "Option A" 