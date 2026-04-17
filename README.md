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
python3 create_headshot_poster.py -i /path/to/images_dir --font_path /path/to/font.ttf -o /path/to/out_dir
```

A more complex example:

```
python3 create_headshot_poster.py -i prefects -o test --font_path /Library/Fonts/Arial\ Unicode.ttf --title_font_size 50 --font_size 30 --page_margin 30 --grid 3x4 -d 1275x1650 --lines --aspect_ratio 1/1 --background_color 255,255,255 --line_color 0,0,0 --font_size 24
```
