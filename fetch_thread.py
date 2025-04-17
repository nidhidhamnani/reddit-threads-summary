from reddit_client import get_reddit_client

def fetch_thread_data(url):
    reddit = get_reddit_client()
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)

    gif_url = None
    image_url = None

    if submission.url.endswith((".gif", ".gifv")):
        gif_url = submission.url
    elif submission.url.endswith((".jpg", ".jpeg", ".png")):
        image_url = submission.url

    if hasattr(submission, "preview"):
        images = submission.preview.get("images", [])
        if images:
            variants = images[0].get("variants", {})
            if "gif" in variants and not gif_url:
                gif_url = variants["gif"]["source"]["url"]

            if not image_url:
                image_url = images[0]["source"]["url"]

    return {
        "id": submission.id,
        "title": submission.title,
        "selftext": submission.selftext,
        "comments": [c.body for c in submission.comments[:30]],
        "gif_url": gif_url,
        "image_url": image_url
    }
