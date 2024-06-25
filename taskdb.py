import sqlite3
import os
from taskClass import *
import config
class TaskDB():
    def __init__(self, dbfile=config.default_db):
        full_path = os.path.join(os.getcwd(), dbfile)
        if not os.path.exists(full_path):
            open(full_path,'a').close()
        try:
            self.conn = sqlite3.connect(full_path)
        except Exception:
            print("[!] open datebase file failure --",full_path)
            return
        print("[+] open database success")

    def create_table(self, table=config.default_table):
        c = self.conn.cursor()
        # c.execute(f"DROP TABLE IF EXISTS {table}")
        c.execute(f'''CREATE TABLE IF NOT EXISTS {table}(
               ID INT PRIMARY KEY NOT NULL,
               CREATING CHAR(27) NOT NULL,
               END CHAR(27),
               EFFORT INT NOT NULL,
               STATE INT NOT NULL,
               CONTENT TEXT NOT NULL);''')
        print("[+] creating table success --",table)
        return table

    def insert_task(self, task:Task, table=config.default_table):
        if self.task_exist(task.id, table) is not None:
            print("[!] task-id already exist, insert fail")
            return
        self.conn.execute(f"INSERT INTO {table} (ID,CREATING,END,EFFORT,STATE,CONTENT)\
            VALUES ({task.id},'{str(task.create_date)}', '{task.end}', {task.effort},\
            {int(task.state)}, '{task.content}')")
        self.conn.commit()

    def task_exist(self, taskid, table=config.default_table):
        if taskid < 24*100*1000:
            return None
        c = self.conn.cursor()
        rslt = c.execute(f"SELECT * FROM {table} WHERE ID={taskid}")
        if rslt is None:
            return None
        for row in rslt:
            return row

    def convert_colum_2_task(self,item):
        t = Task()
        t_str = '#'.join([str(item[4]), str(item[0]),item[1],item[2],str(item[3]),item[5]])
        t.from_str(t_str)
        return t

    def find_task(self, taskid, table=config.default_table):
        item = self.task_exist(taskid, table)
        if item is None:
            print("[!] wrong input taskid, not found")
            return None
        return self.convert_colum_2_task(item)

    def update_task(self, task, table=config.default_table):
        item = self.task_exist(task.id, table)
        if item is None:
            print("[!] wrong input taskid, not found")
            return None
        c = self.conn.cursor()
        c.execute(f'''UPDATE {table} SET
                    STATE={int(task.state)},
                    EFFORT={task.effort},
                    END='{task.end}'
                    WHERE ID={task.id}''')

    def count_by_month(self, month='202406', table=config.default_table):
        month = int(month)
        val_beg = (month%10000)*1000
        val_end = val_beg+1000
        c = self.conn.cursor()
        rslt = c.execute(f"SELECT ID FROM {table} WHERE ID >= {val_beg} AND ID<{val_end}")
        if rslt is None:
            return 0
        return len(list(rslt))

    def get_id_list(self, mfrom=None, mto=None, state=None, table=config.default_table):
        condition = []
        if mfrom is not None:
            mfrom = (int(mfrom)%10000)*1000
            condition.append(f'ID >= {mfrom}')
            if mto is None:
                delta = (100-12) if (mfrom%100)==12 else 1
                mto_ = str(mfrom+delta*1000)
                condition.append(f'ID < {mto_}')
        if mto is not None:
            mto = (int(mto)%10000)*1000
            condition.append(f'ID < f{mto}')
        if state is not None:
            condition.append(f"STATE={int(state)}")
        all_cond = ' AND '.join(condition)
        c = self.conn.cursor()
        print(f"SELECT ID FROM {table} WHERE {all_cond}")
        rslt = c.execute(f"SELECT ID FROM {table} WHERE {all_cond}")
        return list(a[0] for a in rslt)

    def debug(self, table=config.default_table):
        c = self.conn.cursor()
        rslt = c.execute(f"SELECT * FROM {table}")
        for item in rslt:
            print(item)

    def __del__(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    db = TaskDB()
    db.create_table()
    tl = testcase_gen_task(10)
    for a in tl:
        db.insert_task(a)
    task = db.find_task(2406001)
    task.finish()
    db.update_task(task)
    print(task.to_str())
    print(db.get_id_list())


