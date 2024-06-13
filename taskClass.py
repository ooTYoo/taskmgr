import datetime
import math
import enum
from utils import *

class TaskState(enum.IntEnum):
    pending = 2
    abandoned = 0
    running = 5
    close = 9


class Task():
    counter = 0

    def __init__(self):
        self.id = None
        self.content = None
        self.create_date = None
        self.end = None
        self.effort = 0
        self.beg_tick = None
        self.state = None

    def create(self, content=''):
        self.id = Task.counter
        Task.counter += 1
        self.create_date = datetime.datetime.now()
        if len(content)==0:
            ppf("Describe this task")
            self.content = input("(task) => ")
        else:
            self.content = content
        self.state = TaskState.pending

    def start(self):
        if self.state == TaskState.running:
            ppf("task already in running")
            return
        self.beg_tick = datetime.datetime.now()
        self.state = TaskState.running
        ppf("task begin @ " + str(self.beg_tick))

    def stop(self):
        if self.state == TaskState.running:
            now = datetime.datetime.now()
            self.effort += (now - self.beg_tick).seconds
        self.state = TaskState.pending

    def finish(self):
        self.end = datetime.datetime.now()
        ppf("task finish @ " + str(self.end))
        if self.state == TaskState.running:
            self.effort += (self.end - self.beg_tick).seconds
        self.state = TaskState.close
        ppf(f"takes {math.ceil(self.effort/60)} min")

    def abort(self):
        if self.state == TaskState.running:
            now = datetime.datetime.now()
            self.effort += (now - self.beg_tick).seconds
        self.state = TaskState.abandoned

    def recovery(self):
        assert (self.state == TaskState.abandoned)
        self.state = TaskState.pending

    def to_str(self):
        # this is a temp api
        str_form = '#'.join(list(map(str,[self.state, self.id, self.create_date, self.end, self.effort, self.content])))
        return str_form

    def from_str(self, astr):
        if astr[0] == str(TaskState.abandoned):
            return
        task_ptr = astr.split("#")
        self.state = TaskState(int(task_ptr[0]))
        self.id = int(task_ptr[1])
        self.create_date = datetime.datetime.fromisoformat(task_ptr[2])
        if task_ptr[0] == str(TaskState.close):
            self.end = datetime.datetime.fromisoformat(task_ptr[3])
        self.effort = int(task_ptr[4])
        self.content = task_ptr[5]

    def summary(self):
        str_form = f"id={regular_str(self.id,8)}\tcost(min)={regular_str(math.ceil(self.effort/60.0), 8)}\ttask={self.content}"
        return str_form


def testcase_gen_task(num,prefix='test',id_beg=0):
    Task.counter = id_beg
    tl = []
    for i in range(num):
        task = Task()
        task.create(content=(prefix)+str(i))
        tl.append(task)
    return tl


if __name__ == "__main__":
    tl = testcase_gen_task(10,prefix='test-',id_beg=2406000)
    for a in tl:
        print(a.summary())
        b = Task()
        b.from_str(a.to_str())
        print("-->",b.summary())
