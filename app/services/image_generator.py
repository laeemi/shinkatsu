import aiohttp

from app.core.redis import redis_session
from app.services.one_time_code_repository import model_repository, api_key_repository, timeout_repository, \
    negative_prompt_repository, images_count_repository


async def generate_images(api_url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_url}/generate-xl", json=data) as response:
            return await response.json()


async def get_image(user_id: int, prompt: str):
    api_url = "https://visioncraft.top"
    api_key = await api_key_repository.get_code(user_id, redis_session)
    model_sampler = await model_repository.get_code(user_id, redis_session)
    n_prompt = await negative_prompt_repository.get_code(user_id, redis_session)
    image_count = await images_count_repository.get_code(user_id, redis_session)

    model, sampler = model_sampler.split("_")
    width = 1024
    height = 1024
    steps = 30
    cfg_scale = 10

    data = {
        "prompt": prompt,
        "model": model,
        "negative_prompt": n_prompt if n_prompt is not None else 'bad quality',
        "image_count": image_count if image_count is not None else 3,
        "token": api_key,
        "width": width,
        "height": height,
        "sampler": sampler,
        "steps": steps,
        "cfg_scale": cfg_scale
    }

    # Generate images asynchronously
    image_urls = (await generate_images(api_url, data))['images']
    images = []
    await timeout_repository.set(user_id, "timeout", redis_session)
    async with aiohttp.ClientSession() as session:
        for i, image_url in enumerate(image_urls):
            async with session.get(image_url) as image_response:
                images.append(await image_response.read())

    return images
