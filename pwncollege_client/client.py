import re

import requests


class Client:
    def __init__(self, *, url='https://cse466.pwn.college'):
        self.url = url

        self.session = requests.session()


    def login(self, username, password):
        nonce = re.search('<input type="hidden" name="nonce" value="(?P<nonce>.*?)">',
                          self.session.get(f'{self.url}/login').text)['nonce']

        response = self.session.post(f'{self.url}/login', data={'name': username, 'password': password, 'nonce': nonce})

        return 'Your username or password is incorrect' not in response.text


    def challenges(self):
        data = self.session.get(f'{self.url}/api/v1/challenges').json()['data']

        return [{
            'id': challenge['id'],
            'category': challenge['category'],
            'name': challenge['name'],
            'value': challenge['value']
        } for challenge in data]


    def work_on(self, challenge_id):
        csrf = re.search('csrf_nonce = "(?P<csrf>.*?)"',
                         self.session.get(f'{self.url}/challenges').text)['csrf']


        response = self.session.post(f'{self.url}/pwncollege_api/v1/docker', headers={'csrf-token': csrf}, json={'challenge_id': challenge_id})

        return response.json()['success']


    def submit_flag(self, challenge_id, flag):
        csrf = re.search('csrf_nonce = "(?P<csrf>.*?)"',
                         self.session.get(f'{self.url}/challenges').text)['csrf']

        response = self.session.post(f'{self.url}/api/v1/challenges/attempt', headers={'csrf-token': csrf}, json={'challenge_id': challenge_id, 'submission': flag})

        return response.json()['success'] == True and response.json()['data']['status'] in ['correct', 'already_solved']
