import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        '''
        This endpoint is responsible for returning all categories from DB
        '''
        cats = Category.query.all()
        cats_format = [cat.format() for cat in cats]

        cat_result = {}
        for c in cats_format:
            cat_result[c['id']] = c['type']

        result = {
          "success": True,
          "categories": cat_result
        }
        return jsonify(result)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        '''
        This endpoint gets all questions from DB,
        paginate them and return requested page
        '''
        page = request.args.get('page', 1, type=int)
        ques = Question.query.all()
        cats = Category.query.all()
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        if len(ques[start:end]) == 0:
            abort(404)
        questions = [que.format() for que in ques]
        categories = [cat.format() for cat in cats]
        cat_result = {}
        for d in categories:
            cat_result[d['id']] = d['type']
        result = {
          'success': True,
          'questions': questions[start:end],
          'total_questions': len(questions),
          'current_category': "",
          'categories': cat_result
        }
        return jsonify(result)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        '''
        This endpoint delete question given its ID
        '''
        try:
            ques = Question.query.filter_by(id=id).one_or_none()
            ques.delete()
            return jsonify({
              'success': True
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def createAndsearch_question():
        '''
        This endpoint has 2 functionalities:
          1- search for questions given a searchTerm
          2- create new question
        It decides based on keywords in the request.
        '''
        body = request.get_json()
        if 'searchTerm' in body:
            term = body['searchTerm']
            questions = Question.query.filter(
              Question.question.ilike('%'+term+'%')).all()
            questions = [ques.format() for ques in questions]
            return jsonify({
              'success': True,
              'questions': questions,
              'totalQuestions': len(questions),
              'currentCategory': ""
            })
        else:
            try:
                question = Question(
                  question=body['question'],
                  answer=body['answer'],
                  category=body['category'],
                  difficulty=body['difficulty'])
                question.insert()
                return jsonify({
                  'success': True
                })
            except Exception:
                abort(404)

    @app.route('/categories/<int:id>/questions')
    def get_by_category(id):
        '''
        This endpoint gets all questions with a given category
        '''
        category = Category.query.get(id)
        if category is None:
            abort(404)
        questions = Question.query.filter_by(
          category=category.format()['id']).all()
        questions = [q.format() for q in questions]
        category = category.format()
        cat_result = {}
        cat_result[category['id']] = category['type']
        return jsonify({
          'success': True,
          'questions': questions,
          'totalQuestions': len(questions),
          'currentCategory': cat_result
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        '''
        This endpoint return a random question within a given category.
        every question is only returned once.
        '''
        body = request.get_json()
        prev_ques = body['previous_questions']
        category = body['quiz_category']
        result = Question(None, None, None, None)
        # If category ALL is selected
        if category['type'] == 'click':
            cur_ques = Question.query.all()
        else:
            categoryTest = Category.query.get(category['id'])
            if categoryTest is None:
                abort(404)
            cur_ques = Question.query.filter_by(category=category['id']).all()
        # select a question not in previous_questions list
        random.shuffle(cur_ques)
        for cur_id in cur_ques:
            used = 0
            for prev_id in prev_ques:
                if prev_id == cur_id.format()['id']:
                    used = 1
                    break
            if used == 0:
                result = cur_id
                break
        if result.question is None:
            result = ''
        else:
            result = result.format()
        return jsonify({
          'success': True,
          'question': result
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'messege': "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          'success': False,
          'error': 422,
          'messege': "Unprocessable request"
        }), 422

    @app.errorhandler(400)
    def Bad_request(error):
        return jsonify({
          'success': False,
          'error': 400,
          'messege': "Bad request"
        }), 400
    return app
