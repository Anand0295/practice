import requests
from bs4 import BeautifulSoup
import json

def get_profile(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("Could not access profile. Maybe username is wrong or profile is private.")
        return None
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find window._sharedData JavaScript object
    shared_data = None
    for script in soup.find_all("script"):
        if script.text.strip().startswith("window._sharedData"):
            json_str = script.text.strip()[21:-1]
            shared_data = json.loads(json_str)
            break
    if not shared_data:
        print("Could not parse profile details.")
        return None

    user = shared_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]

    # Basic Info
    bio = user.get("biography", "")
    profile_pic_url = user.get("profile_pic_url_hd", "")
    full_name = user.get("full_name", "")
    external_url = user.get("external_url", "")
    posts = user["edge_owner_to_timeline_media"]["count"]
    followers = user["edge_followed_by"]["count"]
    following = user["edge_follow"]["count"]
    is_private = user.get("is_private", False)

    # Available posts on landing page (usually 12)
    edges = user["edge_owner_to_timeline_media"]["edges"]
    post_likes = [edge["node"]["edge_liked_by"]["count"] for edge in edges if "edge_liked_by" in edge["node"]]
    avg_likes = sum(post_likes)//len(post_likes) if post_likes else 0

    # Print details
    print(f"Username: {username}")
    print(f"Full Name: {full_name}")
    print(f"Bio: {bio}")
    print(f"Website: {external_url}")
    print(f"Followers: {followers}")
    print(f"Following: {following}")
    print(f"Number of Posts: {posts}")
    print(f"Private Profile: {'Yes' if is_private else 'No'}")
    print(f"Profile Picture: {profile_pic_url}")

    # Download profile picture if user wants
    choice = input("Download profile picture? (y/n): ")
    if choice.lower() == 'y':
        download_pfp(profile_pic_url, username)

    print(f"Posts Fetched: {len(edges)}")
    print(f"Total Likes (recent posts): {sum(post_likes)}")
    print(f"Average Likes per Post (recent): {avg_likes}")

def download_pfp(url, username):
    resp = requests.get(url)
    if resp.status_code == 200:
        filename = f"{username}_pfp.jpg"
        with open(filename, "wb") as f:
            f.write(resp.content)
        print(f"Profile pic saved as {filename}")
    else:
        print("Could not download profile picture.")

if __name__ == "__main__":
    uname = input("Enter Instagram username (public): ")
    get_profile(uname)
