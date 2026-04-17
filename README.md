Dependencies
============

See [`requirements.txt`](requirements.txt)

Usage
=====

Create prefect poster with prefect images. Image files should be named the name of the prefect 
in the picture.

```
python3 prefect_poster.py -i INPUT_IMAGES_DIR
```

Create lanyards for CS labs.

```
python3 lanyard.py -i INPUT_NAMES_FILE [-l LOGO]
```

Create CMC poster with student images. Image files should be named the name of the student in
the picture. The image directory should be named the title that will go on the slide with the images

```
python3 create_cmc_poster.py -i /path/to/images_dir --font_path /path/to/font.ttf -o /path/to/out_dir
```

Full usages statement:

```
usage: create_cmc_poster.py [-h] [-d DIMENSION] [-g GRID] [--background_color BACKGROUND_COLOR] [--line_color LINE_COLOR] [--aspect_ratio ASPECT_RATIO]
                            [--title_font_size TITLE_FONT_SIZE] [--font_size FONT_SIZE] [--lines] [--page_margin PAGE_MARGIN] --font_path FONT_PATH -i IMAGE_DIR
                            [-o OUT_DIR]

create student poster with headshots

options:
  -h, --help            show this help message and exit
  -d, --dimension DIMENSION
                        Page dimensions as WIDTHxHEIGHT (default: 1920x1080)
  -g, --grid GRID       Grid size as COLxROW (default: 4x2)
  --background_color BACKGROUND_COLOR
                        Background color as R,G,B
  --line_color LINE_COLOR
                        Line color as R,G,B
  --aspect_ratio ASPECT_RATIO
  --title_font_size TITLE_FONT_SIZE
  --font_size FONT_SIZE
  --lines
  --page_margin PAGE_MARGIN
  --font_path FONT_PATH
  -i, --image_dir IMAGE_DIR
  -o, --out_dir OUT_DIR
```
