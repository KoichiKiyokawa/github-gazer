from entity.Repository import Repository


def main():
    repo = Repository('sveltejs', 'svelte')
    print(repo.getStarHistory())


if __name__ == '__main__':
    main()
