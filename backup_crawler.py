import os
import sys
import shutil
import subprocess
import time
import timeit
import pickle
from datetime import datetime


## methods
def get_dir_size(start_path):
    total_size = 0
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                total_files += 1

    return round(total_size/10**6, 2), total_files



def generate_backup_dir(start_path, backup_dir, root_dir, 
                         skip_dirs, large_dirs, 
                         filetypes_code, filetypes_other, 
                         max_filesize, mod_time_diff, overflow_fcnt,
                         verbose, dry_run):
    
    cnt_files = 0
    cnt_copied = 0
    cnt_skipped = 0
    
    size_total = 0
    size_copied = 0
    size_skipped = 0
    
    
    # saving tree
    ftree = os.path.join(backup_dir, os.path.basename(start_path) + "_tree.html")
    
    # only see upto 1st level to reduce tree file size
    # --du won't work properly as it isn't seeing all the files
    if os.path.basename(start_path) in large_dirs:
        
        ftree_dir_version = os.path.join(backup_dir, os.path.basename(start_path) + "_tree-dir.html")
        
        # save dirs
        subprocess.call(["tree", "-hdDFC", "--du", "--dirsfirst", "-H", start_path, "-o", ftree_dir_version, start_path])
        
        # save files by ignoring some patterns
        subprocess.call(["tree", "-hDFC", "-I", "*txt|*phrases|*story|*lex_rank|*tweet|*json|*html", "--du", "--dirsfirst", "-H", start_path, "-o", ftree, start_path])
    
    
    else:
        subprocess.call(["tree", "-hDFC", "--du", "--dirsfirst", "-H", start_path, "-o", ftree, start_path])
    
    
    if verbose: 
        print("  \nBase Dir:", start_path)
        print("  Backup Dir:", backup_dir)
    
    print("len skip_dirs:", len(skip_dirs))
    
    for base_dir, subdirs, filenames in os.walk(start_path, topdown=True):
        print("  Scanning:", base_dir)
         
        # skip hidden directory 
        # os.path.join(base_dir, d) not in skip_dirs to handle full path 
        # d not in skip_dirs to handle direct ignore: ".ipynb_checkpoints", ".data"
        subdirs[:] = [d for d in subdirs if d[0] != "." and os.path.join(base_dir, d) not in skip_dirs and d not in skip_dirs] 
            
        # splitext('.html') --> ('.html', '') :hidden file, ignore it
        # splitext('1.html') --> ('1', '.html')
        # splitext('2.3.html') --> ('2.3', '.html')
        filenames = [f for f in filenames if os.path.splitext(f)[1] in filetypes_code + filetypes_other]
        cnt_files += len(filenames)
        
        
        if len(filenames) > overflow_fcnt:
            print("\t*****Skipping dir coz of overflow_fcnt:", len(filenames), "*****\n")
            continue
            
            
        if verbose:
            print("\tlen subdirs:", len(subdirs))
            print("\tsubdirs:", [os.path.join(base_dir, d) for d in subdirs[:5]])
            print("\tlen files:", len(filenames))
        
        # tree.txt
        for f in filenames:
            # /home/{user}/courses/DeepLearning.ai/tree.txt
            fsrc = os.path.join(base_dir, f)
            
            # skip if it is symbolic link
            if not os.path.islink(fsrc):
                
                # /home/{user}/courses/DeepLearning.ai/
                fsrc_dir = os.path.dirname(fsrc)

                # /home/{user}/research-backup/courses/DeepLearning.ai/
                # don't use lstrip or strip as it's char based and will remove extra chars
                fdest_dir = os.path.join(backup_dir, fsrc_dir.split(root_dir)[1])
                
                if not os.path.isdir(fdest_dir):
                    os.makedirs(fdest_dir)
                    if verbose: print("\tCreated folder:", fdest_dir)
                
                # /home/{user}/research-backup/courses/DeepLearning.ai/tree.txt
                fdest = os.path.join(fdest_dir, f)
                
                fsize = os.path.getsize(fsrc)
                size_total += fsize
                
                # MAX_SIZE is in MB
                # apply MAX_SIZE limit only on filetypes_other
                if os.path.splitext(f)[1] in filetypes_code or (os.path.splitext(f)[1] in filetypes_other and fsize/10**6 <= max_filesize):
                    # file isn't already present in dest_dir: copy it
                    if not os.path.isfile(fdest):
                            if not dry_run: shutil.copy2(fsrc, fdest_dir) 
                            cnt_copied += 1
                            size_copied += fsize
                            if verbose: print("\tCopied first:", fdest)

                    # if file is present: we check modified date difference
                    else:
                        fsrc_time = os.path.getmtime(fsrc)
                        fdest_time = os.path.getmtime(fdest)

                        # if src file is older than mod_time_diff: copy it
                        if fsrc_time - fdest_time > mod_time_diff:
                            if not dry_run: shutil.copy2(fsrc, fdest_dir) 
                            cnt_copied += 1
                            size_copied += fsize
                            if verbose: print("\tCopied mod:", fdest)
                                
                        else:
                            if verbose: print(f"\tSkipped due to time: {fsrc}|  {time.ctime(os.path.getmtime(fsrc)),time.ctime(os.path.getmtime(fsrc))}")
                            
                            cnt_skipped += 1
                            size_skipped += fsize
                
                else:
                    if verbose: print(f"\tSkipped due to size: {fsrc} | size: {fsize}")
                    cnt_skipped += 1
                    size_skipped += fsize
        
        if verbose: print("-"*40, "\n")
    
    print(f"\nTotal files: {cnt_files} |copied: {cnt_copied} |skipped: {cnt_skipped}")
    print(f"Total size: {round(size_total/10**6,2)} MB |copied: {round(size_copied/10**6, 2)} MB |skipped: {round(size_skipped/10**6, 2)} MB")
    print("*"*60, "\n")
    
    return [cnt_files, cnt_copied, cnt_skipped, size_total, size_copied, size_skipped]
          

    

def run_backup(folders_to_backup, backup_dir, root_dir,
            skip_dirs = [".git", ".ipynb_checkpoints", ".data"],
            large_dirs = ["isb", "kp_extraction", "others"],
            filetypes_code = [".py", ".ipynb", ".c", ".cpp", ".sh", ".js"],
            filetypes_other = [".txt", ".csv", ".pkl", ".html", ".json"],
            overflow_fcnt = 100, max_filesize = 10, mod_time_diff = 1*60*60, 
            verbose=False, dry_run=False):
    
    stats = [0,0,0,0,0,0]

    for folder in folders_to_backup:
        folder = os.path.join(root_dir, folder)
        print("Backing up:", folder, os.path.basename(folder))

        # [cnt_files, cnt_copied, cnt_skipped, size_total, size_copied, size_skipped]
        result = generate_backup_dir(folder, backup_dir, root_dir, 
                                     skip_dirs, large_dirs, 
                                     filetypes_code, filetypes_other, 
                                     max_filesize, mod_time_diff, overflow_fcnt,
                                     verbose, dry_run)

        # adding the elements of result with stats
        stats = [sum(x) for x in zip(stats, result)]

    print(f"\nBacked up @ {time.strftime('%d/%m/%Y, %H:%M:%S')}")
    print(f"Total files: {stats[0]} |copied: {stats[1]} |skipped: {stats[2]}")
    print(f"Total size: {round(stats[3]/10**6,2)} MB |copied: {round(stats[4]/10**6, 2)} MB |skipped: {round(stats[5]/10**6, 2)} MB\n")

    

    
def get_backup_details(folders_to_backup, backup_dir):
    """
    gives {file, size} details of backuped up directory
    """
    total_files = 0
    total_size = 0

    for folder in [backup_dir] + folders_to_backup:

        # files on backup dir top level
        if folder == backup_dir:
            files = [os.path.join(backup_dir,f) for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir,f))]

            cnt_file = len(files)
            size = 0
            for f in files:
                size += os.path.getsize(f)
            size = round(size/10**6,2)

        else:
            folder = os.path.join(backup_dir, folder)
            size, cnt_file = get_dir_size(folder)

        total_size += size
        total_files += cnt_file

        print(f"{folder:<60} |size: {size} MB |files: {cnt_file}")


    print(f"\nBackup details @ {time.strftime('%d/%m/%Y, %H:%M:%S')}")
    print(f"size: {total_size:.2f} MB |total files: {total_files}\n")
    
    
    
if __name__ == "__main__":
    
    ## get configs
    with open("backup_config.pkl", "rb") as ip:
        dictionary = pickle.load(ip)

    user = dictionary["user"]
    backup_dir = dictionary["backup_dir"]
    root_dir = dictionary["root_dir"]
    skip_dirs = dictionary["skip_dirs"]
    large_dirs = dictionary["large_dirs"]
    folders_to_backup = dictionary["folders_to_backup"]

    # use this to check if there is no unwanted dir  --> as it doesn't have .txt
    filetypes_code = [".py", ".ipynb", ".c", ".cpp", ".sh"]

    # can have .csv, .pkl as well here since it has limit on max_filesize
    filetypes_other = [".txt"]

    MAX_FILE_SIZE = 10 # 10 MB
    MOD_TIME_DIFF = 1*60*60 # 1 hr

    OVERFLOW_FCNT = 100

    verbose = False

    print("\nSome configs:")
    print(f"  user: {user}")
    print(f"  backup_dir: {backup_dir}")
    print(f"  folders_to_backup:{folders_to_backup}")
    print(f"  filetypes_code:{filetypes_code}")
    print(f"  filetypes_other:{filetypes_other}")
    print("\n\tChange the 'backup_config.py' file and run that.")
    print("-"*80)

    
    print("\nCurrent backup details:")
    get_backup_details(folders_to_backup, backup_dir)
    print("-"*80)

    
    dry_mode_run = input("\nRun backup in dry-mode (y|n): ")
    if dry_mode_run == 'y':
        dry_run =  True
        print("\nRunning in dry run mode:")
        start_time = timeit.default_timer()

        run_backup(folders_to_backup, backup_dir, root_dir, 
                skip_dirs=skip_dirs, large_dirs=large_dirs, 
                filetypes_code=filetypes_code, filetypes_other=filetypes_other, 
                max_filesize=MAX_FILE_SIZE, mod_time_diff=MOD_TIME_DIFF, overflow_fcnt=OVERFLOW_FCNT,
                verbose=verbose, dry_run=dry_run)

    
        elapsed = timeit.default_timer() - start_time
        print("\n##Time Taken: %.2f sec." % elapsed)
        print("-"*80)
        

    dry_run = input("\nRun backup final (y|n): ")
    if dry_run == 'y':
        dry_run =  False
        start_time = timeit.default_timer()

        run_backup(folders_to_backup, backup_dir, root_dir, 
                skip_dirs=skip_dirs, large_dirs=large_dirs, 
                filetypes_code=filetypes_code, filetypes_other=filetypes_other, 
                max_filesize=MAX_FILE_SIZE, mod_time_diff=MOD_TIME_DIFF, overflow_fcnt=OVERFLOW_FCNT,
                verbose=verbose, dry_run=dry_run)

        
        elapsed = timeit.default_timer() - start_time
        print("\n##Time Taken: %.2f sec." % elapsed)
        print("-"*80)

        
    print("\nBackup details:")
    get_backup_details(folders_to_backup, backup_dir)
    print("-"*80)

