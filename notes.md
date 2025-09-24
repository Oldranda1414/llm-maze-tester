Prima di tutto:
Funzione che dato il labirinto e la posizione del player ritorna una descrizione dello stato attuale da fornire al llm

Questa descrizione deve essere più "umana" possibile

Usa le coordinate (nord, est sud ovest)

Esempio: verso nord c'è subito un muro, verso est c'è un corridoio lungo 3 passi fino ad un muro, sembra che poi si possa andare a sud oltre il corridoio.

Fatta questa funzione mandare 2-3 esempi al prof per valutare il "prompt"

Valutare tempi di risoluzione, per considerare di usare gpu ateneo da remoto


Capire che modelli fornisce litellm

Cercare altri lavori che usano maze_dataset


Obiettivo arrivare al caso più semplice risolvibile. 

Esempi di aiuti: labirinto piccolo, prompt iniziale con consigli su come risolvere, aggiornamento su distanza da obiettivo

Inviare al prof link litellm e maze dataset
