import joblib


class Main:
    def __init__(self):
        self.result = {}

    def process(self, num):
        self.result[num] = 1

    def exec(self):
        joblib.Parallel(
            n_jobs=-1)([joblib.delayed(self.process)(num) for num in range(100000)])
        return self.result


def main():
    main = Main()
    print(main.exec())


if __name__ == '__main__':
    main()
