from taskbank import *
from utils import *

menu_month = ["now(default)", "input(e.g.202311)"]

menu_main = ["quick-create-begin",
             "list-tasks",
             "exit"]

menu_state = ["pending", "close", "running", "abandoned", "all"]

menu_action = Actions


def main ():
    ppf("Here is my task workspace, choose the month")
    a = pf_menu_and_chose(menu_month, "[month]")
    if a == '0':
        a = None
    tbank = TaskBank(a)
    while True:
        a = pf_menu_and_chose(menu_main)
        tid = None
        if a == '2':
            break
        elif a == '1':
            aa = pf_menu_and_chose(menu_state)
            if aa == '4':
                state = None
                tbank.db.debug()
            else:
                state = eval("TaskState." + menu_state[int(aa)])
            tbank.list_tasks(state)
            ppf("choose a task id")
            try:
                tid = int(input("[id] = "))
            except:
                continue
        elif a == '0':
            tid = tbank.create_new_tasks()
            tbank.manage_task(tid, 'start')
        while True:
            ppf(f"task-{tid} running, what is the next action?")
            ac = pf_menu_and_chose(menu_action)
            if ac != '0':
                break
        tbank.manage_task(tid, Actions[int(ac)])


if __name__ == "__main__":
    main()
