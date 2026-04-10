import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

def affectation_optimale(r, lieu: str, rayon_km: float = 3.0):
    print(f"\n=== T3 : Affectation optimale — nouvelle commande au {lieu} ===")

    pos = r.geopos("delivery_points", lieu)
    if not pos or not pos[0]:
        print(f"  ERREUR Lieu '{lieu}' introuvable dans delivery_points.")
        return None

    lon, lat = pos[0]

    # Trouve les livreurs dans le rayon de recherche 
    resultats = r.geosearch(
        "drivers_locations",
        longitude=lon, latitude=lat,
        radius=rayon_km, unit="km",
        sort="ASC",
        withdist=True,
    )

    if not resultats:
        print(f"  ERREUR Aucun livreur disponible dans {rayon_km} km du {lieu}.")
        return None

    print(f"\n  Livreurs disponibles dans {rayon_km} km :\n")
    print(f"  {'ID':<6} {'Nom':<22} {'Distance':>10} {'Rating':>8}")
    print("  " + "-"*52)

    candidats = []
    for item in resultats:
        lid, dist = item
        nom    = r.hget(f"driver:{lid}", "nom")    or lid
        rating = r.hget(f"driver:{lid}", "rating") or "0"
        actives = int(r.hget(f"driver:{lid}", "active_deliveries") or 0)

        # On ne propose que les livreurs sans livraison active en cours
        dispo = "OK" if actives == 0 else "ERREUR occupé"
        print(f"  {lid:<6} {nom:<22} {dist:>8.3f} km {float(rating):>8.1f}  {dispo}")

        if actives == 0:
            candidats.append({
                "id":       lid,
                "nom":      nom,
                "distance": dist,
                "rating":   float(rating),
            })

    if not candidats:
        print("\n  ERREUR Aucun livreur disponible (tous occupés).")
        return None

    # ── Stratégie A : le plus proche ──
    meilleur_distance = min(candidats, key=lambda x: x["distance"])

    # ── Stratégie B : le mieux noté ──
    meilleur_rating   = max(candidats, key=lambda x: x["rating"])

    print(f"\n   Stratégie A — Plus proche  : {meilleur_distance['id']} ({meilleur_distance['nom']}) à {meilleur_distance['distance']:.3f} km")
    print(f"   Stratégie B — Mieux noté   : {meilleur_rating['id']} ({meilleur_rating['nom']}) rating {meilleur_rating['rating']}")

    # Pour notre choix final on a privilégié le plus proche si la distance est < 1 km,
    # sinon on choisit le mieux noté
    if meilleur_distance["distance"] < 1.0:
        choix = meilleur_distance
        raison = "distance < 1 km (priorité rapidité)"
    else:
        choix = meilleur_rating
        raison = "distance > 1 km (priorité qualité)"

    print(f"\n  OK Livreur sélectionné : {choix['id']} — {choix['nom']}")
    print(f"     Raison : {raison}")
    return choix

if __name__ == "__main__":
    r = get_redis()
    affectation_optimale(r, "Marais", rayon_km=3.0)
