import requests
import csv
import time

def get_palettes(step:int) -> dict:
	headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
	body = {
		"step":step,
		"sort":"random",
		"tags":""
	}
	r = requests.post("https://colorhunt.co/php/feed.php", data=body, headers=headers)
	return r.json()

def main():
	all_palettes = []
	palette_file = open("data_new.csv", "a+")
	#The last page is around 80-90
	for i in range(0,90):
		palettes = get_palettes(i)
		for palette in palettes:
			y = []
			x = None
			for j in range(0, len(palette["code"]), 6):
				y.append(palette["code"][j:j+6])
			x = y.pop(0)
			all_palettes.append({"x": x, "y": y})
			palette_writer = csv.writer(palette_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
			palette_writer.writerow([x, " ".join(y)])
		time.sleep(5)
		if len(palettes) == 0:
			return
		print(len(palettes))

	palette_file.close()

if __name__ == "__main__":
	main()