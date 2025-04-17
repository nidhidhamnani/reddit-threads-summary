from momento import CacheClient, Configurations, CredentialProvider
from datetime import timedelta
import os
from momento.responses import CacheGet
import json

MOMENTO_CACHE_NAME = "reddit-summaries"
STATS_FILE = "cache_stats.json"

client = CacheClient(
    configuration=Configurations.Laptop.v1(),
    credential_provider=CredentialProvider.from_environment_variable("MOMENTO_AUTH_TOKEN"),
    default_ttl=timedelta(days=30)  # cache TTL
)

def init_db():
    try:
        client.create_cache(MOMENTO_CACHE_NAME)
    except:
        pass

def save_summary_to_cache(post_id, summary):
    client.set(MOMENTO_CACHE_NAME, post_id, summary)

cache_hits = 0
cache_misses = 0

def get_summary_from_cache(post_id):
    result = client.get(MOMENTO_CACHE_NAME, post_id)

    if isinstance(result, CacheGet.Hit):
        record_hit()
        return result.value_string

    if isinstance(result, CacheGet.Miss):
        record_miss()
        return None

    raise Exception(f"Unexpected Momento response: {result}")

def _load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"hits": 0, "misses": 0}

def _save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def record_hit():
    stats = _load_stats()
    stats["hits"] += 1
    _save_stats(stats)

def record_miss():
    stats = _load_stats()
    stats["misses"] += 1
    _save_stats(stats)

def get_cache_stats():
    stats = _load_stats()
    total = stats["hits"] + stats["misses"]
    hit_ratio = (stats["hits"] / total) * 100 if total > 0 else 0
    return {
        "hits": stats["hits"],
        "misses": stats["misses"],
        "total_requests": total,
        "hit_ratio": hit_ratio
    }
