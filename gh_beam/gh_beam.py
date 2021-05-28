import os, argparse, configparser, shutil, sys, stat
import base64
from github import Github
from github import GithubException
from pathlib import Path
import os.path
from pwn import log
from pwnlib import ui

app_args = None
home_path = str(Path.home())
config_path = home_path + '/.config/gh_beam/gh_beam.conf'
gh_beam_path = os.path.abspath(__file__)
gh_beam_dir = os.path.dirname(gh_beam_path)

token = ''

def default_listing(files):
    print(len(files))


def configuration():
    global token

    if not os.path.exists(config_path):
        print(gh_beam_dir)
        print(gh_beam_dir + '/' + 'gh_beam.conf')
        try:
            if not os.path.exists(os.path.dirname(config_path)):
                os.makedirs(os.path.dirname(config_path))
            
            shutil.copyfile(gh_beam_dir + '/' + 'gh_beam.conf', config_path)
        except:
            e = sys.exc_info()[0]
            print("Something went wrong with creating the configuration")
            print(e)

    if os.path.exists(config_path):      
        config = configparser.ConfigParser()
        config.read(config_path)
        
        token = config.get('Settings', 'token')


def arguments():
    #global app_args
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', dest='list_files', help='list files', action='store_true')
    parser.set_defaults(list_files=False)

    return parser


def download_directory(repository, server_path, local_path):
    """
    Download all contents at server_path with commit tag sha in
    the repository.
    """
    if os.path.exists(local_path + "/" + repository.name):
        shutil.rmtree(local_path + "/" + repository.name)

    os.makedirs(local_path + "/" + repository.name)
    contents = repository.get_dir_contents(server_path)

    for content in contents:
        print ("Processing %s" % content.path)
        if content.type == 'dir':
            os.makedirs(content.path)
            download_directory(repository, content.path, local_path)
        else:
            try:
                path = content.path
                file_content = repository.get_contents(path)
                file_data = base64.b64decode(file_content.content)
                file_out = open(local_path + "/" + repository.name + "/" + content.path, "wb+")
                file_out.write(file_data)
                file_out.close()
            except (GithubException, IOError) as exc:
                print('Error processing %s: %s', content.path, exc)



def search_github(github, keywords):
    # SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N
    query = '+'.join(keywords) + '+in:readme+in:description'
    result = github.search_repositories(query, 'stars', 'desc')
    
    
    #print(f'{pm.clone_url}, {pm.stargazers_count} stars')

    print(f'Found {result.totalCount} repo(s)')

    for repo in result:
        print(f'{repo.clone_url}, {repo.stargazers_count} stars')


# might need some fuzzing here
def search_internal_repos(keyword):
    # later on this repo list will come from actual git repositories
    # which will maintain topics directories
    repo_found = []
    test_repos = [['Dewalt-arch/pimpmykali', 'script'], ['WebAssembly/wabt', 'binary']]
    for a_repo in test_repos:
        if keyword in a_repo[0]:
           repo_found.append(a_repo)

    return repo_found

    

  
def main():
        # types of repos
        # 1) pure scripts on root dir
        # 2) binary releases
        # 3) package managers, apt, pip, crates, gems, etc.
        # 4) folders within a repo

        

        parser = arguments()
        app_args = parser.parse_args()        
        configuration()

        g = Github(token)

        #pm = g.get_repo(test_repos[1])
        #print(pm.get_contents("/"))
        #print(pm.get_dir_contents("/"))
        #print(pm.get_tags())

        # for tag in pm.get_tags():
        #     print(tag)

        # release = pm.get_latest_release()     
        # assets = release.get_assets()

        # urls = []
        # for ass in assets:
        #     #log.info(ass.browser_download_url)
        #     urls.append(ass.browser_download_url)

        # answer = ui.options("prompt", urls)

        # print(urls[answer])
        
        # repos = g.get_user().get_repos()

        # for repo in repos:
        #     print(repo)

        keywords = input('Enter keyword(s)[e.g python, flask, postgres]: ')
        keywords = [keyword.strip() for keyword in keywords.split(',')]
        # search_github(g, keywords)
        repo_internal = search_internal_repos(keywords[0])
        if repo_internal:
            print(repo_internal[0])
        else:
            print("Nothing found.")

        # install test
        # 1 check if is installed, if it is compare dates

        # 2 install
        #download_directory(pm, '/', '/opt/test')

        # 3 chmod if necessary, maybe, skip for now
        #os.chmod('/opt/test/pimpmykali/pimpmykali.sh', stat.S_IRWXO)

        # 4 create ln -s in bin directory
        #os.symlink('/opt/test/pimpmykali/pimpmykali.sh', '/bin/scripts/pimpmykali.sh')
  
        dir_list = os.listdir()
        if app_args.list_files:
            print(" ".join(dir_list))
            default_listing(dir_list)
 
 
if __name__ == '__main__':
          main()