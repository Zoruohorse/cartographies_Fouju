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
