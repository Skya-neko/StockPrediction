from multiprocessing import Process, Queue
import time
def square(numbers, queue):
    for i in numbers:
        queue.put(i*i)  # # First in First out
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
        print(queue.get())   # First in First out

if __name__ == '__main__':
    main()
    print(time.time())

