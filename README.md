
Install instruction:

> \# Create virtualenv:
> <tt>cd **project_folder**</tt>
> <tt>virtualenv TLB</tt>
> <tt>source TLB/bin/activate</tt>
> <tt>pip install -r requirements.txt</tt>
> \# Create database
> <tt>python models/manage.py version_control sqlite:///project.db models</tt>
> <tt>python manage.py upgrade</tt>
> \# Check DB version
>  <tt>python manage.py db_version</tt>
> \# Correct command output: "2"
>  \# [optional] Run tests
>  <tt>bash run_tests.sh</tt>
>  \# Run developer server
>  <tt>python server.py</tt>

After that devel server will be avaible on the http://127.0.0.1:5000/

API reference

> <b>/book/</b>
> <tt>GET /book/:book_id:</tt>
> Response:
>     JSON, which contains returned name, authors list and description for book with id=book_id
>     
> <tt>PUT /book/:book_id:</tt>
> Request format:
>     <tt>{"name": "string", "description": "string", "authors": [integer_list]}</tt>
>     All arguments are optional, but request must contain at least one param. Authors is an integer list; each integer should be correct Author id
> Response:
>   status code 200 if update processed successfully
>   status code != 200 if update processed with errors
>   
> <tt>POST /book/new/</tt>
> Request format:
>   <tt>{"name": "string", "description": "string", "authors": [integer_list]}</tt>
>   All params are required
> Response:
>   status code 200 and new book id, if book creation was successfull
>   status code != 200 if update processed with errors
>   
> <tt>DELETE /book/<int:book_id></tt>
> Response:
>   status code 200 if deletion processed successfully
>   status code != 200 if deletion processed with errors
> 
> 
> <b>/authors/</b>
> <tt>GET /authors/:author_id:</tt>
> Response format: 
>     JSON which contains information about author
>
> <tt>PUT /authors/:author_id:</tt>
> Resuest format:
>     <tt>{"name": "string", "description": "string"}</tt>
> Response format:
>   status code 200 if update processed successfully
>   status code != 200 if update processed with errors
>
> <tt>POST /authors/new</tt>
 Resuest format:
>     <tt>{"name": "string", "description": "string"}</tt>
> Response format:
>   status code 200 and new book id, if creation was successfull
>   status code != 200 in case of any errors
>
>    <tt>DELETE /authors/:author_id:</tt>
> Response:
>   status code 200 if deletion processed successfully
>   status code != 200 if deletion processed with errors
>
>
> <b>/library/</b>
> <tt>GET /library/:page_id:</tt>
> Returned paginated library. Page size is set via config file (<tt>LIBRARY_PAGE_SIZE</tt>)
> <tt>:page_id:</tt> is optional argument
>
>
><b>/statistics/</b>
><tt>GET /statistics/</tt>
> Returned stored authors and books amount
>
