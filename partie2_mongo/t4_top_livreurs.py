import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_mongo

def top_livreurs(db, top_n=2):
    print(f"\n=== T4 : Top {top_n} livreurs ===\n")

    col = db["deliveries"]

    pipeline = [
        {
            "$group": {
                "_id": {
                    "driver_id":   "$driver_id",
                    "driver_name": "$driver_name",
                },
                "nb_livraisons":   {"$sum": 1},
                "revenu_total":    {"$sum": "$amount"},
                "duree_moyenne":   {"$avg": "$duration_minutes"},
                "rating_moyen":    {"$avg": "$rating"},
            }
        },
        {"$sort": {"revenu_total": -1}},
        {"$limit": top_n},
        {
            "$project": {
                "_id":           0,
                "driver_id":     "$_id.driver_id",
                "driver_name":   "$_id.driver_name",
                "nb_livraisons": 1,
                "revenu_total":  1,
                "duree_moyenne": {"$round": ["$duree_moyenne", 1]},
                "rating_moyen":  {"$round": ["$rating_moyen",  2]},
            }
        }
    ]

    resultats = list(col.aggregate(pipeline))

    for i, r in enumerate(resultats, 1):
        print(f"  #{i} {r['driver_id']} — {r['driver_name']}")
        print(f"       Livraisons : {r['nb_livraisons']}")
        print(f"       Revenu     : {r['revenu_total']}€")
        print(f"       Durée moy. : {r['duree_moyenne']} min")
        print(f"       Rating moy.: {r['rating_moyen']}\n")

    return resultats

if __name__ == "__main__":
    db = get_mongo()
    top_livreurs(db, top_n=2)
