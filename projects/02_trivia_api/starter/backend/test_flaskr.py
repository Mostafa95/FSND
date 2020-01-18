import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user_name = "postgres"
        self.password = "postgres"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.user_name,
            self.password,
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_endpoint_get_categories(self):
        res = self.client().get('/categori')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_get_questions(self):
        res = self.client().get('/questions?page=2')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_pagination_get_questions(self):
        res = self.client().get('/questions?page=100')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        body = json.loads(res.data)
        ques = Question.query.filter_by(id=1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(ques, None)

    def test_422_wrong_ID_delete_question(self):
        res = self.client().delete('/questions/1000')
        body = json.loads(res.data)
        ques = Question.query.filter_by(id=1000).one_or_none()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(body['success'], False)

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'la'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['totalQuestions'])

    def test_search_question_empty_result(self):
        res = self.client().post('/questions', json={'searchTerm': 'z'})
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['totalQuestions'], 0)

    def test_create_question(self):
        res = self.client().post(
            '/questions',
            json={
                "question": "can you?",
                "answer": "nope",
                "category": "3",
                "difficulty": "1"}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_422_wrong_category_create_question(self):
        res = self.client().post(
            '/questions',
            json={
                "question": "can you?",
                "answer": "nope",
                "category": "1000",
                "difficulty": "1"}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_get_by_category(self):
        res = self.client().get('/categories/1/questions')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_wrong_ID_get_by_category(self):
        res = self.client().get('/categories/1000/questions')
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_quizzes_get_by_category(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": "",
                "quiz_category": {"id": "1", "type": "Science"}}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)

    def test_404_quizzes_get_by_category_wrong_ID(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": "",
                "quiz_category": {"id": "100", "type": "Any"}}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['success'], False)

    def test_quizzes_get_by_category_new_category_ID(self):
        new_cat = Category("newType")
        new_cat.insert()
        id = Category.query.order_by(self.db.desc(Category.id)).first()
        id = id.format()
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": "",
                "quiz_category": {"id": str(id['id']), "type": id['type']}}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['question'], '')
        new_cat.delete()

    def test_quizzes_get_by_category_with_previous_question(self):
        res = self.client().post(
            '/quizzes',
            json={
                "previous_questions": [{"id": "5"}],
                "quiz_category": {"id": "1", "type": "Science"}}
            )
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['success'], True)
        self.assertNotEqual(body['question']['id'], 5)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
