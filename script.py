import datetime
import time
from urllib.parse import urlparse, urlunparse
import feedparser

feeds = [
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC9PBzalIcEQCsiIkq36PyUA", #DigitalFoundry
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCnrVURWNd7VYjlQQ0UDpOQQ", #Tokyo Lens
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCjKSoJlPgcK6BmoSqXpj5xQ", #Action Button
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCO8U0kx_oDhgd3o57rQAlXQ", #Tim Rogers
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCjNErCQgCndSOl6t33m1-nQ", #hazel
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCm8xNi3kuBHE99QH-N_VJVg", #sharmeleon
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCZB6V9fUov0Mx_us3MWWILg", #people make games
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC0fDG3byEcMtbOqPMymDNbw", #noclip
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCb_sF2m3-2azOqeNEdMwQPw", #matthewmatosis
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCvM5uRsbhfp_aW5lLl3SxVg", #unseen
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC-Lg1MlswX4jXkMs93XChMw", #bokeh
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCeTfBygNb1TahcNpZyELO8g", #jacob geller
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCdnmg27qzE0P_mcKSjd7hwQ", #kamiya
    ]

class VideoEntry:
    def __init__(self, channel, title, source, published):
        self.channel = channel
        self.title = title
        self.source = source
        self.published = published

def feedparser_to_local_domain(feedUri, recent_datetime):
    videos = []

    #grab a feed and its title
    video_rss = feedparser.parse(feedUri)
    channel_name = video_rss.feed.title

    #filter down to recent content
    channel_content = video_rss.entries
    recent_channel_content = [video for video in channel_content if datetime.datetime.fromtimestamp(time.mktime(video.published_parsed)) >= recent_datetime]

    #convert from the parser's objects to our own
    for video in recent_channel_content:
        video_entry = VideoEntry(
            channel_name,
            video.get('title', 'No title'),
            video.get('link', 'No link'),
            video.get('published', 'No published')
        )
        videos.append(video_entry)
    return videos
    
#todo: real templating
def render(videoEntries, build_datetime):
    html = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Video Feed: '+str(build_datetime)+'</title><style>.entries {display:flex;flex-wrap:wrap;justify-content:center} .entry {flex: 0 1 40ch;margin:1ch} .thumbnail {width:100%}</style></head><body><div class="entries">'
    for video in videoEntries:
        html += '<div class="entry">'
        html += '<p class="title">'+video.title+'</p>'
        html += '<a class="source" rel="noopener noreferrer nofollow" href="'+video.source+'">Source</a>'
        html += '</div>'
    html += '</div></body></html>'
    with open("public/index.html", "w", encoding="utf-8") as output:
        output.write(html)

build_datetime = datetime.datetime.now()
recent_datetime = build_datetime - datetime.timedelta(30)
all_videos = []

for feed in feeds:
    all_videos += feedparser_to_local_domain(feed, recent_datetime)

#todo: sort by date instead of string
sorted_all_videos = sorted(all_videos, key=lambda v: v.published, reverse=True)
render(sorted_all_videos, build_datetime)
