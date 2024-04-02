import aiohttp

from app.core.redis import redis_session
from app.services.one_time_code_repository import model_repository, api_key_repository, timeout_repository


async def generate_image(api_url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_url}/generate-xl", json=data) as response:
            image = await response.read()
            return image


async def get_image(user_id: int, prompt: str):
    api_url = "https://visioncraft.top"
    api_key = await api_key_repository.get_code(user_id, redis_session)
    model_sampler = await model_repository.get_code(user_id, redis_session)

    model, sampler = model_sampler.split("_")
    width = 1024
    height = 1024
    steps = 40
    cfg_scale = 10

    data = {
        "prompt": prompt,
        "model": model,
        "negative_prompt": "bad quality",
        "token": api_key,
        "width": width,
        "height": height,
        "sampler": sampler,
        "steps": steps,
        "cfg_scale": cfg_scale
    }

    # Generate images asynchronously
    image = await generate_image(api_url, data)
    await timeout_repository.set(user_id, "timeout", redis_session)
    return image
