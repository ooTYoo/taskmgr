import datetime
import os

import config
from taskClass import *
from taskdb import *
from utils import *

import pdb

Actions = ['start', 'stop', 'finish', 'abort', 'recovery']



class TaskBank():
    '''task bank act as the cache of tasks db, indicated by month'''
    def __init__(self, month=None):
        if month is None:
            tick = datetime.datetime.now()
            month = str(tick.month)
            if tick.month<10:
                month = '0' + month
            month = str(tick.year) + month
        self.m = month
        ppf("initializing taskbank for" + month)
        self.db = TaskDB(config.default_db)
        self.table = config.default_table
        self.tasks_id = self.db.get_id_list(mfrom=month,table=self.table)
        Task.counter = self.db.count_by_month(month, table=self.table) + (int(self.m)%10000)*1000
        ppf("loading all tasks done")
        self.runing_list = []
        self.runing_task = {}

    def create_new_tasks(self):
        t = Task()
        t.create()
        print(t.id)
        self.db.insert_task(task=t, table=self.table)
        return t.id

    def list_tasks(self, state=None):
        tlist = self.tasks_id
        if state is not None:
            tlist = self.db.get_id_list(mfrom=self.m, state=state, table=self.table)
        for t in tlist:
            task = self.db.find_task(t, table=self.table)
            print(task.summary())

    def manage_task(self, tid, action):
        if not action in Actions:
            ppf("wrong action, try again")
            return
        task = self.db.find_task(taskid=tid,table=self.table)
        if tid in self.runing_list:
            task.beg_tick = self.runing_task[tid]
            task.state = TaskState.running

        eval("task." + action + "()")

        if action == 'start' and tid not in self.runing_list:
            self.runing_list.append(tid)
            self.runing_task[tid] = task.beg_tick
        elif action != 'start' and tid in self.runing_list:
            print(task.to_str())
            self.runing_list.pop(self.runing_list.index(tid))
            del self.runing_task[tid]
            self.db.update_task(task, table=self.table)

    def __del__(self):
        for i in self.runing_list:
            self.manage_task(i,'stop')




