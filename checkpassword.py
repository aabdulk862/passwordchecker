import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, check with the API and try again')
    return res

def get_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':')for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5)
    return get_leaks_count(response, tail)

def main(args):
    for password in args:
        count = api_check(password)
        if count:
            print(f'Oh no! This password has been seen {count} times before on "haveibeenpwned.com"\nIf you\'ve ever used it anywhere before, change it! :/')
        else:
            print('Good news!! This password was NOT found on "haveibeenpwned.com"\nThat doesn\'t necessarily mean it\'s a good password, merely that it\'s not indexed on the site')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))