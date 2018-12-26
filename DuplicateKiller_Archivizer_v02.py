""" r' Script: DuplicateKiller.py  Generate file hash signatures, removes duplicates in source / destination or both, and copy files from Dir1 to Dir2'

Program can be called as main or used as a seperate definitions if required	
# Script: DuplicateKiller.py
# Author : Bartlomiej Zuranski aka BonZur
# Created 25/12/2018 modified: ..."""

import os,sys,shutil
import hashlib,time
now = time.ctime(int(time.time()))
block_size=256*128 # 4096 octets (Default NTFS)
line = '-'*50
fin= '~'*80
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
            elif os.path.isdir(i) and len(os.listdir(i)) == 0: # # If directory is Empty: rmdir
                os.rmdir(i) 
    print('\n[-] No duplicates in:',directory,'Deleted duplicates:,',r,'\n',line)
    return filed
    
def bobalice(filed,hashh):
    """  Check src_file hash against dest files hashes """
    print('Looking for file match in destination\n')
    if hashh in filed.keys():
            match2 = filed[hashh][0]
            flag2=1
            return flag2,match2
    else:
            print('No match found')
            flag2=0
            return flag2,None

def remove_empty(directory):
    """ Removes dir if dir remains empty after duplicate removal"""
    for i in os.walk(directory):
        ab=(i[0])
        os.chdir(ab)
        for i in os.listdir(ab):
            if os.path.isdir(i) and len(os.listdir(i)) == 0: # If directory is Empty: rmdir
                os.rmdir(i)
                print('[-] Empty Dir: >',i,'< from',directory,'removed')
		
		
def recursive_copy(dir1,dir2,filed):
        """ Reursive file and folder copy, if dest folder in archive doesn't exists: mkdir, if file with same name exists: name append  """
        n2=0
        c=0
        fe=0
        fo=0
        for i in os.walk(dir1):
                ab=(i[0])
                os.chdir(ab) # Directory abs path
                for i in os.listdir(ab):
                        if os.path.isdir(i):
                            if len(os.listdir(i)) == 0: # do not copy empty dir, and rm
                               os.rmdir(i)
                            else:
                                aa=os.path.abspath(i)
                                fp=aa.split('\\',2)[2:]
                                new_dst = os.path.join(dir2, str(fp).strip('[\']'))
                                if os.path.exists(new_dst):
                                        continue
                                else:
                                    try:
                                        os.mkdir(new_dst)
                                    except Exception as e:
                                        print('[!]\n[!]',e,'\n[!] Could not copy:',i,'\n',line,'\n',line)
                                        fo+=1
                        elif os.path.isfile(i):
                                #basename=os.path.basename(i)
                                #dirname=os.path.dirname(i)
                                aa=os.path.abspath(i)
                                fp=aa.split('\\',2)[2:]
                                new_dst = os.path.join(dir2, str(fp).strip('[\']')) 
                                a=open(i,'rb')
                                f_cont=a.read()
                                src_hash=hashlib.md5(f_cont).hexdigest()
                                a.close()
                                cwd = os.getcwd()
                                result1,result2= bobalice(filed,src_hash)
                                if os.path.exists(new_dst) and result1 == 0:
                                        print(line,'\nFile with same name alredy in archive -> Computing Md5sum')  #if same name perform quick hash comparision for log
                                        b= open(new_dst,'rb')
                                        f_contb =b.read()
                                        b.close()
                                        dst_hash=hashlib.md5(f_contb).hexdigest()
                                        j= os.path.basename(new_dst) 
                                        print('\nFile: ',i,'!=',j,'\n','-'*50)
                                        print('\nSrcF',i,src_hash,'\nDstF',j,dst_hash,'\n')
                                        app = j.split('.')
                                        app.insert(1,'{}.')
                                        nfile = ''.join(app)
                                        n=1
                                        while (os.path.exists(os.path.dirname(new_dst)+'\\'+nfile.format(n))):
                                                n+=1
                                        shutil.copy(i,os.path.dirname(new_dst)+'\\'+nfile.format(n))
                                        n2+=1
                                        print('File {} exist, copied file appended with {}'.format(j.format(n),n))
                                        print(line)										
                                elif result1 == 1:
                                    print('Found match: -> SrcF:',i,'\n 	     -> DstF:',result2)
                                    print('-> Skipping duplicate\n',line)
                                else:
                                    try:
                                        print('Copyied file :',shutil.copy(i, new_dst))
                                        c+=1
                                    except Exception as e:
                                        print('[!]\n[!]',e,'\n[!] Could not copy:',i,'\n',line,'\n',line)
                                        fe+=1
        print('[-]',c+n2,' Total files copied,( with appended name:',n2,')\n[!] File Errors:',fe,'\n[!] Folder Errors:',fo)
        #try:							
        #    shutil.rmtree(dir1)  # Remove SrcDir after copy
        #except: OSError
def main():
        gap = '	    '
        if len(sys.argv) != 3:                      
                print(line,'\n[-] Usage:',gap,'C:\Folder_1   C:\Folder_2','\n[-] Enter Top lvl: Src_Directory Dest_Directory')
                print(line)
                sys.exit(1)
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]
        if not os.path.exists(dir2):
            os.mkdir(dir2)
        #hash_box(dir1)   # PERFORMING SOURCE DIR DUPLICATES LOOKUP AND ELIMINATION, can be used as seperate module
        start = time.time()
        #log_file = open(r'C:\tmp\log_file.txt',"a") #try
        print('[-] Program Start...')
        #old_stdout = sys.stdout
        #sys.stdout = log_file
        filed = hash_box(dir2)
        recursive_copy(dir1,dir2,filed)
        remove_empty(dir2)
        end = time.time()
        #print(line,'\n[-] Process complete.{} B.Zuranski_Copyright\n{}'.format(now,fin))
        #sys.stdout = old_stdout
        #log_file.close()
        print("[*] It took: {0:.2f}".format(end - start),"seconds to run the program")
		
        "REFERENCE: To be done : Error read,write handling, Unicodedata Fixing, Chinese and bad chars handling i.e >>> '76-'85  >>>unicodedata.category(u'ヾ') >>>'Lm' "
if __name__ == '__main__':
	main()

	
