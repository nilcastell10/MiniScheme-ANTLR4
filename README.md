### README.md

# Intèrpret de Mini-Scheme

Aquest projecte implementa un intèrpret per Mini Scheme utilitzant ANTLR i Python. L'intèrpret és capaç de llegir i avaluar expressions de Scheme, definir i cridar funcions, i fer servir estructures com llistes, expressions condicionals, i operadors lògics i matemàtics.

## Requisits previs

- **Java**: Necessari per executar ANTLR.
- **Python 3.10+**: Per executar l'intèrpret.
- **ANTLR v4.13.2**: Necessari per compilar la gramàtica del llenguatge.

## Contingut del projecte

- [Instal·lació i execució](#instal·lació-i-execució)
- [Estructura del projecte](#estructura-del-projecte)
- [Característiques](#característiques)
- [Jocs de proves](#jocs-de-proves)
- [Limitacions](#limitacions)
- [Tractament d'errors](#tractament-derrors)
- [Estil de codi](#estil-de-codi)
- [Decisions de disseny](#decisions-de-dissany)
- [Autor](#autor)

---

## Instal·lació i execució

### Pas 1: Instal·lar ANTLR

Si no tens ANTLR instal·lat, segueix aquests passos:

```bash
# Descarregar ANTLR
curl -O https://www.antlr.org/download/antlr-4.13.0-complete.jar
```

### Pas 2: Preparar el projecte

Executa la comanda `make` per generar els fitxers necessaris:

```bash
make
```

Aquest comandament genera els fitxers Python del lexer i el parser a partir de la gramàtica.

### Pas 3: Executar l'intèrpret

Un cop generats els fitxers, l'intèrpret llegeix programes escrits en Scheme i els executa. Pots passar un fitxer .scm com a argument:

```bash
python3 scheme.py programa.scm
```

També pots redirigir entrades i sortides:

```bash
python3 scheme.py programa.scm < entrada.inp > sortida.out
```

## Estructura del projecte

El projecte inclou els següents fitxers:

- `scheme.g4`: La gramàtica ANTLR que defineix la sintaxi de Mini Scheme.
- `scheme.py`: El programa principal de l'intèrpret.
- `visitor.py`: El visitador de l'intèrpret.
- `errorListener`: El tractament d'errors sintàctics de l'intèrpret.
- `Makefile`: Fitxer per compilar i netejar el projecte.
- `README.md`: Explicació del projecte.
- Jocs de proves:
  - `.scm`: Programes de Scheme que demostren les funcionalitats implementades.
  - `.inp`: Entrades per als programes de prova.
  - `.out`: Sortides esperades per als programes de prova.

## Característiques

- **Definició de variables**:
  ```scheme
  (define x 10)
  (define y 20)
  ```

- **Definició de funcions**:
  ```scheme
  (define (suma a b) (+ a b))
  (suma 3 4)  ; Retorna 7
  ```

- **Expressions condicionals**:
  ```scheme
  (if (< x y) "menor" "major")
  (cond ((< x y) "menor") (else "igual o major"))
  ```

- **Operadors matemàtics**: `+`, `-`, `*`, `/`, `mod`
- **Operadors lògics**: `and`, `or`, `not`, `<`, `<=`, `>`, `>=`, `<>`, `=`
- **Operacions amb llistes**: `car`, `cdr`, `cons`, `null?`
- **Quotes**: Suport per a llistes literals:
  ```scheme
  '(1 2 3 4)
  ```
- **Suport per a `let`**:
  ```scheme
  (let ((x 10) (y 20)) (+ x y))
  ```

- **Entrada interactiva amb `read`**:
  ```scheme
  (define llista (read))
  ```

- **Sortida formatada amb `display` i `newline`**.

## Jocs de proves

Els jocs de proves es troben als fitxers `.scm`. Cada prova inclou:

- **Codi**: El programa en Scheme.
- **Entrada**: Si el programa necessita dades d'entrada.
- **Sortida esperada**: El resultat esperat.

Exemple de joc de proves:

### Fitxer `prova.scm`
```scheme
(define x (read))
(define y 20)
(display (+ x y))
```

### Fitxer `prova.inp`
```plaintext
10
```

### Fitxer `prova.out`
```plaintext
30
```

## Limitacions

- Els errors d'execució, com divisions per zero, tenen efectes indefinits.
- Alguns errors com els de tipus també tenen efectes indefinits.

## Tractament d'errors

### Errors de sintaxi

- **Mecanisme:** El lexer i el parser tenen listeners personalitzats `(SchemeErrorListener)` que intercepten errors de sintaxi.
- **Sortida:** Quan es detecta un error de sintaxi, es mostra un missatge clar indicant la línia, columna i el motiu de l'error. Per exemple:
```bash
Error de sintaxi a la línia 3, columna 15: missing ')'
```
### Errors semàntics

- **Funcionament:** El visitor quan detecta un error semàntic treu un missatge com aquest:
```bash
Error a la línia 3, columna 15: Error: Variable 'a' no definida. ')'
```

## Estil de codi

- El codi segueix les regles de l'estíl PEP8, excepte la llargada de les línies.
- No s'utilitzen tabuladors, només espais.

## Decisions de dissany

- Durant el desenvolupament de l'intèrpret de Mini Scheme, s'han pres diverses decisions de disseny clau per garantir la seva funcionalitat, robustesa i mantenibilitat. A continuació, es descriuen aquestes decisions:

### Elecció de l'arquitectura

- **Estructura basada en visitadors:** S'ha utilitzat el patró visitador per implementar la lògica de l'intèrpret.

### Gestió de l'entorn

- **Diccionari per a variables i funcions:** L'entorn d'execució es gestiona amb un diccionari (`self.environment`) que emmagatzema tant variables com funcions. Això permet accedir i modificar fàcilment els valors durant l'execució.

- **Entorns locals per a `let`:** S'han implementat còpies de l'entorn global per suportar declaracions locals en expressions `let`, assegurant que els canvis no afectin l'entorn global.

### Tractament de llistes

- **Format personalitzat:** Les llistes es processen com a estructures natives de Python (`list`) però es mostren en el format de Scheme. 

- **Suport per a llistes citades:** Les llistes citades (`'(1 2 3)`) es processen adequadament tant en lectura com en visualització.

### No implementacions

- **main:** No s'ha implementat la funcionalitat de començar el programa amb un main. Si hi ha un main definit, cal cridar-lo com qualsevol altra funció.


## Autor

Creat per Nil Castell com a projecte de pràctica per al curs de Llenguatges de Programació.


