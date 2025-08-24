Why
===

Simple script to create prefect posters from images. We have been manually creating the 
posters by dragging and resizing images inside Google Docs. As a result, we would end up
with as poster where images had varying sizes with varying aspect ratios. So I wrote this
script to automatically crop the images to have a uniform aspect ratio and create the poster. 

Will it be ever used by any other person than me? I don't know.

Dependencies
============

```
fpdf2
```


Usage
=====

```
python3 prefect_poster.py -i /path/to/images
```
