""" r' Script: DuplicateRemover.py  Generate file hash signatures, removes duplicates 

# Author : Bartlomiej Zuranski aka BonZur
# Created 25/12/2018 modified: ..."""

import os,sys,shutil
import hashlib,time
now = time.ctime(int(time.time()))
block_size=256*128 # 4096 octets (Default NTFS)
line = '-'*50
fin= '~'*180
def hash_box(directory):
    """ CHECK ALL HASHES IN SRC and / r DEST Directory , Find and remove duplicates,empty dirs.Provide big file hssh handling. Adjust in main as needed """
    print('[-] Please wait, creating hashlib record of:',directory,'\n[-] Duplicated files in:',directory,' will be removed ')
    filed={}
    r=0
    for i in os.walk(directory):
        ab=(i[0])
        os.chdir(ab)
        for i in os.listdir(ab):
            if os.path.isfile(i):
                f_hash = hashlib.md5()
                #print('Hashing file: ',i) # %of operation to be implemented
                with open(i,'rb') as f: 
                    for chunk in iter(lambda: f.read(block_size),b''): 
                        f_hash.update(chunk)
                f.close()
                f_hash = f_hash.hexdigest()
                if f_hash in filed.keys():
                    match = filed[f_hash][0]
                    find = filed[f_hash][1]
                    print('\n[!] Match: Identical Files in:',directory,'\n->',i,f_hash,'\n->',match,f_hash)
                    print('\n[-] Location of:',i,'\n->',os.path.abspath(i),'\n[-] Location of:',match,'\n->',find)
                    print('[!] Deleting Duplicate: ',os.path.abspath(i),'\n',line)    
                    r+=1
                    os.remove(i) 
                else:
                    lock = os.path.abspath(i)
                    filed[f_hash]=[i,lock]
            elif os.path.isdir(i) and len(os.listdir(i)) == 0: # If directory is Empty: rmdir
                os.rmdir(i) 
    print('\n[-] No duplicates in:',directory,'Deleted duplicates:,',r,'\n',line)
	
def remove_dir(directory):
    """ Removes dir if dir remains empty after duplicate removal"""
    for i in os.walk(directory):
        ab=(i[0])
        os.chdir(ab)
        for i in os.listdir(ab):
            if os.path.isdir(i) and len(os.listdir(i)) == 0: # If directory is Empty: rmdir
                os.rmdir(i)
                print('[-] Empty Dir:',i,'removed')
	
def main():
        gap = '	    '
        if len(sys.argv) != 2:                      
                print(line,'\n[-] Usage:',gap,'C:\Folder_1','\n[-] Enter Directory')
                print(line)
                sys.exit(1)
        directory = sys.argv[1]
        start = time.time()
        #log_file = log_file = open(r'C:\tmp\log_file.txt',"a")
        #old_stdout = sys.stdout
        #sys.stdout = log_file
        hash_box(directory)   # PERFORMING SOURCE DIR DUPLICATES LOOKUP AND ELIMINATION, can be used as seperate module 
        remove_dir(directory)
        end = time.time()
        #print(line,'\n[-] Process complete.{} B.Zuranski_Copyright\n{}'.format(now,fin))
        #sys.stdout = old_stdout
        #log_file.close()
        print("[*] It took: {0:.2f}".format(end - start),"seconds to run the program")
        print(line,'\n[-] Process complete. B.Zuranski_Copyright')
		
if __name__ == '__main__':
	main()

	
