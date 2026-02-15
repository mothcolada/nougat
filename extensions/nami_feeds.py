# fmt: off
import asyncio
import datetime
import hashlib
import html
import io
import json
import lxml  # do not remove
from urllib.parse import urljoin

import discord
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from discord.ext import commands, tasks

# good lord this file is messy
# TODO: announcements, newsfeed, neocities, youtube, pillowfort

GMT = datetime.timezone(datetime.timedelta(0), 'GMT')

TEST_CHANNEL = 1074754885070897202

icons = {
    'none': '<:icon_none:1454889234853793842>',
    'eggbug': '<:icon_eggbug:1425576567945564272>',
    'anon': '<:icon_anon:1425576581815992320>',
    'treat': '<:icon_treat:1425576593018978385>',
    'mochi': '<:icon_mochi:1425576604062449755>',
    'moxie': '<:icon_moxie:1425576614535888986>',
    'trick': '<:icon_trick:1425576626821005372>',
    'syrup': '<:icon_syrup:1425576638657200148>',
    'pastille': '<:icon_pastille:1425576649407332474>',
    'gumdrop': '<:icon_gumdrop:1425576660165595167>',
    'butterscotch': '<:icon_butterscotch:1425576670538104874>',
    'toffee': '<:icon_toffee:1425576681208287325>',
    'periwinkle': '<:icon_periwinkle:1425576690868031599>',
    'baezel': '<:icon_baezel:1425576703291428977>',
    'poffin': '<:icon_poffin:1425576711764054249>',
    'thyme': '<:icon_thyme:1425576724392972328>',
    'spice': '<:icon_spice:1425576732970324090>',
    'nil': '<:icon_nil:1425576745201041459>',
    'kamilla': '<:icon_kamilla:1425576755930071195>',
    'eleni': '<:icon_eleni:1425576767543971931>',
    'qmin': '<:icon_qmin:1425576779745202278>',
    'cassia': '<:icon_cassia:1425576791950495876>',
    'astra': '<:icon_astra:1425576802218410125>',
    'vinegar': '<:icon_vinegar:1425576819385569360>',
    'salt': '<:icon_salt:1443398214203080715>',
    'pepper': '<:icon_pepper:1443398245991583775>',
    'timber': '<:icon_timber:1443398285225099364>',
    'twigs': '<:icon_twigs:1443398319853408399>',
    'senbei': '<:icon_senbei:1443398342326489238>',
    'manjuu': '<:icon_manjuu:1449580945740009482>',
    'oz': '<:icon_oz:1449615964873167029>',
    'chai': '<:icon_chai:1449580999955714120>',
    'dango': '<:icon_dango:1449580975234355361>',
    'phoenix': '<:icon_phoenix:1450670773009252533>',
    'tundra': '<:icon_tundra:1450670774783578173>',
    'drop': '<:icon_drop:1450670771704827924>',
    'fennel': '<:icon_fennel:1464368764731527335>'
}
emoji = {
    'eggbug': '<:eggbug:1444074342576033793>',
    'eggbug_asleep': '<:eggbug_asleep:1444074343951765686>',
    'eggbug_devious': '<:eggbug_devious:1444074344845283390>',
    'eggbug_heart_sob': '<:eggbug_heart_sob:1444074346296512592>',
    'eggbug_nervous': '<:eggbug_nervous:1444074347986944132>',
    'eggbug_pensive': '<:eggbug_pensive:1444074348473221152>',
    'eggbug_pleading': '<:eggbug_pleading:1444074350050283550>',
    'eggbug_relieved': '<:eggbug_relieved:1444074351011037265>',
    'eggbug_shocked': '<:eggbug_shocked:1444074351853965444>',
    'eggbug_smile_hearts': '<:eggbug_smile_hearts:1444074353208852710>',
    'eggbug_sob': '<:eggbug_sob:1444074354487984181>',
    'eggbug_tuesday': '<:eggbug_tuesday:1444074356060848168>',
    'eggbug_uwu': '<:eggbug_uwu:1444074356878606396>',
    'eggbug_wink': '<:eggbug_wink:1444074357914599537>'
}

SOURCES = json.load(open('feed_data.json', 'r'))


# later ill use these maybe

class ImageAttachment():
    def __init__(self, file_bytes, name: str, spoiler=False):
        self.file_bytes = file_bytes
        self.name = name
        self.spoiler = spoiler


class Message():
    def __init__(
        self,
        source: str,
        id: (int | str),
        description: str,
        title: (str | None) = None,
        url: (str | None) = None,
        author: (str | None) = None,
        author_icon: (str | None) = None,
        images = [],
        timestamp: (str | None) = None,
    ):
        self.source      = SOURCES[source]
        self.id          = id
        self.description = description
        self.title       = title
        self.url         = url    or self.source['embed']['url']
        self.author      = author or self.source['embed']['author']
        self.author_url  = self.source['embed']['author_url']
        self.author_icon = author_icon or self.source['embed']['author_icon']
        self.footer      = self.source['embed']['footer']
        self.color       = self.source['embed']['color']

        self.image = None
        self.attachments = []            
        if len(images) == 1 and (images[0].parent.name != 'details'):  # one unspoilered image
            self.image = url=urljoin('https://nomnomnami.com', images[0]['src'])
        else:
            for img in images:
                response = requests.get(urljoin('https://nomnomnami.com', img['src']))
                filename = img['src'].split('/')[-1]
                if source == 'trick':  # exception for trick pika page
                    filename += '.png'
                discord_file = discord.File(io.BytesIO(response.content),
                                            filename = filename,
                                            spoiler  = (img.parent.name == 'details'))  # spoiler if part of details (for posts)
                self.attachments.append(discord_file)

        self.timestamp = None
        if timestamp:
            self.timestamp = datetime.datetime.strptime(timestamp, self.source['embed']['timestamp_format'])

        if len(self.description) > 4000:
            # do my best to spoiler anything that should be spoilered (could have false positives but that's fine)
            self.description = self.description[:4000]
            if ('||' in self.description[:4000] and '||' in self.description[3999:]):
                self.description += '||'
            self.description += '\n## [READ MORE](' + self.url + ')'

    
    def role_ping(self):
        return f"-# <@&{self.source['role']}>"


    def get_embed(self) -> discord.Embed:
        embed = discord.Embed(color       = self.color,
                              description = self.description,
                              title       = self.title,
                              url         = self.url,
                              timestamp   = self.timestamp)
        if self.image:
            embed.set_image(  url         = self.image)
        if self.author:
            embed.set_author( name        = self.author,
                              url         = self.author_url,
                              icon_url    = self.author_icon)
        embed.set_footer(     text        = self.footer)                # footer is mandatory
        return embed


    # messages = []
    # for post in posts:
    #     # limit description to 4000 chars
        if len(self.description) > 4000:
            # do my best to spoiler anything that should be spoilered (could have false positives but that's fine)
            emergency_spoil = ('||' in self.description[:4000] and '||' in self.description[3999:])
            self.description = self.description[:4000]
            if emergency_spoil:
                self.description += '||'
            self.description += '\n## [READ MORE](' + post['url'] + ')'






def clean(string):
    return html.unescape(string).replace('*', '\\*')


def paragraph(p):
    text = ''
    for c in p.children:
        if isinstance(c, NavigableString):
            c: NavigableString = c
            text += clean(c)
        elif isinstance(c, Tag):
            if c.name == 'a':
                text += '[' + clean(c.string) + '](' + urljoin('https://nomnomnami.com', c['href']) +  ')'
            elif c.name == 'br':
                text += '\n'
            elif c.name == 'strong' or c.name == 'b':
                text += '**' + clean(c.string) + '**'
            elif c.name == 'em':
                text += '*' + clean(c.string) + '*'
            elif c.name == 'code':
                text += '`' + clean(c.string) + '`'
            elif c.name == 'small':
                text += clean(c.string)
            elif c.name == 'span':
                text += clean(c.string)

    return text.strip()


def html_to_discord(html: BeautifulSoup):
    text = ''
    images = []
    for child in html.children:
        if child.name == 'p':
            text += '\n\n' + paragraph(child)
            for grandchild in child.descendants:
                if grandchild.name == 'img':
                    if '/ask/images/emoji/' in grandchild['src']:
                        text += ' ' + emoji[grandchild['src'].split('/')[-1].split('.')[0]] + ' '
                    else:
                        images.append(grandchild)
        elif child.name == 'h3':
            text += '\n### ' + paragraph(child)
        elif child.name == 'small':
            text += '\n\n-# ' + paragraph(child)
        elif child.name == 'ul':
            if 'class' in child.attrs and 'tags' in child['class']:
                pass
            else:
                for grandchild in child.descendants:
                    if grandchild.name == 'li':
                        text += '\n- ' + paragraph(grandchild)
        elif child.name == 'ol':
            for grandchild in child.descendants:
                n = 1
                if grandchild.name == 'li':
                    text += '\n' + str(n) + '. ' + paragraph(grandchild)
                    n += 1
        elif child.name == 'details':
            text += '\n\n' + paragraph(child.find('summary'))
            text += '\n||' + html_to_discord(child)['text'].strip() + '||'
            images = images + html_to_discord(child)['images']
        elif child.name == 'img':
            images.append(child)
        elif child.name == 'div':
            if 'class' not in child.attrs:
                text += html_to_discord(child)['text']
                images = images + html_to_discord(child)['images']
            elif 'bubble' in child['class']:
                text += '\n> '+html_to_discord(child)['text'].replace('\n', '\n> ')
            elif 'response' in child['class']:
                text += html_to_discord(child)['text']
                images = images + html_to_discord(child)['images']
            elif 'asker' in child['class']:
                text += '### ' + html_to_discord(child)['text'] + ' ' + child.text.strip()
            elif 'icon' in child['class']:
                if child['class'][1] in icons.keys():
                    text += icons[child['class'][1]]  # TODO: actually test this
                else:
                    text += icons['none']
            elif 'ask' in child['class']:
                text += html_to_discord(child)['text']
            elif 'youtube-embed' in child['class']:
                text += '\n' + child.find('iframe')['src']
        # elif child.name == 'span':
        #     text += child.text.strip()


    return {'text': text, 'images': images}


# def format_datetime(input, source):
#     if source == 'posts':
#         return datetime.datetime.strptime(input, '%m/%d/%Y, %I:%M%p%z')
#     elif source in ['blog', 'trick']:
#         return datetime.datetime.strptime(input, '%Y-%m-%dT%XZ')
#     elif source == 'status.cafe':
#         return datetime.datetime.strptime(input, '%Y-%m-%dT%X%z')
#     else:
#         return


def parse_announcements(soup):
    posts = soup.find('div', {'class': 'news-banner'})
    
    # messages = []
    # if old_announcement != new_announcement:
    #     embed = discord.Embed(color       = 0xE4E4EC,
    #                           title       = paragraph(new_announcement.find('h3')),
    #                           url         = new_announcement.find('a')['href'],
    #                           description = paragraph(new_announcement.find('p')))
    #     embed.set_image(      url         = urljoin('https://nomnomnami.com/', new_announcement.find('img')['src']))
    #     embed.set_footer(     text        = 'announcements')
    #     messages.append(({'embed': embed, 'images': []}))

    # return messages
    pass


def parse_newsfeed(soup):
    posts = soup.find('article', {'id': 'newsfeed'}).find_all('li')

    messages = []
    for post in posts:
        message = Message('newsfeed',
                          id = post.find('time').string,
                          description = paragraph(post))
        messages.append(message)

    return messages


def parse_posts(soup):
    posts = soup.find_all('article')

    messages = []
    for post in posts:
        footer = 'posts'
        if post.find('section', {'class': 'tags'}) != None:
            post.find('section', {'class': 'tags'})
            tags = [c.string for c in post.find('section', {'class': 'tags'}).children if isinstance(c, Tag)]
            if len(tags) > 0:
                footer += '  •  ' + '  '.join(tags)

        message = Message('posts',
                          id = post.find('time').string,  # should be fine as long as two posts don't have the same timestamp in separate page updates
                          description = html_to_discord(post)['text'],
                          images = html_to_discord(post)['images'],
                          timestamp = post.find('time').string + '-0700')  # mountain time. im pretending daylight savings isnt real
        messages.append(message)

    return messages


def parse_blog(soup):
    posts = soup.find_all('entry')

    messages = []
    for post in posts:
        content = BeautifulSoup(post.find('content').string, 'html.parser').find('div', {'class': 'trix-content'})

        url = post.find('link')['href']
        message = Message('blog',
                          id = post.find('id').string,
                          description = (paragraph(content.find('p')) + f'\n### [READ MORE]({url})'),
                          title = post.find('title').string,
                          url = url,
                          timestamp = post.find('published').string)
        messages.append(message)

    return messages


def parse_ask(soup):
    posts = soup.find_all('article')

    messages = []
    for post in posts:
        bubbles = post.find_all('div', {'class': 'bubble'})
        plain = ''.join([bubble.text.strip() for bubble in bubbles])

        if post.find('ul', {'class': 'tags'}) != None:
            post.find('ul', {'class': 'tags'})
            tags = [c.string for c in post.find('ul', {'class': 'tags'}).children if isinstance(c, Tag)]
            if len(tags) > 0:
                tags = '  •  ' + '  '.join(tags)

        message = Message('ask',
                          id = hashlib.sha1(bytes(plain, 'utf-8')).hexdigest(),
                          description = html_to_discord(post)['text'],
                          images = [image for image in html_to_discord(post)['images']])
        messages.append(message)

    return messages


def parse_status_cafe(soup):
    posts = soup.find_all('entry')

    messages = []
    for post in posts:
        message = Message('status_cafe',
                          id = post.find('id').string,
                          description = clean(post.find('content').string),
                          url = post.find('link')['href'],
                          timestamp = post.find('published').string,
                          author = ' '.join(post.find('title').string.split(' ')[:2]),
                          author_icon = soup.find('icon').string)
        messages.append(message)

    return messages


def parse_trick(soup):
    posts = soup.find_all('entry')

    # make messages
    messages = []
    for post in posts:
        content = BeautifulSoup(post.find('content').string, 'html.parser').find('div', {'class': 'trix-content'})

        message = Message('trick',
                          id = post.find('id').string,
                          description = html_to_discord(content)['text'],
                          title = post.find('title').string,
                          url = post.find('link')['href'],
                          images = content.find_all('img'),
                          timestamp = post.find('published').string)
        messages.append(message)

    return messages


def parse_neocities(soup):
#     posts = BeautifulSoup(soup, 'lxml').find_all('item')

#     messages = []
#     for post in posts:
#         desc = ''
#         for file in post.find_all('div', {'class': 'file'}):
#             desc += '[' + file.find('span').text.strip() + '](' + file.find('a')['href'] + ')\n'  # add line with link for each file

#         messages.append({'title': post.find('div', {'class': 'text'}).text,
#                          'description': desc,
#                          'timestamp': datetime.datetime.fromtimestamp(int(post.find('a', {'class': 'local-date-title'})['data-timestamp'])),
#                          'url': 'https://neocities.org' + post.find('img')['src'],  # first image (should be first file)
#                          'footer': 'Neocities',
#                          'id': })

#     return messages
    pass


def parse_pillowfort(soup):
    pass
    # # not this: posts = soup.find_all('item')

    # print(str(soup)[:20000])

    # messages = []
    # for post in posts:
    #     # print(post)
    #     # print(post.find('div', {'class': 'avatar'}).find('img'))
    #     # print(post.find('a', {'title': 'link to post'})) # ['href'].split('/')[-1]
    #     messages.append({'id': post.find({'title': 'link to post'})['href'].split('/')[-1],
    #                      'author_icon': post.find('div', {'class': 'avatar'}).find('img')['src']})

    # return messages


def parse_apoc(soup):
    saved_ids = json.load(open('feed_data.json', 'r'))['apoc']['saved_ids']
    # we want to check id early to avoid checking every single recent comic
    posts = soup.find_all('item')
    messages = []
    for post in posts:
        id = int(post.find('link').text.split('/')[-2])
        if id not in saved_ids:
            soup = BeautifulSoup(requests.get(post.find('link').text).content, 'html.parser')

            num = int(soup.find('h2', {'class': 'comictitle'}).text.split('#')[1].split(' ')[0])
            authornotes = soup.find('div', {'class': 'authornotes'})
            desc = '' if authornotes == None else authornotes.find('div', {'class': 'notecontent'}).text

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
    saved_ids = json.load(open('feed_data.json', 'r'))['tcs']['saved_ids']
    # we want to check id early to avoid checking every single recent comic
    posts = soup.find_all('item')
    messages = []
    for post in posts:
        id = int(post.find('link').text.split('/')[-2])
        if id not in saved_ids:
            soup = BeautifulSoup(requests.get(post.find('link').text).content, 'html.parser')
            
            num = int(soup.find('h2', {'class': 'comictitle'}).text.split('#')[1].split(' ')[0])
            authornotes = soup.find('div', {'class': 'authornotes'})
            desc = '' if authornotes == None else authornotes.find('div', {'class': 'notecontent'}).text

            message = Message('tcs',
                              id = id,
                              description = desc,
                              title = post.find('title').text,
                              url = f'https://another-piece-of-candy.thecomicseries.com/comics/{num}/',
                              images = [BeautifulSoup(post.find('description').text, 'html.parser').find('img')],
                              timestamp = post.find('pubDate').text)
            messages.append(message)

    return messages


def parse_youtube(soup):
    pass



funcs = {
    # 'announcements':    parse_announcements,
    'newsfeed':         parse_newsfeed,
    'posts':            parse_posts,
    'timber':           parse_posts,
    'blog':             parse_blog,
    'ask':              parse_ask,
    'status_cafe':      parse_status_cafe,
    # 'neocities':        parse_neocities,
    'trick':            parse_trick,
    'apoc':             parse_apoc,
    # 'tcs':              parse_tcs,
    # 'youtube':          parse_youtube
    # 'pillowfort':       parse_pillowfort,
}


def feed(source):
    last_modified = datetime.datetime.fromtimestamp(source['last_modified'], GMT)
    last_modified_string = last_modified.strftime('%a, %d %b %Y %X %Z')
    response = requests.get(source['link'], headers={'If-Modified-Since': last_modified_string})

    if response.status_code == 304:  # not modified since (FIXME: this seems to not actually ever happen?)
        return []
    elif 'Last-Modified' in response.headers.keys():
        source['last_modified'] = int(datetime.datetime.strptime(response.headers['Last-Modified'], '%a, %d %b %Y %X %Z').timestamp())  # update last modified time

    # call parse function for the source type
    if 'text/html' in response.headers['Content-Type']:
        soup = BeautifulSoup(response.content, 'html.parser')
    elif 'application/atom+xml' in response.headers['Content-Type'] or 'application/xml' in response.headers['Content-Type']:
        soup = BeautifulSoup(response.content, 'xml')
    else:
        raise Exception(f'unrecognized content type {response.headers["Content-Type"]}')

    posts: list = funcs[source['name']](soup)
    posts.reverse()  # reversed so earlier posts are read and sent first if there are multiple
    
    # remove any already-seen posts
    posts = [post for post in posts if post.id not in source['saved_ids']]
    
    # save id to seen ids (these loops are separated so posts with the same id can be both posted if they were made in the same update)
    for post in posts:
        if post.id not in source['saved_ids']:
            source['saved_ids'].append(post.id)

    return posts


class NamiFeeds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.feeds.start()

    def cog_unload(self):
        self.feeds.cancel()


    @tasks.loop(seconds=10.0)
    async def feeds(self):
        for s in SOURCES:
            if s in ['apoc', 'posts', 'newsfeed', 'ask', 'status_cafe', 'blog', 'trick']:
                if True:
                    source = SOURCES[s]
                    await self.check(source)

                    # save new stuff
                    json.dump(SOURCES, open('feed_data.json', 'w'), indent=4)
                # except Exception as e:
                #     await self.bot.report(e)

                await asyncio.sleep(0.5)  # avoid heartbeat blocking


    @feeds.before_loop
    async def before_feeds(self):
        await self.bot.wait_until_ready()


    async def check(self, source):
        if self.bot.is_nougat:  # in namiverse use namiverse channels
            channel = self.bot.get_channel(source['channel'])
        else:  # personal test bot
            channel = self.bot.get_channel(TEST_CHANNEL)

        if not channel:
            await self.bot.report('could not retrieve feed channel')

        # get all the messages to send
        messages: list[Message] = feed(source)
        # if (len(messages) > 5 and source['name'] != 'ask') or len(messages) > 10:  # prevent spam pings if a bug happens that makes it detect 5+ new messages from one source at once
        #     await self.bot.report('too many messages to send')

        for message in messages:
            if len(message.attachments) > 10:
                raise Exception('more than 10 files time to die')
            await channel.send(message.role_ping(), embed=message.get_embed())  # type: ignore -- channel is assumed to support send
            if len(message.attachments) > 0:
                await channel.send(files=message.attachments)  # type: ignore -- channel is assumed to support send


async def setup(bot):
    await bot.add_cog(NamiFeeds(bot))
