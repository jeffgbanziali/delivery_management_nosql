import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis
from data.seed_data import LIEUX_LIVRAISON, POSITIONS_LIVREURS

def init_geo(r):
    print("\n=== T1 : Initialisation des positions géo-spatiales ===")

    r.delete("delivery_points")
    r.delete("drivers_locations")

    # Lieux de livraison
    print("\n  Lieux de livraison :")
    for lieu in LIEUX_LIVRAISON:
        r.geoadd("delivery_points", [lieu["lon"], lieu["lat"], lieu["nom"]])
        print(f"  OK {lieu['nom']:<12} ({lieu['lon']}, {lieu['lat']})")

    # Positions des livreurs
    print("\n  Positions des livreurs :")
    for pos in POSITIONS_LIVREURS:
        r.geoadd("drivers_locations", [pos["lon"], pos["lat"], pos["id"]])
        nom = r.hget(f"driver:{pos['id']}", "nom") or pos["id"]
        print(f"  OK {pos['id']} — {nom:<20} ({pos['lon']}, {pos['lat']})")

def verifier_positions(r):
    print("\n--- Vérification : positions stockées ---")

    print("\n  delivery_points :")
    for lieu in LIEUX_LIVRAISON:
        pos = r.geopos("delivery_points", lieu["nom"])
        if pos and pos[0]:
            lon, lat = pos[0]
            print(f"  {lieu['nom']:<12} → lon={lon:.4f}, lat={lat:.4f}")

    print("\n  drivers_locations :")
    for pos in POSITIONS_LIVREURS:
        gpos = r.geopos("drivers_locations", pos["id"])
        if gpos and gpos[0]:
            lon, lat = gpos[0]
            print(f"  {pos['id']} → lon={lon:.4f}, lat={lat:.4f}")

if __name__ == "__main__":
    r = get_redis()
    init_geo(r)
    verifier_positions(r)
