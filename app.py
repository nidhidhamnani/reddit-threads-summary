import streamlit as st
from fetch_thread import fetch_thread_data
from reddit_client import get_reddit_client
from summarizer import summarize_text
from cache import init_db, get_summary_from_cache, save_summary_to_cache, get_cache_stats
from voice import text_to_voice

init_db()

st.set_page_config(page_title="Reddit Thread Summarizer", layout="wide")
st.title("🧵 Reddit Thread Summarizer")
tab1, tab2 = st.tabs(["🧵 Summarize a Thread", "📈 Trending Explorer"])
with tab1:
    url = st.text_input("🔗 Enter Reddit thread URL:")

    if url:
        with st.spinner("Fetching thread..."):
            thread = fetch_thread_data(url)
            post_id = thread.get("id")

        full_text = thread['title'] + "\n" + thread['selftext'] + "\n" + "\n".join(thread['comments'])
        style = st.selectbox("Choose summary style", ["Neutral", "Funny", "Analytical", "Poetic"])

        cache_key = f"{post_id}_{style}"
        cached_summary = get_summary_from_cache(cache_key)

        if cached_summary:
            st.success("✅ Summary retrieved from cache!")
            summary = cached_summary
        else:
            st.warning("⚠️ Not in cache — generating summary...")
            summary = summarize_text(text=full_text, style=style)
            save_summary_to_cache(cache_key, summary)
            st.success("🧠 New summary generated and cached!")

        st.markdown("### 📋 Summary")
        st.write(summary)

        if st.button("🔈 Summary Audio"):
            audio_path = text_to_voice(summary)
            st.audio(audio_path)

        with st.expander("📄 Full Thread (Click to Expand)"):
            st.write(full_text)

        if thread.get("gif_url"):
            st.image(thread["gif_url"], caption="🎬 Media from Post")

        stats = get_cache_stats()
        st.markdown("### 📊 Cache Stats")
        st.metric("Total Requests", stats['total_requests'])
        st.metric("Cache Hits", stats['hits'])
        st.metric("Cache Misses", stats['misses'])
        st.metric("Hit Ratio", f"{stats['hit_ratio']:.2f}%")

with tab2:
    st.subheader("Trending Topic Explorer")

    subreddit_input = st.text_input("Enter subreddit (without r/)", value="AskReddit", key="subreddit_input")
    sort_type = st.selectbox("Choose sort type", ["hot", "top", "new"], key="sort_type")
    num_threads = st.slider("How many threads to summarize?", 1, 20, 5)

    if st.button("🔍 Fetch & Summarize Trending Threads"):
        with st.spinner("Fetching posts..."):
            reddit = get_reddit_client()
            subreddit = reddit.subreddit(subreddit_input)

            if sort_type == "hot":
                posts = subreddit.hot(limit=num_threads)
            elif sort_type == "top":
                posts = subreddit.top(limit=num_threads)
            elif sort_type == "new":
                posts = subreddit.new(limit=num_threads)

            for idx, post in enumerate(posts):
                st.markdown(f"### {idx + 1}. [{post.title}](https://www.reddit.com{post.permalink})")
                submission = reddit.submission(id=post.id)
                submission.comments.replace_more(limit=0)
                comments = [c.body for c in submission.comments[:30]]
                full_text = post.title + "\n" + post.selftext + "\n" + "\n".join(comments)
                summary = summarize_text(text=full_text, style="Neutral")
                st.write(summary)
                st.markdown("---")




#
# url = st.text_input("🔗 Enter Reddit thread URL:")
#
# if url:
#     with st.spinner("Fetching thread..."):
#         thread = fetch_thread_data(url)
#         post_id = thread.get("id")
#
#     full_text = thread['title'] + "\n" + thread['selftext'] + "\n" + "\n".join(thread['comments'])
#     style = st.selectbox(
#         "Choose summary style",
#         ["Neutral", "Funny", "Analytical", "Poetic"]
#     )
#
#     cached_summary = get_summary_from_cache(post_id+style)
#
#     if cached_summary:
#         st.success("✅ Summary retrieved from cache!")
#         summary = cached_summary
#     else:
#         st.warning("⚠️ Not in cache — generating summary...")
#
#         summary = summarize_text(text=full_text, style=style)
#         save_summary_to_cache(post_id+style, summary)
#         st.success("🧠 New summary generated and cached!")
#
#     with st.expander("📄 Full Thread (Raw Text)", expanded=False):
#         st.write(full_text)
#
#     st.markdown("### 📋 Summary")
#     st.write(summary)
#     if thread.get("gif_url"):
#         st.markdown("### 🎬 GIF from Post")
#         st.image(thread["gif_url"])
#
#     if st.button("🔈 Read Summary Aloud"):
#         path = text_to_voice(summary)
#         st.audio(path)
#
#     stats = get_cache_stats()
#     st.markdown("### 📊 Cache Stats")
#     st.metric("Total Requests", stats['total_requests'])
#     st.metric("Cache Hits", stats['hits'])
#     st.metric("Cache Misses", stats['misses'])
#     st.metric("Hit Ratio", f"{stats['hit_ratio']:.2f}%")
#
#
# st.header("📈 Trending Topic Explorer")
#
# subreddit_input = st.text_input("Enter subreddit (without r/)", value="AskReddit")
# sort_type = st.selectbox("Choose sort type", ["hot", "top", "new"])
# num_threads = st.slider("How many threads to summarize?", 1, 20, 5)
#
# if st.button("🔍 Fetch & Summarize Trending Threads"):
#     with st.spinner("Fetching posts..."):
#         reddit = get_reddit_client()
#         subreddit = reddit.subreddit(subreddit_input)
#
#         if sort_type == "hot":
#             posts = subreddit.hot(limit=num_threads)
#         elif sort_type == "top":
#             posts = subreddit.top(limit=num_threads)
#         elif sort_type == "new":
#             posts = subreddit.new(limit=num_threads)
#
#         for idx, post in enumerate(posts):
#             st.markdown(f"### {idx + 1}. [{post.title}](https://www.reddit.com{post.permalink})")
#
#             submission = reddit.submission(id=post.id)
#             submission.comments.replace_more(limit=0)
#             comments = [c.body for c in submission.comments[:30]]
#
#             full_text = post.title + "\n" + post.selftext + "\n" + "\n".join(comments)
#
#             summary = summarize_text(full_text)
#
#             st.write(summary)
#             st.markdown("---")
