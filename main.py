from fetch_thread import fetch_thread_data
from summarizer import summarize_text
from cache import init_db, get_summary_from_cache, save_summary_to_cache

def summarize_reddit_thread(url):
    init_db()

    thread = fetch_thread_data(url)
    post_id = thread.get("id")

    # Check cache
    cached_summary = get_summary_from_cache(post_id)
    if cached_summary:
        print("🧠 Cached summary found!")
        print(cached_summary)
        return

    full_text = thread['title'] + "\n" + thread['selftext'] + "\n" + "\n".join(thread['comments'])

    summary = summarize_text(full_text)

    save_summary_to_cache(post_id, summary)

    print("✅ Summary:")
    print(summary)

if __name__ == "__main__":
    url = input("Enter Reddit thread URL: ")
    summarize_reddit_thread(url)
