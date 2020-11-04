def get(endpoint):
    headers = {'Authorization': f'token {}'}
    response = requests.get(endpoint)
