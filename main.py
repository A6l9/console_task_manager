import click
import csv
import os
from typing import Optional

from pydantic import ValidationError
from validate_models import Task, TaskForChange
from pprint import pprint
from typing import Union

class TaskManager:

    def __init__(self):
        self.main.add_command(self.add_task)
        self.main.add_command(self.get_list_tasks)
        self.main.add_command(self.change_task)

    @click.group()
    def main() -> None:
        pass

    @click.command('task-manager-list', help='Show list tasks')
    @click.option('--category', help='Viewing list of tasks: [String]', type=str)
    def get_list_tasks(category: Optional[str]) -> None:
        if os.path.exists('misc/task_data.csv'):
            with open('misc/task_data.csv', 'r') as file_for_read:
                reader = csv.DictReader(file_for_read)
                task_exists = False
                data = list(reader)
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
        try:
            data = Task(title=title, description=description, category=category, due_date=due_date, priority=priority, status=status)
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
    @click.option('--d', 'description', help='Description: Optional[String], format: "Some text"', type=str)
    @click.option('--c', 'category', help='Category: String, format: "Some text"', type=str)
    @click.option('--dd', 'due_date', help='Due date: Date, format: "%Y-%m-%d"', type=str)
    @click.option('--p', 'priority', help='Priority: String, format: ["High", "Medium", "Low"]', type=str)
    @click.option('--s', 'status', help='Status: Boolean, format: ["True", "False"]', type=str)
    def change_task(id: int, title: Union[str, None], description: Union[str, None], 
                    category: Union[str, None], due_date: Union[str, None], priority: Union[str, None], status: Union[str, None]):
        try:
            data = TaskForChange(id=id, title=title, description=description, 
                                 category=category, due_date=due_date, priority=priority, status=status)
        except (TypeError, ValueError) as exc:
            click.echo(f"{exc.__class__.__name__}: {exc}")
            return
        data = data.model_dump()
        print(data)
        if os.path.exists('misc/task_data.csv'):
            with open('misc/task_data.csv', 'r') as file_for_read:
                reader = csv.DictReader(file_for_read)
                list_data = list(reader)
                if len(list_data) >= id and id > 0:
                    if title:
                        list_data[id - 1]['title'] = title
                    if description:
                        list_data[id - 1]['description'] = description
                    if category:
                        list_data[id - 1]['category'] = category
                    if due_date:
                        list_data[id - 1]['due_date'] = due_date
                    if priority:
                        list_data[id - 1]['priority'] = priority
                    if status:
                        list_data[id - 1]['status'] = status
                    with open('misc/task_data2.csv', 'w') as file_for_write:
                        writer = csv.DictWriter(f=file_for_write, fieldnames=['id', 'title', 'description', 'category', 
                                                                  'due_date', 'priority', 'status'])
                        writer.writeheader()
                        writer.writerows(list_data)
                        os.remove('misc/task_data.csv')
                        os.rename('misc/task_data2.csv', 'misc/task_data.csv')
                else:
                    raise ValueError('Invalid task ID')


if __name__ == '__main__':
    task_manager = TaskManager()    
    task_manager.main()
