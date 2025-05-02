import httpx
async def call_ml_model(data: dict):
    url = "exercise-plan-production.up.railway.app"  # Exercise model endpoint
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        return response.json()