import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

def livreurs_dans_rayon(r, lieu: str, rayon_km: float):
    print(f"\n=== T2.1 : Livreurs dans {rayon_km} km autour de '{lieu}' ===")

    # GEOSEARCH depuis un membre de delivery_points,
    # cherche dans drivers_locations dans le rayon donné
    pos = r.geopos("delivery_points", lieu)
    if not pos or not pos[0]:
        print(f"  ERREUR Lieu '{lieu}' introuvable.")
        return []

    lon, lat = pos[0]

    # GEOSEARCH : depuis coordonnées, rayon en km, tri par distance croissante
    resultats = r.geosearch(
        "drivers_locations",
        longitude=lon, latitude=lat,
        radius=rayon_km, unit="km",
        sort="ASC",
        withcoord=True,
        withdist=True,
    )

    if not resultats:
        print(f"  Aucun livreur trouvé dans {rayon_km} km.")
        return []

    for item in resultats:
        lid, dist, (dlon, dlat) = item
        nom = r.hget(f"driver:{lid}", "nom") or lid
        print(f"  {lid} — {nom:<20} | distance : {dist:.3f} km | ({dlon:.4f}, {dlat:.4f})")

    return resultats

def livreurs_avec_distance(r, lieu: str):
    print(f"\n=== T2.2 : Distance exacte des livreurs par rapport à '{lieu}' ===")

    pos = r.geopos("delivery_points", lieu)
    if not pos or not pos[0]:
        return

    lon, lat = pos[0]

    # On utilise geosearch sans limite de rayon
    resultats = r.geosearch(
        "drivers_locations",
        longitude=lon, latitude=lat,
        radius=500, unit="km",
        sort="ASC",
        withdist=True,
    )
    for item in resultats:
        lid, dist = item
        nom = r.hget(f"driver:{lid}", "nom") or lid
        print(f"  {lid} — {nom:<20} | {dist:.3f} km du {lieu}")

def deux_livreurs_les_plus_proches(r, lieu: str):
    print(f"\n=== T2.3 : 2 livreurs les plus proches de '{lieu}' ===")

    pos = r.geopos("delivery_points", lieu)
    if not pos or not pos[0]:
        return

    lon, lat = pos[0]

    resultats = r.geosearch(
        "drivers_locations",
        longitude=lon, latitude=lat,
        radius=500, unit="km",
        sort="ASC",
        count=2,           # il est limité à 2
        withdist=True,
    )
    for i, item in enumerate(resultats, 1):
        lid, dist = item
        nom    = r.hget(f"driver:{lid}", "nom") or lid
        rating = r.hget(f"driver:{lid}", "rating") or "?"
        print(f"  #{i} {lid} — {nom:<20} | {dist:.3f} km | rating : {rating}")

if __name__ == "__main__":
    r = get_redis()
    livreurs_dans_rayon(r, "Marais", rayon_km=2.0)
    livreurs_avec_distance(r, "Marais")
    deux_livreurs_les_plus_proches(r, "Marais")
