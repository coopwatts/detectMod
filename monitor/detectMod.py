#!/usr/bin/env python
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

FILE_PATH = "/path/to/directory"
IGNORE_PATH = "/path/to/directory" #Set this to ignore a particular directory within the parent

def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)

            if filepath.startswith(IGNORE_PATH):
                continue

            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


# Run the above function and store its results in a variable.
full_file_paths = get_filepaths(FILE_PATH)
newLines = {}

# Create the complete lines as CSV with filpath,timestamp
for filepath in full_file_paths:
        try:
          mtime = os.path.getmtime(filepath)
        except OSError:
          mtime = 0

        last_modified_date = datetime.fromtimestamp(mtime)
        newLines[str(filepath).strip()] = str(last_modified_date).strip()

# Open the file to check for modification
f = open('/monitor/fileinfo.txt', 'r+')
f.seek(0)

# Open a file to document modification, erase its current contents
f2 = open('/monitor/modified.txt', 'r+')
f2.truncate()
f2.seek(0)

# Assume there have been no modifications
emailNeeded = False

oldLines = {}
for oldLine in f:
   oldValues = oldLine.split(',')
   oldLines[str(oldValues[0]).strip()] = str(oldValues[1]).strip()

#Handle files that have been added
for filePath, modTime in newLines.iteritems():

   #Use the new file path as a key to the old file paths modification date
   #If it returns 'empty', then the file is new
   oldModTime = oldLines.get(str(filePath), 'empty')
   if oldModTime == 'empty':
      f2.write(str(filePath) + ' ADDED AT ' + str(modTime) + '\n')
      emailNeeded = True

for filePath, modTime in oldLines.iteritems():

   #Handle files that have been deleted
   #If the old file path is not in the dictionary of new file paths, it's been deleted or moved

   currentModTime = newLines.get(str(filePath), 'empty')
   if currentModTime == 'empty':
      f2.write(str(filePath) + ' DELETED OR MOVED\n')
      emailNeeded = True
      continue

   #Handle files that have been modified
   #If the modTime of the old file path does not match the modTime of the new file path, then the file has been modified
   if str(modTime) != str(currentModTime):
      f2.write(str(filePath) + ' MODIFIED AT ' + str(currentModTime) + '\n')
      emailNeeded = True

f2.close()

if emailNeeded:
  emailContent = open('/monitor/modified.txt', 'r')
  msg = MIMEText(emailContent.read())
  msg['Subject'] = 'File Modification Report'

  FROM = 'youremail@domain.com'
  recipients = ['recipient@domain.com', 'recipient@domain.com']

  msg['From'] = FROM
  msg['To'] = ", ".join(recipients)

  s = smtplib.SMTP('smtp.gmail.com')
  s.starttls()
  s.login(FROM, 'yourpassword')
  s.sendmail(FROM, recipients, msg.as_string())
  s.quit()

# Overwrite with new modification dates
f.seek(0)
f.truncate()
isFirstLine = True
for key, value in newLines.iteritems():
  if isFirstLine:
    f.write(key + ',' + str(value))
    isFirstLine = False
  else:
    f.write('\n')
    f.write(key + ',' + str(value))
f.close()
