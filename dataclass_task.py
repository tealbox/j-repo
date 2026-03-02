from dataclasses import dataclass, field
from typing import List, Optional

task_json = {
    "message": "Task Message",
    "status": "Completed",
    "result": {
        "count": 1,
        "pagination": {
            "has_next": True,
            "next": "https://IP/task/id"
        },
        "data": [
            {
                "_ref": "https://_ref/URL",
                "name": "wf_proj"
            }
        ]
    }
}

@dataclass
class Item:
    _ref: str
    name: str

@dataclass
class Pagination:
    has_next: bool
    next: Optional[str] = None

@dataclass
class Result:
    count: int
    pagination: Pagination
    data: List[Item]

@dataclass
class TaskResponse:
    message: str
    status: str
    result: Result

    @classmethod
    def from_dict(cls, data: dict) -> 'TaskResponse':
        """Convert dict to TaskResponse object"""
        result_data = data.get('result', {})
        return cls(
            message=data.get('message'),
            status=data.get('status'),
            result=Result(
                count=result_data.get('count'),
                pagination=Pagination(
                    has_next=result_data.get('pagination', {}).get('has_next'),
                    next=result_data.get('pagination', {}).get('next')
                ),
                data=[
                    Item(**item) for item in result_data.get('data', [])
                ]
            )
        )

##task = TaskResponse.from_dict(response.json())

task = TaskResponse.from_dict(task_json)

# Access with attribute syntax
print(task.message)                    # "Task Message"
print(task.status)                     # "Completed"
print(task.result.count)               # 1
print(task.result.pagination.has_next) # True
print(task.result.pagination.next)     # "https://IP/task/id"
print(task.result.data[0].name)        # "wf_proj"
print(task.result.data[0]._ref)        # "https://_ref/URL"


