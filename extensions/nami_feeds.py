# fmt: off
import asyncio
import datetime
import zoneinfo
import hashlib
import html
import io
import json
import lxml  # do not remove
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
import discord
import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
from discord.ext import commands, tasks
import re
import copy
from main import Nougat

load_dotenv()

# good lord this file is messy
# TODO: youtube

GMT = datetime.timezone(datetime.timedelta(0), "GMT")

TEST_CHANNEL = 1074754885070897202

ICONS = {
    "none": "<:icon_none:1454889234853793842>",
    "eggbug": "<:icon_eggbug:1425576567945564272>",
    "anon": "<:icon_anon:1425576581815992320>",
    "treat": "<:icon_treat:1425576593018978385>",
    "mochi": "<:icon_mochi:1425576604062449755>",
    "moxie": "<:icon_moxie:1425576614535888986>",
    "trick": "<:icon_trick:1425576626821005372>",
    "syrup": "<:icon_syrup:1425576638657200148>",
    "pastille": "<:icon_pastille:1425576649407332474>",
    "gumdrop": "<:icon_gumdrop:1425576660165595167>",
    "butterscotch": "<:icon_butterscotch:1425576670538104874>",
    "toffee": "<:icon_toffee:1425576681208287325>",
    "periwinkle": "<:icon_periwinkle:1425576690868031599>",
    "baezel": "<:icon_baezel:1425576703291428977>",
    "poffin": "<:icon_poffin:1425576711764054249>",
    "thyme": "<:icon_thyme:1425576724392972328>",
    "spice": "<:icon_spice:1425576732970324090>",
    "nil": "<:icon_nil:1425576745201041459>",
    "kamilla": "<:icon_kamilla:1425576755930071195>",
    "eleni": "<:icon_eleni:1425576767543971931>",
    "qmin": "<:icon_qmin:1425576779745202278>",
    "cassia": "<:icon_cassia:1425576791950495876>",
    "astra": "<:icon_astra:1425576802218410125>",
    "vinegar": "<:icon_vinegar:1425576819385569360>",
    "strudel": "<:icon_strudel:1515865545306538124>",
    "salt": "<:icon_salt:1443398214203080715>",
    "pepper": "<:icon_pepper:1443398245991583775>",
    "timber": "<:icon_timber:1443398285225099364>",
    "twigs": "<:icon_twigs:1443398319853408399>",
    "senbei": "<:icon_senbei:1443398342326489238>",
    "manjuu": "<:icon_manjuu:1449580945740009482>",
    "oz": "<:icon_oz:1449615964873167029>",
    "chai": "<:icon_chai:1449580999955714120>",
    "dango": "<:icon_dango:1449580975234355361>",
    "phoenix": "<:icon_phoenix:1450670773009252533>",
    "tundra": "<:icon_tundra:1450670774783578173>",
    "drop": "<:icon_drop:1450670771704827924>",
    "fennel": "<:icon_fennel:1464368764731527335>",
    "mason": "<:icon_mason:1493038274854260786>",
    "slate": "<:icon_slate:1515864471162322974>",
    "leaf": "<:icon_leaf:1524268345355010248>",
    "marzipan": "<:icon_marzipan:1536014739652481155>",
    "jam": "<:icon_jam:1536014738230738955>",
    "olog": "<:icon_olog:1536014740923355156>",
    "chirval": "<:icon_chirval:1536014737341546588>",
    "searina": "<:icon_searina:1515864486710480896>",
    "illi": "<:icon_illi:1515864501189345420>",
    "vido": "<:icon_vido:1515864521783247070>",
    "ezel": "<:icon_ezel:1515864532877316098>",
    "maia": "<:icon_maia:1524268755717324831>",
    "amphithoe": "<:icon_amphithoe:1524268753406132405>",
    "clio": "<:icon_clio:1524268754295586837>",
    "eudora": "<:icon_eudora:1524268754974933042>"
}
EMOJI = {
    "eggbug": "<:eggbug:1444074342576033793>",
    "eggbug_asleep": "<:eggbug_asleep:1444074343951765686>",
    "eggbug_devious": "<:eggbug_devious:1444074344845283390>",
    "eggbug_heart_sob": "<:eggbug_heart_sob:1444074346296512592>",
    "eggbug_nervous": "<:eggbug_nervous:1444074347986944132>",
    "eggbug_pensive": "<:eggbug_pensive:1444074348473221152>",
    "eggbug_pleading": "<:eggbug_pleading:1444074350050283550>",
    "eggbug_relieved": "<:eggbug_relieved:1444074351011037265>",
    "eggbug_shocked": "<:eggbug_shocked:1444074351853965444>",
    "eggbug_smile_hearts": "<:eggbug_smile_hearts:1444074353208852710>",
    "eggbug_sob": "<:eggbug_sob:1444074354487984181>",
    "eggbug_tuesday": "<:eggbug_tuesday:1444074356060848168>",
    "eggbug_uwu": "<:eggbug_uwu:1444074356878606396>",
    "eggbug_wink": "<:eggbug_wink:1444074357914599537>"
}
TAVERN_CHANNEL_TARGETS = {  # every possible sfw channel and its target 18+ channel in Namitavern
    1074754885070897202: 1537552461605249064,  # test
    1521633877859500072: 1537117062416302150,  # nami-news
    1521633846477721680: 1537117062416302150,  # nami-feeds (same target channel as above)
    1521632401334210659: 1537116000212877392   # nami-asks
}
TAVERN_ROLE_TARGETS = {  # every possible role ping and its respective role in Namitavern
    "<@&1539330597577560164>": "<@&1539330623947276288>",  # Test Ping
    "<@&1521632400491417770>": "<@&1537115998442889268>",  # Nami News
    "<@&1521632400453402739>": "<@&1537115998426235060>",  # Nami Feeds
    "<@&1521632400453402738>": "<@&1537115998426235059>"   # Nami Asks
}

SOURCES: dict = json.load(open("feed_data.json", "r"))


censor_nsfw = False  # god this global variable feels stupid and hacky why did i program everything like this

class Message():
    def __init__(
        self,
        source: str,
        id: (int | str),
        description: (str | None) = None,
        title: (str | None) = None,
        url: (str | None) = None,
        author: (str | None) = None,
        author_icon: (str | None) = None,
        images = [],
        thumbnail: (str | None) = None,
        timestamp: (str | None) = None,
        tags: (str | None) = None,
        embed: bool = True,
        content: str = "",
        nsfw: bool = False,
        ping: bool = True
    ):
        self.source      = SOURCES[source]
        self.id          = id
        self.description = description
        self.title       = title
        self.url         = url    or self.source["embed"]["url"]
        self.author      = author or self.source["embed"]["author"]
        self.author_icon = author_icon or self.source["embed"]["author_icon"]
        self.footer      = self.source["embed"]["footer"]
        self.color       = self.source["embed"]["color"]
        self.thumbnail   = thumbnail
        self.tags        = tags
        self.images      = images
        self.embed       = embed
        self.content     = content
        self.nsfw        = nsfw
        self.footer_icon = self.source["embed"]["footer_icon"]
        self.ping        = ping

        # TEMPORARY FOR SLATE AU
        if self.footer == "ask" and len(self.images) > 0 and self.description and "# slate AU" in self.description:
            self.content += " <@&1521632400453402741>"
            self.footer = "slate au"
            self.color = 0xa15c3e
            self.footer_icon = "https://nomnomnami.com/ask/images/slate.png"


        self.author_url  = self.source["embed"]["author_url"]
        if self.author_url == "[url]":
            self.author_url = self.url

        if tags:
            self.footer += "  •  " + tags

        self.timestamp = None
        if timestamp:
            if ":" in timestamp:  # "real" timestamp, has time
                self.timestamp = datetime.datetime.strptime(timestamp, self.source["embed"]["timestamp_format"])
                # manually set tzinfo because %Z in strptime does not actually do anything???
                if "GMT" in timestamp:
                    self.timestamp = self.timestamp.replace(tzinfo=GMT)
            
            else:  # day only timestamp
                self.footer += "  •  " + timestamp

        # limit description to 4000 chars
        if self.description and len(self.description) > 4000:
            # do my best to spoiler anything that should be spoilered (could have false positives but that's fine)
            self.description = self.description[:4000]
            if ("||" in self.description[:4000] and "||" in self.description[3999:]):
                self.description += "||"
            self.description += "\n## [READ MORE](" + self.url + ")"


    def is_spoiler(self, image: Tag):
        if isinstance(image, dict):
            return False
        if not image.parent:
            return False
        if image.parent.name == "details":
            return True
        if image.parent.parent and image.parent.parent.name == "details":
            return True
        return False

    
    def get_content(self, nougat: bool):
        content = ""
        if self.ping and self.source["role"]:
            if nougat:
                content += f"-# <@&{self.source['role']}>"
            else:
                content += "-# <@&1539330597577560164>" if not self.nsfw else "<@&1539330623947276288>"

        if self.content:
            content += " " + self.content
        return content

    def ready_images(self):
        self.image = None
        self.attachments = []
        if len(self.images) == 1 and not self.is_spoiler(self.images[0]):  # one unspoilered image
            self.image = urljoin("https://nomnomnami.com", self.images[0]["src"])
        else:
            for img in self.images:
                response = requests.get(urljoin("https://nomnomnami.com", img["src"]))
                filename = img["src"].split("/")[-1]
                if self.source == "trick":  # exception for trick pika page
                    filename += ".png"
                discord_file = discord.File(io.BytesIO(response.content),
                                            filename = filename,
                                            spoiler  = self.is_spoiler(img))
                self.attachments.append(discord_file)


    def get_embed(self) -> discord.Embed | None:
        if not self.embed:
            return None
        
        embed = discord.Embed(  color       = self.color,
                                description = self.description,
                                title       = self.title,
                                url         = self.url,
                                timestamp   = self.timestamp)
        embed.set_footer(       text        = self.footer,
                                icon_url    = self.footer_icon)
        if self.image:
            embed.set_image(    url         = self.image)
        if self.author:
            embed.set_author(   name        = self.author,
                                url         = self.author_url,
                                icon_url    = self.author_icon)
        if self.thumbnail:
            embed.set_thumbnail(url         = self.thumbnail)
        return embed


def clean(string: str) -> str:
    return html.unescape(string).replace("*", "\\*").replace("\n", "")


def paragraph(p) -> str:  # TODO: totally rewrite this?? for tag in tag in <p> tag
    text = ""
    for c in p.children:
        if isinstance(c, NavigableString):
            text += clean(c)
        elif isinstance(c, Tag):
            if c.name == "a":
                text += f"[{clean(c.string)}]({urljoin('https://nomnomnami.com', c['href'])})"
            elif c.name == "br":
                text += "\n"
            elif c.name == "strong" or c.name == "b":
                text += "**" + clean(c.string) + "**"
            elif c.name == "em":
                text += "*" + clean(c.string) + "*"
            elif c.name == "del":
                text += "~~" + clean(c.string) + "~~"
            elif c.name == "code":
                text += "`" + clean(c.string) + "`"
            elif c.name == "small":
                text += "-# " + paragraph(c)
            elif c.name == "span":
                text += clean(c.string)

    return text.strip()


def html_to_discord(html: Tag):  # TODO: rewrite this too
    global censor_nsfw  # ughhhhhh
    text = ""
    images = []
    for child in html.children:
        if not child.name:
            continue
        if child.name == "p":
            text += "\n\n" + paragraph(child)
            for grandchild in child.descendants:
                if grandchild.name == "img":
                    if "/ask/images/emoji/" in grandchild["src"]:
                        text += " " + EMOJI[grandchild["src"].split("/")[-1].split(".")[0]] + " "
                    else:
                        images.append(grandchild)
        elif child.name == "h3":
            text += "\n### " + paragraph(child)
        elif child.name == "small":
            text += "\n\n-# " + paragraph(child)
        elif child.name == "ul":
            if "class" in child.attrs and "tags" in child["class"]:
                pass
            else:
                for grandchild in child.descendants:
                    if grandchild.name == "li":
                        text += "\n- " + paragraph(grandchild)
        elif child.name == "ol":
            for grandchild in child.descendants:
                n = 1
                if grandchild.name == "li":
                    text += "\n" + str(n) + ". " + paragraph(grandchild)
                    n += 1
        elif child.name == "details":
            text += "\n\n" + paragraph(child.find("summary"))
            if censor_nsfw and "nsfw" in child.find("summary").string:
                text += "\n[*too gay for Namiverse!*]"
            else:
                text += "\n||" + html_to_discord(child)["text"].strip() + "||"
                images = images + html_to_discord(child)["images"]
        elif child.name == "img":
            images.append(child)
        elif child.name == "div":
            if "class" not in child.attrs or "response" in child["class"] or "content" in child["class"]:
                text += html_to_discord(child)["text"] + "\n"
                images = images + html_to_discord(child)["images"]
            elif "bubble" in child["class"]:
                text += "\n> "+html_to_discord(child)["text"].replace("\n", "\n> ")
            elif "asker" in child["class"]:
                text += "### " + html_to_discord(child)["text"] + " " + child.text.strip()
            elif "icon" in child["class"]:
                if child["class"][1] in ICONS.keys():
                    text += ICONS[child["class"][1]]  # TODO: actually test this
                else:
                    text += ICONS["none"]
            elif "ask" in child["class"]:
                text += html_to_discord(child)["text"]
            elif "youtube-embed" in child["class"]:
                text += "\n" + child.find("iframe")["src"]
        # elif child.name == "span":
        #     text += child.text.strip()


    return {"text": text, "images": images}


def parse_announcements(soup):
    news = soup.find("div", {"class": "news-banner"})
    
    messages = [
        Message("announcements",
                id = news.find("img")["src"],
                title = paragraph(news.find("h3")),
                url = news.find("a")["href"],
                description = paragraph(news.find("p")),
                images = [news.find("img")],
                timestamp = news.find("time").string)
    ]

    return messages


def parse_newsfeed(soup):
    posts = soup.find("article", {"id": "newsfeed"}).find_all("li")

    messages = []
    for post in posts:
        message = Message("newsfeed",
                          id = post.find("time").string,
                          description = paragraph(post),
                          timestamp = post.find("time").string)
        messages.append(message)

    return messages


def parse_posts(soup):
    posts = soup.find_all("article")

    messages = []
    for post in posts:
        footer = "posts"
        if post.find("section", {"class": "tags"}) != None:
            post.find("section", {"class": "tags"})
            tags = [c.string for c in post.find("section", {"class": "tags"}).children if isinstance(c, Tag) and c.string]
            if len(tags) > 0:
                footer += "  •  " + "  ".join(tags)

        message = Message("posts",
                          id = post.find("time").string,  # should be fine as long as two posts don't have the same timestamp in separate page updates
                          description = html_to_discord(post)["text"],
                          images = html_to_discord(post)["images"],
                          timestamp = post.find("time").string + "-0700")  # mountain time. im pretending daylight savings isnt real (TODO)
        messages.append(message)

    return messages


def parse_blog(soup):
    posts = soup.find_all("entry")

    messages = []
    for post in posts:
        content = BeautifulSoup(post.find("content").string, "html.parser").find("div", {"class": "trix-content"})

        url = post.find("link")["href"]
        message = Message("blog",
                          id = post.find("id").string,
                          description = (paragraph(content.find("p")) + f"\n### [READ MORE]({url})"),
                          title = post.find("title").string,
                          url = url,
                          timestamp = post.find("published").string)
        messages.append(message)

    return messages


def parse_ask(soup: BeautifulSoup):
    posts = soup.find_all("article")
    global censor_nsfw

    messages = []
    for post in posts:
        tags = ""
        tags_element = post.find("ul", {"class": "tags"})
        if tags_element:
            tags_list: list[str] = []
            for c in tags_element.children:
                if isinstance(c, Tag) and c.string:
                    tags_list.append(c.string)
            tags = "  ".join(tags_list)

        paragraph = post.find("p")
        beginning = ""
        if paragraph:
            beginning = paragraph.text
            if len(beginning) >= 20:
                beginning = beginning[:20]
        id = beginning + hashlib.sha1(bytes(post.text, "utf-8")).hexdigest()

        # has nsfw content (post uncensored in namitavern)
        has_nsfw = len(post.find_all("summary", string=re.compile("nsfw text"))) > 0  # if any <summary> has the string "nsfw text" in it
        if has_nsfw:
            message = Message("ask",
                            id = id,
                            description = html_to_discord(post)["text"],
                            images = [image for image in html_to_discord(post)["images"]],
                            tags = tags,
                            nsfw = True)
            messages.append(message)

        fully_nsfw = False
        if has_nsfw:
            post_without_nsfw = copy.copy(post)
            if not post_without_nsfw.details:
                raise Exception("no details but yes details?? i dont know i wrote this code when i was tired")
            nsfw_details = post_without_nsfw.details.extract()
            first_details_nsfw = nsfw_details.summary and nsfw_details.summary.string and "nsfw text" in nsfw_details.summary.string
            post_is_only_details = html_to_discord(post_without_nsfw)["text"].strip() == ""
            if first_details_nsfw and post_is_only_details:
                fully_nsfw = True

        # isn't fully nsfw (post in namiverse, censored if applicable)
        if not fully_nsfw:
            censor_nsfw = True
            message = Message("ask",
                            id = id,
                            description = html_to_discord(post)["text"],
                            images = [image for image in html_to_discord(post)["images"]],
                            tags = tags)
            censor_nsfw = False
            messages.append(message)
            

    return messages


def parse_status_cafe(soup):
    posts = soup.find_all("entry")

    messages = []
    for post in posts:
        message = Message("status_cafe",
                          id = post.find("id").string,
                          description = clean(post.find("content").string),
                          url = post.find("link")["href"],
                          timestamp = post.find("published").string,
                          author = " ".join(post.find("title").string.split(" ")[:2]),
                          author_icon = soup.find("icon").string)
        messages.append(message)

    return messages


def parse_trick(soup):
    posts = soup.find_all("entry")

    # make messages
    messages = []
    for post in posts:
        content = BeautifulSoup(post.find("content").string, "html.parser").find("div", {"class": "trix-content"})
        if not content:
            raise Exception("no content found")

        message = Message("trick",
                          id = post.find("id").string,
                          description = html_to_discord(content)["text"],
                          title = post.find("title").string,
                          url = post.find("link")["href"],
                          images = content.find_all("img"),
                          timestamp = post.find("published").string)
        messages.append(message)

    return messages


def parse_neocities(soup):
    saved_ids = json.load(open("feed_data.json", "r"))["neocities"]["saved_ids"]

    posts = soup.find_all("item")
    messages = []
    for post in posts:
        id = post.find("guid").text
        if id not in saved_ids:
            new_soup = BeautifulSoup(requests.get(post.find("link").text).content, "html.parser")
            desc = "\n".join([title.text.replace("\n", "") for title in new_soup.find_all("span", {"class": "title"})])

            message = Message("neocities",
                              id = id,
                              description = desc,
                              title = post.find("title").text,
                              url = post.find("link").text,
                              thumbnail = soup.find("image").find("url").text,
                              timestamp = post.find("pubDate").text)
            messages.append(message)

    return messages


def parse_pillowfort(posts_json):
    posts = posts_json["posts"]
    messages = []
    for post in posts:
        if post["reblogged_from_post_id"]:  # do not count reblogs from other accounts
            continue

        url = f"https://www.pillowfort.social/posts/{post['id']}"

        content: str = post["content"]
        content = content.replace("<p>[READ-MORE]</p>", f"<details><summary>( Read More... )</summary>")
        content = content.replace("<p>[/READ-MORE]</p>", "</details>")

        desc = html_to_discord(BeautifulSoup(content, "html.parser"))["text"]
        # if "[READ-MORE]" in desc:
        #     desc = desc.split("[READ-MORE]")[0] + f"( [Read More...]({url}) )"

        images = html_to_discord(BeautifulSoup(content, "html.parser"))["images"]  # images = []
        for media in post["media"]:
            if media["url"]:  # not null/None
                if media["media_type"] == "picture":
                    images.append({"src": media["url"]})
                else:
                    desc += "\n\n" + media["url"]

        if post["privacy"] == "public":
            message = Message("pillowfort",
                            id = post["id"],
                            title = post["title"],
                            description = desc,
                            url = url,
                            images = images,
                            timestamp = post["publish_at"],
                            author = post["username"],
                            author_icon = post["avatar_url"],
                            tags = " ".join(["#" + tag for tag in post["tags"]]),
                            nsfw = post["nsfw"])
        else:
            ping = True
            if post["privacy"] == "users":
                desc = "[This post is only visible to logged in users.]"
            elif post["privacy"] == "followers":
                desc = "[This post is only visible to followers.]"
            elif post["privacy"] == "mutuals":
                desc = "[This post is only visible to mutuals.]"
                ping = False
            else:
                raise ValueError("unknown pillowfort post privacy value")
            message = Message("pillowfort",
                            id = post["id"],
                            description=desc,
                            url = url,
                            timestamp = post["publish_at"],
                            author = post["username"],
                            author_icon = post["avatar_url"],
                            nsfw = post["nsfw"],
                            ping = ping)
        messages.append(message)
    return messages


def parse_apoc(soup):
    saved_ids = json.load(open('feed_data.json', 'r'))['apoc']['saved_ids']
    # we want to check id early to avoid checking every single recent comic
    posts = soup.find_all('item')
    messages = []
    for post in posts:
        id = int(post.find('link').text.split('/')[-2])
        if id not in saved_ids:
            soup = BeautifulSoup(requests.get(post.find('link').text).content, 'html.parser')
            comic_title = soup.find('h2', {'class': 'comictitle'})
            if not comic_title:
                raise Exception("no comic title")

            num = int(comic_title.text.split('#')[1].split(' ')[0])
            authornotes = soup.find('div', {'class': 'authornotes'})
            if authornotes:
                desc = paragraph(authornotes.find('div', {'class': 'notecontent'}))
            else:
                desc = ''

            message = Message('apoc',
                              id = id,
                              description = desc,
                              title = post.find('title').text,
                              url = f'https://another-piece-of-candy.thecomicseries.com/comics/{num}/',
                              images = [BeautifulSoup(post.find('description').text, 'html.parser').find('img')],
                              timestamp = post.find('pubDate').text)
            messages.append(message)

    return messages


def parse_tcs(soup):
    saved_ids = json.load(open("feed_data.json", "r"))['tcs']['saved_ids']
    # we want to check id early to avoid checking every single recent comic
    posts = soup.find_all("item")
    messages = []
    for post in posts:
        id = int(post.find('link').text.split('/')[-2])
        if id not in saved_ids:
            soup = BeautifulSoup(requests.get(post.find("link").text).content, "html.parser")

            authornotes = soup.find('div', {'class': 'authornotes'})
            if authornotes:
                desc = paragraph(authornotes.find("div", {"class": "notecontent"}))
            else:
                desc = ""

            message = Message("tcs",
                              id = post.find("guid").string,
                              description = desc,
                              title = post.find("title").string,
                              url = post.find("link").string,
                              images = [BeautifulSoup(post.find("description").text, "html.parser").find("img")],
                              timestamp = post.find("pubDate").text)
            messages.append(message)

    return messages


def parse_site_updates(soup):
    posts = soup.find("article", {"id": "site-updates"}).find_all("li")

    messages = []
    for post in posts:
        message = Message("site_updates",
                          id = post.find("time").string + paragraph(post),  # two can have same date
                          description = paragraph(post),
                          timestamp = post.find("time").string)
        messages.append(message)

    return messages


def parse_post_status(soup):
    status = soup.find("section", {"id": "status"})
    table = status.find("table")
    desc = ""
    for tr in table.find_all("tr"):
        th = tr.find("th")
        td = tr.find("td")
        desc += f"**{th.text}** {paragraph(td)}\n"

    messages = [Message("post_status",
                        id = status.find("time").string + desc,  # can change twice in a day i suppose
                        description = desc,
                        timestamp = status.find("time").string)]

    return messages


def parse_youtube(soup):
    posts = soup.find_all("entry")

    messages = []
    for post in posts:
        message = Message("youtube",
                          embed = False,
                          id = post.find("id").string,
                          content = post.find("link")["href"])
        messages.append(message)

    return messages


def parse_patreon(posts_json):
    posts = posts_json["data"]

    for include in posts_json["included"]:
        if include["type"] == "campaign":
            campaign = include
            break

    messages = []
    for post in posts:
        message = Message("patreon",
                          id = post["id"],
                          title = post["attributes"]["title"],
                          description = "",
                          url = post["attributes"]["url"],
                          timestamp = post["attributes"]["created_at"],
                          author = campaign["attributes"]["name"],
                          author_icon = campaign["attributes"]["avatar_photo_url"])
        messages.append(message)
    return messages



funcs = {
    "announcements":    parse_announcements,
    "newsfeed":         parse_newsfeed,
    "posts":            parse_posts,
    "post_status":      parse_post_status,
    "blog":             parse_blog,
    "ask":              parse_ask,
    "status_cafe":      parse_status_cafe,
    "neocities":        parse_neocities,
    "trick":            parse_trick,
    "apoc":             parse_apoc,
    "tcs":              parse_tcs,
    "site_updates":     parse_site_updates,
    "youtube":          parse_youtube,
    "pillowfort":       parse_pillowfort,
    "patreon":          parse_patreon,
    "nsfw_patreon":     parse_patreon
}


eastern_time = zoneinfo.ZoneInfo("America/New_York")  # Use zoneinfo so it tracks EST/EDT changes.

class NamiFeeds(commands.Cog):
    def __init__(self, bot: Nougat):
        self.bot = bot
        self.feeds.start()

    def cog_unload(self):
        self.feeds.cancel()


    @tasks.loop(seconds=15.0)
    async def feeds(self):
        # soups = {}

        # TODO: RE-ADD APOC AND TCS WHEN YOU FIGURE IT OUT!!
        for s in ["youtube", "pillowfort", "neocities", "patreon", "nsfw_patreon", "announcements", "post_status", "posts", "newsfeed", "site_updates", "ask", "status_cafe", "blog", "trick"]:
            # aiohttp asyncio stuff
            try:
                source: dict = SOURCES[s]
                await self.check(source)
                # soups[source["link"]] = self.fetch_source(source)
            except Exception as e:
                await self.bot.report(s + " " + str(e))
            await asyncio.sleep(0.1)  # avoid heartbeat blocking


    @feeds.before_loop
    async def before_feeds(self):
        await self.bot.wait_until_ready()

    
    def fetch_source(self, source: dict):
        headers = source["headers"].copy()
        if "etag" in source.keys():
            headers["If-None-Match"] = source["etag"]
        if source["name"] == "pillowfort":
            headers["Cookie"] = os.environ["PF_COOKIE"]
            headers["X-CSRF-Token"] = os.environ["PF_X-CSRF-TOKEN"]

        response = requests.get(source["link"], headers=headers, timeout=6.1)

        if response.status_code == 304:  # not modified
            return None
        elif "ETag" in response.headers.keys():
            source["etag"] = response.headers["ETag"]

        if source["headers"]["Accept"] not in response.headers["Content-Type"]:
            raise Exception(f"wrong content type for {source['name']}: got {response.headers['Content-Type']} but expected {source['headers']['Accept']}")

        if "text/html" in response.headers["Content-Type"]:
            soup = BeautifulSoup(response.content, "html.parser")
        elif "application/atom+xml" in response.headers["Content-Type"] or "application/xml" in response.headers["Content-Type"] or "text/xml" in response.headers["Content-Type"]:
            soup = BeautifulSoup(response.content, "xml")
        elif "application/json" in response.headers["Content-Type"] or "application/vnd.api+json" in response.headers["Content-Type"]:
            soup = response.json()  # not actually soup
        else:
            raise Exception(f"unrecognized content type {response.headers['Content-Type']} for {source['name']}")

        return soup


    def feed(self, source):
        soup = self.fetch_source(source)
        if not soup:
            return []

        posts: list[Message] = funcs[source["name"]](soup)
        posts.reverse()  # reversed so earlier posts are read and sent first if there are multiple
        
        # remove any already-seen posts
        posts = [post for post in posts if post.id not in source["saved_ids"]]
        
        # save id to seen ids (these loops are separated so posts with the same id can be both posted if they were made in the same update)
        for post in posts:
            post.ready_images()
            if post.id not in source["saved_ids"]:
                source["saved_ids"].append(post.id)

        return posts


    async def check(self, source):
        if self.bot.is_nougat:
            channel_id: int = source["channel"]
        else:
            channel_id: int = TEST_CHANNEL
        channel = self.bot.get_channel(channel_id)

        if channel_id in TAVERN_CHANNEL_TARGETS.keys():
            tavern_channel = self.bot.get_channel(TAVERN_CHANNEL_TARGETS[channel_id])
        else:
            tavern_channel = channel  # shouldnt ever matter but this works until i rewrite it

        if not isinstance(channel, discord.TextChannel):
            raise Exception("could not retrieve feed channel")
        if not isinstance(tavern_channel, discord.TextChannel):
            raise Exception("could not retrieve tavern feed channel")

        # get all the messages to send
        messages: list[Message] = self.feed(source)
        if (len(messages) > 5 and source["name"] != "ask") or len(messages) > 15:  # prevent spam pings if a bug happens that makes it detect 5+ new messages from one source at once
            await self.bot.report("too many messages to send")

        for message in messages:
            if len(message.attachments) > 10:
                raise ValueError("cannot send more than 10 attachments at once")

            content = message.get_content(self.bot.is_nougat)

            m: discord.Message
            if message.nsfw:
                m = await tavern_channel.send(content, embed=message.get_embed())  # type: ignore
            else:
                m = await channel.send(content, embed=message.get_embed())  # type: ignore

            if self.bot.is_nougat and channel.is_news():
                await m.publish()

            if len(message.attachments) > 0:
                m = await channel.send(files=message.attachments)
                if self.bot.is_nougat and channel.is_news():
                    await m.publish()
        
        # save new stuff
        json.dump(SOURCES, open("feed_data.json", "w"), indent=4)


async def setup(bot):
    await bot.add_cog(NamiFeeds(bot))
