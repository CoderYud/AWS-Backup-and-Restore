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
2. To compile the program, in your console enter “python3 filename command directory-name bucket-name”
   
    for example:
      -  **% backup** “python3 aws.py backup testFolder backupBucket”
      -  **% restore** “python3 aws.py restore testFolder restoreBucket”
3. The program will then run and display its progress on the console
![backup](https://github.com/CoderYud/AWS-Backup-and-Restore/assets/73090278/831200c9-fbd8-4a80-9f3a-77f099901d46)

<p align="center">Figure 1. Backup</p>

![restore](https://github.com/CoderYud/AWS-Backup-and-Restore/assets/73090278/c2cee59e-3fac-4930-9fbb-b84b2a82d7a1)

<p align="center">Figure 2. Restore</p>

**Note 1: For directory with spaces enclose them with quotation mark like this “ “C:\Users\Student\Desktop\space test” ”.**

**Note 2: For the directory name, you can either enter the local path name like “localFolder” or absolute path like “C:\Users\Student\Desktop\localFolder” that can be with either forward or backslash.**

**Note 3: You can enter “.” Or “./” for local directory.**

## Services and API
For this program, we will use the AWS S3 Bucket API to backup and restore our files from and to the cloud. For this to work, you will also need to have AWS CLI installed and create a user using IAM console. For more information about that [Click Here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation)
