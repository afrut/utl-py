#exec(open("async_http_requests.py").read())
# Asynchronously fire HTTP requests
import asyncio
import aiohttp
import json
import time
import requests

async def main_async():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.publicapis.org/entries', ssl = False) as response:
            data = await response.json()
            with open("./content.json", "wt") as fl:
                json.dump(data, fl, indent = 4)

        # Create multiple tasks to fire HTTP requests asynchronously
        tasks = list()
        num_tasks = 50
        task_count = 0
        s = time.perf_counter()
        for api in data["entries"]:
            if len(api["Auth"]) > 0:
                continue
            task_count = task_count + 1
            tasks.append(asyncio.create_task(session.get(api["Link"], ssl = False)))
            if task_count >= num_tasks:
                break
        await asyncio.gather(*tasks)
        print(f"Async execution time = {time.perf_counter() - s:.4f}s")

        # Synchronous execution for reference
        task_count = 0
        s = time.perf_counter()
        for api in data["entries"]:
            if len(api["Auth"]) > 0:
                continue
            task_count = task_count + 1
            requests.get(api["Link"])
            if task_count >= num_tasks:
                break
        print(f"Sync execution time = {time.perf_counter() - s:.4f}s")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_async())