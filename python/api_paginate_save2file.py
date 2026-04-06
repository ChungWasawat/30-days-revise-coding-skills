import requests, json, time, logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def fetch_with_retry(url, params, retries=3, wait=2):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.Timeout:
            logging.warning(f"Attempt {attempt}: Timeout")
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP {e.response.status_code} — not retrying")
            break
        except requests.exceptions.ConnectionError:
            logging.warning(f"Attempt {attempt}: Connection error")
        time.sleep(wait)
    return None

def save_raw(data, name):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(f"data/raw/{name}_{ts}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved {len(data)} records → {path}")

# --- Run ---
all_posts = []
page = 1
limit=10
offset = 0
url="https://jsonplaceholder.typicode.com/posts"

# may add sleep() to avoid api rate limit
while True:
    data = fetch_with_retry(
        url,
        params={"_page": page, "_limit": limit}
    )
    if not data:
        break
    all_posts.extend(data)
    page += 1

save_raw(all_posts, "posts")
print(f"Done — {len(all_posts)} posts saved")