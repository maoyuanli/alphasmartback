# for security reason , the tokens used for the project is saved somewhere else and is not uploaded to GitHub.
# this utility class helps to fetch it

import json
import os


class TokenFetcher():

    def __init__(self, token_file):
        self.token_file = token_file

    @property
    def token_file(self):
        return self._token_file

    @token_file.setter
    def token_file(self, token_file):
        if '.json' in token_file:
            self._token_file = token_file
        else:
            raise ValueError('Token File must be in json format')

    def fetch_token(self, key):
        cur_path = os.path.dirname(__file__)
        par_path = os.path.dirname(cur_path)
        while os.path.isfile(os.path.join(par_path, self._token_file)) == False:
            par_path = os.path.dirname(par_path)
        token = json.load(open(os.path.join(par_path, self._token_file), 'r'))
        return token[key]
