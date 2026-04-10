import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

TTL_SECONDES = 30

# On a mis un système de cache on stockant le top 5 livreurs par rating 

def calculer_top5(r):
    """Calcule le top 5 depuis le Sorted Set (source de vérité)."""
    top5 = r.zrevrange("drivers:rating", 0, 4, withscores=True)
    return [{"id": lid, "rating": score, "nom": r.hget(f"driver:{lid}", "nom")} for lid, score in top5]

def get_top5_livreurs(r):
    cle = "cache:top5_rating"
    cached = r.get(cle)

    if cached:
        print(f"  OK Cache HIT  → {cle} (TTL restant : {r.ttl(cle)}s)")
        return json.loads(cached)
    else:
        print(f"  ERREUR Cache MISS → {cle} — recalcul en cours...")
        data = calculer_top5(r)
        r.setex(cle, TTL_SECONDES, json.dumps(data))   # stockage toutes les 30 secondes
        print(f"  OK Cache stocké ({TTL_SECONDES}s)")
        return data

# le Cache des commandes en attente par région ─

def calculer_pending_region(r, region: str):
    """Calcule les commandes en attente pour une région donnée."""
    ids_en_attente = r.smembers("orders:en_attente")
    result = []
    for cid in ids_en_attente:
        dest = r.hget(f"order:{cid}", "destination")
        # Correspondance simplifiée destination → région
        dest_region = "Paris" if dest in ("Marais", "Belleville", "Bercy", "Auteuil", "Nation", "Bastille", "Montmartre") else "Banlieue"
        if dest_region == region:
            result.append({"id": cid, "destination": dest})
    return result

def get_pending_par_region(r, region: str):
    cle = f"cache:pending:{region}"
    cached = r.get(cle)

    if cached:
        print(f"  OK Cache HIT  → {cle} (TTL restant : {r.ttl(cle)}s)")
        return json.loads(cached)
    else:
        print(f"  ERREUR Cache MISS → {cle} — recalcul en cours...")
        data = calculer_pending_region(r, region)
        r.setex(cle, TTL_SECONDES, json.dumps(data))
        print(f"  OK Cache stocké ({TTL_SECONDES}s)")
        return data

def invalider_caches(r):
    """Invalide tous les caches (à appeler après une mise à jour des données)."""
    for key in r.scan_iter("cache:*"):
        r.delete(key)
    print("  OK Tous les caches invalidés.")

if __name__ == "__main__":
    r = get_redis()

    print("\n=== T2 : Cache avec TTL (30s) ===")

    # Premier appel → cache miss
    print("\n[Appel 1 — Top 5 livreurs]")
    top5 = get_top5_livreurs(r)
    for l in top5:
        print(f"    {l['id']} — {l['nom']} — rating {l['rating']}")

    # Deuxième appel → cache hit
    print("\n[Appel 2 — Top 5 livreurs (depuis cache)]")
    top5 = get_top5_livreurs(r)

    # Commandes en attente par région
    print("\n[Commandes en attente — Paris]")
    pending = get_pending_par_region(r, "Paris")
    for c in pending:
        print(f"    {c['id']} → {c['destination']}")

    print("\n[Commandes en attente — Paris (depuis cache)]")
    get_pending_par_region(r, "Paris")
