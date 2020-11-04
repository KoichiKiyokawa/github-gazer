import requests

GITHUB_API_ENDPOINT = 'https://api.github.com'


class Repository:
    def __init__(self, owner: str, repo_name: str):
        self.owner = owner
        self.repo_name = repo_name

    def getStarHistory(self):
        endpoint = f'{GITHUB_API_ENDPOINT}/repos/{self.owner}/{self.repo_name}/stargazers'
        response = requests.get(endpoint, headers={'Accept': 'application/vnd.github.v3.star+json'
                                                   })
        return [each['starred_at'] for each in response.json()]
