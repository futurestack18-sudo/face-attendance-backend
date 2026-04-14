from pydantic import BaseModel

class Attendance(BaseModel):
    name: str
    date: str
    time: str