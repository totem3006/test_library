Install instruction:
1) Create virtualenv
    $ cd <project_folder>
    $ virtualenv TLB
    $ source TLB/bin/activate
    $ pip install -r requirements.txt
2) Create database
    $ python models/manage.py version_control sqlite:///project.db models
    $ migrate manage manage.py --repository=models --url=sqlite:///project.db
    $ python manage.py upgrade
3) Check DB version:
    $ python manage.py db_version
Correct command output: "2"
4) [optional] Run tests
    $ bash run_tests.sh
5) Run test server
    $ python server.py

After that devel server will be avaible on the http://127.0.0.1:5000/

API reference

/book/
GET /book/<int:book_id>
Response:
    JSON, which contains returned name, authors list and description for book with id=book_id
PUT /book/<int:book_id>
Request format:
    {"name": "<string>", "description": "<string>", "authors": [<integer_list>]}
    All arguments are optional, but request must contain at least one param. Authors is an integer list; each integer should be correct Author id
Response:
  status code 200 if update processed successfully
  status code != 200 if update processed with errors
POST /book/new/
Request format:
  {"name": "<string>", "description": "<string>", "authors": [<integer_list>]}
  All params are required
Response:
  status code 200 and new book id, if book creation was successfull
  status code != 200 if update processed with errors
DELETE /book/<int:book_id>
Response:
  status code 200 if update processed successfully
  status code != 200 if update processed with errors
