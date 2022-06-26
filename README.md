# API Gateway example project
Django based wsgi application serving as a web gateway for connections to remote API services.

## Deployment
* clone repo
* `cd api_gateway & python -m venv venv`
* `pip install -r requiremnets.txt`

## Usage
* Start development web server `cd gateway & python manage.py runserver`. 
It starts serving on localhost:8000 by default.
* Make GET request with browser or another tool to `localhost:8000/api/<endpoint>?params`, 
where `<endpoint>` is a currently supported API service and `params` are URL parameter (field/value pairs).

## Services
Currently there is only one API service enabled:
* [newsapi](newsapi.org):
  * required params:
    * endpoint - service's endpoint, currently supported:
      * `top-headlines`
    * country
    * category
    * apiKey
  * no optional params
  * example usage `http://localhost:8000/api/newsapi?endpoint=top-headlines&country=us&category=business&apiKey=af92652e76b745a6bde8dd2fc5739bfd`
