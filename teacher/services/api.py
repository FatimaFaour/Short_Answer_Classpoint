import requests
from ..config import API_BASE

def get_answers(question_id):
    try:
        response = requests.get(
            f"{API_BASE}/answers/{question_id}",
            timeout=5,
        )
        if not response.ok:
            return []
        try:
            return response.json()
        except ValueError:
            return []
    except requests.RequestException:
        return []
def toggle_star(answer_id):
    try:
        requests.post(
            f"{API_BASE}/star/{answer_id}",
            timeout=5,
        )
    except requests.RequestException:
        return