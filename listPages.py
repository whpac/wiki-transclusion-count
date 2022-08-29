from time import sleep
import re
import requests

def listPages(server, namespace, session=None):
    if not server.endswith('.org'):
        server = server + '.org'

    if not session:
        session = requests.Session()

    continue_token = None
    allpages = []
    i = 0
    while True:
        i += 1
        if i % 100 == 0:
            sleep(1)

        payload = {
            'action': 'query',
            'list': 'allpages',
            'apnamespace': namespace,
            'aplimit': 'max',
            'apcontinue': continue_token,
            'format': 'json',
            'formatversion': 2,
        }
        r = session.get(f'https://{server}/w/api.php', params=payload)
        data = r.json()
        pages = data['query']['allpages']
        pages = map(lambda page: page['title'], pages)
        allpages.extend(pages)

        if 'continue' not in data:
            break
        continue_token = data['continue']['apcontinue']
    return allpages


if __name__ == '__main__':
    from argparse import ArgumentParser

    argparser = ArgumentParser()
    argparser.add_argument('server', metavar='serwer', type=str, help='adres URL serwera wiki')
    argparser.add_argument('namespace', metavar='przestrzeń_nazw', type=int, help='numer przestrzeni nazw, z której listować strony')
    argparser.add_argument('--output', '-o', metavar='plik', type=str, help='plik wyjściowy z wynikami')
    argparser.add_argument('--regex', '-r', metavar='filtr', type=str, help='wyrażenie regularne, do którego muszą pasować nazwy stron')
    args = argparser.parse_args()
    pages = listPages(args.server, args.namespace)

    if args.regex:
        regex = re.compile(args.regex)
        pages = filter(lambda page: regex.match(page), pages)
    
    if args.output and args.output != '-':
        with open(args.output, 'w', encoding='utf-8') as f:
            for page in pages:
                f.write(page + '\n')
    else:
        for page in pages:
            print(page)
