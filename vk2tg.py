import html
from threading import Thread
import time
from os import path

import telebot
import yaml
import vk_api


CONFIG_FILE = 'config.yaml'
link_tmp = 'https://vk.com/club{group_id}?w=wall-{group_id}_{post_id}'
reply_tmp = '_reply ->_\n*{owner}*\n{text}\n{reply}\n'
post_tmp = '{text}\n{reply}\n_{owner}_\n{link}'


class ConfigLoader:
    def __init__(self, filename):
        self.FILENAME = filename
        self.load()

    def load(self):
        with open(self.FILENAME) as f:
            self.values = yaml.load(f)

    def save(self):
        with open(self.FILENAME, 'w') as f:
            yaml.dump(self.values, f)
    
    # def get(self, key: str):
    #     return self.values[key]
    
    # def set(self, key: str, value: any):
    #     self.values[key] = value


def load_config():
    global CONFIG
    CONFIG = ConfigLoader(CONFIG_FILE)


def html_escape(text):
    '''Simple HTML escaping function'''
    text = str(text)
    return html.escape(text)


load_config()
vk_session = vk_api.VkApi(CONFIG.values['vk_login'], CONFIG.values['vk_password'])
vk_session.auth()

VK = vk_session.get_api()
BOT = telebot.TeleBot(CONFIG.values['bot_token'])



# Post format

# ---Simple
# Text in post 
#
# Link: http://test.org
# 19-02-1998 12:23

# ---Reply
# Text in post
# reply -> Reply from
# Text in reply post
#
# Link: http://test.org
# 19-02-1998 12:23


def get_post(post, reply=False):
    post_owner = ''
    if post['from_id'] < 0: # author -> group
        post_owner = VK.groups.getById(group_id=-post['from_id'])[0]['name']
    else: # author -> user
        post_owner = '{} {}'.format(VK.users.get(user_ids=str(post['from_id']))[0]['first_name'], VK.users.get(user_ids=str(post['from_id']))[0]['last_name'])

    post_reply_text = ''
    if 'copy_history' in post:
        post_reply_text = get_post(post['copy_history'][0], True)
    if reply:
        return reply_tmp.format(owner=post_owner, text=post['text'], reply=post_reply_text)
    post_time = time.strftime('%d-%m-%Y %H:%M', time.localtime(post['date']))
    post_link = link_tmp.format(group_id=-int(post['owner_id']), post_id=post['id'])
    return post_tmp.format(owner=post_owner, text=post['text'], reply=post_reply_text, link='[{}]({})'.format(post_time, post_link))
#     reply_tmp = 'reply -> {from}\n{text}{reply}'
#     post_tmp = '{from}\n{text}{reply}\n\n{link}\n{date}'

def check_posts():
    while True:
        posts = []
        last_id = CONFIG.values['vk_last_post_id']
        for post in VK.wall.get(owner_id=CONFIG.values['vk_group_id'])['items']:
            if post['id'] <= CONFIG.values['vk_last_post_id']:
                if 'is_pinned' in post and post['is_pinned'] == 1:
                    continue
                else:
                    break
            if post['id'] > last_id:
                last_id = post['id']
            posts.append(get_post(post))
        posts.reverse()
        for post in posts:
            BOT.send_message(CONFIG.values['tg_chat_id'], post, parse_mode='Markdown')
        CONFIG.values['vk_last_post_id'] = last_id
        CONFIG.save()
        time.sleep(10*60)

BOT.send_message(CONFIG.values['tg_chat_id'], 'Bot started')

thread = Thread(target=check_posts)
thread.start()
