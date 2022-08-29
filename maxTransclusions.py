from argparse import ArgumentParser
from countTransclusions import countTransclusions
from listPages import listPages
from time import sleep
import requests

argparser = ArgumentParser()
argparser.add_argument('server', metavar='serwer', type=str, help='adres URL serwera wiki')
argparser.add_argument('templates', metavar='szablon', type=str, nargs='+', help='nazwa szablonu, który ma być zliczany')
group = argparser.add_mutually_exclusive_group(required=True)
group.add_argument('--namespace', '--ns', '-n', metavar='przestrzeń_nazw', type=int, help='numer przestrzeni nazw, z której listować strony')
group.add_argument('--pages', '-p', metavar='strony', type=str, help='plik z listą stron, które mają być wzięte pod uwagę')
argparser.add_argument('--output', '-o', metavar='plik', type=str, help='plik wyjściowy z wynikami')
args = argparser.parse_args()


session = requests.Session()

print('Wczytywanie listy stron...')
if args.pages:
    with open(args.pages, 'r') as f:
        allpages = f.read().splitlines()
else:
    allpages = listPages(args.server, args.namespace)

# allpages = [x for x in allpages if x.endswith('/całość')]

print(f'Znaleziono stron: {len(allpages)}')

i = 1
TOTAL_KEY = '|total'
max_counts = { x: (-1, None) for x in args.templates }
max_counts[TOTAL_KEY] = (-1, None)

for page in allpages:
    total = 0
    for template in args.templates:
        count = countTransclusions(args.server, page, template, session=session)
        total += count
    
        if count > max_counts[template][0]:
            max_counts[template] = (count, page)
    
    if total > max_counts[TOTAL_KEY][0]:
        max_counts[TOTAL_KEY] = (total, page)

    if i % 10 == 0:
        sleep(1)
    if i % 100 == 0:
        print(f'{i}/{len(allpages)}')
    i += 1

print('Zakończono zliczanie')
print('Maksymalne liczba wystąpień:')
for template, (count, page) in max_counts.items():
    if template == TOTAL_KEY:
        continue
    print(f'{{{{{template}}}}}:\t{count}\t({page})')

if len(args.templates) > 1:
    print('\Dla wszystkich szablonów razem wziętych:')
    print(f'{max_counts[TOTAL_KEY][0]}\t({max_counts[TOTAL_KEY][1]})')


if args.output:
    with open(args.output, 'a') as f:
        for template, (count, page) in max_counts.items():
            if template == TOTAL_KEY:
                template = '(wszystkie)'
            print(f'{template}:\t{count}\t({page})')