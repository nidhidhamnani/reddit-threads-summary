from reddit_client import get_reddit_client
from fetch_thread import fetch_thread_data
from summarizer import summarize_text
from cache import init_db, get_summary_from_cache, save_summary_to_cache
from time import sleep

def crawl_and_summarize(subreddit_name="AskReddit", limit=1000):
    init_db()
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)

    hit_count = 0
    miss_count = 0

    print(f"🚀 Crawling r/{subreddit_name} — aiming for {limit} threads...")

    for idx, submission in enumerate(subreddit.hot(limit=limit)):
        post_id = submission.id
        print(f"\n[{idx+1}] Processing: {submission.title} (ID: {post_id})")

        cached_summary = get_summary_from_cache(post_id)
        if cached_summary:
            print("✅ Cache Hit")
            hit_count += 1
            continue

        try:
            thread_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "comments": []
            }

            submission.comments.replace_more(limit=0)
            thread_data["comments"] = [c.body for c in submission.comments[:30]]

            full_text = thread_data["title"] + "\n" + thread_data["selftext"] + "\n" + "\n".join(thread_data["comments"])
            summary = summarize_text(full_text)

            save_summary_to_cache(post_id, summary)
            print("🧠 Summary computed and cached.")
            miss_count += 1

        except Exception as e:
            print("⚠️ Error processing thread:", e)
            continue

        # Optional: Sleep to avoid rate limits
        sleep(0.2)

    total = hit_count + miss_count
    hit_ratio = (hit_count / total) * 100 if total > 0 else 0

    print("\n📊 Summary:")
    print(f"Total Threads: {total}")
    print(f"Cache Hits: {hit_count}")
    print(f"Cache Misses: {miss_count}")
    print(f"Cache Hit Ratio: {hit_ratio:.2f}%")

if __name__ == "__main__":
    crawl_and_summarize(subreddit_name="AskReddit", limit=1000)
