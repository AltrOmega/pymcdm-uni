import numpy as np
from pymcdm import methods, normalizations, weights
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

def main():
    ##### 4.1 Instalacja biblioteki pymcdm
    # Aby zainstalować wymagane biblioteki najpierw robimy venv:
    # python3 -m venv venv

    # Aktywójemy je:
    # source venv/bin/activate

    # Instalujemy wymagane biblioteki:
    # pip install -r requirements.txt

    # Alternatywnie zwykłe: "pip install pymcdm" powinno działać
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
    
    # Alternatywnie w ramach "wyznaczenie wag metodami pymcdm"
    # można użyć metody entropy do wyznaczenia wag (ale wole dać własne numerki)
    weights_entropy = weights.entropy_weights(decision_matrix)
    print("Wagi wyznaczone metodą entropy:", weights_entropy)

    # 3. Ustal, które kryteria mają być maksymalizowane, a które minimalizowane
    # Typy kryteriów (min, max, min, max, max)
    types = np.array([-1, 1, -1, 1, 1])



    ##### 4.3 Wykorzystanie metod decyzyjnych

    # Ekstrakcja punktów refrencyjnych do spotis
    # shape[1] daje size of a given dimension w tym wypadku są to nasze kolumny,
    # czyli poszczególne kryteria
    bounds = []
    for i in range(decision_matrix.shape[1]):
        bound_min = np.min(decision_matrix[:, i])
        bound_max = np.max(decision_matrix[:, i])
        bounds.append([bound_min, bound_max])

    bounds = np.array(bounds)

    # 1. Zaimportuj z biblioteki pymcdm odpowiednie metody 
    topsis = methods.TOPSIS()
    spotis = methods.SPOTIS(bounds)
    vikor = methods.VIKOR()#(dodatkowo)

    # 2. Dokonaj normalizacji danych 
    normalized_matrix = normalizations.minmax_normalization(decision_matrix)

    # 3. Uruchom wybrane metody, oraz 4. Odbierz wyniki
    # topsis (best sister)
    topsis_results = topsis(normalized_matrix, weights_expert, types)

    # spotis (also known as super pootis: https://youtu.be/tIth5VYrJqs?si=49wcVTdNCHz-pOcb&t=12)
    spotis_results = spotis(decision_matrix, weights_expert, types)
    # i tutaj mam troche problem, bo nie jestem pewien czy powinienem dać normalized matrix.
    # ale jak patrze na https://pymcdm.readthedocs.io/en/master/modules/american_school.html#spotis
    # oraz https://pymcdm.readthedocs.io/en/master/modules/american_school.html#topsis
    # to widze że w topsis bezpośredio mówią żeby normalizować minmaxem w spotis nie,
    # więc zakładam że chcą żeby dać bez normalizacji
    # ale z kolei w Viktorze też nie ma tego...

   # Viktor w ramach "ewentualnie inne dostępne w pymcdm"
    vikor_results = vikor(normalized_matrix, weights_expert, types)

    # 4.4 Porównanie wyników i wnioski
    # 1. Uruchom co najmniej dwie różne metody decyzyjne 
    # alredy done: topsis_results, spotis_results + viktor_results

    # 2. Porównaj otrzymane rankingi
    alternatives = list(map(lambda i: f'Samochód {i+1}', range(decision_matrix.shape[0])))# B)
    #alternatives = ['Samochód 1', 'Samochód 2', 'Samochód 3', 'Samochód 4', 'Samochód 5']

    # Rankingi
    topsis_ranking = np.argsort(topsis_results)[::-1] # malejąco 
    spotis_ranking = np.argsort(spotis_results) # rosnąco
    vikor_ranking = np.argsort(vikor_results) # rosnąco

    # tak apropo całej sekcji poniżej tutaj
    # wszystkie list comperhension typu [list(topsis_ranking).index(i) + 1 for i in range(len(alternatives))]
    # są poto żeby uniknąć liczenia rankingów od 0
    # irl nie ma miejsca 0 wego, jest 1 sze miejsce

    topsis_ranks = [list(topsis_ranking).index(i) + 1 for i in range(len(alternatives))]
    spotis_ranks = [list(spotis_ranking).index(i) + 1 for i in range(len(alternatives))]
    vikor_ranks = [list(vikor_ranking).index(i) + 1 for i in range(len(alternatives))]

    # Wyniki Dwarf Fortress: Wyniki Fortecy Kranoludów
    results_df = pd.DataFrame({
        'Alternatywa': alternatives,
        'TOPSIS wynik': topsis_results,
        'TOPSIS ranking': topsis_ranking,
        'SPOTIS wynik': spotis_results,
        'SPOTIS ranking': spotis_ranking,
        'VIKOR wynik': vikor_results,
        'VIKOR ranking': vikor_ranking
    })

    print("Wyniki:")
    print(results_df)

  
    # Obliczenie korelacji Spearmana między rankingami (mam flashbacki ze statystyki tutaj)
    corr_topsis_spotis, _ = spearmanr(topsis_ranks, spotis_ranks)
    corr_topsis_vikor, _ = spearmanr(topsis_ranks, vikor_ranks)
    corr_spotis_vikor, _ = spearmanr(spotis_ranks, vikor_ranks)
    
    print("\nKorelacja Spearmana między rankingami:")
    print(f"TOPSIS vs SPOTIS: {corr_topsis_spotis:.4f}")
    print(f"TOPSIS vs VIKOR: {corr_topsis_vikor:.4f}")
    print(f"SPOTIS vs VIKOR: {corr_spotis_vikor:.4f}")
    
    # Interpretacja wyników
    print("\nInterpretacja wyników:")
    best_topsis = alternatives[topsis_ranking[0]]
    best_spotis = alternatives[spotis_ranking[0]]
    best_vikor = alternatives[vikor_ranking[0]]
    
    print(f"Najlepsza alternatywa według TOPSIS: {best_topsis}")
    print(f"Najlepsza alternatywa według SPOTIS: {best_spotis}")
    print(f"Najlepsza alternatywa według VIKOR: {best_vikor}")
    
    # Wizualizacja rankingów
    plt.figure(figsize=(12, 6))
    bar_width = 0.25
    index = np.arange(len(alternatives))
    
    plt.bar(index, topsis_ranks, bar_width, label='TOPSIS')
    plt.bar(index + bar_width, spotis_ranks, bar_width, label='SPOTIS')
    plt.bar(index + 2*bar_width, vikor_ranks, bar_width, label='VIKOR')
    
    plt.xlabel('Alternatywy')
    plt.ylabel('Pozycja w rankingu')
    plt.title('Porównanie rankingów metod MCDM')
    plt.xticks(index + bar_width, alternatives)
    plt.legend()
    plt.tight_layout()
    plt.savefig('ranking_comparison.png')
    plt.show() # I still didnt fix wsl configs...


if __name__ == '__main__':
    main()
