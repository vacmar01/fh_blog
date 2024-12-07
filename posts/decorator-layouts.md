---
title: How to Define Layouts with Decorators in FastHTML
date: 2024-12-07T15:27:52+01:00
draft: false
excerpt: How to use decorators to elegantly define layouts in FastHTML
---

Recently, I was playing around with `decorators` to understand them better.

If you have used `FastHTML`, `FastAPI` or `Flask` you know what `decorators` are.

Decorators are these things with an `@` that you put above function definitions. Something like `@rt("/hello_world")` in FastHTML.

Playing around with them, made me remember a pattern I saw on [Daniel Roy Greenfeld's blog](https://daniel.feldroy.com/) (or an early FastHTML version of it):

Using a `decorator` to define layouts.

Usually, a website consists of a layout that doesn't change much - like a header, navbar and a footer maybe - and the actual site-specific content. 

Every templating language let's you define a layout where you define constant things like your navbar or the footer and in which the site-specific content will be inserted.

Of course we can do the same thing in `FastHTML`, since we can use the full power of Python for templating. 

Let's build a little website to show you why I think that decorators are a superior way to define layouts in FastHTML.

```python
from fasthtml.common import *

app, rt = fast_app(pico=True)

def Layout(*args, **kwargs):
    return Div(style="padding 2rem;", **kwargs)(
        Header("This is the header", style="border-bottom: 1px solid black; padding: 1rem;"),
        *args, #this will be where the site-specific content will be inserted
        Footer("This is the footer", style="border-top: 1px solid black; padding: 1rem;")
    )

@rt("/")
def get():
    return Layout(
        Div(H1("Hello World"))
    )

@rt("/about")

def get():
    return Layout(
        Div(H1("About Us"))
    )


serve()
```

This is a very simple toy website in FastHTML with two routes and a `Layout`. The layout defines a `Header` (with a crude navbar) and a `Footer`. We want to show the `Header` and the `Footer` on every route. 

Easy enough: We just wrap the Content of the route with `Layout`.

Here is a way to do the same thing using a `decorator`:

First let's actually define the `decorator`.

```python
from functools import wraps

def with_layout(layout_func):          
    def decorator(f):                  
        @wraps(f)
        def wrapper(*args, **kwargs): 
            return layout_func(f(), *args, **kwargs)
        return wrapper
    return decorator
```

Now let's use it.

```python
@rt("/")
@with_layout(Layout)
def get():
    return Div(H1("Hello World"))
    
@rt("/about")
@with_layout(Layout)
def get():
    return Div(H1("About Us"))
```

I think this looks much cleaner. The decorator also let's you specify different layouts for different routes by passing another function to `with_layout` - Maybe you want to have a `BlogPostLayout` and a `ContentLayout` or whatever. 

Granted, the code for the `with_layout` decorator is a mouthful. But you'll only have to write it once (or just *steal it* from this post 🤫).

What do you think of this pattern? 

You can reach out to me on [Bluesky](https://bsky.app/profile/rasmus1610.bsky.social) (I tend to be inactive on Twitter now).

