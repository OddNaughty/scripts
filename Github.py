import os
import requests

class Github(object):
    """
    A Github class to use Github API
    """

    def __init__(self):
        """
        Instantiation of class.
        Use of Github OAuth. Token must be in your environnement variable (GITHUB_OAUTH_TOKEN)
        """
        self.api = "https://api.github.com/"
        self.oauth_token = os.environ["GITHUB_OAUTH_TOKEN"]
        self.request_header = {'Authorization': 'token ' + self.oauth_token}

    def do_get_request(self, endpoint, payload=None):
        """
        Performs a GET request at endpoint
        :param endpoint: String: Github API endpoint
        :param payload: Dictionnary: GET parameters
        :return: Dictionnary: JSON response of Github
        """
        return requests.get(self.api + endpoint, headers=self.request_header, params=payload).json()

    def do_post_request(self, endpoint, payload=None):
        """
        Performs a GET request at endpoint
        :param endpoint: String: Github API endpoint
        :param payload: Dictionnary: POST parameters
        :return: Dictionnary: JSON response of Github or requests.HTTPError exception if it fails
        """
        r = requests.post(self.api + endpoint, headers=self.request_header, json=payload)
        r.raise_for_status()
        # except requests.HTTPError:
        #     print (r.json())
        #     return False
        return r.json()

    def user(self):
        endpoint = "user"
        return self.do_get_request(endpoint)

    def get_repos(self):
        endpoint = "user/repos"
        return self.do_get_request(endpoint)

    def create_repo(self, name, description="Repo created by Github API", private=False, auto_init=True, **kwargs):
        repo_object = {'name': name, 'description': description, 'private' : private, 'auto_init': auto_init}
        endpoint = "user/repos"
        return self.do_post_request(endpoint, {**repo_object, **kwargs})
