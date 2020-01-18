# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<int:id>/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/<int:id>'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: JSON response containing:
    ='success':response status(True or False)
    ='categories': dictionary conating key-value pairs

e.g.  
{"categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}


GET '/questions'
- Fetch a dictionary of questions where keys are attributes of questions table, and values are their corresponding values
- Request Arguments: page number
- Returns : JSON response containing following keys:
    ='success': response status(True or False)
    ='questions': list of dictionary of paginated questions
    ='total_questions': number of all questions in DB
    ='current_category': category of returned questions 
    ='categories': list of dictionaries containing all categories

e.g.
{"categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 22
}


POST '/questions'
- This endpoint has 2 functionalities:
    1- Create question and insert it into DB
        Request arguments: 'question','answer','category','difficulty'
        Returns : JSON response constaining status of request:
            ='success': response status(True or False)
        
        e.g.
        {'success':true}

    2- Search for a given keyword in all questions
        Request arguments: 'searchTerm'
        Returns: JSON response containing following keys:
            ='success':response status(True or False)
            ='questions':list of dictionaries of questions containing keyword
            ='totalQuestions': number of all questions in DB
            ='currentCategory':category of returned questions 
        
        e.g.
        {"currentCategory": "", 
        "questions": [
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }
        ], 
        "success": true, 
        "totalQuestions": 1
        }



DELETE '/questions/<int:id>'
- Delete a question with given ID
- Request Arguments: Queestion ID
- Returns : JSON response constaining status of request:
    ='success': response status(True or False)

e.g.
{'success':true}


GET '/categories/<int:id>/questions'
- Fetch a dictionary of questions with given category ID.
- Request Arguments: Category ID
- Returns: JSON response containing following:
    ='success':response status(True or False)
    ='questions':list of dictionaries of questions with category ID
    ='totalQuestions':number of all questions in DB
    ='currentCategory':category of returned questions 

e.g.
{"currentCategory": {
    "1": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "totalQuestions": 3
}


POST '/quizzes'
- Fetches a question based on a given category. Unique question will always be returned, meaning a question will never be returned twice. It usees a list of previous questions for reference.
- Request Arguments: 'previous_questions','quiz_category'
- Returns: JSON response containing following:
    ='success':response status(True or False)
    ='question':question selected based on category.

e.g.
{
  "question": {
    "answer": "Maya Angelou", 
    "category": 4, 
    "difficulty": 2, 
    "id": 5, 
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }, 
  "success": true
}
```


## Testing  
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```