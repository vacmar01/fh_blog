---
title: How to Add CSRF Protection to your FastHTML App
date: 2025-02-22T11:20:06+01:00
draft: false
excerpt: Let's look at how to secure your FastHTML routes against CSRF attacks.
---

Cross-Site Request Forgery (CSRF) is an attack where a malicious website tricks your browser into making an unwanted request to another site where you are currently authenticated (logged in). This can lead to unauthorized actions being performed on your behalf, such as changing account settings, submitting forms, or making transactions.

Unfortunately, FastHTML doesn't provide CSRF protection out of the box. 

Fortunately, it's easy to implement yourself. 

In this blog post I'll show you how. 

## Overall idea
The overall idea of CSRF protection is this: We must only allow requests that change some kind of state like a POST, PUT or DELETE request if they come from our own site. 
The idea how we can check whether the request comes from our website or not is actually quite easy: 
When we log in the user we not only store its credentials like its username in the user's session to mark the user as authenticated (like `session["auth"] = username`), but we store a randomly generated secret key in the session as well (like `session["csrf"] = secrets.token_urlsafe(16)`). 

In every Form on our website we then add a hidden input field that sends this secret key with the form submission to our backend again. In our route handler for the form submission, we check whether a CSRF token was included and if it matches the token stored in the user’s session. If yes, we further process the request. If not, we throw an error with status code `401` indicating an "Unauthorized" request.

Let's implement it in actual code now. 

```python 
from fasthtml.common import *
import secrets

app, rt = fast_app()


def Layout(*args):
    return Main(cls="container", **kwargs)(
        *args,
    )


@rt("/login")
def get():
    return Layout(
        Form(
            action="/login",
            method="post",
        )(
            Div(
                Label("Username"),
                Input(id="username"),
                Label("Password"),
                Input(id="password", type="password"),
                Button("Login", type="submit"),
            ),
        )
    )
```

This code initializes a new FastHTML app, defines a simple Layout and then defines a `/login` route. All very basic stuff, I assume. 

```python 
@rt("/login")
def post(session, username: str, password: str):
    if username == "admin" and password == "admin":
        session["auth"] = username
        session["csrf"] = secrets.token_hex(32)

        return RedirectResponse("/dashboard", status_code=303)
    raise HTTPException(401, "Invalid credentials")
```

Now we define the `post` handler for logging in the user. We take a little shortcut for this tutorial and we let the user log in if the username is `admin` and the password is `admin` as well. 

Then we'll save the username in the `auth` key of the session (to mark the user as authenticated and logged in) and we generate a secret key of length 32 bytes which we will use as the CSRF token.

```python
@rt("/dashboard")
def get(session):
    if session.get("auth") == "admin":
        return Layout(
            H1("Welcome admin!"),
            P("You are now logged in."),
            Form(
                hx_post="/add-todo",
                hx_target="#todos",
                hx_swap="beforeend",
                **{"hx-on::after-request": "this.reset()"},
            )(
                Hidden(id="csrf", value=session["csrf"]),
                Input(type="text", id="todo", placeholder="Enter todo"),
                Button("Add Todo", type="submit"),
            ),
            Div(id="todos"),
        )
    return RedirectResponse("/login", status_code=303)


@rt("/add-todo")
def post(session, csrf: str, todo: str):
    if session.get("csrf") == csrf:
        return Div(todo)
    else:  # CSRF token mismatch
        raise HTTPException(401, "Invalid credentials")
```

Then to test it we'll define a `/dashboard` route that has a simple form where the user can add todos. The form does a POST request to the `/add-todo` endpoint and that's the endpoint we want to secure from CSRF. 

It's actually very easy. When creating the Form, we'll add a hidden input field (`Hidden()` is a shortcut for that in FastHTML) to our form that has the csrf token from the session as its value. 

In the `/add-todo` handler, we then check if the csrf token in the session is equal to the csrf token coming from the request. If yes, we do whatever we do (in this case adding the todo) and if not, we'll throw an `HTTPException` of `401`. 

Now this endpoint is secured from csrf attacks. 

To test it we can do this: 
Open up the developer tools of your browser, go to the network tab and fill out and submit the form. Now you should see the request to `add-todo` in the list of network requests. Now right-click on the request and go to "Copy -> Copy as cURL". Now you should have a `curl` request with a lot of headers that looks really complicated (at least in my browser). Paste the command in a terminal and find where the CSRF token is defined. Change it somehow and send the command. You should get an HttpException back. 

But we can actually protect it more elegantly. 

We can use  python decorators: 

```python
from functools import wraps


def csrf_protected(handler):
    @wraps(handler)
    def wrapper(session, csrf: str, *args, **kwargs):
        if session.get("csrf") != csrf:
            raise HTTPException(401, "Invalid CSRF token")
        return handler(session, csrf, *args, **kwargs)

    return wrapper
```

Now we can use it like this: 

```python
@rt("/add-todo")
@csrf_protected
def post(session, csrf: str, todo: str):
    return Div(todo)
```

As you can see it's not that difficult to protect your FastHTML routes against CSRF attacks. 



