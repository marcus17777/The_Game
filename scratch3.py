import multiprocessing, pygame


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            # print('%s: %s' % (proc_name, next_task))
            answer = next_task
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        # pygame
        self.screen = pygame.display.set_mode((self.a, self.b))
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption('The Game')
        self.screen.fill((80, 80, 80))
        self.clock = pygame.time.Clock()
        self.ms = self.clock.tick(50)

    def __str__(self):
        return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 1
    print('Creating %d consumers' % num_consumers)
    consumers = [Consumer(tasks, results) for i in range(num_consumers)]
    for w in consumers:
        w.start()

    # Enqueue jobs
    tasks.put(Task(800, 600))
    tasks.put(Task(400, 400))

    # Wait for all of the tasks to finish
    tasks.join()
