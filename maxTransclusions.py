from time import sleep
from countTransclusions import countTransclusions
from listPages import listPages
import sys

if len(sys.argv) <= 3:
    print('Brakujące parametry')
    print(f'Użycie: {sys.argv[0]} <serwer> <przestrzeń nazw> <szablon>')
    print('    serwer           - adres URL serwera wiki')
    print('    przestrzeń nazw  - numer przestrzeni nazw, w której listować strony')
    print('    szablon          - nazwa szablonu, który ma być zliczany')
    sys.exit(-1)

server, namespace, template = sys.argv[1:4]

print('Pobieranie listy stron...')

allpages = listPages(server, namespace)

print(f'Znaleziono stron: {len(allpages)}')

i = 1
max_count = -1
max_page = None
for page in allpages:
    count = countTransclusions(server, page, template)
    
    if count > max_count:
        max_count = count
        max_page = page

    if i % 10 == 0:
        sleep(1)
    if i % 100 == 0:
        print(f'{i}/{len(allpages)}: {page} ({count})')
    i += 1

print('Zakończono zliczanie')
print(f'Maksymalna liczba wystąpień: {max_count}')

with open('output.txt', 'w') as f:
    f.write(f'{max_page} ({max_count})')