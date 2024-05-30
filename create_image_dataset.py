from PIL import Image
import numpy as np
import csv

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return list(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_palettes():
	palettes = []
	with open("data_new.csv") as palette_file:
		palette_reader = csv.reader(palette_file, delimiter=",")
		for pl in palette_reader:
			new_palette = [hex_to_rgb(f"#{pl[0]}")] + [hex_to_rgb(f"#{x}") for x in pl[1].split(" ")]
			palettes.append(new_palette)
	palette_file.close()
	return palettes

def gen_image(palette):
	val_iter = 0
	img = np.random.randint(0, 256, (16, 64, 3), dtype=np.uint8)
	for val in palette:
		for i in range(0+(16*val_iter), 16+(16*val_iter)):
			for j in range(16):
				img[j][i] = palette[val_iter]
		val_iter+=1
	return img

if __name__ == "__main__":
	palettes = get_palettes()
	img_count = 0
	for pal in palettes:
		Image.fromarray(gen_image(pal)).save(f"dataset/{img_count}.png", "PNG")
		img_count+=1