
## backup crawler
Creates an incremental backup directory for all your important stuffs.

*You can keep the backup directory to a small size by using multiple filters so that it can be pushed to github or drive.*

**Features:**

 - 2 types of filters based on filetypes:
	 - Compulsory files: [.py, .ipynb, .c, .cpp, .sh]
	 - Files that you want but upto a size limit: [.txt, .csv]

 - Filter based on folders:
	 - Compulsory folders
	 - Folders to skip - can also skip their sub-folders
	 - Skip hidden folders like [.git, .data]
	 - Skip a folder if it has large number of files (can be changed)

 - Incremental backup 
	- Files are copied only if they are new or modified after a slot of 1 hr (can be changed) 

 - Generate html tree structure of folders backed up (helps in navigating later)
	 - Only dirs for large folders
	 - Full tree structure for other folders

 - Get stats for size and file count while generating backup to see if everything is as you want.
 
 - Make a dry run before running final backup.

## todo

 - [ ] Make .py version
 - [x] Code refactoring
 - [ ] Add scheduling
 - [x] Add backup to git
