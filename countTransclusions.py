import requests

TEMPLATE_MARKER = '`@!#%@`'

def fetchTemplateWikitext(server, template, session=None):
    if not server.endswith('.org'):
        server = server + '.org'
    
    if not session:
        session = requests.Session()

    payload = {
        'action': 'parse',
        'page': f'Template:{template}',
        'prop': 'wikitext',
        'format': 'json',
        'formatversion': 2,
    }

    r = session.get(f'https://{server}/w/api.php', params=payload)
    data = r.json()
    return data['parse']['wikitext']


def countTransclusions(server, page, template, session=None, template_content=''):
    if not server.endswith('.org'):
        server = server + '.org'
    
    if not session:
        session = requests.Session()

    payload = {
        'action': 'parse',
        'page': page,
        'prop': 'text',
        'templatesandboxtitle': f'Template:{template}',
        'templatesandboxtext': TEMPLATE_MARKER + template_content,
        'disablelimitreport': 1,
        'format': 'json',
        'formatversion': 2,
    }

    r = session.post(f'https://{server}/w/api.php', params=payload)
    data = r.json()
    text = data['parse']['text']
    return text.count(TEMPLATE_MARKER)


if __name__ == '__main__':
    from argparse import ArgumentParser

    argparser = ArgumentParser()
    argparser.add_argument('server', metavar='serwer', type=str, help='adres URL serwera wiki')
    argparser.add_argument('page', metavar='strona', type=str, help='nazwa strony, na której szablon ma być zliczony')
    argparser.add_argument('template', metavar='szablon', type=str, help='nazwa szablonu, który ma być zliczony')
    argparser.add_argument('--no-use-content', '-c', action='store_true', help='nie pobieraj zawartości szablonu z wiki (mniej dokładny wynik)')
    args = argparser.parse_args()

    template_content = ''
    if not args.no_use_content:
        template_content = fetchTemplateWikitext(args.server, args.template)

    print(countTransclusions(args.server, args.page, args.template, template_content=template_content))