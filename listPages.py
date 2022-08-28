import json
from time import sleep
import urllib.parse
import urllib.request

def listPages(server, namespace):
    if not server.endswith('.org'):
        server = server + '.org'

    continue_token = None
    allpages = []
    i = 0
    while True:
        i += 1
        if i % 100 == 0:
            sleep(1)

        if continue_token is not None:
            continue_token = urllib.parse.quote(continue_token)
            apcontinue = f'&apcontinue={continue_token}'
        else:
            apcontinue = ''
        url = rf'https://{server}/w/api.php?action=query&list=allpages&apnamespace={namespace}&aplimit=max&format=json&formatversion=2' + apcontinue;

        with urllib.request.urlopen(url) as f:
            response = f.read().decode('utf-8')
            data = json.loads(response)
            pages = data['query']['allpages']
            pages = map(lambda page: page['title'], pages)
            allpages.extend(pages)

            if 'continue' in data and 'apcontinue' in data['continue']:
                continue_token = data['continue']['apcontinue']
            else:
                break
    return allpages


if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 2:
        print('Brakujące parametry')
        print(f'Użycie: {sys.argv[0]} <serwer> <przestrzeń nazw>')
        print('    serwer           - adres URL serwera wiki')
        print('    przestrzeń nazw  - numer przestrzeni nazw, w której listować strony')
        sys.exit(-1)
    print(listPages(*sys.argv[1:3]))