from entity.Repository import Repository


def main():
    repo = Repository('sveltejs', 'svelte')
    print(repo.get_star_history())


if __name__ == '__main__':
    main()
