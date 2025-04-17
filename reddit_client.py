import praw

def get_reddit_client():
    return praw.Reddit(
        client_id='',
        client_secret='',
        user_agent='Reddit Thread Summarizer by Nidhi!'
    )
