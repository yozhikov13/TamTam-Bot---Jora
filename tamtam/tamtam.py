import requests
import json

class TamTam:
    """место куда отправляются файлики:
    https://fu.mycdn.me/"""

    _chatsCount = 0
    sender = 0
    text_msg = 0
    user_id_msg = 0
    user_name_msg = 0

    _url = 'https://botapi.tamtam.chat/'
    _headers = {
        'Content-Type': 'application/json',
        'charset': 'utf-8',
    }
    _token = ''

    def __init__(self, token):
        self._token = token

    def _get(self, url, params=None, json=True):
        if not params:
            params = {}
        params['access_token'] = self._token
        rr = requests.get(self._url + url, params=params)
        rr.raise_for_status()
        if json:
            z = rr.json()
        else:
            z = rr.content.decode('utf-8')
        return z

    def _post_messages(self, data, ai=False, params=None):
        if not params:
            params = {}
        params['access_token'] = self._token
        rr = requests.post(self._url + 'me/messages',
                           params=params,
                           json=data,
                           headers=self._headers)
        rr.raise_for_status()
        try:
            z = rr.json()
        except TypeError:
            raise TypeError(rr.text)
        if not ai:
            if not z['message_id'].startswith('mid.'):
                raise MessageNotSendException(z)
        return z

    def send(self, chat_id, text):
        data = {
            "recipient": {"chat_id": chat_id},
            "message": {"text": text},
        }
        return self._post_messages(data=data)

    def get_chats(self, count=100, marker=None):
        params = {'count': count}
        if marker:
            params['marker'] = marker
        zz = self._get(url='me/chats', params=params)
        return zz['chats'], zz['marker'] if 'marker' in zz else None

    def get_chats_all(self):
        marker = None
        step = 0
        zz = []
        rr = []
        while (step == 0) or ((len(zz) == 100) and (step < 50)):
            zz, marker = self.get_chats(count=100, marker=marker)
            rr = rr + zz
            step = step + 1
        return rr

    def get_result(data, key_key, key_value):
        labels_list = {}
        for index in data:
            labels_list[index[key_key]] = index.get(key_value, '')
        return labels_list

    def get_flat_chats(self):
        json = self.get_chats_all()

        return self.get_result(data=json, key_key='chat_id', key_value='title')


    def get_chat(self, chat_id):
        params = {'chat_id': chat_id}
        zz = self._get(url='me/chat', params=params)
        if 'error_code' in zz:
            raise ChatNotFondException(zz['error_msg'])
        return zz

    def get_messages(self, chat_id):
        zz = self._get(url='me/messages', params={'chat_id': chat_id})
        return zz['messages']

class MessageNotSendException(Exception):
    pass

class ChatNotFondException(Exception):
    pass
class UserDonTHaveChatException(Exception):
    pass
