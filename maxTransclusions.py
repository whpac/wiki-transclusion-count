from argparse import ArgumentParser
from countTransclusions import countTransclusions, fetchTemplateWikitext
from listPages import listPages
from time import time
import requests

argparser = ArgumentParser()
argparser.add_argument('server', metavar='serwer', type=str, help='adres URL serwera wiki')
argparser.add_argument('templates', metavar='szablon', type=str, nargs='+', help='nazwa szablonu, który ma być zliczany')
group = argparser.add_mutually_exclusive_group(required=True)
group.add_argument('--namespace', '--ns', '-n', metavar='przestrzeń_nazw', type=int, help='numer przestrzeni nazw, z której listować strony')
group.add_argument('--pages', '-p', metavar='strony', type=str, help='plik z listą stron, które mają być wzięte pod uwagę')
argparser.add_argument('--output', '-o', metavar='plik', type=str, help='plik wyjściowy z wynikami')
args = argparser.parse_args()


start_time = time()
session = requests.Session()

print('Wczytywanie listy stron...')
if args.pages:
    with open(args.pages, 'r', encoding='utf-8') as f:
        allpages = f.read().splitlines()
else:
    allpages = listPages(args.server, args.namespace, session=session)

print(f'Znaleziono stron: {len(allpages)}')

i = 1
TOTAL_KEY = '|total'
max_counts = { x: (-1, None) for x in args.templates }
max_counts[TOTAL_KEY] = (-1, None)

template_contents = {}
for template in args.templates:
    template_contents[template] = fetchTemplateWikitext(args.server, template, session=session)

for page in allpages:
    total = 0
    for template in args.templates:
        count = countTransclusions(args.server, page, template, session=session, template_content=template_contents[template])
        total += count
    
        if count > max_counts[template][0]:
            max_counts[template] = (count, page)
    
    if total > max_counts[TOTAL_KEY][0]:
        max_counts[TOTAL_KEY] = (total, page)

    if i % 100 == 0:
        print(f'{i}/{len(allpages)}')
    i += 1

end_time = time()

print('Zakończono zliczanie')
print('Maksymalna liczba wystąpień:')
for template, (count, page) in max_counts.items():
    if template == TOTAL_KEY:
        continue
    print(f'{{{{{template}}}}}:\t{count}\t({page})')

if len(args.templates) > 1:
    print('\nDla wszystkich szablonów razem wziętych:')
    print(f'{max_counts[TOTAL_KEY][0]}\t({max_counts[TOTAL_KEY][1]})')

print(f'\nCzas wykonania: {round(end_time - start_time)} sekund')

if args.output:
    with open(args.output, 'a') as f:
        for template, (count, page) in max_counts.items():
            if template == TOTAL_KEY:
                template = '(wszystkie)'
            f.write(f'{template}:\t{count}\t({page})\n')