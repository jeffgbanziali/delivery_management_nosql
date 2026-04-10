import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_mongo

def historique_livreur(db, driver_id: str):
    print(f"\n=== T2 : Historique du livreur {driver_id} ===")

    col = db["deliveries"]

    #  filtre sur driver_id
    livraisons = list(col.find({"driver_id": driver_id}, {"_id": 0}))

    if not livraisons:
        print(f"  Aucune livraison trouvée pour {driver_id}.")
        return

    print(f"\n  Toutes les livraisons de {driver_id} ({livraisons[0]['driver_name']}) :\n")
    for l in livraisons:
        print(f"  - {l['command_id']} | {l['client']:<20} | {l['amount']}€ | {l['duration_minutes']} min | rating {l['rating']}")

    # Agrégation : nombre et montant total
    agg = list(col.aggregate([
        {"$match": {"driver_id": driver_id}},
        {"$group": {
            "_id":          "$driver_id",
            "nb_livraisons": {"$sum": 1},
            "montant_total": {"$sum": "$amount"},
            "rating_moyen":  {"$avg": "$rating"},
        }}
    ]))

    if agg:
        r = agg[0]
        print(f"\n  Résumé :")
        print(f"    Nombre de livraisons : {r['nb_livraisons']}")
        print(f"    Montant total         : {r['montant_total']}€")
        print(f"    Rating moyen          : {r['rating_moyen']:.2f}")

if __name__ == "__main__":
    db = get_mongo()
    historique_livreur(db, "d1")
