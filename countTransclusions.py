import requests

TEMPLATE_MARKER = '`@!#%@`'

def countTransclusions(server, page, template, session=None):
    if not server.endswith('.org'):
        server = server + '.org'
    
    if not session:
        session = requests.Session()

    payload = {
        'action': 'parse',
        'page': page,
        'prop': 'text',
        'templatesandboxtitle': f'Template:{template}',
        'templatesandboxtext': TEMPLATE_MARKER,
        'disablelimitreport': 1,
        'format': 'json',
        'formatversion': 2,
    }

    r = session.get(f'https://{server}/w/api.php', params=payload)
    data = r.json()
    text = data['parse']['text']
    return text.count(TEMPLATE_MARKER)


if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 3:
        print('Brakujące parametry')
        print(f'Użycie: {sys.argv[0]} <serwer> <strona> <szablon>')
        print('    serwer   - adres URL serwera wiki')
        print('    strona   - nazwa strony, na której szablon ma być zliczony')
        print('    szablon  - nazwa szablonu, który ma być zliczony')
        sys.exit(-1)
    print(countTransclusions(*sys.argv[1:4]))