import joblib
import re
import requests

from env import token


class Repository:
    def __init__(self, owner: str, repo_name: str, step: int = 10):
        self.owner = owner
        self.repo_name = repo_name
        self.step = step

        self.starred_at_count = {}
        self.repo_id, self.last_index = self.__get_repo_id_and_last_index()

    def get_star_history(self):
        # ref) https://karupoimou.hatenablog.com/entry/20200305/1583407204
        res = joblib.Parallel(
            n_jobs=-2, verbose=2)([joblib.delayed(self.process)(index) for index in range(0, self.last_index + 1, self.step)])
        return res

    def process(self, index):
        response = self.__get(
            f'https://api.github.com/repositories/{self.repo_id}/stargazers?page={index}')

        last_response = response.json()[-1]
        date_str = last_response['starred_at'].split('T')[0]
        res = {}
        res[date_str] = len(response.json()) * (index + 1)
        return res  # e.g. {'2016-11-27': 30}

    def __get(self, endpoint):
        response = requests.get(
            endpoint,
            headers={
                'Accept': 'application/vnd.github.v3.star+json',
                'Authorization': f'token {token}'
            }
        )
        return response

    def __get_repo_id_and_last_index(self):
        endpoint = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/stargazers'
        response = self.__get(endpoint)

        # pagination_info e.g.) <https://api.github.com/repositories/74293321/stargazers?page=2>; rel="next", <https://api.github.com/repositories/74293321/stargazers?page=1303>; rel="last"
        pagination_info = response.headers['link']
        match = re.search(r'<https://api.github.com/repositories/(\d+)/stargazers\?page=(\d+)>; rel="last"',
                          pagination_info)
        repo_id, last_index = match.group(1), match.group(2)

        return repo_id, int(last_index)
