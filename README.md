# AWS-Backup-and-Restore
The purpose of this program is to recursively traverse the files of a directory and make a backup to the cloud. The program should also be able to restore from the cloud as well.

## Commands
**% backup** directory-name bucket-name::directory-name

This will make a backup to the cloud of the specified directory to the specified “bucket”
in either Azure or AWS. The directory structure of the files should be respected and visible in
the cloud.

**% restore** bucket-name::directory-name directory-name

This will restore from the specified bucket-name in the cloud to the specified directory.
The directory structure of the files should be respected.

## Compiling
1. Set up your config and credentials in the .aws folder
2. To compile the program, in your console enter “python3 filename operation directory-name bucket-name” 
for example:
  -  **% backup** “python3 aws.py backup testfile thebucket”
  -  **% restore** “python3 aws.py restore testfile thebucket”

3. The program will then run and display its progress on the console
**Note 1: For directory with spaces enclose them with quotation mark like this “ “C:\Users\Student\Desktop\space test” ”**
**Note 2: for the directory name, you can either enter the local path name like “awstest” or absolute path like “C:\Users\Student\Desktop\awstest” that can be with either forward or back slash.**
**Note 3: you can enter “.” Or “./” for local directory**

