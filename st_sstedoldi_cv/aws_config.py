
aws_agent_info = {
    "AWS_KEY": "", # AWS Access Key ID - Saul Good AI
    "AWS_SECRET": "", # AWS Secret Access Key - Saul Good AI
    "REGION": "us-east-1",
    "AGENT_ID": "4EPNZWKAQL",
    "AGENT_ALIAS_ID": "PLDM3BMU5L",
    "KNOWLEDGE_BASE_ID": "BYQKNMPG1N",
    "LLM_ID": "meta.llama3-3-70b-instruct-v1:0",
    "MAX_QUESTIONS_PER_HOUR": 10,
    # "MAX_QUESTIONS_PER_IP": 5,
}

from collections import deque
from datetime import datetime, timedelta

_request_times = deque()  # holds datetime of each request

def allow_request(MAX_REQUESTS_PER_HOUR: int) -> bool:
    """
    Returns True if we can accept another request (under the hourly cap),
    False if we've hit MAX_REQUESTS_PER_HOUR in the last 60 minutes.
    """
    now = datetime.now()
    cutoff = now - timedelta(hours=1)
    # cutoff = now - timedelta(minutes=1)

    # 1) remove anything older than an hour
    while _request_times and _request_times[0] < cutoff:
        _request_times.popleft()

    # 2) check count
    if len(_request_times) <= MAX_REQUESTS_PER_HOUR:
        _request_times.append(now)
        return True
    else:
        return False
