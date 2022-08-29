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
    from argparse import ArgumentParser

    argparser = ArgumentParser()
    argparser.add_argument('server', metavar='serwer', type=str, required=True, help='adres URL serwera wiki')
    argparser.add_argument('namespace', metavar='przestrzeń_nazw', type=int, required=True, help='numer przestrzeni nazw, z której listować strony')
    argparser.add_argument('--output', '-o', metavar='plik', type=str, help='plik wyjściowy z wynikami')
    args = argparser.parse_args()
    pages = listPages(args.server, args.namespace)
    
    if args.output and args.output != '-':
        with open(args.output, 'w') as f:
            for page in pages:
                f.write(page + '\n')
    else:
        for page in pages:
            print(page)
