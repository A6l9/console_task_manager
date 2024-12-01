from datetime import date
from pydantic import BaseModel, Field, field_validator, model_validator
import os
import csv
from typing import Union


class TaskModel(BaseModel):
    """
    A model for validating input data for the add_task() function
    """
    id: int = Field(name='id', default_factory=lambda: TaskModel.generate_id())
    title: str = Field(name='title')
    description: str = Field(name='description')
    category: str = Field(name='category')
    due_date: date = Field(name='due_date')
    priority: str = Field(name='priority')
    status: str = Field(name='status')


    @model_validator(mode='before')
    @classmethod
    def check_parameters(cls, values: dict) -> dict:
        """
        Checks whether the required parameters have been passed
        """
        if not values['title'].strip():
            raise TypeError("The title is mandatory")
        if not values['category'].strip():
            raise TypeError("The category is mandatory")
        if not values['due_date']:
            raise TypeError("The due date is mandatory")
        if not values['priority']:
            raise TypeError("The priority is mandatory")
        if not values['status']:
            raise TypeError("The status is mandatory")
        return values
    
    @classmethod
    def generate_id(cls) -> int:
        """
        Generates a unique ID for the task
        """
        file_exists = os.path.exists('misc/task_data.csv')
        if not file_exists:
            with open('misc/task_data.csv', 'a') as file_for_write:
                writer = csv.DictWriter(f=file_for_write, fieldnames=['id', 'title', 'description', 'category', 
                                                                    'due_date', 'priority', 'status'])
                if not file_exists:
                    writer.writeheader()
        with open('misc/task_data.csv', 'r') as file_for_read:
            reader = csv.DictReader(file_for_read)
            return len(list(reader)) + 1

    @field_validator('due_date', mode='after')
    @classmethod
    def check_date(cls, due_date: date) -> date:
        """
        Checks whether the date was transmitted correctly
        """
        if due_date < date.today():
            raise ValueError("Due date must be in the future or present")
        return due_date

    @field_validator('priority', mode='before')
    @classmethod
    def check_priority(cls, value: str) -> str:
        """
        Checks whether the priority corresponds to the correct values
        """
        if value.lower() not in ['high', 'medium', 'low']:
            raise ValueError("Priority must be 'High', 'Medium', or 'Low'")
        return value.title()

    @field_validator('description', mode='before')
    @classmethod
    def validate_description(cls, value: str) -> str:
        """
        Checks the passed task description, 
        if the description was not passed, returns the default value
        """
        if not value:
            value = 'Not specified' 
        return value

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, value: str) -> str:
        """
        Checks whether the status corresponds to the correct values
        """
        if value not in ['True', 'False']:
            raise ValueError("Status must be 'True' or 'False'")
        return value


class TaskModelForChange(BaseModel):
    id: int = Field(name='id')
    title: Union[str, None] = Field(name='title')
    description: Union[str, None] = Field(name='description')
    category: Union[str, None] = Field(name='category')
    due_date: Union[date, None] = Field(name='due_date')
    priority: Union[str, None] = Field(name='priority')
    status: Union[str, None] = Field(name='status')

    @model_validator(mode='before')
    @classmethod
    def check_parameters(cls, values: dict) -> dict:
        """
        Checks whether whitespace characters 
        have been passed instead of parameters
        """
        if values['title']:
            if values['title'].strip() == '':
                raise TypeError("The title cannot be a space character")
        if values['description']:
            if values['description'].strip() == '':
                raise TypeError("The description cannot be a space character")
        if values['category']:
            if values['category'].strip() == '':
                raise TypeError("The category cannot be a space character")
        return values

    @field_validator('due_date', mode='after')
    @classmethod
    def check_date(cls, due_date: date) -> Union[date, None]:
        """
        Checks whether the date was transmitted correctly
        """
        if not due_date:
            return None
        if due_date < date.today():
            raise ValueError("Due date must be in the future or present")
        return due_date

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, value: str) -> Union[str, None]:
        """
        Checks whether the status corresponds to the correct values
        """
        if not value:
            return None
        if value not in ['True', 'False']:
            raise ValueError("Status must be 'True' or 'False'")
        return value
    
    @field_validator('priority', mode='before')
    @classmethod
    def validate_priority(cls, value: str) -> Union[str, None]:
        """
        Checks whether the priority corresponds to the correct values
        """
        if not value:
            return None
        if value.lower() not in ['high', 'medium', 'low']:
            raise ValueError("Priority must be 'High', 'Medium', or 'Low'")
        return value.title()


class TaskModelForRemove(BaseModel):
    """
    A model for validating input data for the remove_task() function
    """
    id: Union[int, None] = Field(name='id')
    category: Union[str, None] = Field(name='category')

class TaskModelForSearch(BaseModel):
    """
    A model for validating input data for the task_search() function
    """
    keyword: Union[str, None] = Field(name='keyword')
    category: Union[str, None] = Field(name='category')
    status: Union[str, None] = Field(name='status')

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, value: str) -> Union[str, None]:
        """
        Checks whether the status corresponds to the correct values
        """
        if not value:
            return None
        if value not in ['True', 'False']:
            raise ValueError("Status must be 'True' or 'False'")
        return value
    