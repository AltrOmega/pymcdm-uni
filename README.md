# raport

```
Wagi wyznaczone metodą entropy: [0.23292433 0.28732955 0.16765463 0.12709512 0.18499637]
Wyniki:
  Alternatywa  TOPSIS wynik  TOPSIS ranking  SPOTIS wynik  SPOTIS ranking  VIKOR wynik  VIKOR ranking
0  Samochód 1      0.535781               4      0.487782               1     0.475793              4
1  Samochód 2      0.554583               1      0.399662               4     0.198842              1
2  Samochód 3      0.548059               2      0.500000               0     0.828571              0
3  Samochód 4      0.451941               0      0.500000               2     1.000000              2
4  Samochód 5      0.597147               3      0.418131               3     0.092031              3

Korelacja Spearmana między rankingami:
TOPSIS vs SPOTIS: 0.8000
TOPSIS vs VIKOR: 0.9000
SPOTIS vs VIKOR: 0.9000

Interpretacja wyników:
Najlepsza alternatywa według TOPSIS: Samochód 5
Najlepsza alternatywa według SPOTIS: Samochód 2
Najlepsza alternatywa według VIKOR: Samochód 5

/home/altr/programming/pymcdm-uni/main.py:161: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
  plt.show() # I still didnt fix wsl configs...
```
_output img załączone jako [ranking_comparison.png](ranking_comparison.png)


Apropo dlaczego te alternatywy są jakie są: Po prostu tak wyszło.
Dane które są na inpucie są kompletnie wyciągnięte z... nikąd więc jakiekolwiek "wniski" są bezużetczne.
Ostatecznie sprowadza się to do "Bigger number better". Jeśli bym na starcie dał inne wagi, np w formie cena czyni cuda, to automatycznie w rankingu wygrałoby to auto które ma najmniejszą cene.
Nie jestem do końca pewien co można więcej o tym powiedzieć. I guess ciekawe jest to że Topsis i Viktor mają ten sam first pick. Nie jest to też niewiadomo jak dziwne so idk.