import requests
from ..config import API_BASE

def get_answers(question_id):
    return requests.get(
        f"{API_BASE}/answers/{question_id}"
    ).json()

def toggle_star(answer_id):
    requests.post(
        f"{API_BASE}/star/{answer_id}"
    )