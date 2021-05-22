import os
import argparse

def default_listing(files):
    print(len(files))
  
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--list', dest='list_files', help='list files', action='store_true')
        parser.set_defaults(list_files=False)
        args = parser.parse_args()
  
        dir_list = os.listdir()
        if args.list_files:
            print(" ".join(dir_list))
            default_listing(dir_list)
 
 
if __name__ == '__main__':
          main()