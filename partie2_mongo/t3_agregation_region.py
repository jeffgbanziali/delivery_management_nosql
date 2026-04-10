import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_mongo

def agregation_par_region(db):
    print("\n Performance de livraison par région \n")

    col = db["deliveries"]

    pipeline = [
        {
            "$group": {
                "_id":             "$region",
                "nb_livraisons":   {"$sum": 1},
                "revenu_total":    {"$sum": "$amount"},
                "duree_moyenne":   {"$avg": "$duration_minutes"},
                "rating_moyen":    {"$avg": "$rating"},
            }
        },
        {"$sort": {"revenu_total": -1}},   
        {
            "$project": {
                "region":        "$_id",
                "nb_livraisons": 1,
                "revenu_total":  1,
                "duree_moyenne": {"$round": ["$duree_moyenne", 1]},
                "rating_moyen":  {"$round": ["$rating_moyen",  2]},
                "_id":           0,
            }
        }
    ]

    resultats = list(col.aggregate(pipeline))

    print(f"  {'Région':<12} {'Livraisons':>12} {'Revenu':>10} {'Durée moy.':>12} {'Rating moy.':>12}")
    print("  " + "-"*60)
    for r in resultats:
        print(f"  {r['region']:<12} {r['nb_livraisons']:>12} {r['revenu_total']:>9}€ {r['duree_moyenne']:>11} min {r['rating_moyen']:>11}")

    return resultats

if __name__ == "__main__":
    db = get_mongo()
    agregation_par_region(db)
