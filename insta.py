import instaloader
import json
from datetime import datetime

def fetch_account_info(username):
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        metadata = profile._metadata()

        json_metadata = json.dumps(metadata, indent=4)
        
        print(json_metadata)

        account_info = {
            "username": metadata['username'],
            "followers": metadata['edge_followed_by']['count'],
            "following": metadata['edge_follow']['count'],
            "posts": metadata['edge_owner_to_timeline_media']['count'],
            "profile_picture": metadata['profile_pic_url'],
            "bio": metadata['biography'],
            "is_private": metadata['is_private'],
            "is_verified": metadata['is_verified']
        }

        return account_info

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile {username} does not exist.")
        return None
    except instaloader.exceptions.InstaloaderException as e:
        print(f"An error occurred: {e}")
        return None



if __name__ == "__main__":
    usernames = input("Enter Instagram usernames separated by commas: ").split(',')
    usernames = [username.strip() for username in usernames]  # Strip any extra whitespace

    for username in usernames:
        account_info = fetch_account_info(username)

        if account_info:
            print(f"Account Info for {username}: {json.dumps(account_info, indent=4)}")
          
            
            
        else:
            print(f"Could not fetch account information for {username}.")