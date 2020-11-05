import joblib
import re
import requests

from env import token


class Repository:
    def __init__(self, owner: str, repo_name: str):
        self.owner = owner
        self.repo_name = repo_name
        self.starred_at_count = {}
        repo_id, last_index = self.__get_last_index()
        self.repo_id = repo_id
        self.last_index = last_index

    def getStarHistory(self):
        # ref) https://karupoimou.hatenablog.com/entry/20200305/1583407204
        joblib.Parallel(
            n_jobs=-2, verbose=2)([joblib.delayed(self.process)(index) for index in range(self.last_index + 1)])
        return self.starred_at_count

    def process(self, index):
        response = self.__get(
            f'https://api.github.com/repositories/{self.repo_id}/stargazers?page={index}')
        for each_response in response.json():
            date_str = each_response['starred_at'].split('T')[0]
            if date_str not in self.starred_at_count:
                self.starred_at_count[date_str] = 0

            self.starred_at_count[date_str] += 1

    def __get(self, endpoint):
        response = requests.get(
            endpoint,
            headers={
                'Accept': 'application/vnd.github.v3.star+json',
                'Authorization': f'token {token}'
            }
        )
        return response

    def __get_last_index(self):
        endpoint = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/stargazers'
        response = self.__get(endpoint)

        # pagination_info e.g.) <https://api.github.com/repositories/74293321/stargazers?page=2>; rel="next", <https://api.github.com/repositories/74293321/stargazers?page=1303>; rel="last"
        pagination_info = response.headers['link']
        match = re.search(r'<https://api.github.com/repositories/(\d+)/stargazers\?page=(\d+)>; rel="last"',
                          pagination_info)
        repo_id, last_index = match.group(1), match.group(2)

        return repo_id, int(last_index)
