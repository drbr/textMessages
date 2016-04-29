# Text Message Parser

This repository contains some python scripts that transform an archive of messages into a simple CSV format. Currently, there are scripts for iPhone and Facebook messages.

[This article](http://www.iphonebackupextractor.com/blog/2012/apr/23/what-are-all-files-iphone-backup/) lists the names of various source files on the phone.

## Basic info and prerequisites

To use these scripts, acquire the necessary input files and update the paths in the `Makefile` to point to them. Then run `make` in this directory. The resulting CSV files will be written to the `output` directory.

The scripts were written with Python 2.7.11. They require the following 3rd party libraries (available through pip): `beautifulsoup4` and `vobject`.

## iPhone

To get the text messages from an iPhone, follow these steps:

1. Back up the phone through iTunes
2. Access the backups at `~/Library/Application Support/MobileSync/Backup/`
3. Open the most recent backup folder and find the file named `3d0d7e5fb2ce288813306e4d4636395e047a3d28`. This is a sqlite file that contains all the text messages from the phone.
4. Copy the above file to this directory, or update the path in the `Makefile` to point to it.

You will also need a copy of your address book as a vCard. One way to get this is from the Contacts application on the Mac: select all the contacts and choose `File` > `Export...` > `Export vCard`. Save this as `Contacts.vcf` or update the path in the `Makefile` to point to it.

Once you have the SMS sqlite file and the Contacts vCard file, run `make text` to parse the Contacts and cross-reference them with the contents of the SMS file. The result will be a file called `txts.csv` in the `output` directory.


## Facebook

To get the facebook messages, download a copy of your Facebook data (as of this writing, this feature is accessed through the General pane of the user settings). Within this archive is a file called `messages.htm`. Copy that file to this directory, or update the path in the `Makefile` to point to it.

You will also need an access token to the Facebook Graph API, in order to fill in the missing user names. Get one at [https://developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer); the basic permissions are sufficient. Copy it into a file named `facebookAccessToken.txt`, or point to it in the `Makefile`.

Finally, update the array in `extract_facebook.py` to include your name in the various forms it appears in the Facebook message archive file.

Once this setup is done, run `make facebook` to convert the HTML file to a CSV. The script will call the Graph API to get the actual name for any user who appears in the archive only by ID. This will take a long time; HTML parsing is slow.