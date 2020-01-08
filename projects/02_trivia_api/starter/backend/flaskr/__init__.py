import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,DELETE')
    return response

  @app.route('/categories',methods=['GET'])
  def get_categories():
    cats = Category.query.all()
    result = {
      "success":True,
      "categories": [cat.format() for cat in cats]
    }
    return jsonify(result)


  ''' 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
    page = request.args.get('page',1,type=int)

    ques = Question.query.all()
    cats = Category.query.all()
    
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    if len(ques[start:end]) == 0:
      abort(404)

    questions = [que.format() for que in ques]
    categories = [cat.format() for cat in cats ]
    result = {
      'success':True,
      'questions':questions[start:end],
      'total_questions':len(questions[start:end]),
      'current_category':"",
      'categories':categories
    }

    return jsonify(result)

  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_question(id):
    try:
      
      ques = Question.query.filter_by(id=id).one_or_none()
      if ques == None:
        abort(404)
      
      ques.delete()
      return jsonify({
        'success':True
      })
    except:
      abort(422)
  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions',methods=['POST'])
  def create_question():
    body = request.get_json()
    
    if 'searchTerm' in body:
      term = body['searchTerm']
      questions = Question.query.filter(Question.question.ilike('%'+ term +'%')).all()
      questions = [ques.format() for ques in questions]
      print(questions)    
      return jsonify({
        'questions':questions,
        'totalQuestions':len(questions),
        'currentCategory':""
      })


    else:
      try:
        question = Question(question=body['question'],answer=body['answer'],
                          category=body['category'],difficulty=body['difficulty'])
        question.insert()
        return jsonify({
          'success':True
        })
      except:
        abort(422)
  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_by_category(id):
    category = Category.query.get(id)
    
    if category == None:
      abort (404)

    questions = Question.query.filter_by(category=id).all()
    
    category = category.format()['type']
    questions = [q.format() for q in questions]
    return jsonify({
      'questions':questions,
      'totalQuestions':len(questions),
      'currentCategory':category
    })


  '''
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def quiz():
    body = request.get_json()
    prev_ques = body['previousQuestions']
    category = body['quizCategory']
    result = Question(None,None,None,None)
    
    try:
      if 'id' in category:
        cur_ques = Question.query.filter_by(category = category['id']).all()
      else:
        cur_ques = Question.query.all()
    except:
      abort(404)

    for cur_id in cur_ques:
      used = 0
      for prev_id in prev_ques:
        if prev_id['id'] == str(cur_id.format()['id']):
          used = 1
          break
      if used == 0:
        result = cur_id
        break
      
    if result.question == None:
      result = ''
    else:
      result = result.format()
      
    return jsonify({
      'question':result
    })

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'messege':"Not found"
    }),404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'messege':"Unprocessable request"
    }),422

  @app.errorhandler(400)
  def Bad_request(error):
    return jsonify({
      'success':False,
      'error':400,
      'messege':"Bad request"
    }),400
  return app

    