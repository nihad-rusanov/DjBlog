## Installation

Firstly run this in terminal

``` git clone  git@github.com:nihad-rusanov/DjBlog.git ```

 And then 

``` cd djblog ```

Create venv

``` py -m venv venv ```

Run venv

``` venv\Scripts\activate ```

Install dependencies

``` pip install -r requirements.txt ```

Then 

``` py manage.py migrate ```

Finally

``` py manage.py runserver ```
