import json
import urllib.parse
import urllib.request

TEMPLATE_MARKER = '`@!#%@`'

def countTransclusions(server, page, template):
    if not server.endswith('.org'):
        server = server + '.org'

    page = urllib.parse.quote(page)
    template = urllib.parse.quote(template)
    marker = urllib.parse.quote(TEMPLATE_MARKER)
    url = rf'https://{server}/w/api.php?action=parse&page={page}&prop=text&templatesandboxtitle=Template:{template}&templatesandboxtext={marker}&disablelimitreport=1&format=json&formatversion=2';

    with urllib.request.urlopen(url) as f:
        response = f.read().decode('utf-8')
        data = json.loads(response)
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