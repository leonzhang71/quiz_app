import pytest
from django.urls import reverse

from quiz_project.quiz.models import Question, Choice

pytestmark = pytest.mark.django_db


@pytest.fixture
def quiz_questions():
    """Create a small set of questions with choices for testing."""
    q1 = Question.objects.create(text="Capital of France?", points=2)
    Choice.objects.create(question=q1, text="Paris", is_correct=True)
    Choice.objects.create(question=q1, text="London", is_correct=False)

    q2 = Question.objects.create(text="2 + 2 = ?", points=1)
    Choice.objects.create(question=q2, text="4", is_correct=True)
    Choice.objects.create(question=q2, text="5", is_correct=False)

    return [q1, q2]


def test_quiz_view_get_renders_questions(client, quiz_questions):
    url = reverse("quiz")
    response = client.get(url)
    assert response.status_code == 200

    content = response.content.decode()
    for question in quiz_questions:
        assert question.text in content


def test_quiz_view_post_all_correct(client, quiz_questions):
    url = reverse("quiz")
    post_data = {
        str(q.id): q.choices.filter(is_correct=True).first().id for q in quiz_questions
    }
    response = client.post(url, post_data)
    assert response.status_code == 200

    total_points = sum(q.points for q in quiz_questions)
    assert f"Your Score: {total_points}/{total_points}" in response.content.decode()


def test_quiz_view_post_partial_correct(client, quiz_questions):
    url = reverse("quiz")
    # Only answer the first question correctly
    q1 = quiz_questions[0]
    post_data = {str(q1.id): q1.choices.filter(is_correct=True).first().id}

    response = client.post(url, post_data)
    assert response.status_code == 200

    total_points = sum(q.points for q in quiz_questions)
    expected_score = q1.points
    assert f"Your Score: {expected_score}/{total_points}" in response.content.decode() 