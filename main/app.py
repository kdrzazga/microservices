from main.utills.files import read_yaml_file


def init():
    props = read_yaml_file()
    print(props['url']['project'])


if __name__ == '__main__':
    init()
