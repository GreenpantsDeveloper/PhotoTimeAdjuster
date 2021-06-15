# Photo Date/Time Adjuster

Did you forget to change the daylight savings time of your camera? Did you let someone else borrow your camera and mess up the internal clock? Or does your camera not properly keep track of the time anymore? Whatever the reason may be, this script lets you quickly adjust the EXIF timestamps of an image or a directory of images.

This script works by checking the MIMETypes of an image and verifying whether we're dealing with an image (as the number of file extensions indicating (RAW) images is too large and continuously changing). By checking MIMETypes and changing EXIF data, <b>this works on most &ndash; if not all &ndash; image file types</b>. Let me know if you find a file type that isn't supported!


## How to run

Make sure your system has [ExifTool](https://exiftool.org/) present in its PATH, or simply put the executable (`exiftool.exe` on Windows) in the root directory of this project. Then run the code with:

```
python adjust_time.py [path_to_file_or_dir] [adjustment_regex] (optional [-m])
```

The `adjustment_regex` is valid when it contains at least:

* A sign (+ or -) at the start.
* Any combination of days (d), hours (h), minutes (m), or seconds (s).

Examples work best, don't they? You can for instance add 1 day, 2 hours, 3 minutes, and 42 seconds to all images in a directory called `/home/images` by running:
```
python adjust_time.py "/home/images" +1d2h3m42s
```

Alternatively, if a single file needs to be set back 1 hour, just run:
```
python adjust_time.py "/home/images/damn_timezones.jpg" -1h
```

Don't worry, the script will ask (once) whether you're really okay with modifying the EXIF data of the images (it does overwrite the existing images; no original copy is kept). But hey, if you made a mistake and you want to undo a time adjustment, simply flip the sign and `adjust_time` again!

Finally, note that there's an additional, optional parameter `-m` that can be used to disregard MIMETypes altogether. However, this means that all files in the directory and subdirectories will have their dates adjusted, <i>including non-image files</i>. You probably do not want this. Use at your own risk, ideally when images don't have MIMETypes and you've already separated them.



## For SuperUsers (or anyone looking into the code)

In `utils.py` you can find which EXIF date keys are adjusted. This was based on my own images; feel free to let me know if you come across any other Date(Time) EXIF keys where its value also represents the `date_taken` of an image (on Windows for instance, the `FileAccessDate` and `FileCreateDate` are often much later dates than the main `DateTimeOriginal` EXIF key).

## Potential improvements

If you're program-hungry, here are two ideas I thought of already:

* Modify the regular expression to allow setting one specific datetime rather than being relative to the existing datetime of each file.
* Instead of using MIMETypes, give users the option to check whether files are images based on file extension alone (for when MIMETypes aren't available).
