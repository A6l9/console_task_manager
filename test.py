from typing import Generator
from main import TaskManager
import pytest
import os
import csv
from click.testing import CliRunner



task_manger = TaskManager()


@pytest.fixture(autouse=True)
def mock_task_data():
    mock_data = [
        {"id": "1", "title": "Task 1", "description": "Description 1", "category": "Work", "due_date": "2024-12-05", "priority": "High", "status": "True"},
        {"id": "2", "title": "Task 2", "description": "Description 2", "category": "Personal", "due_date": "2024-12-06", "priority": "Medium", "status": "False"},
        {"id": "3", "title": "Task 3", "description": "Description 3", "category": "Work", "due_date": "2024-12-07", "priority": "Low", "status": "True"},
    ]
    with open('misc/task_data.csv', 'w') as file_for_write:
        writer = csv.DictWriter(file_for_write, fieldnames=["id", "title", "description", 
                                                            "category", "due_date", "priority", "status"])
        writer.writeheader()
        writer.writerows(mock_data)


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


def test_get_list_tasks_no_category(runner: CliRunner) -> None:
    result = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result.exit_code == 0
    assert "Task 1" in result.stdout
    assert "Task 2" in result.stdout
    assert "Task 3" in result.stdout


def test_get_list_tasks_with_category(runner: CliRunner) -> None:
    result = runner.invoke(cli=task_manger.get_list_tasks, args=['--category', 'Work'])
    
    assert result.exit_code == 0
    assert "Task 1" in result.stdout
    assert "Task 3" in result.stdout
    assert "Task 2" not in result.stdout


def test_get_list_tasks_no_tasks(runner: CliRunner) -> None:
    with open('misc/task_data.csv', 'w', newline='') as file:
        file.truncate(0)

    result = runner.invoke(task_manger.get_list_tasks)
    
    assert result.exit_code == 0
    assert "No tasks found." in result.stdout


def test_get_list_tasks_invalid_category(runner: CliRunner) -> None:
    result = runner.invoke(cli=task_manger.get_list_tasks, args=['--category', 'NonExistingCategory'])
    
    assert result.exit_code == 0
    assert "No tasks found in this category." in result.stdout


def test_add_task_valid_input(runner: CliRunner) -> None:
    result_with_description = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 4', '--d', 'Description 4',
                                                '--c', 'Study', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    result_without_description = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 5', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'High', '--s', 'True'])
    result_tasks_list = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result_with_description.exit_code == 0
    assert result_without_description.exit_code == 0
    assert 'Task 4' in result_tasks_list.stdout
    assert 'Task 5' in result_tasks_list.stdout


def test_add_task_invalid_input(runner: CliRunner) -> None:
    result_invalid_date = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 4', '--d', 'Description 4',
                                                '--c', 'Study', '--dd', '2024-13-04', '--p', 'Low', '--s', 'False'])
    result_invalid_priority = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 5', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'Priority', '--s', 'True'])
    result_invalid_status = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 6', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'High', '--s', 'Complete'])
    result_tasks_list = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result_invalid_date.exit_code == 0
    assert result_invalid_priority.exit_code == 0
    assert result_invalid_status.exit_code == 0
    #checking that an exception was caused
    assert 'ValidationError' in result_invalid_date.stdout
    assert 'ValidationError' in result_invalid_priority.stdout
    assert 'ValidationError' in result_invalid_status.stdout
    #Сhecking the task list for incorrect tasks
    assert 'Task 4' not in result_tasks_list.stdout
    assert 'Task 5' not in result_tasks_list.stdout
    assert 'Task 6' not in result_tasks_list.stdout


def test_add_task_missing_parameters(runner: CliRunner) -> None:
    result_missing_title = runner.invoke(cli=task_manger.add_task, args=['--t', '', '--d', 'Description 3',
                                                '--c', 'Study', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    result_missing_description = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 4', '--d', '',
                                                '--c', 'Study', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    result_missing_category = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 5', '--d', 'Description 5',
                                                '--c', '', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    result_missing_date = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 6', '--d', 'Description 6',
                                                '--c', 'Study', '--dd', '', '--p', 'Low', '--s', 'False'])
    result_missing_priority = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 7', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', '', '--s', 'True'])
    result_missing_status = runner.invoke(cli=task_manger.add_task, args=['--t', 'Task 8', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'High', '--s', ''])
    result_tasks_list = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result_missing_title.exit_code == 0
    assert result_missing_description.exit_code == 0
    assert result_missing_category.exit_code == 0
    assert result_missing_date.exit_code == 0
    assert result_missing_priority.exit_code == 0
    assert result_missing_status.exit_code == 0
    #checking that an exception was caused
    assert 'TypeError' in result_missing_title.stdout
    assert 'TypeError' in result_missing_category.stdout
    assert 'TypeError' in result_missing_date.stdout
    assert 'TypeError' in result_missing_priority.stdout
    assert 'TypeError' in result_missing_status.stdout
    #Сhecking the task list for incorrect tasks
    assert 'Task 5' not in result_tasks_list.stdout
    assert 'Task 6' not in result_tasks_list.stdout
    assert 'Task 7' not in result_tasks_list.stdout
    assert 'Task 8' not in result_tasks_list.stdout
    #check if the task with the default description has been added
    assert '| Task 4 | Not specified |' in result_tasks_list.stdout


def test_edit_task_valid_input(runner: CliRunner) -> None:
    result_change_all_data = runner.invoke(cli=task_manger.change_task, args=['--id', '1', '--t', 'Task 4', '--d', 'Description 4',
                                                '--c', 'Study', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    result_change_status = runner.invoke(cli=task_manger.change_task, args=['--id', '2', '--t', 'Task 5',
                                                '--c', 'Study', '--dd', '2024-12-05', '--p', 'High', '--s', 'True'])
    result_change_date = runner.invoke(cli=task_manger.change_task, args=['--id', '3', '--t', 'Task 6',
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'High', '--s', 'True'])
    result_tasks_list = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result_change_all_data.exit_code == 0
    assert result_change_status.exit_code == 0
    assert result_change_date.exit_code == 0
    assert 'Task 4' in result_tasks_list.stdout
    assert 'Task 5' in result_tasks_list.stdout
    assert 'Task 6' in result_tasks_list.stdout
    assert '2024-12-03' in result_tasks_list.stdout


def test_edit_task_invalid_input(runner: CliRunner) -> None:
    result_empty_input = runner.invoke(cli=task_manger.change_task, args=['--id', '1', '--t', '', '--d', 'Description 1',
                                                '--c', 'Study', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    result_space_character = runner.invoke(cli=task_manger.change_task, args=['--id', '2', '--t', '           ', 
                                                '--c', '', '--dd', '2024-12-03', '--p', '', '--s', ''])
    result_invalid_date = runner.invoke(cli=task_manger.change_task, args=['--id', '1', '--t', 'Task 6', 
                                                '--c', 'Study', '--dd', '2024-11-03', '--p', 'High', '--s', 'True'])
    result_invalid_status = runner.invoke(cli=task_manger.change_task, args=['--id', '2', '--t', 'Task 7', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'High', '--s', 'Complete'])
    result_invalid_priority = runner.invoke(cli=task_manger.change_task, args=['--id', '3', '--t', 'Task 8', 
                                                '--c', 'Study', '--dd', '2024-12-03', '--p', 'None', '--s', 'True'])
    result_tasks_list = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result_empty_input.exit_code == 0
    assert result_space_character.exit_code == 0
    assert result_invalid_date.exit_code == 0
    assert result_invalid_status.exit_code == 0
    assert result_invalid_priority.exit_code == 0
    assert 'TypeError' in result_space_character.stdout
    assert 'ValidationError' in result_invalid_date.stdout
    assert 'ValidationError' in result_invalid_status.stdout
    assert 'ValidationError' in result_invalid_priority.stdout
    assert 'Task 1' in result_tasks_list.stdout
    assert 'Task 2' in result_tasks_list.stdout
    assert 'Task 6' not in result_tasks_list.stdout
    assert 'Task 7' not in result_tasks_list.stdout
    assert 'Task 8' not in result_tasks_list.stdout


def test_edit_task_no_tasks(runner: CliRunner) -> None:
    with open('misc/task_data.csv', 'w', newline='') as file:
        file.truncate(0)

    result = runner.invoke(cli=task_manger.change_task, args=['--id', '1', '--t', 'Task 4', '--d', 'Description 4',
                                                 '--c', 'Study', '--dd', '2024-12-04', '--p', 'Low', '--s', 'False'])
    
    assert result.exit_code == 0
    assert "Invalid task ID" in result.stdout


def test_remove_task_valid_input(runner: CliRunner) -> None:
    result_remove_by_id = runner.invoke(cli=task_manger.remove_task, args=['--id', '2'])
    result_remove_by_category = runner.invoke(cli=task_manger.remove_task, args=['--c', 'Work'])
    result_tasks_list = runner.invoke(cli=task_manger.get_list_tasks, args=[])
    assert result_remove_by_id.exit_code == 0
    assert result_remove_by_category.exit_code == 0
    assert 'No tasks found.' in result_tasks_list.stdout


def test_remove_task_invalid_input(runner: CliRunner) -> None:
    result_non_existent_id = runner.invoke(cli=task_manger.remove_task, args=['--id', '32'])
    result_invalid_id = runner.invoke(cli=task_manger.remove_task, args=['--id', '32ID'])
    result_non_existent_category = runner.invoke(cli=task_manger.remove_task, args=['--c', 'Games'])
    assert result_non_existent_id.exit_code == 0
    assert result_invalid_id.exit_code == 2
    assert result_non_existent_category.exit_code == 0
    assert 'Invalid task ID' in result_non_existent_id.stdout
    assert 'Error' in result_invalid_id.stdout
    assert 'No tasks found in this category.' in result_non_existent_category.stdout


def test_remove_task_no_tasks(runner: CliRunner) -> None:
    with open('misc/task_data.csv', 'w', newline='') as file:
        file.truncate(0)

    result = runner.invoke(cli=task_manger.remove_task, args=['--id', '2'])
    
    assert result.exit_code == 0
    assert "Invalid task ID" in result.stdout


def test_search_task_valid_input(runner: CliRunner) -> None:
    result_search_by_keyword1 = runner.invoke(cli=task_manger.task_search, args=['--kw', 'Task 2'])
    result_search_by_keyword2 = runner.invoke(cli=task_manger.task_search, args=['--kw', '1'])
    result_search_by_category = runner.invoke(cli=task_manger.task_search, args=['--c', 'Work'])
    result_search_by_status = runner.invoke(cli=task_manger.task_search, args=['--s', 'False'])
    assert result_search_by_keyword1.exit_code == 0
    assert result_search_by_keyword2.exit_code == 0
    assert result_search_by_category.exit_code == 0
    assert result_search_by_status.exit_code == 0
    assert 'Task 2' in result_search_by_keyword1.stdout
    assert 'Task 1' in result_search_by_keyword2.stdout
    assert 'Task 1' in result_search_by_category.stdout
    assert 'Task 3' in result_search_by_category.stdout
    assert 'Task 2' in result_search_by_status.stdout


def test_search_task_invalid_input(runner: CliRunner) -> None:
    result_search_by_keyword1 = runner.invoke(cli=task_manger.task_search, args=['--kw', 'Task 36'])
    result_search_by_keyword2 = runner.invoke(cli=task_manger.task_search, args=['--kw', '112'])
    result_remove_by_category = runner.invoke(cli=task_manger.task_search, args=['--c', 'KWork'])
    result_remove_by_invalid_status = runner.invoke(cli=task_manger.task_search, args=['--s', 'Falses'])
    assert result_search_by_keyword1.exit_code == 0
    assert result_search_by_keyword2.exit_code == 0
    assert result_remove_by_category.exit_code == 0
    assert result_remove_by_invalid_status.exit_code == 0
    assert 'No tasks were found for the specified parameters' in result_search_by_keyword1.stdout
    assert 'No tasks were found for the specified parameters' in result_search_by_keyword2.stdout
    assert 'No tasks were found for the specified parameters' in result_remove_by_category.stdout
    assert 'No tasks were found for the specified parameters' in result_remove_by_category.stdout
    assert 'ValidationError' in result_remove_by_invalid_status.stdout


def test_search_task_no_tasks(runner: CliRunner) -> None:
    with open('misc/task_data.csv', 'w', newline='') as file:
        file.truncate(0)

    result = runner.invoke(cli=task_manger.task_search, args=['--kw', 'Task 2'])
    
    assert result.exit_code == 0
    assert "No tasks found." in result.stdout


@pytest.fixture(autouse=True)
def cleanup() -> Generator[None]:
    yield
    if os.path.exists('misc/task_data.csv'):
        os.remove('misc/task_data.csv')
