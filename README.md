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
the picture 

```
python3 create_cmc_poster.py -i /path/to/images_dir --font_path /path/to/font.ttf -o /path/to/out_dir
```
