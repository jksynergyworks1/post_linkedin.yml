import pandas as pd
import requests
import os
from datetime import datetime

# LinkedIn API details - replace with your LinkedIn API credentials
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # GitHub secret for the access token

# Read posts from Excel file
def read_excel_file(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    return df

# Post content to LinkedIn
def post_to_linkedin(post_content):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    payload = {
        "author": "urn:li:person:YOUR_PERSON_URN",  # Replace with your LinkedIn Person URN
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.json()

# Function to check posts scheduled for today and post them to LinkedIn
def post_scheduled_content(file_path):
    df = read_excel_file(file_path)
    today = datetime.today().strftime('%Y-%m-%d')
    
    for index, row in df.iterrows():
        post_date = row['Post_Date'].strftime('%Y-%m-%d')
        post_content = row['Post_Content']
        
        if post_date == today:
            status_code, response = post_to_linkedin(post_content)
            if status_code == 201:
                print(f"Post successful: {post_content}")
            else:
                print(f"Failed to post: {response}")

# Main function to trigger the posting process
if __name__ == "__main__":
    file_path = "posts.xlsx"  # The Excel file path in the repository
    post_scheduled_content(file_path)
