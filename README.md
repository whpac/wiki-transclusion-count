# Zliczarka wywołań szablonów w MediaWiki

Niniejszy skrypt służy do zliczania wywołań danych szablonów na stronach wiki.

## Zliczanie na jednej stronie
Aby policzyć transkluzje szablonu na pojedyczej stronie, należy wykorzystać skrypt `countTransclusions.py`. Przyjmuje on jako parametry adres serwera, nazwę strony i nazwę szablonu:
```bash
countTransclusions.py pl.wikipedia "C (język programowania)" Cytuj
```

Wynikiem powyższego skryptu będzie liczba wystąpień szablonu `{{Cytuj}}` na stronie *C (język programowania)* na polskiej Wikipedii. Domyślnie, zagnieżdżone szablony są zliczane jako kilka. Jeśli zamierzonym efektem dla wikikodu `{{f|{{f}}...}}` byłoby 1, należy użyć przełącznika `-c`.

## Określanie maksimum spośród wielu stron
Skrypt `maxTransclusions.py` pozwala na znalezienie strony, która najwięcej razy wywołuje dany szablon. W jednym przebiegu skryptu możliwe jest zliczanie wystąpień dla kilku szablonów. W takiej sytuacji zostanie również podana strona, gdzie występuje sumarycznie najwięcej rozważanych szablonów.

Ten skrypt może działać na stronach wczytanych z pliku (wygenerowanego np. z użyciem `listPages.py`) albo pobrać wszystkie strony z danej przestrzeni przed przystąpieniem do zliczania. Przykłady zastosowania:
```bash
maxTransclusions.py pl.wikipedia Cytuj --ns 0 -o raport.txt
maxTransclusions.py pl.wikipedia Cytuj "Cytuj pismo" -p strony.txt
```

Warto możliwie ograniczyć liczbę sprawdzanych stron, ponieważ każda para (strona, szablon) powoduje konieczność wykonania żądania do API serwisu i parsowania zawartości strony. Spodziewane tempo działania to około 1 sprawdzenie na sekundę.

## Listowanie stron
Skryptem pomocniczym jest `listPages.py`, który pozwala na wylistowanie wszystkich stron z danej przestrzeni nazw, spełniających pewne wyrażenie regularne. Przykłady:
```bash
listPages.py pl.wikipedia 0 -o strony.txt
listPages.py pl.wikipedia 0 -r "\(ujednoznacznienie\)$" -o ujednoznacznienia.txt
```

## Wymagania
Skrypty wymagają do działania środowiska Python 3 z zainstalowaną biblioteką requests, którą można zainstalować poniższym poleceniem:
```bash
python -m pip install requests
```