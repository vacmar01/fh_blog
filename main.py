from fasthtml.common import *

from lucide_fasthtml import Lucide

import yaml

from datetime import datetime

import os

plausible = Script(defer=True, data_domain='blog.mariusvach.com', src='https://plausible.io/js/script.js')
frankenui = Link(rel='stylesheet', href='https://unpkg.com/franken-wc@0.1.0/dist/css/zinc.min.css'), Script(src='https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js'),Script(src='https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js')
tailwind = Link(rel="stylesheet", href="/public/app.css", type="text/css")

og_headers = (
    Meta(property="og:image", content="https://blog.mariusvach.com/public/images/og.png"),
    Meta(property="twitter:image", content="https://blog.mariusvach.com/public/images/og.png"),
)

app, rt = fast_app(pico=False, static_path='public', hdrs=(frankenui, tailwind, plausible, *og_headers, MarkdownJS(), HighlightJS(langs=['python', 'bash', 'yaml', 'json'], light="atom-one-dark")))

@rt('/')
def get():

    posts = []
    posts_dir = 'posts'

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            with open(os.path.join(posts_dir, filename), 'r') as file:
                content = file.read()
                parts = content.split('---')
                if len(parts) > 2:
                    post = yaml.safe_load(parts[1])
                    post['slug'] = os.path.splitext(filename)[0]
                    post['content'] = parts[2].strip()
                    lines = post['content'].split('\n')
                    if 'excerpt' not in post:
                        for line in lines:
                            if line.strip() and not line.strip().startswith('!['):
                                post['excerpt'] = line.strip()
                                break
                    
                    # Convert date string to datetime object if it exists
                    if 'date' in post and isinstance(post['date'], str):
                        post['date'] = datetime.strptime(post['date'], "%Y-%m-%d")
                    
                    if not post["draft"]:
                        posts.append(post)

    # Sort posts by date, most recent first
    posts.sort(key=lambda x: x.get('date', datetime.min), reverse=True)
    
    def BlogCard(post, *args, **kwargs):
        return Div(
            Div(
                *args,
                A(
                    H2(post["title"], cls="text-2xl font-bold font-heading tracking-tight"),
                    P(post["date"].strftime("%B %d, %Y"), cls="uk-text-muted uk-text-small uk-text-italic"),
                    P(post["excerpt"], cls="uk-text-muted uk-margin-small-top marked"),
                    href=f"/posts/{post['slug']}",
                ),
                cls="uk-card-body",
            ),
            cls=f"uk-card {kwargs.pop('cls', '')}",
            **kwargs
        )
    
    return Title('Marius Vach Blog'), Div(
        H1("Hey, I'm Marius!", cls="text-4xl font-bold font-heading tracking-tight uk-margin-small-bottom"),
        P("I'm a radiologist and software developer. I love building software and learning new things.", cls="text-lg uk-text-muted"),
        Div()(
            A(Lucide('mail', cls="w-4 h-4 mr-2"), "Email me", href="mailto:mariusvach@gmail.com", cls="uk-button uk-button-primary uk-margin-small-top uk-margin-small-right"),
            A(Lucide('github', cls="w-4 h-4 mr-2 text-white"), "GitHub", href="https://github.com/vacmar01/fh_blog", cls="uk-button uk-button-primary  uk-margin-small-right uk-margin-small-top"),
            A(Lucide('twitter', cls="w-4 h-4 mr-2 text-white"), "Twitter", href="https://twitter.com/rasmus1610", cls="uk-button uk-button-primary uk-margin-small-top")
        ),
        H2("Here are some things I wrote:", cls="text-3xl font-bold font-heading tracking-tight uk-margin-large-top"),
        Div(
            *[BlogCard(post) for post in posts], 
            cls="md:grid md:grid-cols-3 md:gap-4 uk-margin-top space-y-4 md:space-y-0",
        ),
        cls="uk-container uk-container-xl py-16",
    )
    
@rt('/posts/{slug}')
def get(slug: str):
    with open(f'posts/{slug}.md', 'r') as file:
        content = file.read()
        
    post_content = content.split('---')[2]
    
    frontmatter = yaml.safe_load(content.split('---')[1])
    
    return Title(f"{frontmatter['title']} - Marius Vach Blog"), Div(
        A(Lucide('arrow-left', cls="w-4 h-4 text-black mr-2"), 'Go Back', href='/', cls="absolute md:top-0 left-0 top-2 md:-ml-48 md:mt-16 uk-button uk-button-ghost"),
        H1(frontmatter["title"], cls="text-4xl font-bold font-heading tracking-tight uk-margin-small-bottom"),
        P(frontmatter['date'].strftime("%B %d, %Y"), " by Marius Vach", cls="uk-text-muted uk-text-small uk-text-italic"),
        Div(post_content, cls="marked prose mx-auto uk-margin-top"),
        cls="uk-container max-w-[65ch] mx-auto relative py-16",
    )
    
serve()