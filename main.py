from fasthtml.common import *
import frontmatter

from lucide_fasthtml import Lucide

import yaml

from datetime import datetime

import os

plausible = Script(
    defer=True,
    data_domain="blog.mariusvach.com",
    src="https://plausible.io/js/script.js",
)
frankenui = (
    Link(
        rel="stylesheet",
        href="https://unpkg.com/franken-ui@1.1.0/dist/css/core.min.css",
    ),
    Script(src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js"),
    Script(src="https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js"),
)
tailwind = Link(rel="stylesheet", href="/app.css", type="text/css")

# og_headers = (
#     Meta(property="og:image", content="https://blog.mariusvach.com/images/og.png"),
# )

app, rt = fast_app(
    pico=False,
    static_path="public",
    bodykw={"class": "uk-theme-zinc"},
    hdrs=(
        frankenui,
        tailwind,
        plausible,
        Meta(
            name="google-site-verification",
            content="AHzT8BdRGuJ20gfBTqIHtWBGoleIfJ0e9gfjWwA_7HA",
        ),
        # *og_headers,
        MarkdownJS(),
        HighlightJS(langs=["python", "bash", "yaml", "json"], light="atom-one-dark"),
    ),
)


def get_posts(posts_dir="posts"):
    posts = []

    for filename in os.listdir(posts_dir):
        if filename.endswith(".md"):
            with open(os.path.join(posts_dir, filename), "r") as file:
                post = frontmatter.load(file)
                post["slug"] = os.path.splitext(filename)[0]
                post["content"] = post.content

                # Convert date string to datetime object if it exists
                if "date" in post and isinstance(post["date"], str):
                    try:
                        # Try ISO 8601 format first (with time and timezone)
                        post["date"] = datetime.fromisoformat(post["date"])
                    except ValueError:
                        try:
                            # Fall back to simple date format
                            post["date"] = datetime.strptime(post["date"], "%Y-%m-%d")
                        except ValueError:
                            post["date"] = None

                if not post.get("draft", False):
                    posts.append(post)

    # Sort posts by date, most recent first
    posts.sort(key=lambda x: x.get("date", datetime.min), reverse=True)
    return posts


@rt("/")
def get():
    posts = get_posts()

    def BlogCard(post, *args, **kwargs):
        return Div(
            Div(
                *args,
                A(
                    H2(
                        post["title"],
                        cls="text-2xl font-bold font-heading tracking-tight",
                    ),
                    P(
                        post["date"].strftime("%B %d, %Y"),
                        cls="uk-text-muted uk-text-small uk-text-italic",
                    ),
                    P(
                        post["excerpt"] if "excerpt" in post else "",
                        cls="uk-text-muted uk-margin-small-top marked",
                    ),
                    href=f"/posts/{post['slug']}",
                ),
                cls="uk-card-body",
            ),
            cls=f"uk-card {kwargs.pop('cls', '')}",
            **kwargs,
        )

    return Title("Marius Vach Blog"), Div(
        H1(
            "Hey, I'm Marius!",
            cls="text-4xl font-bold font-heading tracking-tight uk-margin-small-bottom",
        ),
        P(
            "I'm a Machine Learning Engineer, Medical AI researcher and radiologist. I love building software and learning new things.",
            cls="text-lg uk-text-muted",
        ),
        Div(
            A(
                Lucide("mail", cls="w-4 h-4 mr-2"),
                "Email me",
                href="mailto:mariusvach@gmail.com",
                cls="uk-button uk-button-primary uk-margin-small-top uk-margin-small-right",
            ),
            A(
                Lucide("github", cls="w-4 h-4 mr-2 text-white"),
                "GitHub",
                href="https://github.com/vacmar01/fh_blog",
                cls="uk-button uk-button-primary  uk-margin-small-right uk-margin-small-top",
            ),
            A(
                Lucide("twitter", cls="w-4 h-4 mr-2 text-white"),
                "Twitter",
                href="https://twitter.com/rasmus1610",
                cls="uk-button uk-button-primary uk-margin-small-top uk-margin-small-right",
            ),
        ),
        H2(
            "Here are some things I wrote:",
            cls="text-3xl font-bold font-heading tracking-tight uk-margin-large-top",
        ),
        Div(
            *[BlogCard(post) for post in posts],
            cls="md:grid md:grid-cols-3 md:gap-4 uk-margin-top space-y-4 md:space-y-0",
            hx_boost="true",
        ),
        cls="uk-container uk-container-xl py-16",
    )


@rt("/posts/{slug}")
def get(slug: str):
    with open(f"posts/{slug}.md", "r") as file:
        post = frontmatter.load(file)

    twitter_headers = (
        Meta(name="twitter:card", content="summary"),
        Meta(name="twitter:title", content=post["title"]),
        Meta(
            name="twitter:description",
            content=post["excerpt"] if "excerpt" in post else "Blog by Marius Vach",
        ),
        Meta(
            name="twitter:image",
            content=f"https://blog.mariusvach.com/images/{post['image']}"
            if "image" in post
            else "https://blog.mariusvach.com/images/og.png",
        ),
        Meta(
            name="og:image",
            content=f"https://blog.mariusvach.com/images/{post['image']}"
            if "image" in post
            else "https://blog.mariusvach.com/images/og.png",
        ),
    )

    return (
        *twitter_headers,
        Title(f"{post['title']} - Marius Vach Blog"),
        Div(
            A(
                Lucide("arrow-left", cls="w-4 h-4 text-black mr-2"),
                "Go Back",
                href="/",
                cls="absolute md:top-0 left-0 top-2 md:-ml-48 md:mt-16 uk-button uk-button-ghost",
            ),
            H1(
                post["title"],
                cls="text-4xl font-bold font-heading tracking-tight uk-margin-small-bottom",
            ),
            P(
                post["date"].strftime("%B %d, %Y"),
                " by Marius Vach",
                cls="uk-text-muted uk-text-small uk-text-italic",
            ),
            Div(post, cls="marked prose mx-auto uk-margin-top"),
            cls="uk-container max-w-[65ch] mx-auto relative py-16",
        ),
    )


@rt("/feed.xml")
def get():
    posts = get_posts()
    feed_items = []
    for post in posts:
        item = f"""
        <item>
            <title>{post["title"]}</title>
            <link>https://blog.mariusvach.com/posts/{post["slug"]}</link>
            <description>{post["excerpt"] if "excerpt" in post else ""}</description>
            <pubDate>{post["date"].strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate>
            <guid>https://blog.mariusvach.com/posts/{post["slug"]}</guid>
        </item>
        """
        feed_items.append(item)

    feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>Marius Vach Blog</title>
        <link>https://blog.mariusvach.com/</link>
        <description>Blog by Marius Vach</description>
        {"".join(feed_items)}
    </channel>
    </rss>
    """
    return Response(feed, media_type="application/rss+xml")


serve()
