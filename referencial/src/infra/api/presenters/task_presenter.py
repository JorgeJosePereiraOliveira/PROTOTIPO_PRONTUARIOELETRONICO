import xml.etree.ElementTree as ET
from application.task.find_task.find_task_dto import FindTaskOutputDto


class TaskPresenter:

    @staticmethod
    def toJSON(task: FindTaskOutputDto) -> dict:
        return {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
        }

    @staticmethod
    def toXML(task: FindTaskOutputDto) -> str:
        task_data = ET.Element("task")
        ET.SubElement(task_data, "id").text = str(task.id)
        ET.SubElement(task_data, "user_id").text = str(task.user_id)
        ET.SubElement(task_data, "title").text = task.title
        ET.SubElement(task_data, "description").text = task.description
        ET.SubElement(task_data, "completed").text = str(task.completed).lower()
        return ET.tostring(task_data, encoding="unicode")
