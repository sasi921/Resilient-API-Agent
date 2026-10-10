from resilient_http import get_json

def inspect_api(url: str) -> dict:
    result = get_json(url)

    if not result.ok:
        return {
            "status": "degraded",
            "message": "The API tool failed after retries.",
            "tool_result": result.model_dump(),
        }

    data = result.data

    if isinstance(data, dict):
        preview = {key: data[key] for key in list(data)[:5]}
        shape = f"object with {len(data)} keys"
    elif isinstance(data, list):
        preview = data[:3]
        shape = f"array with {len(data)} items"
    else:
        preview = data
        shape = type(data).__name__

    return {
        "status": "healthy",
        "shape": shape,
        "preview": preview,
        "tool_result": result.model_dump(),
    }
