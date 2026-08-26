# Touying Presentation Boilerplate

Boilerplate generico e minimale per presentazioni in [Typst](https://typst.app/) con il pacchetto [Touying](https://github.com/touying-typ/touying) (tema *Metropolis*).

---

## 📁 Struttura del Progetto

```
slides/
├── main.typ                  # File principale di ingresso
├── theme.typ                 # Configurazione tema, colori e box personalizzati
├── Makefile                  # Comandi di compilazione veloci
├── README.md                 # Documentazione del progetto
└── sections/                 # Contenuto diviso in sezioni modulari
    ├── 01-section.typ        # Prima sezione (slide base ed elenchi)
    ├── 02-section.typ        # Seconda sezione (ambienti def/thm e layout a colonne)
    └── 03-section.typ        # Terza sezione (conclusioni e focus slide)
```

---

## 🚀 Come Compilare

### Compilazione Singola
```bash
make
# Oppure: typst compile main.typ main.pdf
```

### Modalità Live (Watch)
```bash
make watch
# Oppure: typst watch main.typ main.pdf
```

---

## 🎨 Personalizzazione

- **Metadati (Titolo, Autore, Data):** Modificabili all'inizio di `main.typ`.
- **Tema e Colori:** Modificabili in `theme.typ`.
- **Nuove Sezioni:** Crea un file `.typ` dentro `sections/` e includilo in `main.typ` con `#include "sections/nome-file.typ"`.
