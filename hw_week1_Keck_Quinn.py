import paramiko
from os.path import expanduser, isdir
import os
from user_definition import *


# ## Assumption : Anaconda, Git (configured)

def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f "
                         "~/venv/environment.yml")
    if (b'already exists' in stderr.read()):
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f "
                             "~/venv/environment.yml")


# https://stackoverflow.com/questions/36488659/
# paramiko-scp-check-if-file-exists-on-remote-host
def git_clone(ssh):
    # ---- HOMEWORK ----- #
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        test = 'cd  ~ ;' + 'test -e {0} && echo exists'.format(git_repo_name)
        stdin, stdout, stderr = ssh.exec_command(test)
        out = stdout.read()
        if(b'exist' in out):
            git_directory = "cd " + git_repo_name + " ; git pull origin"
            stdin, stdout, stderr = ssh.exec_command(git_directory)
        else:
            clone = "git clone https://github.com/" + git_user_id
            repo = "/" + git_repo_name + ".git"
            stdin, stdout, stderr = ssh.exec_command(clone + repo)


def main():
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    git_clone(ssh)
    create_or_update_environment(ssh)


if __name__ == '__main__':
    main()
