import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

def afficher_dashboard(r):
    print("\n" + "="*55)
    print("         DASHBOARD TEMPS REEL — LIVRAISONS")
    print("="*55)

    # Commandes par statut
    print("\nCommandes par statut :")
    for statut in ["en_attente", "assignee", "livree"]:
        nb = r.scard(f"orders:{statut}")
        print(f"  {statut:<12} : {nb}")

    # Livraisons actives par livreur
    print("\nLivraisons actives par livreur :")
    livreurs = r.zrange("drivers:rating", 0, -1)
    actifs = False
    for lid in livreurs:
        actives = r.hget(f"driver:{lid}", "active_deliveries") or "0"
        if int(actives) > 0:
            nom = r.hget(f"driver:{lid}", "nom")
            print(f"  {lid} — {nom:<20} : {actives} en cours")
            actifs = True
    if not actifs:
        print("  Aucun livreur actif en ce moment.")

    # Top 2 livreurs
    print("\nTop 2 livreurs :")
    top2 = r.zrevrange("drivers:rating", 0, 1, withscores=True)
    for i, (lid, score) in enumerate(top2, 1):
        nom       = r.hget(f"driver:{lid}", "nom")
        region    = r.hget(f"driver:{lid}", "region")
        completees = r.hget(f"driver:{lid}", "completed_deliveries") or "0"
        print(f"  #{i} {lid} — {nom:<20} | rating : {score} | region : {region} | completees : {completees}")

    print("\n" + "="*55)

if __name__ == "__main__":
    r = get_redis()
    afficher_dashboard(r)
