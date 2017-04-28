# detectMod
File addition, deletion and modifaction detection and notification for servers

How to use:
1. Drop the 'monitor' directory to your root folder
2. Ensure the correct permissions are set for each file within the 'monitor' folder
3. Change FILE_PATH and IGNORE_PATH to whatever directory you would like to monitor/ignore
4. Change the email credentials on lines 98-106 in 'detectMod.py'
5. Add to cron tab for desired run time.

For example: 

*/15 * * * * /monitor/detectMod.py 2>> /monitor/errors.txt

*/20 * * * * /monitor/sendErrors.py

- On the first run, the program will detect every file in the directory as being added (This can be avoided by changing the 'emailNeeded' variable to always be false on the first run, then run the program, and change the variable back. Or just let it run and send a large email.

- On subsqequent runs, the program will only send an email if it detects a change, or if there is an error running the program. 

