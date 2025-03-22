
# Oleksandr Konovlenko

## Temat projektu
Język umożliwiający opis punktów i odcinków w przestrzeni trójwymiarowej. Punkt i odcinek (zbudowany z punktów) są wbudowanymi typami języka. Z odcinków można budować bryły. Kolekcja brył tworzy scenę wyświetlaną na ekranie.

## Specyfikacja
- Język: Python
- Typowanie zmiennych: slabe, dynamiczne

## Typy wbudowane
- **Typy proste**: `int`, `float`, `bool`, `string`
- **Typy złożone**:
  - `List`: Przechowuje obiekty, dostępne metody: 
    - `length()` : zwraca ilość elementów w liście
    - `get(x)`: zwraca element znajdujący się na pozycji x
    - `add(x)` : dodaje x-element na koniec listy
    - `remove(x)`: usuwa element znajdujący się na pozycji x, lub ostatni element jeśli x nie został podany
  - `Point`: Typ punktu z polami x, y, z oraz metodami do ich ustawiania (`set_x(x)`) i odczytu (`get_x()`).
  - `Line`: Definiowanie odcinka, dostępne metody: 
    - `set_start(start)` : ustawia punkt start
    - `set_end(end)`: ustawia punkt end
    - `get_start()`: zwraca punkt start
    - `get_end()`: zwraca punkt end
    - `length()` : długość odcinka
  - `Polyhedron`: Typ umożliwiający definiowanie bryły składającej się z dowolnej liczby odcinków, przy czym warunkiem koniecznym do jej stworzenia jest połączenie odcinków w jednolitą strukturę, gdzie każdy punkt bryły posiada co najmniej 3 różne wychodzące z niego odcinki. Typ ten oferuje następujące metody:
    - `points()` : zwraca listę punktów tworzących bryłę
    - `lines()`: zwraca listę odcinków wchodzących w skład bryły
  - `Collection`: Typ umożliwiający definiowanie zbioru brył, który może być wyświetlany na ekranie. Zawiera następujące metody:
    - `add(Polyhedron)` : dodaje bryłę do zbioru
    - `remove(Polyhedron)` : usuwa bryłę ze zbioru
    - `display()` : wyświetla trójwymiarowy rzut zbioru brył na ekranie
    - `empty()` : usuwa wszystkie bryły ze zbioru

## Operatory

| Typ               | Operator                             | 
|-------------------|--------------------------------------|
| Arytmetyczne      | `+, -, *, /`                         |
| Logicze           | `==, !=, >, <, >=, <=` oraz `or, and`|
| Przypisania       | `=`                                  |
| Dostęp do obiektu | `.`                                  |
| Negacja           |`-, !`                                |

### Dla poszczególnych typów dostępne są następujące operatory:

| Typ          | Operator                                 |
|--------------|------------------------------------------|
| int, float   | `=, +, -, *, /, ==, !=, >, <, >=, <=`    |
| bool         | `=, ==, !=, or, and, !`                  |
| string       | `=, +, ==, !=`                           |
| List         | `=, +, ==, !=, .`                        |
| Point, Line, Polyhedron, Collection | `=, ==, !=, .`    |

## Tworzenie zmiennych
Zmienne można tworzyć przez określenie ich typu i przypisanie wartości np.
```
int liczba = 0;
string tekst = "przyklad";
```

## Komentarze
Komentarze tworzymy dodając `#` na początku linii.

## Struktury kontrolne
- **Instrukcja warunkowa** `if (warunek) { ... } else { ... }`
 ```
if (liczba == 0)
{
    liczba = 1;
}
else
{
    liczba = 2;
}
```
- **Pętla** `while(warunek) { ... }`
 ```
while(liczba >= 17)
{
    liczba = liczba * liczba;
}
```

## Definiowanie funkcji
Wszystkie programy muszą zawierać funkcję `int main()`, która jest punktem startowym wykonania. Funkcje można definiować z typem zwracanej wartości, np.:
```
int suma(a, b) {
    return a + b;
}
```

## Przykładowy kod programu

```
# przykładowa funkcja
bool is_vertex(Point a, Polyhedron p)
{
    bool vertex = False;
    int n = p.points().length();
    int i = 0;

    while(i < n)
    {
        if(p.points().get(i).x == a.x and p.points().get(i).y == a.y and p.points().get(i).z == a.z)
        {
            vertex = True;
        }
        i = i + 1;
    }

    return vertex;
}

int main()
{
  # definicja zmiennych
  a = Point(0, 0, 0);
  b = Point(2, 3, 0);
  c = Point(6, 1, 2);
  d = Point(4, 7, 5);

  ab = Line(a, b);
  ac = Line(a, c);
  ad = Line(a, d);
  bc = Line(b, c);
  bd = Line(b, d);
  cd = Line(c, d);

  p = Polyhedron(ab, ac, ad, bc, bd, cd);

  scene = Collection();


  # dodanie wielokąta do sceny i wyświetlenie go
  scene.add(p);
  scene.display();


  # wywołanie funkcji oraz wypisanie wartości do konsoli
  bool result = is_vertex(c, p);
  print(result);
}
```

### Analiza kodu

#### Funkcja `is_vertex`

Funkcja `is_vertex` przyjmuje dwa argumenty:
- `Point a`: punkt, który chcemy sprawdzić,
- `Polyhedron p`: bryła, w której sprawdzamy, czy punkt `a` jest jednym z jej wierzchołków.

Funkcja działa w następujący sposób:
1. Inicjuje zmienną `vertex` jako `False`, która będzie przechowywać wynik (czy punkt `a` jest wierzchołkiem `p`).
2. Pobiera liczbę punktów bryły `p` i przypisuje ją do zmiennej `n`.
3. Iteruje przez każdy punkt bryły `p` i sprawdza, czy współrzędne tego punktu są takie same, jak współrzędne punktu `a`.
4. Jeśli współrzędne są zgodne, ustawia zmienną `vertex` na `True`.
5. Zwraca wartość `vertex`, która mówi, czy punkt `a` jest wierzchołkiem bryły `p`.

#### Funkcja `main`

Funkcja `main` jest główną funkcją programu. Wykonuje następujące operacje:

1. Tworzy cztery punkty `a`, `b`, `c` i `d` o podanych współrzędnych.
2. Na podstawie punktów tworzy sześć odcinków: `ab`, `ac`, `ad`, `bc`, `bd` i `cd`.
3. Używając odcinków, tworzy bryłę `p`.
4. Tworzy obiekt `Collection` o nazwie `scene`, który przechowuje bryły.
5. Dodaje bryłę `p` do `scene` i wyświetla ją na ekranie za pomocą metody `display`.
6. Wywołuje funkcję `is_vertex` dla punktu `c` i bryły `p`, by sprawdzić, czy `c` jest wierzchołkiem `p`.
7. Wypisuje wynik (`True` lub `False`) do konsoli za pomocą funkcji `print`.

## Funkcje wbudowane
- print - wypisuje linię na wyjście standardowe.
- input - wejście


## Podział na moduły
Projekt podzielono na moduły odpowiadające za analizę leksykalną, składniową i interpretację kodu:

- **Lekser** - Moduł realizujący analizę leksykalną, który składa się z plików `source.py`, `lexer.py` oraz testów zawartych w `test_lexer.py`:
  - `source.py` - Moduł odpowiedzialny za wczytywanie kodu z pliku tekstowego lub ciągu znaków przekazanego w argumencie wywołania,
  - `lexer.py` - Moduł przeprowadzający analizę leksykalną, tworzący listę tokenów gotowych do analizy składniowej,

- **Parser** - Moduł realizujący analizę składniową, obejmujący pliki `nodes.py`, `parser.py` oraz testy w `test_parser.py`:
  - `nodes.py` - Moduł zawierający klasy reprezentujące węzły drzewa składniowego,
  - `parser.py` - Moduł odpowiedzialny za analizę składniową, tworzący drzewo składniowe gotowe do interpretacji,

- **Interpreter** - Moduł realizujący interpretację kodu, składający się z plików `classes.py`, `context.py`, `visitor.py`, `interpreter.py` oraz testów zawartych w `test_interpreter.py`:
  - `classes.py` - Moduł definiujący klasy reprezentujące typy danych złożonych, które są używane podczas interpretacji,
  - `context.py` - Moduł zawierający klasę reprezentującą kontekst interpretacji, przechowującą zmienne i funkcje,
  - `visitor.py` - Moduł implementujący klasę wizytatora drzewa składniowego, która przekształca drzewo składniowe na drzewo interpretacji,
  - `interpreter.py` - Moduł wykonujący interpretację kodu, zwracający wynik jego wykonania,

Dodatkowo, w pliku `errors.py` znajdują się klasy reprezentujące błędy, które mogą wystąpić podczas analizy leksykalnej, składniowej i interpretacji, a plik `main.py` zawiera funkcję `main`, odpowiedzialną za uruchomienie programu.

## Uruchamianie programu
Skrypt `main.py` uruchamiamy z argumentami:
- `-f` interpretacja kodu z pliku
- `-s` interpretacja kodu z ciągu znaków

Przykładowe wywołanie:
```
python3 main.py -f ./test/figury.txt
```

## Przykładowe wyświetlenie sceny
Scena wyświetlana na ekranie zawiera wielościany zbudowane z odcinków i punktów, układających się w bryły 3D, przedstawione w rzucie trójwymiarowym.

## Testowanie
Każdy moduł ma przygotowane testy jednostkowe za pomocą `pytest`. Testy znajdują się w folderze `tests`, a przykładowe pliki testowe w podfolderze `test_cases`.

## Biblioteki
Do wizualizacji brył używane są:
- `numpy` - do obliczeń,
- `matplotlib` i `scipy` - do renderowania brył na ekranie.

Dodatkowe wymagane biblioteki są w pliku `requirements.txt`.

## Gramatyka języka
Gramatyka języka określa zasady składni, które interpreter sprawdza i przetwarza podczas interpretacji kodu.

```
program                 = {function_declaration} ;

block                   = "{", {statement}, "}" ;

statement               = assignment | if_statement | while_statement | function_call, ";" | method_call, ";" | return, ";" ;

assignment              = type, identifier, "=", expression, ";" | identifier, "=", expression, ";"

if_statement            = "if", "(", expression, ")", block, ["else", block] ;

for_statement           = "for", identifier, "in", expression, block ;

while_statement         = "while", "(", expression, ")", block ;

function_call           = identifier, "(", [call_parameters_list], ")" ;

method_call             = identifier, ".", identifier, "(", [call_parameters_list], ")" ;

call_parameters_list    = expression, {",", expression} ;

function_declaration    = function_type, identifier, "(", [parameters_list], ")", block ;

parameters_list         = type, identifier, {",", type, identifier} ;

return                  = "return", [expression] ;

expression              = or_expression ;

or_expression           = and_expression, {or_operator, and_expression} ;

and_expression          = comparison_expression, {and_operator, comparison_expression} ;

comparison_expression   = arithmetic_expression, [comparison_operator, arithmetic_expression] ;

arithmetic_expression   = multiplicative_expression, {arithmetic_operator, multiplicative_expression} ;

multiplicative_expression = negation_expression, {multiplicative_operator, negation_expression} ;

negation_expression     = [negation_operator], method_call_expression ;

method_call_expression  = factor, {".", identifier, "(", [call_parameters_list], ")"} ;

factor                  = literal | identifier | function_call | "(", expression, ")" ;

arithmetic_operator     = "+" | "-" ;

multiplicative_operator = "*" | "/" ;

comparison_operator     = "==" | "!=" | ">" | "<" | ">=" | "<=" ;

or_operator             = "or" ;

and_operator            = "and" ;

negation_operator       = "-" | "!" ;

function_type           = "void" | type ;

type                    = "int" | "float" | "bool" | "string" | "Point" | "Line" | "Collection" | "List" ;

identifier              = letter, {letter | digit} ;

literal                 = int | float | bool | string ;

int                     = "0" | (non_zero_digit, {digit}) ;

float                   = int, ".", digit, {digit} ;

bool                    = "True" | "False" ;

string                  = '"', {char}, '"' ;

char                    = ({letter} | {digit} | {symbol}) ;

letter                  = #'[a-z]' | #'[A-Z]' ;

digit                   = "0" | "1" | ... | "9" ;

symbol                  = " " | "." | "," | "!" | "?" | ":" | "/" | "@" | "$" | "%" | "^" | "*" | "-" | "+" | "_";
```

## Analiza wymagań
- Program interpretuje kod z pliku tekstowego lub ciągu znaków przekazanego jako argument wywołania,
- Program wyświetla wynik działania na konsoli,
- Sprawdza poprawność leksykalną i składniową kodu, zgłaszając wykryte błędy,
- Zapewnia unikalność nazw zmiennych i funkcji,
- Weryfikuje poprawność tworzenia zmiennych typów złożonych,
- Umożliwia wielokrotne tworzenie i wyświetlanie scen zawierających bryły.


## Obsługa błędów
Program generuje komunikaty w przypadku błędów krytycznych, przerywając działanie programu.

Przykładowe komunikaty:
```
InvalidTokenError:
Błąd w linii 3, kolumna 4: Nieprawidłowy znak '^'
```

```
InvalidNumberOfArgumentsError:
Nieprawidłowa liczba argumentów:
Funkcja 'dodaj_zmienną' wywołana z nieprawidłową liczbą argumentów
```
