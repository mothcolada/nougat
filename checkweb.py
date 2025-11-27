import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import datetime
import discord
import lxml
import html
from urllib.parse import urljoin
import io
import hashlib


emoji = {
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

    return text.strip()


def html_to_discord(html: BeautifulSoup):
    text = ''
    images = []
    for child in html.children:
        if child.name == 'p':
            text += '\n\n' + paragraph(child)
            for grandchild in child.descendants:
                if grandchild.name == 'img':  # TODO: differentiate between normal imgs and eggbug emojis maybe
                    images.append(grandchild)
        elif child.name == 'h3':
            text += '\n### ' + paragraph(child)
        elif child.name == 'small':
            text += '\n\n-# ' + paragraph(child)
        elif child.name == 'ul':
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
                text += emoji[child['class'][1]]
            elif 'ask' in child['class']:
                text += html_to_discord(child)['text']


    return {'text': text, 'images': images}



def parse_announcements(new_file):
    posts = BeautifulSoup(new_file, 'html.parser').find('article', {'id': 'announcement'})
    messages = []
    if old_announcement != new_announcement:
        embed = discord.Embed(color       = 0xE4E4EC,
                              title       = paragraph(new_announcement.find('h3')),
                              url         = new_announcement.find('a')['href'],
                              description = paragraph(new_announcement.find('p')))
        embed.set_image(      url         = urljoin('https://nomnomnami.com/', new_announcement.find('img')['src']))
        embed.set_footer(     text        = 'announcements')
        messages.append(({'embed': embed, 'images': []}))
    
    return messages


def parse_newsfeed(new_file):
    new_news = BeautifulSoup(new_file, 'html.parser').find('article', {'id': 'newsfeed'}).find_all('li')
    news_to_post = difference(new_news, old_news)

    messages = []
    for news in news_to_post:
        embed = discord.Embed(color       = 0x8E8D98,
                              url         = 'https://nomnomnami.com/',
                              description = paragraph(news))
        embed.set_footer(     text        = 'newsfeed')

        messages.append(({'embed': embed, 'images': []}))

    return messages


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
    new_posts = new_file.decode('utf-8').split('const posts = [')[1].split('];')[0].split('{')[1:]
    posts_to_post = difference(new_posts, old_posts)
    
    messages = []
    for post in posts_to_post:
        title = post.split('"title": `')[1].split('`')[0]
        filename = post.split('"filename": `')[1].split('`')[0]
        tags = post.split('"tags": [`')[1].split('`]')[0].split('`, `')
        url = 'https://nomnomnami.com/blog/posts/' + filename + '.html'
        page = BeautifulSoup(requests.get(url).content, 'html.parser')

        embed = discord.Embed(title       = title,
                              url         = url,
                              description = paragraph(page.find('p')) + '\n### [READ MORE](' + url + ')')  # first paragraph
        embed.set_footer(     text        = 'blog  •  ' + '#' + '  #'.join(tags),)
        messages.append({'embed': embed})
    return messages  # reversed to return in order of upload if there are several new updates


def parse_ask(new_file):
    posts = BeautifulSoup(new_file, 'html.parser').find_all('article')

    messages = []
    for post in posts:
        bubbles = post.find_all('div', {'class': 'bubble'})
        plain = ''.join([bubble.text.strip() for bubble in bubbles])
        id = hashlib.sha1(bytes(plain, 'utf-8')).hexdigest()
        
        footer = 'ask'
        if post.find('section', {'class': 'tags'}) != None:
            post.find('section', {'class': 'tags'})
            tags = [c.string for c in post.find('section', {'class': 'tags'}).children if isinstance(c, Tag)]
            if len(tags) > 0:
                footer += '  •  ' + '  '.join(tags)

        messages.append({'description': html_to_discord(post)['text'],
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
    new_updates = BeautifulSoup(new_file, 'html.parser').find_all('div', {'class': 'news-item update'})
    
    # find updates added since last time
    old_hrefs = list(update.find('a', {'class': 'local-date-title'})['href'] for update in old_updates)  # get hrefs of each update
    updates_to_post = []
    for update in new_updates:
        href = update.find('a', {'class': 'local-date-title'})['href']  # basically just compare updates by event id
        if href not in old_hrefs:
            updates_to_post.append(update)

    messages = []
    for update in updates_to_post:
        desc = ''
        for file in update.find_all('div', {'class': 'file'}):
            desc += '[' + file.find('span').text.strip() + '](' + file.find('a')['href'] + ')\n'  # add line with link for each file
        
        embed = discord.Embed(color       = 0xE93250,  # update color (comment color is 0xDAEEA5 if i feel like adding that ig)
                              title       = update.find('div', {'class': 'text'}).text,
                              description = desc,
                              timestamp   = datetime.datetime.fromtimestamp(int(update.find('a', {'class': 'local-date-title'})['data-timestamp'])))
        embed.set_thumbnail(  url         = 'https://neocities.org' + update.find('img')['src'])  # first image (should be first file)
        embed.set_footer(     text        = 'Neocities')
        messages.append({'embed': embed})

    return messages  # reversed to return in order of upload if there are several new updates


def parse_pillowfort(new_file):
    posts = BeautifulSoup(new_file, 'html.parser').find_all('div', {'class': 'post-container'})

    messages = []
    for post in posts:
        messages.append({})

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
    'pillowfort':       parse_pillowfort
}


def check(source):
    # ask internet pretty please give me the thing i want
    response = requests.get(source['link']) # , headers={'If-Modified-Since': source['last_modified']})
    if 'Content-Type' in response.headers and 'application/atom+xml' in response.headers['Content-Type']:  # rss feed
        pass #response = requests.get(source['link'], headers={'If-Modified-Since': source['last_modified']})
    else:
        if response.status_code == 304:  # not modified since
            return []
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
            post['description'] = post['description'][:4000] + '\n### [READ MORE](' + post['url'] + ')'
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
            if len(post['images']) == 1 and post['images'][0].parent.name != 'details':
                embed.set_image(url=urljoin('https://nomnomnami.com', post['images'][0]['src']))
            else:
                for img in post['images']:
                    response = requests.get(urljoin('https://nomnomnami.com', img['src']))
                    filename = img['src'].split('/')[-1] + ('.png' if source['name'] == 'trick' else '')  # trick pika page exception
                    discord_file = discord.File(io.BytesIO(response.content),
                                                filename = filename,
                                                spoiler  = (img.parent.name == 'details'))  # spoiler if part of details (for posts)
                    images.append(discord_file)
            
        messages.append({'content': source['message'], 'embed': embed, 'images': images})
    
    return messages
