import requests
import re
import json
from datetime import datetime
from .utils_time import parse_relative_time

class LinkedInParser:
    BASE_URL = "https://www.linkedin.com"

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            )
        }

    def _fetch_html(self, post_url):
        try:
            response = requests.get(post_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[Error] Failed to fetch post: {e}")
            return ""

    def _extract_json_data(self, html):
        match = re.search(r"com.linkedin.voyager.dash.feed.update.Update:(.*?)\"", html)
        if not match:
            return []
        post_id = match.group(1)
        return self._mock_comments(post_id)

    def _mock_comments(self, post_id):
        now = datetime.utcnow()
        return [
            {
                "comment_id": f"{post_id}_1",
                "text": "This is a great post!",
                "posted_at": {
                    "timestamp": int(now.timestamp()),
                    "date": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "relative": "2d"
                },
                "is_edited": False,
                "is_pinned": False,
                "comment_url": f"{self.BASE_URL}/feed/update/{post_id}/",
                "comment_type": "comment",
                "author": {
                    "name": "Jane Doe",
                    "headline": "Marketing Specialist",
                    "profile_url": f"{self.BASE_URL}/in/janedoe/",
                    "profile_picture": "https://media.licdn.com/dms/image/C4E03AQExample"
                },
                "stats": {
                    "total_reactions": 5,
                    "reactions": {"like": 4, "appreciation": 1},
                    "comments": 0
                },
                "post_input": post_id
            },
            {
                "comment_id": f"{post_id}_2",
                "text": "Totally agree with your point!",
                "posted_at": {
                    "timestamp": int(now.timestamp()),
                    "date": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "relative": "1d"
                },
                "is_edited": False,
                "is_pinned": False,
                "comment_url": f"{self.BASE_URL}/feed/update/{post_id}/",
                "comment_type": "reply",
                "author": {
                    "name": "John Smith",
                    "headline": "Tech Analyst",
                    "profile_url": f"{self.BASE_URL}/in/johnsmith/",
                    "profile_picture": "https://media.licdn.com/dms/image/C4E03AQExample2"
                },
                "stats": {
                    "total_reactions": 2,
                    "reactions": {"like": 2},
                    "comments": 0
                },
                "post_input": post_id,
                "parent_comment_id": f"{post_id}_1"
            }
        ]

    def scrape_post(self, post_url):
        html = self._fetch_html(post_url)
        data = self._extract_json_data(html)
        for item in data:
            item["posted_at"]["relative"] = parse_relative_time(item["posted_at"]["timestamp"])
        return data