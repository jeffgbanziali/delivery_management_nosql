import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

def afficher_statuts(r):
    print("\n Les commandes par statut ")

    for statut in ("en_attente", "assignée", "livrée"):
        ids = r.smembers(f"orders:{statut}")
        nb  = len(ids)
        liste = ", ".join(sorted(ids)) if ids else "—"
        print(f"\n  [{statut.upper()}] → {nb} commande(s)")
        print(f"  IDs : {liste}")

def afficher_meilleur_livreur(r):
    print("\nLe livreur avec le rating maximal ")

    # ZREVRANGE avec WITHSCORES : le premier élément est le meilleur
    top = r.zrevrange("drivers:rating", 0, 0, withscores=True)
    if top:
        lid, score = top[0]
        nom    = r.hget(f"driver:{lid}", "nom")
        region = r.hget(f"driver:{lid}", "region")
        print(f"  TOP {lid} — {nom} — rating : {score} — région : {region}")
    else:
        print("  Aucun livreur trouvé.")

if __name__ == "__main__":
    r = get_redis()
    afficher_statuts(r)
    afficher_meilleur_livreur(r)
