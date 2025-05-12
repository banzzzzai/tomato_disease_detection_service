from celery import current_app as current_celery_app


def get_task_info(task_id: str) -> dict:
    """
    :param task_id - номер таски
    :return: Возвращает статус таски по id
    """
    task_result = current_celery_app.AsyncResult(task_id)
    if not task_result.info:
        result = {"error": "not found"}
    else:
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result,
        }
    return result
