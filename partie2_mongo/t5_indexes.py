import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pymongo import ASCENDING, DESCENDING
from config.settings import get_mongo

def creer_indexes(db):
    print("\n=== T5 : Création des index ===")

    col = db["deliveries"]

    # Supprime les anciens index sauf les (_id)
    col.drop_indexes()

    # Index 1 : driver_id
    idx1 = col.create_index([("driver_id", ASCENDING)], name="idx_driver_id")
    print(f"  OK Index créé : {idx1}")
    print(f"     Utilité : accès rapide à l'historique d'un livreur sans scan complet.")

    # Index 2 : composé region + delivery_time
    idx2 = col.create_index(
        [("region", ASCENDING), ("delivery_time", DESCENDING)],
        name="idx_region_delivery_time"
    )
    print(f"  OK Index créé : {idx2}")
    print(f"     Utilité : analyses régionales filtrées par période")

    # Affiche tous les index
    print("\n  Index actifs sur la collection 'deliveries' :")
    for idx in col.list_indexes():
        print(f"    - {idx['name']} : {idx['key']}")

def expliquer_requete(db):
    """Utilise explain() pour montrer l'impact des index."""
    print("\n--- explain() : requête par driver_id ---")
    col  = db["deliveries"]
    plan = col.find({"driver_id": "d1"}).explain()
    stage = plan["queryPlanner"]["winningPlan"].get("stage", "?")
    print(f"  Stage gagnant : {stage}")
    # IXSCAN = index utilisé OK | COLLSCAN = scan complet ERREUR
    if stage == "FETCH":
        print("  OK MongoDB utilise l'index c'est à dire pas de scan complet.")
    else:
        print(f"  Stage : {stage}")

if __name__ == "__main__":
    db = get_mongo()
    creer_indexes(db)
    expliquer_requete(db)
