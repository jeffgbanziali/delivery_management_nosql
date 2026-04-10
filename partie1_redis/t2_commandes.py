import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from faker import Faker
import random
from config.settings import get_redis
from data.seed_data import COMMANDES

fake = Faker("fr_FR")

DESTINATIONS = ["Marais", "Belleville", "Bercy", "Auteuil", "Nation", "Bastille"]

def init_commandes(r):
    print("\n Initialisation des commandes")

    # Nettoyage
    for key in r.scan_iter("order:*"):
        r.delete(key)
    for statut in ("en_attente", "assignée", "livrée"):
        r.delete(f"orders:{statut}")

    toutes_les_commandes = COMMANDES.copy()

    # Génère des commandes supplémentaires
    for i in range(6, 16):
        toutes_les_commandes.append({
            "id":          f"c{i}",
            "client":      f"Client {fake.last_name()}",
            "destination": random.choice(DESTINATIONS),
            "montant":     random.randint(10, 60),
            "creee":       f"{random.randint(14, 18)}:{random.randint(0,59):02d}",
        })

    for cmd in toutes_les_commandes:
        cid = cmd["id"]

        # Hash : données complètes
        r.hset(f"order:{cid}", mapping={
            "client":      cmd["client"],
            "destination": cmd["destination"],
            "montant":     cmd["montant"],
            "creee":       cmd["creee"],
            "statut":      "en_attente",
            "timestamp":   int(time.time()),
        })

        # Set de statut
        r.sadd("orders:en_attente", cid)

        print(f"  OK {cid} — {cmd['client']} → {cmd['destination']} ({cmd['montant']}€) [en_attente]")

    print(f"\n  → {len(toutes_les_commandes)} commandes initialisées avec statut 'en_attente'.")

def afficher_commandes_par_statut(r, statut="en_attente"):
    print(f"\n--- Commandes [{statut}] ---")
    ids = r.smembers(f"orders:{statut}")
    for cid in sorted(ids):
        data = r.hgetall(f"order:{cid}")
        print(f"  {cid} — {data.get('client')} → {data.get('destination')} ({data.get('montant')}€)")
    print(f"  Total : {len(ids)}")

if __name__ == "__main__":
    r = get_redis()
    init_commandes(r)
    afficher_commandes_par_statut(r, "en_attente")
