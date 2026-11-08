# Cartographie des acteurs du Campus IA Fouju

Dépôt statique prêt pour GitHub Pages. Les deux rendus utilisent le même référentiel central.

## Structure

- `data/actors.json` : identités, rôles et catégories
- `data/claims.json` : positions contextualisées
- `data/evidence.json` : verbatims et synthèses
- `data/relations.json` : liens entre acteurs et justification
- `data/sources.json` : sources réutilisables
- `config/taxonomy.json` : catégories, couleurs, positions et types de liens
- `apps/cards/` : vue en cartes
- `apps/network/` : vue réseau

## Publication GitHub Pages

1. Décompresser l’archive.
2. Envoyer le contenu du dossier dans un dépôt GitHub.
3. Dans `Settings > Pages`, choisir `Deploy from a branch`, branche `main`, dossier `/root`.
4. Ouvrir l’URL GitHub Pages fournie.

## Test local

Les données sont chargées par `fetch`, donc il faut un serveur HTTP local :

```bash
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000`.

## Validation

```bash
python3 validate.py
```

## Qualification documentaire

Le modèle accepte plusieurs preuves et plusieurs sources par position ou relation. Les fichiers fournis ne contenaient pas les URL individuelles pour chaque affirmation. Elles n’ont pas été inventées : les éléments concernés portent `source_status: to_qualify` ou une source avec `url: null`.

Pour ajouter une deuxième preuve :

1. ajouter un objet dans `data/evidence.json` ;
2. ajouter ou réutiliser une source dans `data/sources.json` ;
3. ajouter l’identifiant de preuve dans `evidence_ids` de la position ou relation.
 
## Qualification documentaire — novembre 2026
La cartographie est reconstruite à partir du lot `Fouju.xlsx` et de sources complémentaires publiques. Les positions sont **attribuées**, les relations du nuage sont **justifiées** et les liens des fiches ouvrent les sources documentaires. Une source journalistique fournie dans le classeur peut ne pas être directement consultable en ligne (paywall), ce qui est signalé dans `data/sources.json`.

« Position non établie » signifie que la participation de l'acteur au dossier, ou son rôle, est documentée, **mais pas un avis individuel favorable ou opposé**. Le rôle administratif de RTE, de la MRAe, du préfet ou de la commission d'enquête n'implique aucune opinion politique personnelle.

```bash
python3 validate.py
```

Détails de l'audit et noms écartés : [AUDIT_QUALIFICATION_2026-11-06.md](AUDIT_QUALIFICATION_2026-11-06.md).


## Cinquième onglet : Évolution des acteurs — 8 novembre 2026

La vue cartes comporte désormais cinq onglets : **Cartographie des acteurs**, **Synthèse des oppositions**, **Points de vigilance et sources**, **Évolution des acteurs**, **Chronologie**.

Le nouvel onglet utilise `data/timeline.json`, en conservant les **70 acteurs existants** : **65 ont une date documentaire exploitable** et **5 restent dans une rubrique distincte faute de datation fiable**. Les entrées sont sourcées avec des URL dans `data/sources.json` et des preuves dédiées dans `data/evidence.json`. La visualisation offre un histogramme empilé, un affichage mensuel **Nouveaux/Cumulés**, des filtres par typologie et la liste nominative des acteurs avec les sources de datation.

Une « première apparition documentaire » n'est pas une première prise de position historique. Certaines dates désignent une réunion relatée dans un article postérieur ou une annonce reconstituée rétrospectivement. Quand seule la période mensuelle est vérifiable, la date reste au format `AAAA-MM` : aucun premier jour fictif du mois n'est inventé. Les dates de simple actualisation GitHub ou les échéances prospectives de 2028/2038 ne sont pas comptées.

**Acteurs non datés dans l'état du corpus** : Aline Aurias, Jean-Louis Thiériot, Hervé Jeannin, Valérie Pécresse et Terres de luttes. Ils restent présents dans la cartographie mais sont exclus du graphique, avec la raison affichée. Les fichiers `actors.json`, `claims.json`, `relations.json` et `sources.json` n'ont pas été modifiés.

Audit complet : [data/evolution-audit-20261108.json](data/evolution-audit-20261108.json). Contrôle : `python3 validate.py`.
