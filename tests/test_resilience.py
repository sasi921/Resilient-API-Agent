import resilient_http
from agent import inspect_api

class FakeResponse:
    def __init__(self, status, data=None):
        self.status_code = status
        self._data = data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise resilient_http.requests.HTTPError(str(self.status_code))

    def json(self):
        return self._data

def test_success(monkeypatch):
    monkeypatch.setattr(
        resilient_http.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(200, {"ok": True}),
    )
    result = resilient_http.get_json("https://example.test", backoff=0)
    assert result.ok
    assert len(result.attempts) == 1

def test_retry_then_success(monkeypatch):
    responses = [FakeResponse(503), FakeResponse(200, {"ready": True})]
    monkeypatch.setattr(
        resilient_http.requests,
        "get",
        lambda *args, **kwargs: responses.pop(0),
    )
    result = resilient_http.get_json("https://example.test", retries=2, backoff=0)
    assert result.ok
    assert len(result.attempts) == 2
    assert result.attempts[0].status_code == 503

def test_exhausted_retries(monkeypatch):
    monkeypatch.setattr(
        resilient_http.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(503),
    )
    result = resilient_http.get_json("https://example.test", retries=1, backoff=0)
    assert not result.ok
    assert len(result.attempts) == 2

def test_agent_degrades(monkeypatch):
    class FailedResult:
        ok = False
        def model_dump(self):
            return {"ok": False}

    monkeypatch.setattr("agent.get_json", lambda url: FailedResult())
    assert inspect_api("https://example.test")["status"] == "degraded"

def test_object_preview(monkeypatch):
    class SuccessResult:
        ok = True
        data = {"a": 1, "b": 2}
        def model_dump(self):
            return {"ok": True}

    monkeypatch.setattr("agent.get_json", lambda url: SuccessResult())
    result = inspect_api("https://example.test")
    assert result["shape"] == "object with 2 keys"
