
## backup crawler
Create an incremental backup directory for all your important stuffs.

*You can keep the backup directory to a small size by using multiple filters so that it can be pushed to github or drive.*

**Features:**

 - 2 types of filters based on filetypes:
	 - Compulsory files: [".py", ".ipynb", ".c", ".cpp", ".sh"]
	 - Files that you want but up-to a size limit: [".txt", ".csv"]

 - Filters based on folders:
	 - Compulsory folders: [".py", ".ipynb", ".c", ".cpp", ".sh"]
	 - Folders to skip - will also skip their sub-folders
	 - Skip hidden folders like [.git, .data]
	 - Skip a folder if it has large number of files

 - Incremental backup 
	Files are copied only if they are new or modified after a slot of 1 hr (can be changed) 

 - Generate html tree structure of folders backed up (help in navigating later)
	 - Only dirs for large folders
	 - Full tree structure for other folders

 - Give stats for size and file count while generating backup to see if everything is as you want.

## todo

 - Make .py version
 - Add more comments to the code
 - Add scheduling
 - Add backup to git
