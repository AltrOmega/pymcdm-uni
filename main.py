import numpy as np
from pymcdm import methods, normalizations, weights
import pandas as pd

def main():
    ##### 4.1 Instalacja biblioteki pymcdm
    # Aby zainstalować wymagane biblioteki najpierw robimy venv:
    # python3 -m venv venv

    # Aktywójemy je:
    # source venv/bin/activate

    # Instalujemy wymagane biblioteki:
    # pip install -r requirements.txt

    # Alternatywnie zwykłe: "pip install pymcd" powinno działać
    # Lepiej jest i tak zrobić python envoirment aby nie mieć potem problemów z
    # globalnie zainstalowanymi bibliotekami.

    # Jeśli z jakiegoś powodu nie działa noto pozostaje: https://www.google.com/



    ##### 4.2 Przygotowanie danych
    # 1. Zdefiniuj macierz decyzyjną
    # (cena, moc, zużycie paliwa, pojemność bagażnika, bezpieczeństwo)
    decision_matrix = np.array([
        [35000, 120, 7.5, 380, 4],
        [42000, 150, 8.2, 450, 5],
        [28000, 90, 5.8, 320, 3],
        [52000, 180, 9.5, 500, 5],
        [38000, 130, 6.5, 400, 4]
    ])

    # 2. Określ wektor wag dla poszczególnych kryteriów (jak silne znacznie ma konkretny numer)
    weights_expert = np.array([0.25, 0.15, 0.25, 0.15, 0.20])

    # 3. Ustal, które kryteria mają być maksymalizowane, a które minimalizowane
    # Typy kryteriów (min, max, min, max, max)
    types = np.array([-1, 1, -1, 1, 1])



    ##### 4.3 Wykorzystanie metod decyzyjnych
    # 1. Zaimportuj z biblioteki pymcdm odpowiednie metody 
    topsis = methods.TOPSIS()
    spotis = methods.SPOTIS()
    vikor = methods.VIKOR()#(dodatkowo)

    # 2. Dokonaj normalizacji danych 
    normalized_matrix = normalizations.minmax_normalization(decision_matrix)

    # 3. Uruchom wybrane metody, oraz 4. Odbierz wyniki
    # topsis (best sister)
    topsis_results = topsis(decision_matrix, weights_expert, types)

    # spotis (also known as super pootis: https://youtu.be/tIth5VYrJqs?si=49wcVTdNCHz-pOcb&t=12)

    # Ekstrakcja punktów refrencyjnych do spotis
    bounds = np.zeros((2, decision_matrix.shape[1])) # shape[1] daje size of a given dimension
    for i in range(decision_matrix.shape[1]):#         w tym wypadku są to nasze kolumny, czyli
        if types[i] == 1:#                             poszczególne kryteria
            bounds[0, i] = np.min(decision_matrix[:, i])
            bounds[1, i] = np.max(decision_matrix[:, i])
        else:# no i oczywiście patrzymy po typach kryteriów: 1 to max, -1 to min
            bounds[0, i] = np.max(decision_matrix[:, i])
            bounds[1, i] = np.min(decision_matrix[:, i])

    # pootispenserhere
    spotis_results = spotis(decision_matrix, weights_expert, types, bounds)

   # Viktor w ramach "ewentualnie inne dostępne w pymcdm"
    vikor_results = vikor(decision_matrix, weights_expert, types)

    # 4.4 Porównanie wyników i wnioski
    # 1. Uruchom co najmniej dwie różne metody decyzyjne 
    # alredy done: topsis_results, spotis_results + viktor_results

    # 2. Porównaj otrzymane rankingi
    alternatives = list(map(lambda i: f'Samochód {i+1}', enumerate(decision_matrix.shape[0])))# B)
    #alternatives = ['Samochód 1', 'Samochód 2', 'Samochód 3', 'Samochód 4', 'Samochód 5']

    # Rankingi
    topsis_ranking = np.argsort(topsis_results)[::-1] # malejąco 
    spotis_ranking = np.argsort(spotis_results) # rosnąco
    vikor_ranking = np.argsort(vikor_results) # rosnąco

    # Wyniki Dwarf Fortress: Wyniki Fortecy Kranoludów
    results_df = pd.DataFrame({
        'Alternatywa': alternatives,
        'TOPSIS wynik': topsis_results,
        'TOPSIS ranking': [list(topsis_ranking).index(i) + 1 for i in range(len(alternatives))],
        'SPOTIS wynik': spotis_results,
        'SPOTIS ranking': [list(spotis_ranking).index(i) + 1 for i in range(len(alternatives))],
        'VIKOR wynik': vikor_results,
        'VIKOR ranking': [list(vikor_ranking).index(i) + 1 for i in range(len(alternatives))]
    })

    print("Wyniki:")
    print(results_df)


if __name__ == '__main__':
    main()