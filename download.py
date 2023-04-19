# Import requests library
import requests

# Define the GitHub URL of the file to download
github_url = "https://github.com/Music-Recommendation-Engine-Project/Data-Music-Repo/raw/main/user_track_df.parquet"

# Send a GET request to the URL and get the content as bytes
response = requests.get(github_url)
content = response.content

# Open a local file with write and binary modes
with open("user_track_df.parquet", "wb") as f:
    # Write the content to the local file
    f.write(content)

# Print a success message
print("File downloaded successfully.")