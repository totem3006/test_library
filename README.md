Install instruction:

> \# Create virtualenv:<br/>
> <tt>cd **project_folder**</tt><br/>
> <tt>virtualenv TLB</tt><br/>
> <tt>source TLB/bin/activate</tt><br/>
> <tt>pip install -r requirements.txt</tt><br/>
> \# Create database<br/>
> <tt>python models/manage.py version_control sqlite:///project.db models</tt><br/>
> <tt>python manage.py upgrade</tt><br/>
> \# Check DB version<br/>
>  <tt>python manage.py db_version</tt><br/>
> \# Correct command output: "2"<br/>
>  \# [optional] Run tests<br/>
>  <tt>bash run_tests.sh</tt><br/>
>  \# Run developer server<br/>
>  <tt>python server.py</tt><br/>

After that devel server will be avaible on the <tt>http://127.0.0.1:5000/</tt>

API reference

> <b>/book/</b><br/>
> <tt>GET /book/:book_id:</tt><br/>
> Response:<br/>
>     JSON, which contains returned name, authors list and description for book with id=book_id<br/>
>     <br/>
> <tt>PUT /book/:book_id:</tt><br/>
> Request format:<br/>
>     <tt>{"name": "string", "description": "string", "authors": [integer_list]}</tt><br/>
>     All arguments are optional, but request must contain at least one param. Authors is an integer list; each integer should be correct Author id<br/>
> Response:<br/>
>   status code 200 if update processed successfully<br/>
>   status code != 200 if update processed with errors<br/>
>   <br/>
> <tt>POST /book/new/</tt><br/>
> Request format:<br/>
>   <tt>{"name": "string", "description": "string", "authors": [integer_list]}</tt><br/>
>   All params are required<br/>
> Response:<br/>
>   status code 200 and new book id, if book creation was successfull<br/>
>   status code != 200 if update processed with errors<br/>
>   <br/>
> <tt>DELETE /book/<int:book_id></tt><br/>
> Response:<br/>
>   status code 200 if deletion processed successfully<br/>
>   status code != 200 if deletion processed with errors<br/>
> <br/>
> <br/>
> <b>/authors/</b><br/>
> <tt>GET /authors/:author_id:</tt><br/>
> Response format: <br/>
>     JSON which contains information about author<br/>
><br/>
> <tt>PUT /authors/:author_id:</tt><br/>
> Resuest format:<br/>
>     <tt>{"name": "string", "description": "string"}</tt><br/>
> Response format:<br/>
>   status code 200 if update processed successfully<br/>
>   status code != 200 if update processed with errors<br/>
><br/>
> <tt>POST /authors/new</tt><br/>
 Resuest format:<br/>
>     <tt>{"name": "string", "description": "string"}</tt><br/>
> Response format:<br/>
>   status code 200 and new book id, if creation was successfull<br/>
>   status code != 200 in case of any errors<br/>
><br/>
>    <tt>DELETE /authors/:author_id:</tt><br/>
> Response:<br/>
>   status code 200 if deletion processed successfully<br/>
>   status code != 200 if deletion processed with errors<br/>
><br/>
><br/>
> <b>/library/</b><br/>
> <tt>GET /library/:page_id:</tt><br/>
> Returned paginated library. Page size is set via config file (<tt>LIBRARY_PAGE_SIZE</tt>)<br/>
> <tt>:page_id:</tt> is optional argument<br/>
><br/>
><br/>
><b>/statistics/</b><br/>
><tt>GET /statistics/</tt><br/>
> Returned stored authors and books amount<br/>
>
