---
title: How to Implement Social Login using OAuth and FastHTML
date: 2024-09-25T11:20:06+01:00
draft: false
excerpt: Let's implement social logins in FastHTML
---

This is part 3 of a series of posts on how to build a simple user management system with FastHTML.

You can find the other parts of this series here:

- [Part 1: Classic password-based login](/posts/login-fasthtml.md)
- [Part 2: Passwordless Authentication](/posts/passwordless-auth-fasthtml)
- Part 3: Social Logins using OAuth (*you are here*)

__________

In the last posts, we looked at how to implement a simple email/password-based authentication system as well as a password-less login system using magic links in FastHTML. 

While this is all well and good, most modern websites let you sign up using another account of yours, like your Facebook, Google or your Github account. 

This is what we will build in this post.

As you will see, it's not super complicated once you’ve understood the basic principle behind it. 

The protocol to facilitate these kind of authentication is called **OAuth**. 

It’s a little bit annoying to work with, but since we are not the first ones who want to use OAuth, many smart people have produced a lot of documentation and libraries around this topic: FastHTML has some really nice helper classes for OAuth that make working with it a breeze.

Also there is an example in the [“fasthtml-example" repo](https://github.com/AnswerDotAI/fasthtml-example/tree/main/oauth_example) for OAuth log-in. This post builds on it.

## How OAuth works

Here is a **tl;dr** on how logging in using another account works from a *user's point of view*:
* The user clicks on a link that says “Log in with \<insert your favorite social login provider here\>”
* The user is redirected to the service and is asked to log in, if they aren't logged in already
* The user is asked to accept sharing of their data from the service to our app
* The user is redirected to our app and logged in. 

From a *developer's point of view* (our view in this case) the whole process looks like this: 
* The user clicks on a link that says “Log in with X”
* The user is redirected to the service and does the *spiel* described above
* The service redirects back to a specified URL of your app and also sends a “authentication code” with - if the user approved the data sharing
* We'll use this authentication code to ask for the user info from the service
* Then we'll use this info to sign in the user

## Setup 
In this example we’ll use [GitHub](https://github.com) as our OAuth provider, but the steps are similar for other providers like Google or X. 

### Create your OAuth app on GitHub 
You need to register your app on GitHub to make OAuth with GitHub work.

These are the steps for Github: 
* Go to https://github.com/settings/developers
* Click on OAuth apps on the left
* Create a new OAuth app
    * give it any name you want, I named mine *“oauth-example”*
    * The homepage url can be your localhost, something like “http://127.0.0.1:5001”
    * the authorization callback url is the endpoint that is being called with the authentication code and will be implemented by us. I named mine “http://127.0.0.1:5001/auth_redirect/github”. 
* Save it. 

You should see a `CLIENT_ID`. Click to create a client secret and copy it. 

Now that we have the `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET` obtained, create a `.env` file in your project folder and insert the ID and secret:

```
GITHUB_CLIENT_ID="xxxxx"
GITHUB_CLIENT_SECRET="xxxxx"
```

This is all the setup we need. 

Trust me from here on it will get faster.

The next step is to make sure that you use the latest FastHTML version. 

With version 0.5 there were some changes to the OAuth module that will trip you up if you have a version <0.5. So update it with `pip install -U python-fasthtml`.

## Let's get coding

We will start from scratch with the code. Let's import everything we need, instantiate a new `fast_app()` with all the CSS and other shenanigans we need and let's set up the database. 

This should all be very familiar to you, if you read the other two parts of this series.

```python
from fasthtml.common import * 
from fasthtml.svg import Svg, Path
from fasthtml.oauth import GitHubAppClient

import requests
import os
from dotenv import load_dotenv

load_dotenv()

import secrets 

frankenui = Link(rel='stylesheet', href='https://unpkg.com/franken-wc@0.1.0/dist/css/zinc.min.css')

tailwind = Script(defer=True, src='https://cdn.tailwindcss.com')

client = GitHubAppClient(os.getenv("GITHUB_CLIENT_ID"), 
                         os.getenv("GITHUB_CLIENT_SECRET"),
                         scope="user:email",
                         redirect_url="http://0.0.0.0:5001/auth_redirect/github")

login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login', '/auth_redirect/github'])

app, rt = fast_app(live=True, debug=True, pico=False, hdrs=(frankenui, tailwind), before=bware)

db = database('data/users.db')   

users = db.t.users

if "users" not in db.t:
    users.create(dict(id=int, email=str), pk='id')
    
User = users.dataclass()

```

You probably need to install the `requests` and `python-dotenv` libraries with `pip install requests python-dotenv`. Also note that we imported `GitHubAppClient` from `fasthtml.oauth`. This is the class that encapsulates at lot of functionality we need here. 

WE a new instance of this class and save it in `client`. The client takes in the `client_id`, the `client_secret`, the `redirect_url` (the one you specified on github.com when you created your OAuth app) as well as a `scope`. The `scope` defines what data you need from the OAuth provider. In our case, we only need the user including his email (on GitHub email and OAuth is a little bit complicated, more on that later). 

## The Login Page

Now let’s implement our login page with a **"Login with GitHub"** button, including the GitHub Icon as a SVG. 

But where should the button link to?

Somehow we need to send a request to the endpoint on github.com that handles all the OAuth authentication stuff and also send the right parameters with. 

Luckily, the `GitHubAppClient` class from FastHTML exposes a method called `login_link()` that returns the url that handles all the GitHub OAuth login stuff. 

That’s where our button (link) in the login form should take us. Let’s implement this.

```python
# there is no homepage, so let's always redirect the user to the login page.
@rt('/')
def get():
    return RedirectResponse('/login')

@rt('/login')
def get(session):
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    
    gh_login_link = client.login_link(client.redirect_url, state=state)
    
    def GithubIcon(*args, **kwargs):
        return Svg(
            *args,
            Path(fill_rule='evenodd', clip_rule='evenodd', d='M48.854 0C21.839 0 0 22 0 49.217c0 21.756 13.993 40.172 33.405 46.69 2.427.49 3.316-1.059 3.316-2.362 0-1.141-.08-5.052-.08-9.127-13.59 2.934-16.42-5.867-16.42-5.867-2.184-5.704-5.42-7.17-5.42-7.17-4.448-3.015.324-3.015.324-3.015 4.934.326 7.523 5.052 7.523 5.052 4.367 7.496 11.404 5.378 14.235 4.074.404-3.178 1.699-5.378 3.074-6.6-10.839-1.141-22.243-5.378-22.243-24.283 0-5.378 1.94-9.778 5.014-13.2-.485-1.222-2.184-6.275.486-13.038 0 0 4.125-1.304 13.426 5.052a46.97 46.97 0 0 1 12.214-1.63c4.125 0 8.33.571 12.213 1.63 9.302-6.356 13.427-5.052 13.427-5.052 2.67 6.763.97 11.816.485 13.038 3.155 3.422 5.015 7.822 5.015 13.2 0 18.905-11.404 23.06-22.324 24.283 1.78 1.548 3.316 4.481 3.316 9.126 0 6.6-.08 11.897-.08 13.526 0 1.304.89 2.853 3.316 2.364 19.412-6.52 33.405-24.935 33.405-46.691C97.707 22 75.788 0 48.854 0z', fill='#fff'),
            width='1.25rem',
            height='1.25rem',
            viewBox='0 0 98 96',
            xmlns='http://www.w3.org/2000/svg',
            **kwargs
        )
    
    return Div(
        Div(
            H1("Login", cls="text-3xl font-bold tracking-tight uk-margin text-center"),
            A(GithubIcon(cls="uk-margin-small-right"), "Login with GitHub", href=gh_login_link, cls="uk-button uk-button-primary w-full"),
            cls="uk-card uk-card-body"
        ),
        cls="uk-container max-w-[400px] uk-margin-top"
    )
```

You may have noticed that we also created a random token (or string) called `state`, saved it in the session and also passed it to the `login_link()` function. What’s that again? 

The `state` is just some string that will be sent from your web app through the whole OAuth workflow and back to your web app. It won’t do anything and it won’t be changed by GitHub. So why do we need it then? 

OAuth state is a security measure against something called [CSRF (cross-site request forgery)](https://owasp.org/www-community/attacks/csrf). That’s a type of vulnerability where people will try to send requests to your web app from other web sites. 

To prevent this, we will use a `state` string that will be sent from our web app to the OAuth workflow. When it is returned, we will compare the returned `state` string with the one we created initially. If both strings match, great. If they don’t match or the `state` parameter misses, e.g. because someone from outside of our web app tried to send the request, we will abort the whole authentication process.

We save the specific `state` string in the session to compare it later. Remember the session is a simple key/value storage, that persists between requests. It is a kind of “server-side state”, which might help to wrap your head around it if you come from javascript land. 

Okay now the first half of OAuth authentication is done on our part. You can click on the button and it should take you to GitHub and ask you to login (if you are not already logged in). Then you have to verify that your app can access your GitHub data. If you click "yes", it should redirect you to whatever callback url you have specified. You should get an error, because we haven’t implemented this endpoint yet. 

Let's do this now.

```python
@rt('/auth_redirect/github')
def get(code: str, state: str, session):
    if state != session.get('oauth_state'):
        return "Invalid state parameter. Possible CSRF attack."
    
    user_info = client.retr_info(code, client.redirect_url)
    
    if user_info['email'] is None:
        token = client.token["access_token"]
        
        res = requests.get("https://api.github.com/user/emails", headers={"Authorization": f"token {token}"})
        
        primary_email = next(email['email'] for email in res.json() if email['primary'])
        
        user_info['email'] = primary_email
    
    #check if the user already exists in the database, if not, create it.
    try:
        u = users(where=f"email='{user_info['email']}'")[0]
    except IndexError:
        u = users.insert(User(email=user_info['email']))
    
    # log in the user
    session['auth'] = u.id
    
    # Clear the oauth_state from the session
    session.pop('oauth_state', None)
    
    return RedirectResponse('/dashboard')

```

As you can see, the endpoint receives the authentication `code` as well as the `state` we specified before as request parameters. 

First, we’ll check if the received `state` matches with the `state` we saved in the session. If it does, great. If not, we’ll return early with a string indicating the error. 

Then we use the received `code` to retrieve info about our user save it in `user_info`. The info coming back is a plain old dictionary.

If we want to receive the user's email from GitHub, that’s where it gets a little bit messy. 

You would think that asking for the user's email from GitHub using `scope="user:email"` should do the trick and give us the user's email in the `user_info`.

Well, Me [and others](https://stackoverflow.com/questions/35373995/github-user-email-is-null-despite-useremail-scope) thought so too. 

But it turns out, the email will only be returned this way if the user has specified a public email on GitHub.

If the email is not public on GitHub, it won’t be returned and we have nothing to save to the database.

It turns out, in this case you have to hit another GitHub API endpoint to get the actual email for a user. 

For this we can use the `token` we received from GitHub through the OAuth auth process. We call the `/user/emails` endpoint of the GitHub API and use the received token for authorization. 

Then we'll retrieve the `primary_email` from the JSON response and use this as the user's email. 

Now that we have the user's email we can save it to the database. If a user with this email already exists in the database, we'll use this record, otherwise we'll create a new user record (we should probably add a unique contraint for the email column in SQLite, but for demonstration purposes it's fine like this).

To actually login the user we will save the user's `id` to the session under the `auth` key, like we always do. This way the `Beforeware` we implemented in the beginning (and in the last part) can understand which user is logged in and not and authorize the access to certain pages accordingly. 

Now the only thing that's left is to implement the restricted `/dashboard` page again as well as a way for the user to log out. 

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

As you can see, the `/logout` endpoint does nothing but deleting the `auth` key from the session and redirecting the user to the login page again. *Simple stuff.*

## Conclusion 

So that's it. 

That's how you add OAuth-based social authentication to your FastHTML app. As you can see, it's really not that complicated once you understand the concept behind it. 

And the good thing is: The pattern redirecting to an external service from your web app and then receiving data in a callback endpoint is really common for integrating other services as well. 

Another service that utilizes this pattern is [Stripe](https://stripe.com).

How you can integrate payments into your FastHTML app will be the topic of a next post. 

Don't want to miss it? 

Then follow [me on Twitter](https://twitter.com/rasmus1610) and I'll keep you updated there. 

Thanks again for reading!



