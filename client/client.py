import uuid
import httpx
from typing import Any, Optional

class A2AClient:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url.rstrip('/')
        self._card = None
        self._http = httpx.Client(timeout=30)

    def fetch_agent_card(self) -> dict:
        """Fetch and cache the Agent Card."""
        if self._card is None:
            url = f'{self.agent_url}/.well-known/agent.json'
            print(f"[REQUEST] GET {url}")

            resp = self._http.get(url)
            resp.raise_for_status()
            print(f"[RESPONSE] {resp.status_code} {url}")

            self._card = resp.json()
        return self._card

    def _build_task(self, text: str,
        task_id: Optional[str] = None,
        session_id: Optional[str] = None) -> dict:
        return {
            'id': task_id or str(uuid.uuid4()),
            'sessionId': session_id,
            'message': {
                'role': 'user',
                'parts': [{'type': 'text', 'text': text}]
            }
        }

    def send_task(self, text: str, **kwargs) -> dict:
        self.fetch_agent_card()
        payload = self._build_task(text, **kwargs)
        url = f'{self.agent_url}/tasks/send'

        preview = {
            "id": payload["id"],
            "text": text[:50] + ("..." if len(text) > 50 else "")
        }
        print(f"[REQUEST] POST {url}")
        print(f"          payload={preview}")

        resp = self._http.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        print(f"[RESPONSE] {resp.status_code} {url}")
        print(f"           status={data.get('status')}")

        state = data.get("status", {}).get("state")
        if state != 'completed':
            raise RuntimeError(
                f"Task did not complete successfully. Expected state "
                f"'completed', got {state!r}. Full status: {data.get('status')}"
            )
        return resp.json()

    @staticmethod
    def extract_text(response: dict) -> str:
        artifacts = response.get('artifacts', [])
        for artifact in artifacts:
            for part in artifact.get('parts', []):
                if part.get('type') == 'text':
                    return part['text']
                if part.get("type") == "file":
                    return part.get("url", "")
        return ''

    def get_skills(self) -> list:
        card = self.fetch_agent_card()
        return card.get("skills", [])

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "A2AClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
