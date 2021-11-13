
import boto3
import os
import sys

from datetime import datetime
from botocore.exceptions import ClientError

backup="% backup"
restore="% restore"
admin="% admin"
success=[]
fail=[]
#testpath ="C:\Users\Bin Map\Desktop\awstest"
def main():
	checkbucket=False
	checkpath=False
	print("Available action for this application:")
	print("-----------------actions-----------------------")
	print("% backup")
	print("% restore")
	print("-----------------------------------------------")
	action=input("Enter one of the action above: ")

	#Check condition to call the correct operation
	if action == backup:

		while checkpath!= True:
			directory_name=input("Enter the directory path: ")

			#Check for back slash and replace it with forward slash
			if directory_name.find('\\')!=-1:
				directory_name=directory_name.replace('\\','/')
				print(directory_name)

				#check if it is absolute path or local path
				#return either path
				checkpath,final_path=Check_Path(directory_name)

			else:

				#check if it is absolute path or local path
				#return either path
				checkpath,final_path=Check_Path(directory_name)

			#invalid path
			if not checkpath:
				print("The inserted directory path doesn't exist in your system")
			
		#Get the bucket name
		#Check if bucket created or not
		bucket_name= input("Enter the bucket name: ")
		checkbucket=Check_Bucket(bucket_name)
		
		#if both condition meet, call back up otherwise stop the program
		if checkpath==True and checkbucket==True:
			Call_Backup(final_path,bucket_name)
			
	#Check condition to call the correct operation
	elif action == restore:
		directory_name=input("Enter a name for local path or absolute directory path: ")
		if directory_name.find('\\')!=-1:
			directory_name=directory_name.replace('\\','/')
	
		bucket_name= input("Enter the bucket name: ")
		Call_Restore(bucket_name,directory_name)
	
	elif action == admin:
		directory_name=input("Enter the directory name: ")
		bucket_name= input("Enter the bucket name: ")

		#Check for back slash and replace it with forward slash
		if directory_name.find('\\')!=-1:
			directory_name=directory_name.replace('\\','/')
		
		test_admin()
	#If input is not one of the following action, exit
	else:
		print("Please Try Again")
		sys.exit(0)
	
	#for root, dirs, files in os.walk(path):
	#	for file in files:
	#		print(os.path.join(root,file))
	
		backup(file,"dahbucket")


#go through the directory
#pass the absolute path to Backup for backuu
def Call_Backup(path,bucket):
	new_path=None
	
	#go through the directory and each subdirectory
	for root, dirs, files in os.walk(path):
		for file in files:
			Backup(root+'/'+file,bucket)
	#files=glob.glob(path+'/*')
	#for file in files:
	#	Backup(file,bucket)
	print("Backup successfully")
	print("---------------------------------------------------")
	print(len(success),"Files successfully backup")
	print(len(fail),"Files unsuccessfully backup")
#s3 = boto3.resource("s3")
#buckets=s3.buckets.all()
#for bucket in buckets:
#	print(bucket.name)

#check file condition before uploading to aws
#if file already up in the cloud move on to next file
def Backup(file_name,bucket,object_name=None,args=None):
	"""
	file_name is the path
	bucket is name of the bucket 
	object_name is the key
	"""
	#replace backslash with forward slash
	if file_name.find('\\')!=-1:
			file_name=file_name.replace('\\','/')

	#set flag for uploading
	is_in= False

	#get S3 client service
	client = boto3.client('s3')

	#set file path to key
	if object_name is None:
		object_name=file_name
	
	#Get a list of objects in the bucket
	check=client.list_objects(Bucket=bucket)

	#get the file name from the path to compare
	newfile=os.path.basename(os.path.normpath(file_name))

	#get file last modified timestamp
	time=os.path.getmtime(file_name)

	s3= boto3.resource('s3')
	s3_bucket= s3.Bucket(bucket)
	bucket_list= list(s3_bucket.objects.all())
	if len(bucket_list)!=0:
		#check if file already in the bucket
		for file in check['Contents']:
		
			#get file name from the bucket key
			bucketfile=os.path.basename(os.path.normpath(file["Key"]))

			#if file is already in the bucket
			if bucketfile==newfile:

				#check modified time
				#if the file waiting to upload is the newest, upload
				#set flag to True
				if file['LastModified'].timestamp() < time:
					print("Uploading......")
					success.append(newfile)
					client.upload_file(file_name,bucket,object_name,ExtraArgs=args)
					is_in=True

				#if match but already updated, break loop early 
				else:
					print("'",newfile,"' is already in the bucket")
					fail.append(newfile)
					is_in=True
					break

	#Check condition for upload
	#if file not in bucket then upload it
	if is_in==False:
		client.upload_file(file_name,bucket,object_name,ExtraArgs=args)
		success.append(newfile)
		print("Uploading......")
		

#get bucket objects into a list
#loop through and get each file key to download
#pass all the key into Restore function
def Call_Restore(bucket_name,path):
	#get s3 service resouce
	s3=boto3.resource('s3')

	#create a bucket resource
	bucket=s3.Bucket(bucket_name)

	#store a list of file key from the bucket to files
	files=list(bucket.objects.all())

	#go through the bucket and restore each file
	for file in files:
		Restore(bucket_name,file.key,path)

	print("All files restored")
	

#get client service and download the file with the given key
def Restore(bucket,key,path):

	#get s3 client service
	client = boto3.client('s3')

	#Check if the given directory already exist
	#root_dir=os.path.dirname(os.path.abspath(file_name))
	filename=os.path.basename(key)
	isExist=os.path.exists(path)
	print(isExist)
	if not isExist:
		os.makedirs(path)

	#download all the file from the selecting bucket back to the folder
	print(path)
	client.download_file(bucket,key,path+'/'+filename)
	print("Restoring......") 

def test_admin():

	"""for root, dirs, files in os.walk(path):
		for file in files:
			print(root.replace('\\','/'))
			isExist=os.path.exists(root.replace('\\','/'))
			print(isExist)
	client= boto3.client('s3')
	session= boto3.session.Session()
	myRegion= session.region_name
	print(myRegion)
	try:
		check= client.create_bucket(Bucket="dahbucket2",CreateBucketConfiguration={'LocationConstraint': myRegion})
		print("Bucket created")
		print(check)
	except ClientError as error:
		if error.response['Error']['Code']=='BucketAlreadyExists':
			print("Bucket already exist, exit the program")
			sys.exit(0)
		elif error.response['Error']['Code']=='BucketAlreadyOwnedByYou':
			print("Bucket already owned by you, proceed to the bucket")
	"""
	client= boto3.client('s3')
	files= client.list_objects(Bucket= "dahbucket")
	for file in files["Contents"]:
		print(file["LastModified"])


	
		
#check if the bucket is already exists or not
#create a new bucket
def Check_Bucket(bucket):
	client= boto3.client('s3')
	session= boto3.session.Session()
	myRegion= session.region_name

	#if bucket not existed, create a new bucket
	try:
		check= client.create_bucket(Bucket=bucket,CreateBucketConfiguration={'LocationConstraint': myRegion})
		print("Bucket created successfully")
		return True

	#check if bucket already exist or already owned 
	except ClientError as error:
		if error.response['Error']['Code']=='BucketAlreadyExists':
			print("Bucket already exist, exit the program")
			sys.exit(0)
		elif error.response['Error']['Code']=='BucketAlreadyOwnedByYou':
			print("Bucket already owned by you, proceed to the bucket")
			return True

def Check_Path(path):
	is_exist=os.path.exists(path)
	#if the directory doesnt exist
	if not is_exist:
		#check if it is the current local path
		if os.path.dirname(os.path.realpath(path)) == os.getcwd():
			return True,os.getcwd().replace('\\','/')
		else:
			return False,path
	else:
		return True,path

main()



