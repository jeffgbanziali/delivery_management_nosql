import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

def terminer_livraison(r, command_id: str):
    print(f"\n=== T5 : Fin de la livraison de {command_id} ===")

    # Vérifie que la commande est bien assignée
    statut = r.hget(f"order:{command_id}", "statut")
    if statut != "assignée":
        print(f"  ERREUR La commande {command_id} n'est pas assignée. Voir son statut: '{statut}'")
        return False

    # Récupère le livreur affecté
    driver_id = r.get(f"assignment:{command_id}")
    if not driver_id:
        print(f"  ERREUR Aucun livreur trouvé pour {command_id}")
        return False

    nom = r.hget(f"driver:{driver_id}", "nom")

    # Mise à jour atomique via pipeline
    pipe = r.pipeline()
    pipe.hset(f"order:{command_id}", "statut", "livrée")      # 1. Statut commande
    pipe.srem("orders:assignée", command_id)                   # 2. Retire de assignée
    pipe.sadd("orders:livrée",   command_id)                   # 3. Ajoute à livrée
    pipe.hincrby(f"driver:{driver_id}", "active_deliveries",   -1)  # 4. Décrémente actives
    pipe.hincrby(f"driver:{driver_id}", "completed_deliveries", 1)  # 5. Incrémente complétées
    pipe.execute()

    # Affiche l'état final du livreur
    actives    = r.hget(f"driver:{driver_id}", "active_deliveries")
    completees = r.hget(f"driver:{driver_id}", "completed_deliveries")

    print(f"  OK {command_id} marquée 'livrée' par {driver_id} ({nom})")
    print(f"  OK {driver_id} — actives : {actives} | complétées : {completees}")
    return True

if __name__ == "__main__":
    r = get_redis()
    terminer_livraison(r, "c1")
