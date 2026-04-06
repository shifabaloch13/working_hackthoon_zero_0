"""Direct Facebook Post Test"""
import facebook

# Your Page Access Token
token = "EAANxrrU9WAEBQ51oDMNZBkQzx170gzV9zja4YtKhMZCIUIISY6sOPba6ALfl2DzluSZALBiCwAuJ1LROQ7WAIPou06FABDNQr7ce08dBa3zQhT4lxuCEXVWArXNMzy2VJ0bOzit8qhslKgKGflbLWuL9aZCO6nAgVBexOCRVHZBtb3mgbmw4EZAhZC6k1zZAyUFuSWZBrWUELaGwnGYRv8b1n4MrUXVxVK25mczRk5FtHDggZD"

# Initialize Graph API
graph = facebook.GraphAPI(access_token=token)

# Try to post
try:
    result = graph.put_object(
        parent_object="1004531386081562",
        connection_name="feed",
        message="Direct test post from AI Employee!"
    )
    print("✅ SUCCESS! Post created!")
    print(f"Post ID: {result.get('id')}")
    print(f"View: https://facebook.com/{result.get('id')}")
except Exception as e:
    print(f"❌ Error: {e}")
