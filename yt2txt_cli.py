from youtube_transcript_api import YouTubeTranscriptApi
import re
import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("url", metavar="url", type=str, help="Enter YouTube Url")
args = parser.parse_args()

# Ask the user for the Video URL
#url = input("Video URL: ")
url = args.url



###########################
# EXTRACTING THE VIDEO ID # 
###########################

def extract_video_id(url):
    # Define a regex pattern for YouTube video URLs
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def fetch_video_title(url):
    try:
        # Send a GET request to the YouTube video page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the title tag
        title = soup.find('title').text

        # Remove the " - YouTube" suffix (if present)
        if title.endswith(" - YouTube"):
            title = title[:-10]

        return title
    except Exception as e:
        return f"Error fetching title: {e}"

video_title = fetch_video_title(url)

# save the video id into a variable
video_id = extract_video_id(url)
print("EXTRACTING VIDEO ID:", video_id)
print("EXTRACTING VIDEO TITLE:", video_title)



###########################################
# DOWNLOADING THE SUBTITLES IN TXT FORMAT #
###########################################

# Fetch transcript
print("FETCHING TRANSCRIPT")
srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['de-DE', 'de', 'en'])

# Extract text directly from the transcript
output_lines = [item['text'] for item in srt if 'text' in item]

print("WRITING FILE")
# Write the extracted text to the file
with open(f"transcript-{video_title[:10]}.txt", "w") as f:
    f.write('\n'.join(output_lines))

print("DONE!")
