#  Projet NoSQL — Système de Livraison

Projet utilisant **Redis** (temps réel) et **MongoDB** (historique/analyses) pour gérer une plateforme de livraison.

---

## Structure du projet Structure du projet

```
projet_nosql/
├── docker-compose.yml            # Redis + MongoDB via Docker
├── requirements.txt              # Dépendances Python
│
├── config/
│   └── settings.py               # Paramètres de connexion Redis & MongoDB
│
├── data/
│   └── seed_data.py              # Données initiales centralisées
│
├── partie1_redis/
│   ├── t1_init_livreurs.py       # T1 : Initialiser les livreurs
│   ├── t2_commandes.py           # T2 : Gérer les commandes
│   ├── t3_affectation.py         # T3 : Affectation atomique
│   ├── t4_statuts.py             # T4 : Commandes par statut
│   ├── t5_livraison.py           # T5 : Fin de livraison
│   └── t6_dashboard.py           # T6 : Dashboard temps réel
│
├── partie2_mongo/
│   ├── t1_import_historique.py   # T1 : Import historique
│   ├── t2_historique_livreur.py  # T2 : Historique d'un livreur
│   ├── t3_agregation_region.py   # T3 : Performance par région
│   ├── t4_top_livreurs.py        # T4 : Top livreurs
│   ├── t5_indexes.py             # T5 : Indexation
│   └── t6_sync.py                # T6 : Sync Redis → MongoDB (bonus)
│
├── partie3_advanced/
│   ├── t1_multi_regions.py       # T1 : Livreurs multi-régions
│   └── t2_cache_ttl.py           # T2 : Cache avec expiration
│
└── partie4_geo/
    ├── t1_geo_init.py             # T1 : Positions géo-spatiales
    ├── t2_livreurs_proches.py     # T2 : Livreurs proches
    ├── t3_affectation_optimale.py # T3 : Affectation optimale
    └── t4_monitoring.py           # T4 : Monitoring (bonus)
```

---

## Installation Installation

### 1. Prérequis
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé
- Python 3.9+

### 2. Lancer Redis et MongoDB
```bash
docker-compose up -d
```

Vérifier que les conteneurs tournent :
```bash
docker ps
```
Vous devez voir `nosql_redis` et `nosql_mongo` avec le statut `Up`.

### 3. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

---

## Lancement Ordre de lancement des scripts

> [ALERTE] Respecter l'ordre : chaque script dépend des données insérées par le précédent.

### Partie 1 — Redis (temps réel)
```bash
python partie1_redis/t1_init_livreurs.py     # Initialise les livreurs (Hash + Sorted Set)
python partie1_redis/t2_commandes.py          # Initialise les commandes (Hash + Set par statut)
python partie1_redis/t3_affectation.py        # Affecte c1 à d3 de manière atomique
python partie1_redis/t4_statuts.py            # Affiche les commandes par statut + meilleur livreur
python partie1_redis/t5_livraison.py          # Simule la fin de la livraison de c1
python partie1_redis/t6_dashboard.py          # Dashboard temps réel global
```

### Partie 2 — MongoDB (historique)
```bash
python partie2_mongo/t1_import_historique.py  # Crée la collection et insère les livraisons
python partie2_mongo/t2_historique_livreur.py # Historique complet du livreur d1
python partie2_mongo/t3_agregation_region.py  # Performance par région (agrégation)
python partie2_mongo/t4_top_livreurs.py       # Top 2 livreurs (agrégation avancée)
python partie2_mongo/t5_indexes.py            # Crée les index + explain()
python partie2_mongo/t6_sync.py               # Synchronise une livraison Redis → MongoDB
```

### Partie 3 — Structures avancées
```bash
python partie3_advanced/t1_multi_regions.py   # Livreurs opérant dans plusieurs régions
python partie3_advanced/t2_cache_ttl.py       # Cache top 5 et commandes en attente (TTL 30s)
```

### Partie 4 — Géo-spatial
```bash
python partie4_geo/t1_geo_init.py              # Stocke les positions GPS dans Redis
python partie4_geo/t2_livreurs_proches.py      # Livreurs dans un rayon autour du Marais
python partie4_geo/t3_affectation_optimale.py  # Affectation optimale (proximité vs rating)
python partie4_geo/t4_monitoring.py            # Simulation déplacement + alerte hors zone
```

---

## Connexions Connexions par défaut

| Service  | Host      | Port  |
|----------|-----------|-------|
| Redis    | localhost | 6379  |
| MongoDB  | localhost | 27017 |

Pour modifier ces valeurs : éditez `config/settings.py`.

---

## Arret Arrêter les conteneurs
```bash
docker-compose down
```

Pour supprimer aussi les données :
```bash
docker-compose down -v
```
