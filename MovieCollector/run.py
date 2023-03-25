from moviecollector import app

if __name__ == '__main__':
    app.run(debug=True)
    
"""
#DONE
-Form per il register e login
-Scheletro della home page con layout dei film

#TODO
-Login e register non salvano in database all'effettivo
-Ogni film ha una pagina personale con vari dati
Tale pagina andrà poi collegata al database dove verranno salvate le informazioni inserite dagli utenti
-Qualche miglioria grafica (?)
-Migliorare l'usabilità, ad esempio se si clicca l'immagine accede comunque alla pagina del film
-Il numero di pagine di adatta al numero effettivo
-Possibilità di creare nuove pagine di film
- chiamate a database per ottenere le informazoni necessarie da mostrare

#PROBLEMI
-Non sappiamo come creare in modo automatico un link univoco per film (per avere pagine separate)
-Al momento problema più grande che rallenta tutto il resto
- Difficoltà di come inserire nel database i dati (problema di tipo logico, non sappiamo come suddividere tutto
- chiamate a database per ottenere le informazoni necessarie da mostrare
"""