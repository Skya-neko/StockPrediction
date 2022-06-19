from multiprocessing import Process, Queue

def square(numbers, queue):
    for i in numbers:
        queue.put(i*i)  # First in First out

def main():
    numbers = range(5)
    queue = Queue()
    square_process = Process(target=square, args=(numbers, queue))
    square_process.start()
    square_process.join()  # Continue the main process after execution of child process
    print('end of child process')
    while not queue.empty():
        print(queue.get())   # First in First out

if __name__ == '__main__':
    main()


