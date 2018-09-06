# Runstastic export
This tool will help you to export your Runtastic activities in GPX format, so you can import them later in another apps, like Garmin.

Original frontend script is based on (Download all activities from Runtastic)[https://gist.github.com/christianewald/0009d3ce1a372a11ae82].

Exporting all the activities is done in two steps:
1. Make a list of all the activities to download.
2. Download them all. The difference with other projects is that the donwload part is executed by a Python script. Runtastic only allows you to downlad 5 files, and then you will get a *HTTP Error 403: Forbidden*. Then you need to run again the Python file, that it will download another 5 (new) files.

You need Python 3 to make it work.

## Get all the list of activities to export:
1. Log in in (runtastic)[https://www.runtastic.com/]
2. Open the Chrome developers tool: View -> Developer -> Developer Tools
3. Go to the Runtastic activitis page, then open the Chrome console and paste the content of *export_activity_list.js*.
4. Press enter, a file called *list.txt* will be downloaded. This file contains all the activities we will download later.

## Download all the activities:
To download all the activities we will use the python script.
1. Being logged in into runtastic, open a new tab and visit the website (check_export_quota)[https://www.runtastic.com/check_export_quota]. You need to be logged in, because we need to capture the cookie details.
2. Open the Chrome Developer tools (View -> Developer -> Developer Tools).
3. Select *check_export_quota* request, copy, and copy as cUrl.
4. Paste the content in between the double quotes of variable *quota_call* (line 16 in *download_activities.py*).
5. Update also variables *DOWNLOADS* and *QUOTE_URL* with your paths. 
6. Run the python script, by calling 
> python3 download_activities.py

After around 5 downloads, you will get an error like *HTTP Error 403: Forbidden*. If you run it again, you will get a different error *Exception: No export allowed*. You are not allowed to download more files,so wait a couple of hours and run it again (the script will skip the files already downloaded).

