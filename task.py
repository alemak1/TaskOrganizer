from datetime import timedelta
from datetime import date,datetime,time

class Task:
    '''A task object represents a task and has stored properties that provide a name and description of task, the date on which
    the task was already completed or is expected to be completed, and boolean flag to indicate whether the task has been completed or not
    In the future, Task can be refactored into a base class, with derived classes for future tasks and past tasks;
    In addition, we can sublcass Task to represent large tasks (whose completion time is a matter of hours,minutes, and seconds)
    versus small tasks (whose completion time occurs on larger time scales)


    '''

    @classmethod
    def getSQLCreateStatement(cls, table_name):
        ''' Generates a MySQL Create Statement that allows for the Task class to be converted into a MySQL table, which can
      then be used with a MySQL client to create a Task table

        :return:
        '''
        create_statement = "CREATE TABLE {} ".format(table_name)
        create_statement += "("
        create_statement += "id INT AUTO_INCREMENT,"
        create_statement += "name VARCHAR NOT NULL, "
        create_statement += "description VARCHAR NULL, "
        create_statement += "difficulty_level INT NULL, "
        create_statement += "priority_level INT NULL, "
        create_statement += "task_date DATE NOT NULL, "
        create_statement += "actual_time_required TIME NOT NULL DEFAULT = 00:00:00, "
        create_statement += "predicted_time_required TIME NOT NULL DEFAULT = 00:00:00, "
        create_statement += "completed INT NOT NULL DEFAULT = 0,"
        create_statement += "PRIMARY KEY(id)"
        create_statement += ");"
        return create_statement

    sortingKey = 0

    @classmethod
    def setSortingKey(cls,sortKey = 0):
        '''Users can set the sorting key to priority, difficulty_level, task_date and time_required in order to change the
        implementation of the overloaded operators and allow for task objects to be sorted by different algorithm based
        on user-specified criteria

        :param sortKey: an integer representing a sort key
        :return: None: sortKeys are specified based on integer values
        '''

        if sortKey not in range(0,5):
            raise ValueError

        cls.sortingKey = sortKey

    def __init__(self, name, description = None,
                 task_difficulty_level = None,
                 task_priority_level = None,
                 task_date = None,
                 predicted_time_required = timedelta(seconds=0),
                 actual_time_required = timedelta(seconds=0),
                 completed = False):
        if not isinstance(predicted_time_required, timedelta) or not isinstance(actual_time_required,timedelta):
            raise TypeError

        if task_date and not isinstance(task_date,datetime.date):
            raise TypeError

        if description and not isinstance(description,str):
            raise TypeError

        if task_difficulty_level and not isinstance(task_difficulty_level, int):
            raise TypeError

        if task_priority_level and not isinstance(task_priority_level,int):
            raise TypeError

        if not isinstance(name,str):
            raise TypeError

        self.name = name
        self.difficulty_level = task_difficulty_level
        self.priority_level = task_priority_level
        self.description = description
        self.task_date = task_date
        self.actual_time_required = actual_time_required
        self.predicted_time_required = predicted_time_required
        self.completed = completed

    #define the setter methods for task attributes
    def setPriorityLevel(self,priority_level):
        if not isinstance(priority_level,int):
            raise TypeError
        self.priority_level = priority_level

    def setDifficultyLevel(self,difficulty_level):
        if not isinstance(difficulty_level,int):
            raise TypeError
        self.difficulty_level = difficulty_level

    def setDescription(self,task_description):
        if not isinstance(task_description,str):
            raise TypeError
        self.description = task_description

    def setTaskDate(self,day=0,month=0,year=0):
        if not isinstance(day,int) or not isinstance(month,int) or not isinstance(year,int):
            raise TypeError
        self.task_date = datetime.date(year=year,month=month,day=day)

    def setPredictedTimeRequired(self,seconds = 0, minutes = 0, hours = 0):
        if not isinstance(seconds,int) or not isinstance(minutes,int) or not isinstance(hours,int):
            raise TypeError
        self.predicted_time_required = timedelta(seconds=seconds,minutes=minutes,hours=hours)

    def setActualTimeRequired(self,seconds=0,minutes=0,hours=0):
        if not isinstance(seconds, int) or not isinstance(minutes, int) or not isinstance(hours, int):
            raise TypeError
        self.actual_time_required = timedelta(seconds=seconds,minutes=minutes,hours=hours)

    def toggleCompletion(self):
        self.completed = not self.completed

    #Overloaded arithmetic operators

    def __add__(self, other):
        '''Overloads the arithmetic addition operator; As a precondition, the sortKey must be set to 0 or 1, since
        task addition only makes sense in the context of adding time_required (predicted or actual), and not with
        date of task, priority_level, or difficulty level

        :param      Other can be another Task object, a timedelta object, or a float/int
        :return:    Return values can be of type Task, timedelta, or float/int
        '''

        #The sortingKey must be 0 or 1 in order for arithmetic addition to make sense
        if Task.sortingKey not in range(0,2):
                raise TypeError

        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required + other.actual_time_required #returns a timedelta object
            if isinstance(other, (float, int)):
                return self.actual_time_required + other.actual_time_required.total_seconds() #returns an integer in seconds
            if isinstance(other, timedelta):
                return self.actual_time_required + other.actual_time_required #returns a timedelta object
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required + other.predicted_time_required #returns a timedelta
            if isinstance(other, (float, int)):
                return self.predicted_time_required + other.predicted_time_required.total_seconds() #returns an integer
            if isinstance(other, timedelta):
                return self.predicted_time_required + other.predicted_time_required #returns a timedelta
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                raise NotImplemented
            elif isinstance(other, Task):
                raise NotImplemented
            else:
                raise NotImplemented
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                raise NotImplementedError
            elif isinstance(other, (float, int)):
                raise NotImplementedError
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                raise NotImplemented
            elif isinstance(other, (float, int)):
                raise NotImplemented

    #Overloaded relational operators for task objects

    def __gt__(self, other):
        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required > other.actual_time_required
            if isinstance(other, (float,int)):
                return self.actual_time_required > other.actual_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.actual_time_required > other.actual_time_required
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required > other.predicted_time_required
            if isinstance(other, (float,int)):
                return self.predicted_time_required > other.predicted_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.predicted_time_required > other.predicted_time_required
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                return self.task_date > other
            elif isinstance(other, Task):
                return self.task_date > other.task_date
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                return self.difficulty_level > other.difficulty_level
            elif isinstance(other,(float,int)):
                return self.difficulty_level > other
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                return self.priority_level > other.priority_level
            elif isinstance(other, (float,int)):
                return self.priority_level > other.priority_level

    def __lt__(self, other):
        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required < other.actual_time_required
            if isinstance(other, (float,int)):
                return self.actual_time_required < other.actual_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.actual_time_required < other.actual_time_required
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required < other.predicted_time_required
            if isinstance(other, (float,int)):
                return self.predicted_time_required < other.predicted_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.predicted_time_required < other.predicted_time_required
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                return self.task_date < other
            elif isinstance(other, Task):
                return self.task_date < other.task_date
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                return self.difficulty_level < other.difficulty_level
            elif isinstance(other,(float,int)):
                return self.difficulty_level < other
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                return self.priority_level < other.priority_level
            elif isinstance(other, (float,int)):
                return self.priority_level < other.priority_level

    def __ge__(self, other):
        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required >= other.actual_time_required
            if isinstance(other, (float,int)):
                return self.actual_time_required >= other.actual_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.actual_time_required >= other.actual_time_required
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required >= other.predicted_time_required
            if isinstance(other, (float,int)):
                return self.predicted_time_required >= other.predicted_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.predicted_time_required >= other.predicted_time_required
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                return self.task_date >= other
            elif isinstance(other, Task):
                return self.task_date >= other.task_date
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                return self.difficulty_level >= other.difficulty_level
            elif isinstance(other,(float,int)):
                return self.difficulty_level >= other
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                return self.priority_level >= other.priority_level
            elif isinstance(other, (float,int)):
                return self.priority_level >= other.priority_level

    def __le__(self, other):
        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required >= other.actual_time_required
            if isinstance(other, (float,int)):
                return self.actual_time_required >= other.actual_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.actual_time_required >= other.actual_time_required
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required >= other.predicted_time_required
            if isinstance(other, (float,int)):
                return self.predicted_time_required >= other.predicted_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.predicted_time_required >= other.predicted_time_required
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                return self.task_date >= other
            elif isinstance(other, Task):
                return self.task_date >= other.task_date
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                return self.difficulty_level >= other.difficulty_level
            elif isinstance(other,(float,int)):
                return self.difficulty_level >= other
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                return self.priority_level >= other.priority_level
            elif isinstance(other, (float,int)):
                return self.priority_level >= other.priority_level

    def __eq__(self, other):
        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required == other.actual_time_required
            if isinstance(other, (float,int)):
                return self.actual_time_required == other.actual_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.actual_time_required == other.actual_time_required
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required == other.predicted_time_required
            if isinstance(other, (float,int)):
                return self.predicted_time_required == other.predicted_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.predicted_time_required == other.predicted_time_required
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                return self.task_date == other
            elif isinstance(other, Task):
                return self.task_date == other.task_date
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                return self.difficulty_level == other.difficulty_level
            elif isinstance(other,(float,int)):
                return self.difficulty_level == other
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                return self.priority_level == other.priority_level
            elif isinstance(other, (float,int)):
                return self.priority_level == other.priority_level

    def __ne__(self, other):
        if Task.sortingKey == 0:
            if isinstance(other, Task):
                return self.actual_time_required != other.actual_time_required
            if isinstance(other, (float,int)):
                return self.actual_time_required != other.actual_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.actual_time_required != other.actual_time_required
        elif Task.sortingKey == 1:
            if isinstance(other, Task):
                return self.predicted_time_required != other.predicted_time_required
            if isinstance(other, (float,int)):
                return self.predicted_time_required != other.predicted_time_required.total_seconds()
            if isinstance(other, timedelta):
                return self.predicted_time_required != other.predicted_time_required
        elif Task.sortingKey == 2:
            if isinstance(other, datetime.date):
                return self.task_date != other
            elif isinstance(other, Task):
                return self.task_date != other.task_date
        elif Task.sortingKey == 3:
            if isinstance(other, Task):
                return self.difficulty_level != other.difficulty_level
            elif isinstance(other,(float,int)):
                return self.difficulty_level != other
        elif Task.sortingKey == 4:
            if isinstance(other, Task):
                return self.priority_level != other.priority_level
            elif isinstance(other, (float,int)):
                return self.priority_level != other.priority_level

    def getSQLInsertStatement(self, table_name):
        '''Converts a task object into a SQL insert statement in order to allow for easy interfacing with MySQL
        clients and shells

        :param      table_name: Name of MySQL table into which the task object will loaded
        :return:    SQLInsertStatement: a MySQL InsertStatement that allows for task object data to be stored in a
                    MySQL database
        '''
        insert_statement = "INSERT INTO {}".format(table_name)
        insert_statement += "(name,"
        if self.description:
            insert_statement += "description,"

        if self.difficulty_level:
            insert_statement += "difficulty_level,"

        if self.priority_level:
            insert_statement += "priority_level,"

        #insert attributes here
        insert_statement += ")"

        insert_statement += "VALUES ("
        insert_statement += self.name + ","

        if self.description:
            insert_statement += self.description + ","

        if self.difficulty_level:
            insert_statement +=  str(self.difficulty_level) + ","

        if self.priority_level:
            insert_statement += str(self.priority_level)  + ","

        insert_statement += str(self.task_date) + ","
        insert_statement += str(self.predicted_time_required) + "," #default value for predicted time required is 00:00:00
        insert_statement += str(self.actual_time_required) + "," #efault value for actual time required is 00:00:00
        insert_statement += str(self.completed)
        #insert values here
        insert_statement += ");"
        return insert_statement

    def __str__(self):
        output_str = "Task Name: {}".format(self.name)
        if self.description:
            output_str += "Task Description: {}".format(self.description)
        if self.difficulty_level:
            output_str += "Difficult Level: {}".format(str(self.difficulty_level))
        if self.priority_level:
            output_str += "Priority Level: {}".format(str(self.priority_level))
        output_str += "Task Date: {}".format(self.task_date)
        output_str += "Actual Time Required: {}".format(self.actual_time_required)
        output_str += "Predicted Time Required: {}".format(self.predicted_time_required)
        status = ""
        if self.completed:
            status = "True"
        else:
            status = "False"
        output_str += "Completion Status: {}".format(self.completed)
        return output_str

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    task1 = Task("Do laundry",
                 "Wash and dry all whites, towels, and bedding in separate washes; "
                 "use bleach on whites, low-heat or no heat for delicates",
                5,      #difficulty_level
                5,     #priority_level
                datetime.date(year=2017,month=1,day=20),
                datetime.time(hours=1,minutes=30,seconds=0),
                datetime.time(hours=0,minutes=0,seconds=0),
                False)  #completion_status