import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis
from data.seed_data import LIVREURS

def init_multi_regions(r):
    print("\n=== T1 : Livreurs multi-régions ===")

    # Nettoyage
    for key in r.scan_iter("region:*"):
        r.delete(key)

    # les affectations de base depuis les données initiales
    for l in LIVREURS:
        r.sadd(f"region:{l['region']}", l["id"])

    # le driver d1 opère aussi en Banlieue 
    r.sadd("region:Banlieue", "d1")
    print("  OK d1 ajouté à Paris ET Banlieue.")

    #le driver d5 opère aussi en Banlieue
    r.sadd("region:Banlieue", "d5")
    print("  OK d5 ajouté à Paris ET Banlieue.")

def lister_livreurs_region(r, region: str):
    print(f"\n--- Livreurs opérant à {region} ---")
    ids = r.smembers(f"region:{region}")
    for lid in sorted(ids):
        nom = r.hget(f"driver:{lid}", "nom") or "?"
        print(f"  {lid} — {nom}")
    print(f"  Total : {len(ids)}")
    return ids

def livreurs_toutes_regions(r):
    print("\n--- Livreurs présents dans TOUTES les régions ---")
    # SUNION fusionne les membres de plusieurs sets
    tous = r.sunion("region:Paris", "region:Banlieue")
    for lid in sorted(tous):
        nom = r.hget(f"driver:{lid}", "nom") or "?"
        # Vérifie dans quelles régions il opère
        regions = []
        for reg in ("Paris", "Banlieue"):
            if r.sismember(f"region:{reg}", lid):
                regions.append(reg)
        print(f"  {lid} — {nom} — régions : {', '.join(regions)}")

if __name__ == "__main__":
    r = get_redis()
    init_multi_regions(r)
    lister_livreurs_region(r, "Paris")
    lister_livreurs_region(r, "Banlieue")
    livreurs_toutes_regions(r)
