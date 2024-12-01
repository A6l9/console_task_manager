import click
import csv
import os
from typing import Optional

from validate_models import TaskModel, TaskModelForChange, TaskModelForRemove, TaskModelForSearch
from typing import Union
import re

class TaskManager:
    """
    The task manager class
    """
    def __init__(self):
        self.main.add_command(self.add_task)
        self.main.add_command(self.get_list_tasks)
        self.main.add_command(self.change_task)
        self.main.add_command(self.remove_task)
        self.main.add_command(self.task_search)

    @click.group()
    def main() -> None:
        """
        A function that groups commands 
        for the task manager
        """
        pass

    @click.command('task-manager-list', help='Show list tasks')
    @click.option('--category', help='Viewing list of tasks: [String]', type=str)
    def get_list_tasks(category: Optional[str]) -> None:
        """
        Viewing the task list
        parameters:
            category: Optional[str] - Category of the task
        return: None
        """
        if os.path.exists('misc/task_data.csv'):
            with open('misc/task_data.csv', 'r') as file_for_read:
                reader = csv.DictReader(file_for_read)
                task_exists = False
                data = list(reader)
                if len(data) == 0:
                    click.echo('No tasks found.')
                    return
                data.insert(0, reader.fieldnames)
                for row in data:
                    if category:
                        if isinstance(row, list):
                            click.echo(' | '.join(row))
                        elif row['category'].lower() == category.lower():
                            task_exists = True
                            click.echo(f'{row["id"]} | {row["title"]} | '
                                    f'{row['description']} | {row['category']} | '
                                    f'{row['due_date']} | {row['priority']} | '
                                    f'{row['status']}')
                    else:
                        if isinstance(row, list):
                            click.echo(' | '.join(row))
                        else:
                            click.echo(f'{row["id"]} | {row["title"]} | '
                                    f'{row['description']} | {row['category']} | '
                                    f'{row['due_date']} | {row['priority']} | '
                                    f'{row['status']}')
                if not task_exists and category:
                    click.echo('No tasks found in this category.')
        else:
            click.echo('No tasks found.')
    
    @click.command('task-manager-add', help='Add a new task')
    @click.option('--t', 'title', help='Title: String, format: "Some text"', type=str)
    @click.option('--d', 'description', help='Description: Optional[String], format: "Some text"', type=str)
    @click.option('--c', 'category', help='Category: String, format: "Some text"', type=str)
    @click.option('--dd', 'due_date', help='Due date: Date, format: "%Y-%m-%d"', type=str)
    @click.option('--p', 'priority', help='Priority: String, format: ["High", "Medium", "Low"]', type=str)
    @click.option('--s', 'status', help='Status: Boolean, format: ["True", "False"]', type=str)
    def add_task(title: str, description: str, category: str, due_date: str, priority: str, status: str) -> None:
        """
        Adding a new task to the list
        
        parameters:
            title: str - Title of the task
            description: str - Description of the task
            category: str - Category of the task
            due_date: str - Due date of the task
            priority: str - Priority of the task
            status: str - Status of the task
        return: None
        """
        try:
            data = TaskModel(title=title, description=description, category=category, due_date=due_date, priority=priority, status=status)
        except (TypeError, ValueError) as exc:
            click.echo(f"{exc.__class__.__name__}: {exc}")
            return
        data = data.model_dump()
        file_exists = os.path.exists('misc/task_data.csv')
        with open('misc/task_data.csv', 'a') as file_for_write:
            writer = csv.DictWriter(f=file_for_write, fieldnames=['id', 'title', 'description', 'category', 
                                                                  'due_date', 'priority', 'status'])
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    
    @click.command('task-manager-edit', help='Editing a task')
    @click.option('--id', 'id', help='ID of the task, type: Integer', type=int)
    @click.option('--t', 'title', help='Title: String, format: "Some text"', type=str)
    @click.option('--d', 'description', help='Description: String, format: "Some text"', type=str)
    @click.option('--c', 'category', help='Category: String, format: "Some text"', type=str)
    @click.option('--dd', 'due_date', help='Due date: Date, format: "%Y-%m-%d"', type=str)
    @click.option('--p', 'priority', help='Priority: String, format: ["High", "Medium", "Low"]', type=str)
    @click.option('--s', 'status', help='Status: Boolean, format: ["True", "False"]', type=str)
    def change_task(id: int, title: Union[str, None], description: Union[str, None], 
                    category: Union[str, None], due_date: Union[str, None], priority: Union[str, None], status: Union[str, None]) -> None:
        """
        Changing the status of a task or any 
        of its other parameters
        parameters:
            id: int - ID of the task
            title: str - Title of the task
            description: str - Description of the task
            category: str - Category of the task
            due_date: str - Due date of the task
            priority: str - Priority of the task
            status: str - Status of the task
        return: None
        """
        try:
            data = TaskModelForChange(id=id, title=title, description=description, 
                                 category=category, due_date=due_date, priority=priority, status=status)
        except (TypeError, ValueError) as exc:
            click.echo(f"{exc.__class__.__name__}: {exc}")
            return
        data = data.model_dump()
        if os.path.exists('misc/task_data.csv'):
            with open('misc/task_data.csv', 'r') as file_for_read:
                reader = csv.DictReader(file_for_read)
                list_data = list(reader)
                if id in [int(i['id']) for i in list_data]:
                    if title:
                        list_data[id - 1]['title'] = data['title']
                    if description:
                        list_data[id - 1]['description'] = data['description']
                    if category:
                        list_data[id - 1]['category'] = data['category']
                    if due_date:
                        list_data[id - 1]['due_date'] = data['due_date']
                    if priority:
                        list_data[id - 1]['priority'] = data['priority']
                    if status:
                        list_data[id - 1]['status'] = data['status']
                    with open('misc/task_data2.csv', 'w') as file_for_write:
                        writer = csv.DictWriter(f=file_for_write, fieldnames=['id', 'title', 'description', 'category', 
                                                                  'due_date', 'priority', 'status'])
                        writer.writeheader()
                        writer.writerows(list_data)
                        os.remove('misc/task_data.csv')
                        os.rename('misc/task_data2.csv', 'misc/task_data.csv')
                else:
                    click.echo('Invalid task ID')
        else:
            click.echo('No tasks found.')

    @click.command('task-manager-remove', help='Removing a task')
    @click.option('--id', 'id', help='ID of the task, type: Integer', type=int)
    @click.option('--c', 'category', help='Category: String, format: "Some text"', type=str)
    def remove_task(id: Union[int, None], category: Union[str, None]) -> None:
        """
        Removing tasks by ID or category
        parameters:
            id: int - ID of the task
            category: str - Category of the task
        return: None
        """
        try:
            data = TaskModelForRemove(id=id, category=category)
        except(TypeError, ValueError) as exc:
            click.echo(f"{exc.__class__.__name__}: {exc}")
            return
        data = data.model_dump()
        if os.path.exists('misc/task_data.csv'):
            with open('misc/task_data.csv', 'r') as file_for_read:
                reader = csv.DictReader(file_for_read)
                list_data = list(reader)
                if data['id']:
                    if id in [int(i['id']) for i in list_data]:
                        list_data = [i for i in list_data if int(i['id']) != id]
                        with open('misc/task_data2.csv', 'w') as file_for_write:
                            writer = csv.DictWriter(f=file_for_write, fieldnames=['id', 'title', 'description', 'category', 
                                                                    'due_date', 'priority', 'status'])
                            writer.writeheader()
                            writer.writerows(list_data)
                            os.remove('misc/task_data.csv')
                            os.rename('misc/task_data2.csv', 'misc/task_data.csv')
                    else:
                        click.echo('Invalid task ID')
                elif data['category']:
                    pattern = re.compile(r'\b{}\b'.format(re.escape(category)), re.IGNORECASE)
                    list_search = [i for i in list_data if bool(pattern.search(i['category']))]
                    if len(list_search) != 0:
                        list_data = [i for i in list_data if i not in list_search]
                        with open('misc/task_data2.csv', 'w') as file_for_write:
                            writer = csv.DictWriter(f=file_for_write, fieldnames=['id', 'title', 'description', 'category', 
                                                                    'due_date', 'priority', 'status'])
                            writer.writeheader()
                            writer.writerows(list_data)
                            os.remove('misc/task_data.csv')
                            os.rename('misc/task_data2.csv', 'misc/task_data.csv')
                    else:
                        click.echo('No tasks found in this category.')
                else:
                    click.echo('The ID or category was not specified')
        else:
            click.echo('No tasks found.')
    
    @click.command('task-manager-search', help='Task search')
    @click.option('--kw', 'keyword', help='Search by keywords', type=str)
    @click.option('--c', 'category', help='Search by category', type=str)
    @click.option('--s', 'status', help='Search by status', type=str)
    def task_search(keyword: Union[str, None], category: Union[str, None], status: Union[str, None]) -> None:
        """
        Search for tasks by keywords in the title 
        or description, search by category or status
        parameters:
            keyword: str - Keywords to search in the title or description
            category: str - Category of the task
            status: str - Status of the task
        return: None
        """
        try:
            data = TaskModelForSearch(keyword=keyword, category=category, status=status)
        except(TypeError, ValueError) as exc:
            click.echo(f"{exc.__class__.__name__}: {exc}")
            return
        data = data.model_dump()
        if os.path.exists('misc/task_data.csv'):
            with open('misc/task_data.csv', 'r') as file_for_read:
                reader = csv.DictReader(file_for_read)
                task_exists = False
                tasks_data = list(reader)
                if len(tasks_data) == 0:
                    click.echo('No tasks found.')
                    return
                tasks_data.insert(0, reader.fieldnames)
                for row in tasks_data:
                    if data['keyword']:
                        pattern = re.compile(r'\b{}\b'.format(re.escape(data['keyword'])), re.IGNORECASE)
                        if isinstance(row, list): 
                            click.echo(' | '.join(row))
                        elif bool(pattern.search(row['title'])) or bool(pattern.search(row['description'])):
                            task_exists = True
                            click.echo(f'{row["id"]} | {row["title"]} | '
                                    f'{row['description']} | {row['category']} | '
                                    f'{row['due_date']} | {row['priority']} | '
                                    f'{row['status']}')
                    elif data['category']:
                        pattern = re.compile(r'\b{}\b'.format(re.escape(data['category'])), re.IGNORECASE)
                        if isinstance(row, list):
                            click.echo(' | '.join(row))
                        elif bool(pattern.search(row['category'])):
                            task_exists = True
                            click.echo(f'{row["id"]} | {row["title"]} | '
                                    f'{row['description']} | {row['category']} | '
                                    f'{row['due_date']} | {row['priority']} | '
                                    f'{row['status']}')
                    elif data['status']:
                        if isinstance(row, list):
                            click.echo(' | '.join(row))
                        elif data['status'].lower() == row['status'].lower():
                            task_exists = True
                            click.echo(f'{row["id"]} | {row["title"]} | '
                                    f'{row['description']} | {row['category']} | '
                                    f'{row['due_date']} | {row['priority']} | '
                                    f'{row['status']}')
                    else:
                        click.echo('The status, category or keyword was not specified')
                        return
                if not task_exists:
                    click.echo('No tasks were found for the specified parameters')
        else:
            click.echo('No tasks found.')
        

if __name__ == '__main__':
    task_manager = TaskManager()    
    task_manager.main()
