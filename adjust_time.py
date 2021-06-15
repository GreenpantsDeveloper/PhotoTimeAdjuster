import os, sys

from utils import InvalidPathException, parse_delta_time, adjust_file_time


# Ensures path `p` is a dir, or a file
def dir_or_file(p):
    if os.path.isfile(p) or (os.path.isdir(p) and len(os.listdir(p)) > 0):
        return p
    else:
        raise InvalidPathException("Path '%s' is not valid (it is either not a file, not a directory, or an empty directory)" % p)

def main():
    # Initialize
    assert len(sys.argv) >= 3, "\n\ntwo arguments required: the path to a file or directory, and the delta time (e.g. +1d2h3m4s or -1h20s)\n\t-m\t(optional) ignore mimetype; will update times of non-image files too."
    root = dir_or_file(sys.argv[1])
    delta_time = sys.argv[2]

    ignore_mimetype = True if (len(sys.argv) >= 4 and sys.argv[3] == '-m') else False
    if ignore_mimetype:
        print("\nIgnoring mimetype for this batch!")

    # Get the time adjustment in seconds
    delta_seconds = parse_delta_time(delta_time)
    if delta_seconds is None:
        sys.exit(0)

    # Handle a single file
    if os.path.isfile(root):
        filepath = root
        print("\nOne file found: %s\n" % filepath)

        if input("Are you sure you want to update this file's date by %s? [[Y]/n]" % delta_time).lower() in ['', 'y', 'yes', 'yep', 'totally', 'absolutely', 'no problem', 'why not']:
            adjust_file_time(filepath, delta_seconds, ignore_mimetype)
        else:
            print("Exiting...")
            sys.exit(0)

    # Handle a set of files (finds files recursively)
    else:
        filepaths = []
        for base, dirs, files in os.walk(root):
            filepaths.extend([os.path.join(base, f) for f in files])

        # Tell user how many files will be adjusted
        num_files = len(filepaths)

        if input("\nAre you sure you want to update roughly %d files' dates by %s? (some may not be images) [[Y]/n]\n> " % (num_files, delta_time)).lower() in ['', 'y', 'yes', 'yep', 'totally', 'absolutely', 'no problem', 'why not']:
            for filepath in filepaths:
                adjust_file_time(filepath, delta_seconds, ignore_mimetype)
        else:
            print("Exiting...")
            sys.exit(0)


    print("\n~~~ My work here is done ~~~")



if __name__ == '__main__':
    main()
