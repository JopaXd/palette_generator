from itertools import chain
import aiohttp
import asyncio
import json
import csv

async def fetch_step(session, step:int):
	async with session.post("https://colorhunt.co/php/feed.php", data={"step": step, "sort": "random", "tags": ""}) as r:
		if r.status == 200:
			result = json.loads(await r.text())
			processed_palettes = []
			for palette in result:
				y = []
				x = None
				for j in range(0, len(palette["code"]), 6):
					y.append(palette["code"][j:j+6])
				x = y.pop(0)
				processed_palettes.append({"x": x, "y": y})
			return processed_palettes
		else:
			print(f"[ERROR] Failed to fetch step {step}!")

async def fetch_palettes(session, steps):
	tasks = []
	for step in steps:
		task = asyncio.create_task(fetch_step(session, step))
		tasks.append(task)
	res = await asyncio.gather(*tasks)
	return res

async def main():
	headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
	steps = range(0,90)
	async with aiohttp.ClientSession(headers=headers) as session:
		palettes = await fetch_palettes(session, steps)
	palettes = list(chain.from_iterable(palettes))
	palette_file = open("data_new.csv", "a+")
	palette_writer = csv.writer(palette_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for p in palettes:
		palette_writer.writerow([p["x"], " ".join(p["y"])])
	palette_file.close()

if __name__ == "__main__":
	asyncio.run(main())