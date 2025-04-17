from cache import get_cache_stats
import time

def monitor_cache(interval=2):
    print("📈 Live Momento Cache Stats (Ctrl+C to quit)\n")
    while True:
        stats = get_cache_stats()
        print(f"💾 Total Requests: {stats['total_requests']}")
        print(f"✅ Hits: {stats['hits']} | ❌ Misses: {stats['misses']}")
        print(f"🎯 Hit Ratio: {stats['hit_ratio']:.2f}%\n")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_cache()
