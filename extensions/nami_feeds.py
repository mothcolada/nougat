# fmt: off
import asyncio
import datetime
import hashlib
import html
import io
import json
from urllib.parse import urljoin

import discord
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from discord.ext import commands, tasks

# good lord this file is messy

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
            if 'tags' in child['class']:
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


    return {'text': text, 'images': images}



def parse_announcements(new_file):
    # posts = BeautifulSoup(new_file, 'html.parser').find('article', {'id': 'announcement'})
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


def parse_newsfeed(new_file):
    # new_news = BeautifulSoup(new_file, 'html.parser').find('article', {'id': 'newsfeed'}).find_all('li')
    # news_to_post = difference(new_news, old_news)

    # messages = []
    # for news in news_to_post:
    #     embed = discord.Embed(color       = 0x8E8D98,
    #                           url         = 'https://nomnomnami.com/',
    #                           description = paragraph(news))
    #     embed.set_footer(     text        = 'newsfeed')

    #     messages.append(({'embed': embed, 'images': []}))

    # return messages
    pass


def parse_posts(new_file):
    posts = BeautifulSoup(new_file, 'html.parser').find_all('article')

    messages = []
    for post in posts:
        footer = 'posts'
        if post.find('section', {'class': 'tags'}) != None:
            post.find('section', {'class': 'tags'})
            tags = [c.string for c in post.find('section', {'class': 'tags'}).children if isinstance(c, Tag)]
            if len(tags) > 0:
                footer += '  •  ' + '  '.join(tags)

        messages.append({'description': html_to_discord(post)['text'],
                         'images': html_to_discord(post)['images'],
                         'author': '@nomnomnami',
                         'url': 'https://nomnomnami.com/posts',
                         'footer': footer,
                         'timestamp': datetime.datetime.strptime(post.find('time').string + '-0700', '%m/%d/%Y, %I:%M%p%z'),
                         'id': int(datetime.datetime.strptime(post.find('time').string + '-0700', '%m/%d/%Y, %I:%M%p%z').timestamp())})  # should be fine as long as two posts don't have the same timestamp in separate page updates

    return messages


def parse_blog(new_file):
    posts = BeautifulSoup(new_file, 'xml').find_all('entry')

    messages = []
    for post in posts:
        content = BeautifulSoup(post.find('content').string, 'html.parser').find('div', {'class': 'trix-content'})

        url = post.find('link')['href']
        messages.append({'description': (paragraph(content.find('p')) + f'\n### [READ MORE]({url})'),
                         'title': post.find('title').string,
                         'url': url,
                         'timestamp': datetime.datetime.strptime(post.find('published').string, '%Y-%m-%dT%XZ'),
                         'footer': 'blog',
                         'id': int(post.find('id').text.split('/')[-1])})
    return messages


def parse_ask(new_file):
    posts = BeautifulSoup(new_file, 'html.parser').find_all('article')

    messages = []
    for post in posts:
        bubbles = post.find_all('div', {'class': 'bubble'})
        plain = ''.join([bubble.text.strip() for bubble in bubbles])
        id = hashlib.sha1(bytes(plain, 'utf-8')).hexdigest()

        footer = 'ask'
        if post.find('ul', {'class': 'tags'}) != None:
            post.find('ul', {'class': 'tags'})
            tags = [c.string for c in post.find('ul', {'class': 'tags'}).children if isinstance(c, Tag)]
            if len(tags) > 0:
                footer += '  •  ' + '  '.join(tags)
        description = html_to_discord(post)['text']

        messages.append({'description': description,
                         'url': 'https://nomnomnami.com/ask/latest',
                         'footer': footer,
                         'id': id,
                         'images': [image for image in html_to_discord(post)['images']]})
    return messages


def parse_status_cafe(new_file):
    posts = BeautifulSoup(new_file, 'xml').find_all('entry')

    messages = []
    for post in posts:
        messages.append({'description': clean(post.find('content').string),
                         'url': post.find('link')['href'],
                         'timestamp': datetime.datetime.strptime(post.find('published').string, '%Y-%m-%dT%X%z'),
                         'author': ' '.join(post.find('title').string.split(' ')[:2]),
                         'footer': 'status.cafe',
                         'id': int(post.find('id').text.split('/')[-1])})
    return messages


def parse_trick(new_file):
    posts = BeautifulSoup(new_file, 'xml').find_all('entry')

    # make messages
    messages = []
    for post in posts:
        content = BeautifulSoup(post.find('content').string, 'html.parser').find('div', {'class': 'trix-content'})

        messages.append({'description': html_to_discord(content)['text'],
                         'title': post.find('title').string,
                         'url': post.find('link')['href'],
                         'timestamp': datetime.datetime.strptime(post.find('published').string, '%Y-%m-%dT%XZ'),
                         'author': 'trick',
                         'footer': 'Letters from Trick',
                         'images': content.find_all('img'),
                         'id': int(post.find('id').text.split('/')[-1])})
    return messages


def parse_neocities(new_file):
    # new_updates = BeautifulSoup(new_file, 'html.parser').find_all('div', {'class': 'news-item update'})

    # # find updates added since last time
    # old_hrefs = list(update.find('a', {'class': 'local-date-title'})['href'] for update in old_updates)  # get hrefs of each update
    # updates_to_post = []
    # for update in new_updates:
    #     href = update.find('a', {'class': 'local-date-title'})['href']  # basically just compare updates by event id
    #     if href not in old_hrefs:
    #         updates_to_post.append(update)

    # messages = []
    # for update in updates_to_post:
    #     desc = ''
    #     for file in update.find_all('div', {'class': 'file'}):
    #         desc += '[' + file.find('span').text.strip() + '](' + file.find('a')['href'] + ')\n'  # add line with link for each file

    #     embed = discord.Embed(color       = 0xE93250,  # update color (comment color is 0xDAEEA5 if i feel like adding that ig)
    #                           title       = update.find('div', {'class': 'text'}).text,
    #                           description = desc,
    #                           timestamp   = datetime.datetime.fromtimestamp(int(update.find('a', {'class': 'local-date-title'})['data-timestamp'])))
    #     embed.set_thumbnail(  url         = 'https://neocities.org' + update.find('img')['src'])  # first image (should be first file)
    #     embed.set_footer(     text        = 'Neocities')
    #     messages.append({'embed': embed})

    # return messages  # reversed to return in order of upload if there are several new updates
    pass


def parse_pillowfort(new_file):
    pass
    # # not this: posts = BeautifulSoup(new_file, 'xml').find_all('item')

    # print(str(BeautifulSoup(new_file, 'html.parser'))[:20000])

    # messages = []
    # for post in posts:
    #     # print(post)
    #     # print(post.find('div', {'class': 'avatar'}).find('img'))
    #     # print(post.find('a', {'title': 'link to post'})) # ['href'].split('/')[-1]
    #     messages.append({'id': post.find({'title': 'link to post'})['href'].split('/')[-1],
    #                      'author_icon': post.find('div', {'class': 'avatar'}).find('img')['src']})

    # return messages


def parse_apoc(new_file):
    saved_ids = json.load(open('feed_data.json', 'r'))['apoc']['saved_ids']
    # we want to check id early to avoid checking every single recent comic
    posts = BeautifulSoup(new_file, 'xml').find_all('item')
    messages = []
    for post in posts:
        soup = BeautifulSoup(requests.get(post.find('link').text).content, 'html.parser')
        id = int(post.find('link').text.split('/')[-2])
        if id not in saved_ids:
            num = int(soup.find('h2', {'class': 'comictitle'}).text.split('#')[1].split(' ')[0])
            authornotes = soup.find('div', {'class': 'authornotes'})
            desc = '' if authornotes == None else authornotes.find('div', {'class': 'notecontent'}).text
            messages.append({'id': id,
                            'title': post.find('title').text,
                            'url': f'https://another-piece-of-candy.thecomicseries.com/comics/{num}/',
                            'description': desc,
                            'images': [BeautifulSoup(post.find('description').text, 'html.parser').find('img')],
                            'footer': 'another piece of candy'})
    return messages


funcs = {
    'announcements':    parse_announcements,
    'newsfeed':         parse_newsfeed,
    'posts':            parse_posts,
    'timber':           parse_posts,
    'blog':             parse_blog,
    'ask':              parse_ask,
    'status_cafe':      parse_status_cafe,
    'neocities':        parse_neocities,
    'trick':            parse_trick,
    'pillowfort':       parse_pillowfort,
    'apoc':             parse_apoc
}


def feed(source):
    # ask internet pretty please give me the thing i want
    response = requests.get(source['link']) # , headers={'If-Modified-Since': source['last_modified']})
    if 'Content-Type' in response.headers and 'application/atom+xml' in response.headers['Content-Type']:  # rss feed
        pass #response = requests.get(source['link'], headers={'If-Modified-Since': source['last_modified']})
    else:
        if response.status_code == 304:  # not modified since
            return []
        if 'last_modified' in response.headers.keys():
            source['last_modified'] = response.headers['Last-Modified']  # update last modified time

    # response errors will be caught in main.py

    # call parse function for the source type
    posts = list(reversed(funcs[source['name']](response.content)))  # reversed so earlier posts are read and sent first if there are multiple
    # remove any already-seen posts
    posts = [post for post in posts if post['id'] not in source['saved_ids']]
    # save id to seen ids (these loops are separated so posts with the same id can be both posted if they were made in the same update)
    for post in posts:
        if post['id'] not in source['saved_ids']:
            source['saved_ids'].append(post['id'])

    messages = []
    for post in posts:
        # limit description to 4000 chars
        if len(post['description']) > 4000:
            # do my best to spoiler anything that should be spoilered (could have false positives but that's fine)
            emergency_spoil = ('||' in post['description'][:4000] and '||' in post['description'][3999:])
            post['description'] = post['description'][:4000]
            if emergency_spoil:
                post['description'] += '||'
            post['description'] += '\n## [READ MORE](' + post['url'] + ')'

        # EMBED
        embed = discord.Embed(color       = source['embed']['color']       if 'color'       in source['embed'].keys() else None,
                              description = post['description'],           # description is mandatory
                              title       = post['title']                  if 'title'       in post.keys()            else None,
                              url         = post['url']                    if 'url'         in post.keys()            else None,
                              timestamp   = post['timestamp']              if 'timestamp'   in post.keys()            else None)
        if 'author' in post.keys():
            embed.set_author( name        = post['author'],
                              url         = source['embed']['author_url']  if 'author_url'  in source['embed'].keys() else None,
                              icon_url    = source['embed']['author_icon'] if 'author_icon' in source['embed'].keys() else None)
        embed.set_footer(     text        = post['footer'])                # footer is mandatory


        images = []
        if 'images' in post.keys():
            if len(post['images']) == 1 and (post['images'][0].parent.name != 'details'):
                embed.set_image(url=urljoin('https://nomnomnami.com', post['images'][0]['src']))
            else:
                for img in post['images']:
                    response = requests.get(urljoin('https://nomnomnami.com', img['src']))
                    filename = img['src'].split('/')[-1] + ('.png' if source['name'] == 'trick' else '')  # trick pika page exception
                    discord_file = discord.File(io.BytesIO(response.content),
                                                filename = filename,
                                                spoiler  = (img.parent.name == 'details'))  # spoiler if part of details (for posts)
                    images.append(discord_file)

        messages.append({'content': f'-# <@&{source["role"]}>', 'embed': embed, 'images': images})

    return messages


sources = json.load(open('feed_data.json', 'r'))

class NamiFeeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feeds.start()

    def cog_unload(self):
        self.feeds.cancel()

    @tasks.loop(seconds=10.0)
    async def feeds(self):
        sources = json.load(open('feed_data.json', 'r'))

        for s in sources:
            if s in ['ask']: # ['apoc', 'blog', 'posts', 'status_cafe', 'ask', 'trick']:
                source = sources[s]
                await self.check(source)

                # save new stuff
                json.dump(sources, open('feed_data.json', 'w'), indent=4)

                await asyncio.sleep(0.5)  # avoid heartbeat blocking
        # except Exception as e:
        #     await self.bot.report(e)


    async def check(self, source):
        if self.bot.is_nougat:  # in namiverse use namiverse channels
            channel = self.bot.get_channel(source['channel'])
        else:  # personal test bot
            channel = self.bot.get_channel(TEST_CHANNEL)

        if channel == None:
            return

        # get all the messages to send
        messages = feed(source)
        if (len(messages) > 5 and source['name'] != 'ask') or len(messages) > 100:  # prevent spam pings if a bug happens that makes it detect 5+ new messages from one source at once
            raise Exception('too many messages to send')

        for message in messages:
            await channel.send(message['content'], embed=message['embed'])
            if 'images' in message.keys() and len(message['images']) >= 1:  # i'll (situationally) put images in the embed later
                await channel.send(files=message['images'])


async def setup(bot):
    await bot.add_cog(NamiFeeds(bot))
