---
title: How to Build a Simple Login System in FastHTML
date: 2024-09-01T11:20:06+01:00
draft: false
excerpt: Authentication doesn't have to be scary or complicated. Let's implement a classic login and authentication system using the user's email and password in FastHTML.
---

This is part 1 of a series of posts on how to build a simple user management system with FastHTML.

You can find the other parts of this series here:

- Part 1: Classic password-based login
- [Part 2: Passwordless Authentication](/posts/passwordless-auth-fasthtml)

__________

So many developers - especially in the JavaScript community - are afraid of building their own authentication and login system. They rather send their user data to a 3rd party service like auth0 or uses a library like Lucia than creating their own authentication and login system.

But authentication doesn't have to be scary or complicated.

I will show you how to create a simple session based login system on your own using the new [FastHTML](https://fastht.ml) python library. The library is very similar to [FastAPI](https://fastapi.tiangolo.com/), but geared towards HTML generation and interactivity instead of JSON APIs. 

But even if you don't know FastAPI or FastHTML, you should be able to follow along. The syntax is quite easy to grasp if you understand the basics of web development. 

If you know the basics of web development, [this guide](https://docs.fastht.ml/tutorials/quickstart_for_web_devs.html) gives you a good headstart on FastHTML.

And the idea behind session based authentication can be transfered to every web framework out there, obviously. 

Okay let's start: 

## Installing packages and setup

First things first. Let's install the needed packages and initialize a new FastHTML app. 

```
pip install python-fasthtml passlib
```

The code installs the [FastHTML library](https://fastht.ml) as well as the passlib library we use to hash the passwords (more on that later). 

Now create a `main.py` file and paste in the following code:

```python
from fasthtml.common import * 

from passlib.context import CryptContext

from functools import wraps

custom_styles = Style("""
.mw-960 { max-width: 960px; }
.mw-480 { max-width: 480px; }
.mx-auto { margin-left: auto; margin-right: auto; }

""")

app, rt = fast_app(live=True, debug=True, hdrs=(custom_styles,))

# all future code goes in here

serve()
```

This code imports the necessary classes and functions and then it initializes a new FastHTML app using the `fast_app` function. It returns the app instance as well as an instance of the router (`rt`) that we use to define our routes. 

The `serve()` function starts the web server, when we run the python file with `python main.py`. 

## Database setup

Next we need some kind of mechanism to persist the data of registered users. We'll use SQLite as our database here. 

[`fastlite`](https://answerdotai.github.io/fastlite/) is a simple python package that ships with FastHTML that makes working with SQLite a breeze. 

```python

db = database('data/users.db')

users = db.t.users

if users not in db.t:
    users.create(dict(email=str, password=str), pk='email')
    
User = users.dataclass()

```

This code initializes a new connection to a database called `users.db` in the `/data` folder (it will automatically create this file if it doesn't exist). All tables of the database are available in the `t` attribute. 

Then we create a new table called `users` if it doesn't already exist with the columns `email` and `password`, both of type string. The `email` column will be used as the primary key. 

`fastlite` has also the ability to generate a dataclass from a table schema automatically. That's what the last line does. 

## Creating a registration form

Okay so now that we have the basic database structure in place, we need a way to create users. 

Let's build a registration form together with a route handler for `/register`.

```python
def MyForm(btn_text, target):
    return Form(
        Input(id="email", type="email", placeholder="Email", required=True),
        Input(id="password", type="password", placeholder="Password", required=True),
        Button(btn_text, type="submit"),
        Span(id="error", style="color:red"),
        hx_post=target,
        hx_target="#error",
    )

@rt('/register')
def get():
    return Container(
        Article(
            H1("Register"),
            MyForm("Register", "/register"),
            Hr(),
            P("Already have an account? ", A("Login", href="/login")),
            cls="mw-480 mx-auto"
        )
    )

```

As you can see, in FastHTML we don't need to write HTML. We use something called `ft` instead. 

It's basically a representation of HTML elements as python functions. It maps 1:1 to HTML and HTML element attributes can be added as simple arguments to the functions. The neat thing is that we can use the full power of python for "templating", much similar to JSX in the JavaScript world. 

Here we define a `MyForm()` function that defines a simple form with two inputs for the email and the password of the user. We extracted it out in a seperate function because we will reuse it for the Login form later. 

You can also see that we use two `htmx` attributes of the form. FastHTML uses [`htmx`](https://htmx.org/) out of the box for frontend interactivity. 

## Handling the registration

The form sends a simple post request to the `/register` endpoint, which handles the creation of a new user in the database. Let's build this next. 

```py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@rt('/register')
def post(email:str, password:str):
    
    try:
        users[email]
        return "User already exists"
    except NotFoundError:

        new_user = User(email=email, password=get_password_hash(password))
    
        users.insert(new_user)
        
        return HttpHeader('HX-Redirect', '/login')
```

Here we define a post handler for `/register` (the decorated function name specifies which HTTP method it responds to). It receives the email and password strings as arguments because we named our input elements accordingly (`id` on an input element sets both the `id` and `name` to the specified string).

It then tries to fetch a user with the email from the database. If it exists it'll return a string with an error message which will be inserted into a `#error` span by `htmx` (see the `hx_target` attribute in `MyForm()`). 

If a user with this email cannot be found we are save and can create the user in the database. 

We create a new instance of the `User` dataclass and insert it into the users table. 

## Hashing passwords
But we also hash the password. What is this? 

You should **never ever save users passwords as plain strings in your database.** Never ever. Should the database get hacked, the attackers can see all of your users passwords in the open. That's a huge security issue.

What you should do instead is saving the passwords not in it's plain form but as hashes. You can think of hashes as a kind of encrypted version of the original string. 

That's what the `get_password_hash()` does. It creates a hash from the given password.

## Creating a login form

Okay now we have the registration of users in place. Let's now get to the actual login under the `/login` route.

```py
@rt('/login')
def get():
    return Container(
        Article(
            H1("Login"),
            MyForm("Login", target="/login"),
            Hr(),
            P("Want to create an Account? ", A("Register", href="/register")),
            cls="mw-480 mx-auto"
        )
    )
```

As you can see, it looks almost identical to the registration form and we reuse our `MyForm` component here.

## Handling the login

Again, it sends a `post` request to `/login`. Let's build the handler next. 

```py

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@rt('/login')
def post(session, email:str, password:str):
    try:
        user = users[email]
    except NotFoundError:
        return "Email or password are incorrect"
    
    if not verify_password(password, user.password):
        return "Email or password are incorrect"

    session['auth'] = user.email
    
    return HttpHeader('HX-Redirect', '/dashboard')

```

Here we try to retrieve a user with the given email from the database. If we can't find a user with this email we return an error text. 

Then we use the `verify_password` function to check whether the entered password is the same as the one we saved encrypted to the database. It basically creates a hash from the entered password and compares the hash to the saved password hash in the database. It returns `True` if both passwords match. 

If the passwords don't match, we will again, return an error message. 

## Session handling

If they do match we will save the users email in the session. The session is a simple key/value storage mechanism that persists between requests. It's unique to every user. Logging a user in means having a value for the `auth` key in the session in our case. The session is also cryptographically encrypted, so it can't be tampered with. 

As the last step we redirect the user to a '/dashboard' route when he or she logged in succcessfully using a client-side redirection by `htmx`.

## Basic auth decorator

This `/dashboard` should only be reachable for logged in users. So we need some kind of mechanism that checks if the user that sends a request to `/dashboard` is logged in or not. 

We could just add an if clause to our route handler that checks if the session has a key of `auth` and this would work. But it becomes tedious really fast, if you want do this for multiple route handlers. 

Instead let's leverage python decorators. 

Decorators are a way to wrap a function in another function. They are a way to extend the functionality of a function without modifying it. 

```python

def basic_auth(f):
    @wraps(f)
    def wrapper(session, *args, **kwargs):
        if "auth" not in session:
            return Response('Not Authorized', status_code=401)
        return f(session, *args, **kwargs)
    return wrapper

```

This function creates a `@basic_auth` decorator that checks of `auth` is in the session and if it's not, it will intercept the request and return a `401 Not Authorized` response. If there is a `auth` key in the `session` object, it will do nothing and the normal route handler will be run. 

We can use this decorator like this:

```py

@rt('/dashboard')
@basic_auth
def get(session):    
    return Container(
        H1("Dashboard"),
        Button("Logout", hx_post="/logout")
    )

```

Of course we need a way to log out the user. 

This is actually really simple: 

```py
@rt('/logout')
def post(session):
    del session['auth']
    return HttpHeader('HX-Redirect', '/login')
```

## Conclusion

Now we have a fully functioning user management system. And as you see it wasn't that hard. With AI tools like Claude or Cursor you can even generate this code very fast. 

Of course this login system lacks some advanced functionality like password confirmation via email, forgot password functionality or social log ins, but these are all great topics for future posts. Or this are all great exercises to you, dear reader. 

If you have any questions or feedback, you can find me on twitter [@rasmus1610](https://twitter.com/rasmus1610).

Thank you for reading. 