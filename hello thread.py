import threading
from time import sleep


def main():
    thread = threading.Thread(target=hello_name, args=('Sviat', 3), daemon=True)
    thread.start()
    print(' - Hello from main')
    print(' - Done')


def hello_name(name, count):
    for _ in range(count):
        print(f'Hello {name}')
        sleep(1)


if __name__ == '__main__':
    main()