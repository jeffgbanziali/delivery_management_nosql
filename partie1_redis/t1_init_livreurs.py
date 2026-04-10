import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from faker import Faker
import random
from config.settings import get_redis
from data.seed_data import LIVREURS

fake = Faker("fr_FR")

def init_livreurs(r):
    print("\n=== T1 : Initialisation des livreurs ===")

    # Supprime les anciennes données pour un démarrage propre
    for key in r.scan_iter("driver:*"):
        r.delete(key)
    r.delete("drivers:rating")

    tous_les_livreurs = LIVREURS.copy()

    # Génère 10 livreurs supplémentaires aléatoires
    regions = ["Paris", "Banlieue"]
    for i in range(5, 15):
        tous_les_livreurs.append({
            "id":     f"d{i+1}",
            "nom":    fake.name(),
            "region": random.choice(regions),
            "rating": round(random.uniform(3.8, 5.0), 1),
        })

    for livreur in tous_les_livreurs:
        lid = livreur["id"]

        # Hash : stocke toutes les infos du livreur
        r.hset(f"driver:{lid}", mapping={
            "nom":                  livreur["nom"],
            "region":               livreur["region"],
            "rating":               livreur["rating"],
            "active_deliveries":    0,
            "completed_deliveries": 0,
        })

        # Sorted Set : score = rating pour classement rapide
        r.zadd("drivers:rating", {lid: livreur["rating"]})

        print(f"  OK {lid} — {livreur['nom']} (rating {livreur['rating']}, {livreur['region']})")

    print(f"\n  → {len(tous_les_livreurs)} livreurs initialisés.")

def afficher_tous_les_livreurs(r):
    print("\n--- Liste complète des livreurs avec rating ---")
    # ZREVRANGE : du meilleur au moins bon, WITHSCORES retourne aussi le score
    livreurs = r.zrevrange("drivers:rating", 0, -1, withscores=True)
    for lid, score in livreurs:
        nom = r.hget(f"driver:{lid}", "nom")
        print(f"  {lid} — {nom} — rating : {score}")

def chercher_meilleurs_livreurs(r, rating_min=4.7):
    print(f"\n--- Livreurs avec rating ≥ {rating_min} ---")
    # ZRANGEBYSCORE : récupère les membres dont le score est dans [min, max]
    meilleurs = r.zrangebyscore("drivers:rating", rating_min, "+inf", withscores=True)
    for lid, score in meilleurs:
        nom = r.hget(f"driver:{lid}", "nom")
        print(f"  OK {lid} — {nom} — rating : {score}")
    return meilleurs

if __name__ == "__main__":
    r = get_redis()
    init_livreurs(r)
    afficher_tous_les_livreurs(r)
    chercher_meilleurs_livreurs(r, rating_min=4.7)
