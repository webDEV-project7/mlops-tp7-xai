# Model Card - Détection de fraude

## 1. Modèle

**Nom dans le registre MLflow :** `fraude`

**Alias :** `production`

**Version :** 1 (à vérifier dans MLflow)

**Algorithme :** RandomForestClassifier

**Hyperparamètres :**
- Nombre d'arbres : 500
- Profondeur maximale : 16
- Random state : 42

**Run MLflow d'origine :** `[RUN_ID_MODELE]`

## 2. Objectif et usage prévu

Le modèle a pour objectif de détecter les transactions potentiellement frauduleuses à partir de leurs caractéristiques.

Il utilise quatre variables : le montant, l'ancienneté du client, la fréquence des transactions sur 24 heures et l'indicateur de paiement nocturne.

Il est destiné à faciliter l'identification des transactions suspectes nécessitant une vérification humaine.

## 3. Usages exclus

Le modèle ne doit pas être utilisé pour bloquer définitivement un compte bancaire ou sanctionner automatiquement un client sans intervention humaine.

Il ne doit pas être déployé directement dans un environnement bancaire réel sans validation supplémentaire sur des données représentatives.

## 4. Données

**Fichier :** `data/transactions.csv`

**Origine :** données synthétiques générées dans le cadre du TP02.

**Nombre total de transactions :** 5 000

**Nombre de fraudes :** 568

**Proportion de fraudes :** 11,36 %

**Variables utilisées :**
- `montant` : montant de la transaction en MAD.
- `anciennete` : ancienneté du client en mois.
- `freq_24h` : nombre de transactions sur 24 heures.
- `nuit` : indicateur de paiement nocturne.

**Empreinte MD5 des données :** `[MD5_TRANSACTIONS]`

Les données sont divisées en 75 % pour l'entraînement et 25 % pour le test, avec `random_state=42`.

## 5. Performances

Les performances du modèle de référence sur 1 250 transactions de test sont :

| Métrique | Résultat |
|---|---|
| F1-score | 0,8669 |
| Précision | 0,8837 |
| Rappel | 0,8507 |
| AUC-ROC | 0,9872 |
| Fraudes détectées | 114 / 134 |
| Fausses alertes | 15 |
| Fraudes non détectées | 20 |

Le modèle présente de bonnes performances sur les données synthétiques utilisées. Il détecte 114 des 134 fraudes présentes dans le jeu de test.

## 6. Méthodes d'explicabilité

### Explicabilité globale

Trois approches ont été utilisées :

- **MDI :** importance des variables calculée à partir des réductions d'impureté de la forêt.
- **Permutation Importance :** mesure de la diminution du F1 lorsqu'une variable est mélangée.
- **SHAP TreeExplainer :** calcul des contributions des variables aux prédictions.

Le montant est globalement la variable la plus influente dans la détection de fraude.

Les résultats SHAP globaux de référence sont :

| Variable | Importance SHAP moyenne |
|---|---:|
| montant | 0,1157 |
| anciennete | 0,0576 |
| nuit | 0,0571 |
| freq_24h | 0,0556 |

### Explicabilité locale

Les méthodes SHAP et LIME ont été appliquées à la transaction de Mme Benali :

- Montant : 1 800 MAD.
- Ancienneté : 30 mois.
- Fréquence : 4 transactions sur 24 heures.
- Paiement nocturne : oui.

**Probabilité de fraude prédite :** 0,924.

Les contributions SHAP sont :

| Variable | Contribution |
|---|---:|
| nuit | +0,3697 |
| montant | +0,3665 |
| anciennete | +0,0903 |
| freq_24h | −0,0183 |

Le paiement nocturne et le montant sont les deux facteurs qui augmentent le plus le risque estimé pour cette transaction.

LIME permet également de produire des règles locales, mais la stabilité des explications dépend du nombre de voisins générés et de la graine aléatoire.

## 7. Comparaison avec des modèles interprétables

Plusieurs modèles ont été comparés sur le même jeu de test.

| Modèle | F1 | Fraudes détectées |
|---|---:|---:|
| Random Forest | 0,8669 | 114 / 134 |
| Régression logistique, montant brut | 0,7407 | 90 / 134 |
| Régression logistique, log10(montant) | 0,8593 | 113 / 134 |
| Arbre de profondeur 2 | 0,2293 | 18 / 134 |
| Arbre de profondeur 3 | 0,5737 | 72 / 134 |
| Arbre de profondeur 6 | 0,7510 | 95 / 134 |
| Arbre sans limite | 0,7556 | 102 / 134 |

La régression logistique utilisant `log10(montant)` présente un compromis intéressant entre performance et interprétabilité.

Elle détecte 113 fraudes contre 114 pour la forêt aléatoire, tout en permettant une interprétation directe des coefficients.

## 8. Limites et risques connus

Le modèle présente plusieurs limites :

- Les données sont synthétiques et peuvent différer des transactions bancaires réelles.
- Certaines fraudes ne sont pas détectées.
- Certaines transactions normales peuvent être signalées comme frauduleuses.
- Les explications SHAP ne démontrent pas de relations causales.
- Les explications LIME peuvent varier selon les perturbations aléatoires.
- Les performances peuvent diminuer lorsque les caractéristiques des transactions évoluent.

## 9. Recommandations d'utilisation et de surveillance

Le modèle doit être utilisé comme outil d'aide à la décision, avec vérification humaine des transactions signalées.

Il est recommandé de surveiller régulièrement le F1-score, la précision, le rappel et les fausses alertes.

Les explications SHAP et LIME doivent être réévaluées après un changement important du modèle ou des données.

Tout nouveau modèle doit être évalué avant son passage en production.

## 10. Traçabilité et auditabilité

Les explications sont archivées dans MLflow dans l'expérience `tp7-explicabilite`.

**Modèle :** `fraude`

**Alias :** `production`

**Version expliquée :** 1 (à vérifier)

**Run d'origine du modèle :** `[RUN_ID_MODELE]`

**Run des explications :** `[RUN_ID_XAI]`

**Empreinte des données :** `[MD5_TRANSACTIONS]`

**Méthodes :** permutation, SHAP TreeExplainer et LIME.

Les graphiques, les fichiers JSON et les explications LIME sont conservés comme artefacts MLflow.

Un tag `explications_run` relie la version du modèle au run contenant ses explications.

## 11. Informations de suivi

**Auteurs :** `[NOMS_DU_GROUPE]`

**Formation :** 5IASD

**Année universitaire :** 2026-2027

**Date de rédaction :** 12 novembre 2026

**Prochaine revue :** à définir après une nouvelle évaluation du modèle.