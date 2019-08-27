import sys
import getpass
import re

import pwncollege_client


def main():
    username = input('username: ')
    password = getpass.getpass('password: ')

    client = pwncollege_client.Client()
    logged_in = client.login(username, password)

    if not logged_in:
        print('Your username or password is incorrect', file=sys.stderr, flush=True)
        exit(1)

    import pwn  # late import because pwntools messes up readline, needed by getpass

    for challenge in client.challenges():
        if challenge['name'] == 'cat' and challenge['category'] == '/bin':

            path = challenge['category'] + '/' + challenge['name']

            pwn.log.info(f"Challenge: {challenge['id']} -- {path}")
            client.work_on(challenge['id'])

            # You must `ssh-add <path to private key` first
            ssh = pwn.ssh('cse466', 'cse466.pwn.college', ssh_agent=True)

            output = ssh('/bin/cat /flag').decode()

            flag = re.search('pwn_college{(?P<flag>.*?)}', output)

            if flag:
                flag = flag['flag']
                pwn.log.info(f"Flag: {flag}")

                correct_flag = client.submit_flag(challenge['id'], flag)
                pwn.log.info(f"Correct: {correct_flag}")


if __name__ == '__main__':
    main()
