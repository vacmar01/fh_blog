---
title: How to Implement Passwordless Authentication in FastHTML
date: 2024-09-07T15:27:52+01:00
draft: false
excerpt: Let's implement a passwordless authentication system using magic links.
---

This is part 2 of a series of posts on how to build a simple user management system with FastHTML.

You can find the other parts of this series here:

- [Part 1: Classic password-based login](/posts/login-fasthtml)
- Part 2: Passwordless authentication with magic links
- [Part 3: OAuth authentication](/posts/oauth-fasthtml)

__________

In the last post, we implemented a classic login and authentication system using the user's email and password. And it works great. 

But if you are like me, you have so many accounts on so many websites with so many different passwords, it’s hard to keep track. 

Of course, we could use a password manager for it, but there is another way. 

We can implement a login/authentication system without any password, only using the user's email. 

This type of authentication is often called *magic link authentication*. 

## The basic idea

Here is the basic idea behind it: 

1. The user enters their email on a website   
2. The website generates a random string (a "token") and saves it together with the user's email into a database  
3. The website sends an email to the user with a link that encodes the generated token  
4. The user clicks on the link  
5. The website looks for a record in the users database table with the token from the link   
6. If it can find a record, the user will be logged in (again by storing information in the session)

Doesn’t sound that complicated, right?

Okay let’s get to it. 

We will start from scratch.

## Setup

`pip install python-fasthtml`

Let’s import what we need and create a new `app`.

```python
from fasthtml.common import *
import secrets
from datetime import datetime, timedelta

frankenui = Link(rel='stylesheet', href='https://unpkg.com/franken-wc@0.1.0/dist/css/zinc.min.css')
tailwind = Script(defer=True, src='https://cdn.tailwindcss.com')

app, rt = fast_app(live=True, debug=True, pico=False, hdrs=(frankenui, tailwind))
```

This time, we will use [FrankenUI](https://franken-ui.dev/) as well as [TailwindCSS](https://tailwindcss.com) to style our website. FrankenUI is an awesome port of the popular [shadcn](https://ui.shadcn.com/) package into pure HTML/Web components (the original shadcn is written for React).

## Database setup

Next we will create the database schema. 

```python
db = database('data/users_magic_link.db')

SQL_CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
   email TEXT PRIMARY KEY NOT NULL,
   magic_link_token TEXT,
   magic_link_expiry TIMESTAMP,
   is_active BOOLEAN DEFAULT FALSE
);
"""

db.execute(SQL_CREATE_USERS)   
users = db.t.users
User = users.dataclass()
```

Here we create the table using a vanilla SQL query instead of the [`fastlite`](https://github.com/answerDotAi/fastlite) syntax, but the rest is the same as last time. 

## Login Form

Okay, now let’s build the login form next: 

```python
def MyForm(btn_text: str, target: str, cls: str = ""):
   return Form(
       Div(
           Div(
               Input(id='email', type='email', placeholder='foo@bar.com', cls='uk-input'),
               cls='uk-form-controls'
           ),
           cls='uk-margin'
       ),
       Button(btn_text, type="submit", cls="uk-button uk-button-primary w-full", id="submit-btn"),
       P(id="error", cls="uk-text-danger uk-text-small uk-text-italic uk-margin-top"),
       hx_post=target,
       hx_target="#error",
       hx_disabled_elt="#submit-btn",
       cls=f'uk-form-stacked {cls}'
   )

@rt('/login')
def get():   
   return Div(
       Div(
           H1("Sign In", cls="text-3xl font-bold tracking-tight uk-margin text-center"),
           P("Enter your email to sign in to The App.", cls="uk-text-muted uk-text-small text-center"),
           MyForm("Sign In with Email", "/send_magic_link", cls="uk-margin-top"),
           cls="uk-card uk-card-body"
       ),
       cls="uk-container max-w-[400px] uk-margin-top"
   )

serve()

```

Start the FastHTML server with `python main.py` and look at the gorgeous sign in page. Isn’t she pretty? 

Again, the actual form element is extracted into a `MyForm()` function. It’s not really needed this time, since we don't use it a second time, but I kept it nonetheless. 

## Handling form submit

The form sends a post request to `/send_magic_link`, so let's build this endpoint next. 

```python
@rt('/send_magic_link')
def post(email: str):
   if not email:
       return "Email is required"
  
   try:
       user = users[email]
   except NotFoundError:
       user = User(email=email, is_active=False, magic_link_token=None, magic_link_expiry=None)
       users.insert(user)
  
   magic_link_token = secrets.token_urlsafe(32)
   magic_link_expiry = datetime.now() + timedelta(minutes=15)
  
   users.update({'email': email, 'magic_link_token': magic_link_token, 'magic_link_expiry': magic_link_expiry})
  
   magic_link = f"http://0.0.0.0:5001/verify_magic_link/{magic_link_token}"
  
   send_magic_link_email(email, magic_link)
  
   return P("A link to sign in has been sent to your email. Please check your inbox. The link will expire in 15 minutes.", id="success", cls="uk-margin-top uk-text-muted uk-text-small"), HttpHeader('HX-Reswap', 'outerHTML'), Button("Magic link sent", type="submit", cls="uk-button uk-button-primary w-full", id="submit-btn", disabled=True, hx_swap_oob="true")
```

This handler first checks if the `email` is present. If it’s not, it returns an error that will be swapped into the `#error` paragraph in the form by HTMX, just like last time. 

Then it tries to find a user with the given email and if there is no user with this email it will create one. 

Then we come to the heart of the whole login flow. 

We create a `magic_link_token` using the `secrets` package from the python standard library. This token is a 32 characters long string. Also we generate an expiry date, which lies 15 minutes in the future. 

The token should only be valid for a certain amount of time to increase the security of the authentication system. 

Then we update the user row in the database with the expiration date and the token itself. 

Then we create the login link by putting the token into the url. 

If everything went well, we return a success message to the user. Remember, the form has been defined to swap the content of the `#error` paragraph. Since I want to change the appearance of the text we send back, I also send back a `HX-Reswap` header with the value `outerHTML`. This tells HTMX to swap the outer HTML of the `#error` html element with the content we send back, a paragraph tag with the success message. 

Also I want to disable the submit button and show a message that the magic link has been sent. To do this, we use one of the most powerful features of HTMX, out-of-band swaps. 

In HTMX you can update more than one piece of UI by setting the `hx-swap-oob` attribute to `true` on an element. HTMX will then swap in the returned element at the location of the element with the same id (`#submit-btn` in this case). You can read more about HTMX's out-of-band swaps [here](https://htmx.org/docs/#oob_swaps).

## Send the magic link

Now we only need to send an email to the user with the link in it. 

Since I’m too lazy to sign up for an email provider, let’s just mock sending the email by printing the email content to the console.

That’s what `send_magic_link_email()` does. 

```python
def send_magic_link_email(email: str, magic_link: str):
  
   email_content = f"""
   To: {email}
   Subject: Sign in to The App
   ============================
  
   Hey there,
  
   Click this link to sign in to The App: {magic_link}
  
   If you didn't request this, just ignore this email.
  
   Cheers,
   The App Team
   """
   # Mock email sending by printing to console
   print(email_content)
```

Now when the user enters his or her email into the sign in form, he or she should get an email with a link to log in. The link then sends a get request to the `/verify_magic_link/{token}` endpoint. 

Let’s implement this endpoint next.

## Verify the token and authenticate the user

```python
@rt('/verify_magic_link/{token}')
def get(session, token: str):
   now = datetime.now()
   try:
       user = users(where=f"magic_link_token = '{token}' AND magic_link_expiry > '{now}'")[0]
       session['auth'] = user.email
       users.update({'email': user.email, 'magic_link_token': None, 'magic_link_expiry': None, 'is_active': True})
       return RedirectResponse('/dashboard')
   except IndexError:
       return "Invalid or expired magic link"
```

That endpoint isn’t very complicated I think. 

We save the current time into the variable `now`, because we need to look whether the token is already expired. 

Then we retrieve the first item with the specified token and an expiration date that lies in the future from the users table. 

There should only be one or no user coming back from this query, so we wrap this whole code in a try/catch block. 

If a user has been found using this query, we will save his or hers email in the `auth` key of our session dictionary, like we did last time. If it’s the first time the user logs in, we set `is_active` to true for this database record. 

We do this to keep our database clean. Imagine a hacker enters thousands of random email addresses into our beautiful sign in form and therefore creates thousands of records in our database. 

To keep our database clean, we can use this `is_active` column to delete all inactive database records periodically using cron jobs. 

## Beforeware

Now to test our nice little authentication flow, we need a page that is only accessible for authenticated users and a mechanism to restrict the access to this page for non-authenticated users. 

Last time we used a Python decorator for this. This works great and there is nothing wrong with it, but let’s change this up a little this time. 

We will use FastHTML’s concept of `beforeware` for restricting access this time. 

```python
login_redir = RedirectResponse('/login', status_code=303)

def before(req, session):
   auth = req.scope['auth'] = session.get('auth', None)
   if not auth: return login_redir
  
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login', '/send_magic_link', r'/verify_magic_link/.*'])

app, rt = fast_app(...,before=bware)
```

Here we define a function called `before` that takes in the request and saves whatever in the `auth` key of the session into the `auth` variable as well as the `scope` of the request (this is copied straight from an example from the FastHTML repo and it’s the first time I see this double assignment syntax in Python). The request `scope` is something that comes from [ASGI](https://asgi.readthedocs.io/en/latest/), the underlying webserver technology of FastHTML. Think of it as a kind of “metadata” or “context” of the request. 

If there is nothing in `session["auth"]`, `auth` will evaluate to `False` and we will redirect the user to the login page. 

Then we’ll define a `Beforeware` object with our newly defined `before` function. 

This will make sure that every request runs first through our function, unless it’s targeting one of the paths we define in the `skip` list. Everything else will be guarded by this `Beforeware`. Now we just need to pass our newly created `Beforeware` class to our `fast_app` function as the `beforeware` argument. 

## The Dashboard Page

Last, let’s implement a `/dashboard` page that will be only reachable for users who are signed in. 

```python
@rt('/logout')
def post(session):
   del session['auth']
   return HttpHeader('HX-Redirect', '/login')

@rt('/dashboard')
def get(session): 
   u = users[session['auth']]
    
   return Nav(
       Div(
           Ul(
               Li(
                   A("Dashboard",href='#'),
                   cls='uk-active'
               ),
               Li(
                   A("About",href='#'),
               ),
               Li(
                   A("Contact",href='#')
               ),
               cls='uk-navbar-nav'
           ),
           cls='uk-navbar-left'
       ),
       Div(
           Div(
               Button(
                   "Logout",
                   cls='uk-button uk-button-primary',
                   hx_post='/logout'
               ),
               cls="uk-navbar-item"
           ),
           cls='uk-navbar-right'
       ),
       uk_navbar=True,
       cls='uk-navbar uk-navbar-container px-4'
   ), Div(
       Div(
           H1("Dashboard", cls="text-3xl font-bold tracking-tight uk-margin text-center"),
           P(f"You are logged in as '{u.email}'"),
           cls="uk-card uk-card-body"
       ),
       cls="uk-container uk-margin-top"
   )
```

The route defines a simple navbar and a card component using FrankenUI and also shows the email of the user logged in. We also added a button and a route for the user to log out.

## Conclusion

That’s basically all I wanted to show to you in this blog post. As you can see, passwordless authentication isn’t that complicated. 

From a developer standpoint I’m happy if I don’t need to save sensitive information like user passwords to my database. Yes sure, the \`token\` is also somewhat sensitive, but it’s only in the database until the user has logged in or for a maximum of 15 minutes, so the opportunity window for a potential hacker to steal sensitive data is much smaller. 

From a user stand-point I’m happy if I don’t need to remember yet another password. 

All in all, I think passwordless login using a magic link is a good authentication technique to know. And now you know how to implement it in Python :) 

On to the next authentication procedure: **Social logins with OAuth**. 

If you don’t want to miss the next post or just want to reach out, follow me on [Twitter](https://twitter.com/rasmus1610).

Thank you for reading.
