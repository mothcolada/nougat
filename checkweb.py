import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import datetime
import discord
import lxml
import html
from urllib.parse import urljoin
import io


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
    'vinegar': '<:icon_vinegar:1425576819385569360>'
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
            else:
                print('weird html thing: ' + c.name)
    return text.strip()


def html_to_discord(html: BeautifulSoup):
    text = ''
    images = []
    for child in html.children:
        if child.name == 'p':
            text += '\n\n' + paragraph(child)
        elif child.name == 'h3':
            text += '\n### ' + paragraph(child)
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
            text += '||' + html_to_discord(child)['text'] + '||'
            for image in html_to_discord(child)['images']:
                images.append(image)
        elif child.name == 'img':
            images.append(child)
        elif child.name == 'div':
            if 'bubble' in child['class']:
                text += '\n> '+html_to_discord(child)['text'].replace('\n', '\n> ')
            elif 'response' in child['class']:
                text += html_to_discord(child)['text']
            elif 'asker' in child['class']:
                text += '### ' + html_to_discord(child)['text'] + ' ' + child.text.strip()
            elif 'icon' in child['class']:
                text += emoji[child['class'][1]]
            elif 'ask' in child['class']:
                text += html_to_discord(child)['text']

    return {'text': text, 'images': images}



def parse_posts(old_file, new_file):
    old_soup = BeautifulSoup(old_file, 'html.parser')
    new_soup = BeautifulSoup(new_file, 'html.parser')
    old_posts = old_soup.find_all('article')
    new_posts = new_soup.find_all('article')
    posts_to_post = []
    for post in new_posts:
        if post not in old_posts:
            posts_to_post.append(post)

    messages = []
    for post in posts_to_post:
        tags = []
        if post.find('section', {'class': 'tags'}) != None:
            for c in post.find('section', {'class': 'tags'}).children:
                if isinstance(c, Tag):
                    tags.append(c.string)

        embed = discord.Embed(color       = 0xBDB7FF,
                              url         = 'https://nomnomnami.com/posts/',
                              description = html_to_discord(post)['text'],
                              timestamp   = datetime.datetime.strptime(post.find('time').string, '%m/%d/%Y, %I:%M%p'))
        embed.set_author(     name        = '@nomnomnami',
                              url         = 'https://nomnomnami.com/posts/',
                              icon_url    = 'https://nomnomnami.com/images/icon_nami2.png'),
        if len(tags) == 0:
            embed.set_footer( text        = 'posts')
        else:
            embed.set_footer( text        = 'posts  •  ' + '  '.join(tags))

        images = []
        for image in html_to_discord(post)['images']:
            # file = discord.File()
            images.append(image)

        messages.append(({'embed': embed, 'images': images}))

    return messages  # tuple woa


def parse_blog(old_file, new_file):
    old_posts = old_file.decode('utf-8').split('const posts = [')[1].split('];')[0].split('{')[1:]
    new_posts = new_file.decode('utf-8').split('const posts = [')[1].split('];')[0].split('{')[1:]
    posts_to_post = []  # find posts added since last time
    for post in new_posts:
        if post not in old_posts:
            posts_to_post.append(post)
    
    messages = []
    for post in posts_to_post:
        title = post.split('"title": `')[1].split('`')[0]
        filename = post.split('"filename": `')[1].split('`')[0]
        tags = post.split('"tags": [`')[1].split('`]')[0].split('`, `')
        url = 'https://nomnomnami.com/blog/posts/' + filename + '.html'
        page = BeautifulSoup(requests.get(url).content, 'html.parser')

        embed = discord.Embed(color       = 0x69DBFF,
                              title       = title,
                              url         = url,
                              description = paragraph(page.find('p')) + '\n### [READ MORE](' + url + ')')  # first paragraph
        embed.set_footer(     text        = 'blog  •  ' + '#' + '  #'.join(tags),)
        messages.append({'embed': embed})
    return messages  # reversed to return in order of upload if there are several new updates


def parse_ask(old_file, new_file):
    old_soup = BeautifulSoup(old_file, 'html.parser')
    new_soup = BeautifulSoup(new_file, 'html.parser')
    old_asks = old_soup.find_all('article')
    new_asks = new_soup.find_all('article')
    asks_to_post = []
    for ask in new_asks:
        if ask not in old_asks:
            asks_to_post.append(ask)

    messages = []
    for ask in asks_to_post:
        tags = []
        for c in ask.find('section', {'class': 'tags'}).children:
            if isinstance(c, Tag):
                tags.append(c.string)

        embed = discord.Embed(color       = 0xFFD8A8,
                              url         = 'https://nomnomnami.com/ask/latest',
                              description = html_to_discord(ask)['text'],)
        if len(tags) == 0:
            embed.set_footer( text        = 'ask')
        else:
            embed.set_footer( text        = 'ask  •  ' + '  '.join(tags))

        images = []
        for image in html_to_discord(ask)['images']:
            # file = discord.File()
            images.append(image)

        messages.append(({'embed': embed, 'images': images}))

    return messages  # tuple woa


def parse_status_cafe(old_file, new_file):
    old_soup = BeautifulSoup(old_file, 'xml')
    new_soup = BeautifulSoup(new_file, 'xml')               
    old_entries = old_soup.find_all('entry')
    new_entries = new_soup.find_all('entry')
    
    entries_to_post = []  # find entries added since last time
    for entry in new_entries:
        if entry not in old_entries:
            entries_to_post.append(entry)

    # make messages
    messages = []
    for entry in entries_to_post:
        embed = discord.Embed(description = clean(entry.find('content').string),
                              timestamp   = datetime.datetime.strptime(entry.find('published').string, '%Y-%m-%dT%X%z'))
        embed.set_author(     name        = ' '.join(entry.find('title').string.split(' ')[:2]),  # first two words of title (should be name and emoji)
                              url         = entry.find('link')['href'],  # to status.cafe page for the post
                              icon_url    = 'https://nomnomnami.com/images/icon_nami.png')
        embed.set_footer(     text        = 'status.cafe')
        messages.append({'embed': embed})
        

    return messages  # reversed to return in order of upload if there are several new updates


def parse_trick(old_file, new_file):
    old_entries = BeautifulSoup(old_file, 'xml').find_all('entry')
    new_entries = BeautifulSoup(new_file, 'xml').find_all('entry')
    entries_to_post = []  # find entries added since last time
    for entry in new_entries:
        if entry not in old_entries:
            entries_to_post.append(entry)
    # make messages
    messages = []
    for entry in entries_to_post:
        content = BeautifulSoup(entry.find('content').string, 'html.parser').find('div', {'class': 'trix-content'})
        embed = discord.Embed(color       = 0xE47485,
                              title       = entry.find('title').string,
                              url         = entry.find('link')['href'],
                              description = html_to_discord(content)['text'],
                              timestamp   = datetime.datetime.strptime(entry.find('published').string, '%Y-%m-%dT%XZ'))
        embed.set_author(     name        = 'Trick',
                              url         = 'https://trick.pika.page',
                              icon_url    = 'https://nomnomnami.com/games/treat/charasort/src/assets/chars/trick.png')
        embed.set_image(      url         = content.find('img')['src'])
        embed.set_footer(  text        = 'Letters from Trick')
        messages.append({'embed': embed})
        

    return messages  # reversed to return in order of upload if there are several new updates


def parse_neocities(old_file, new_file):
    old_soup = BeautifulSoup(old_file, 'html.parser')
    new_soup = BeautifulSoup(new_file, 'html.parser')
    old_updates = old_soup.find_all('div', {'class': 'news-item update'})
    new_updates = new_soup.find_all('div', {'class': 'news-item update'})
    
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


def check(source):
    # ask internet pretty please give me the thing i want
    response = requests.get(source['link'])
    if response.status_code != 200:
        if not source['down']:  # if not yet marked as offline
            print(str(source['link']) + ' returned status code ' + str(response.status_code))
            source['down'] = True  # mark this link as being offline
        return []
    elif source['down']:  # if marked as offline, but it works, that means it's back up
        print(str(source['link']) + ' is back online')
    
    # compare to currently saved version
    old_file = open('saved/' + source['file'], 'rb').read()
    new_file = response.content
    if old_file == new_file:
        return []  # nothing new, no updating necessary; will not happen for pages like status.cafe that update parts of its content regularly lol
    
    # call parse function for the source type
    messages: list[dict] = list(reversed(source['parse'](old_file, new_file)))
    
    # save to file
    with open('saved/' + source['file'], 'wb') as file:
        file.write(new_file)

    for message in messages:
        message['files'] = []
        if 'images' in message.keys():
            for image in message['images']:
                response = requests.get(urljoin('https://nomnomnami.com', image['src']))
                discord_file = discord.File(io.BytesIO(response.content),
                                            filename = image['src'].split('/')[-1],
                                            spoiler  = (image.parent == 'details'))  # spoiler if part of details (for posts)
                message['files'].append(discord_file)
    return messages
