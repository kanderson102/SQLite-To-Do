#!/usr/bin/python3
import sqlite3

def get_cursor():
    conn = sqlite3.connect("company.db")
    c = conn.cursor()
    return c

class Task:

    def __init__(self,**kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table')

    def sql_do(self, sql, *params):
        self._db.execute(sql,params)
        self._db.commit()

    def task_count(self):
        c = self._db.execute('SELECT COUNT(*) FROM {} as mycount'.format(self.table))
        count = c.fetchall()
        return count[0][0]

    def insert(self,row):
        # self._db.execute('UPDATE {} SET priority = ? WHERE priority >= ? '.format(self.table),
        #                  (row['priority'] + 1, row['priority']))
        self._db.execute('INSERT INTO {} (priority, task) VALUES (?, ?)'.format(self.table),
                         (row['priority'], row['task']))

        self._db.commit()

    def delete(self,key):
        self._db.execute('DELETE FROM {} WHERE priority = ?'.format(self.table), (key,))
        self._db.commit()

    def decrease_priority(self, row):
        self._db.execute('UPDATE {} SET priority = ? WHERE priority = ? '.format(self.table),
                        (row['priority'] - 1, row['priority']))
        self._db.commit()

    def increase_priority(self,row):
        self._db.execute('UPDATE {} SET priority = ? WHERE priority = ? '.format(self.table),
                         (row['priority']+1,row['priority']))
        self._db.commit()

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self,f):
        self._filename = f
        self._db = sqlite3.connect(f)
        self._db.row_factory = sqlite3.Row

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self,t):
        self._table = t

    def __iter__(self):
        cursor = self._db.execute('SELECT * FROM {} ORDER BY priority'.format(self.table))
        for row in cursor:
            yield dict(row)
    #
    # @classmethod
    # def taskcount(cls):
    #     cls._db.execute('SELECT COUNT(*) in {}'.format(cls.table))
    #     return cls._db.execute


def compile():
    import os, re
    os.system('cls')


    db = Task(filename='listoftasks', table='main_tasks')
    # create table
    db.sql_do('CREATE table IF NOT EXISTS main_tasks( priority int, task text )')

    #db.sql_do('DELETE FROM main_tasks')
    startmenu()
    display_list(db)

   #Add, delete, or quit
    arg = input("\n\n")
    if arg == 'a':
        task = input("New Task: ")
        if db.task_count() < 1: #if the task list is empty, just add it without asking more
            db.insert(dict(priority = 1, task = task))
        else:
            position = int(input("What's the priority? [0] to put at end:"))
            if position == 0 or position > db.task_count(): #put task at the end without incrementing any priorities
                db.insert((dict(priority = db.task_count() + 1, task = task)))
            else:
                update_list = []
                for row in db:
                    if row['priority'] >= position:
                        update_list.append(row)
                s = sorted(update_list,key = lambda k: k['priority'], reverse = True)
                for r in s:
                    db.increase_priority(r)
                db.insert(dict(priority = position, task = task))

    # elif arg == 's':
    #     taskbranch = input("What task do you want to add to?")
    #     order = input("What's the priority? [0] to put at end:")
    #     subTask = input("New Sub Task: ")
    #     addSubTask(list,subTask,int(order),taskbranch)

    elif arg == 'd':
        index = int(input("Which task do you want to delete?"))
        if db.task_count() < index:
            TypeError('Index: {} out of range'.format(index))
        else:
            db.delete(index)
            print('Row {} deleted'.format(index))

            delete_list = []
            for row in db:
                if row['priority'] > index:
                    delete_list.append(row)
            for r in delete_list:
                print(r)
                db.decrease_priority(r)

    elif arg == 'q':
        exit()

    compile()

def startmenu():
    print("[a] add task, [d] delete, [q] quit")
    print("To-Do List:")

def display_list(db):
    dictlist = []
    for row in db:
        dictlist.append(row)

    slist = sorted(dictlist, key=lambda k: k['priority'])
    for r in (slist):
        print(str(r['priority']) + ")", r['task'])


if __name__ == "__main__":
    compile()