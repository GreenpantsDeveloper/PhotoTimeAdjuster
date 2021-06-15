import os, re, datetime
import exif_tool


class InvalidPathException(Exception):
    pass


def parse_delta_time(time_string):
    # Ensure the time string is valid
    if len(time_string) <= 1:
        print("\nError: delta_time could not be parsed correctly!\nDid you make sure it is in the format +1d2h3m4s or -1d2h3m4s?")
        return None

    # Turn regex into specifics
    match = re.match('^(\+|-)([0-9]+d)?([0-9]+h)?([0-9]+m)?([0-9]+s)?$', time_string)
    if match is not None:
        groups = match.groups()
        sign = groups[0]
        days = int(groups[1][:-1]) if groups[1] is not None else 0
        hours = int(groups[2][:-1]) if groups[2] is not None else 0
        minutes = int(groups[3][:-1]) if groups[3] is not None else 0
        seconds = int(groups[4][:-1]) if groups[4] is not None else 0

    else:
        print("\nError: delta_time could not be parsed correctly!\nDid you make sure it is in the format +1d2h3m4s or -1d2h3m4s?")
        return None

    # Compute the number of seconds for later adjustment
    total_seconds = datetime.timedelta(days=days,hours=hours,minutes=minutes,seconds=seconds).total_seconds()
    if sign == '-':
        total_seconds = -total_seconds

    if total_seconds == 0:
        print("\nError: it looks like delta_time is zero!")
        return None

    return total_seconds


# Whether a file is an image; 
def is_image(filepath, metadata, ignore_mimetype=False):
    exif_mimetype_key = 'File:MIMEType'
    if exif_mimetype_key in metadata:
        if os.path.split(metadata[exif_mimetype_key])[0].lower() in ['image', 'img', 'picture', 'pic', 'photograph', 'photo']:
            return True
        else:
            print("\tNote: file '%s' MIMEType is not an image; skipping..." % filepath)
            return False
    elif ignore_mimetype:
        print("Ignoring MIMEType for '%s'" % filepath)
        return True
    else:
        print("Warning: file '%s' has no File:MIMEType in its EXIF" % filepath)

        return False


# EXIF date format to Python datetime format
def exif_to_datetime(exif):
    return datetime.datetime.strptime(exif, '%Y:%m:%d %H:%M:%S')


# Python datetime format to EXIF date format
def datetime_to_exif(dtime):
    return datetime.datetime.strftime(dtime, '%Y:%m:%d %H:%M:%S')


def adjust_file_time(filepath, delta_seconds, ignore_mimetype=False):
    with exif_tool.ExifTool() as et:
        metadata = et.get_metadata(filepath)
        
        if not is_image(filepath, metadata, ignore_mimetype=False):
            return

        # List of keys related to the `date taken`
        date_keys = [
            'EXIF:DateTimeOriginal',
            'MakerNotes:SonyDateTime',
            'EXIF:CreateDate',
            'EXIF:ModifyDate'
        ]
        # 'File:FileModifyDate' -- may contain timezones (e.g. +01:00) that are not reflected in Windows' properties oddly enough
        # 'File:FileAccessDate' -- not relevant on Windows
        # 'File:FileCreateDate' -- not relevant on Windows either

        available_keys = [key for key in date_keys if key in metadata.keys()]

        if len(available_keys) == 0:
            print("Warning: file '%s' has no proper date available in the EXIF; skipping..." % filepath)
            return

        # Get old date based on priority in `date_keys`
        old_date = None
        for key in available_keys:
            date = metadata[key]
            if date is not None and date != "":
                old_date = date
            if old_date is not None:
                break

        # Turn EXIF time into datetime, compute the difference, then put back as EXIF time
        old_time = exif_to_datetime(old_date)
        new_time = old_time + datetime.timedelta(seconds=delta_seconds)
        exif_time = datetime_to_exif(new_time)
        
        # Adjust all relevant EXIF tags
        for key in available_keys:
            tag = key.split(':')[1]
            et.execute(str.encode("-%s=%s" % (tag, exif_time), 'utf-8'), str.encode(filepath, 'utf-8'), str.encode('-overwrite_original', 'utf-8'))
    print("Successfully updated %s \t (%s -> %s)" % (filepath, old_time, new_time))
