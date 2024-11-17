"""
Method to search YouTube and return the first result
"""

from youtube_search import YoutubeSearch
import json

def searchYoutube(query):
    print("[+] Searching YouTube for songs.\n[+] Note: This may take a while")
    searchQuery = query[0] + " " + query[1]
    print("[+] Searching for >>", searchQuery)
    results = YoutubeSearch(searchQuery, max_results=1).to_json()
    results_dict = json.loads(results)
    url = "https://youtube.com" + results_dict['videos'][0]['url_suffix']
    print("[+] URL found >> " + url)
    return url