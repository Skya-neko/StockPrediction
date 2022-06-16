from multiprocessing import Process, Queue

def square(numbers, queue):
    for i in numbers:
        queue.put(i*i)
def main():
    numbers = range(5)
    queue = Queue()
    square_process = Process(target=square, args=(numbers, queue))
    try:
        square_process.start()
    except EOFError:
        pass

    square_process.join()
    print('end of child process')
    while not queue.empty():
        print(queue.get())

if __name__ == '__main__':
    main()

