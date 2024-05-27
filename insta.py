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

def is_fake_account(account_info):
    if account_info is None:
        return True, "Account not found or error fetching account info"

    if account_info['followers'] / (account_info['following'] + 1) < 0.1:
        return True, "Low follower to following ratio"

    if not account_info['profile_picture'] or len(account_info['bio']) < 5:
        return True, "Missing profile picture or generic bio"

    if account_info['is_private']:
        return True, "Private account"


    return False, "Account appears genuine"

if __name__ == "__main__":
    username = input("Enter Instagram username: ")
    account_info = fetch_account_info(username)

    if account_info:
        print(f"Account Info: {json.dumps(account_info, indent=4)}")
        is_fake, reason = is_fake_account(account_info)
        print(f"Is the account fake? {is_fake}")
        print(f"Reason: {reason}")
    else:
        print("Could not fetch account information.")
