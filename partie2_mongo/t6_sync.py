import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime, timezone
from config.settings import get_redis, get_mongo

def synchroniser_livraison(command_id: str):
    """
    Clôture une livraison dans Redis ET l'insère dans MongoDB.
    Appelé après qu'une commande passe en statut 'livrée'.
    """
    r  = get_redis()
    db = get_mongo()

    print(f"\n=== T6 : Synchronisation Redis → MongoDB pour {command_id} ===")

    # Lecture dans Redis 
    order = r.hgetall(f"order:{command_id}")
    if not order:
        print(f"  ERREUR Commande {command_id} introuvable dans Redis.")
        return False

    driver_id = r.get(f"assignment:{command_id}")
    if not driver_id:
        print(f"  ERREUR Aucune affectation trouvée pour {command_id}.")
        return False

    driver = r.hgetall(f"driver:{driver_id}")
    if not driver:
        print(f"  ERREUR Livreur {driver_id} introuvable dans Redis.")
        return False

    # Mise à jour du statut dans Redis 
    statut_actuel = order.get("statut")
    if statut_actuel == "assignée":
        pipe = r.pipeline()
        pipe.hset(f"order:{command_id}", "statut", "livrée")
        pipe.srem("orders:assignée", command_id)
        pipe.sadd("orders:livrée",   command_id)
        pipe.hincrby(f"driver:{driver_id}", "active_deliveries",    -1)
        pipe.hincrby(f"driver:{driver_id}", "completed_deliveries",  1)
        pipe.execute()
        print(f"  OK Redis mis à jour : {command_id} → 'livrée'")
    else:
        print(f"  INFO Redis : {command_id} déjà en statut '{statut_actuel}'")

    # On fait une vérification de doublon MongoDB 
    col = db["deliveries"]
    if col.find_one({"command_id": command_id}):
        print(f"  INFO MongoDB : {command_id} déjà présent, pas de doublon.")
        return True

    # Construction du document MongoDB ─
    now = datetime.now(timezone.utc)
    document = {
        "command_id":       command_id,
        "client":           order.get("client", "Inconnu"),
        "driver_id":        driver_id,
        "driver_name":      driver.get("nom", "Inconnu"),
        "pickup_time":      now,               
        "delivery_time":    now,
        "duration_minutes": 0,                 
        "amount":           int(order.get("montant", 0)),
        "region":           driver.get("region", "Inconnu"),
        "rating":           float(driver.get("rating", 0)),
        "review":           "Synchronisé automatiquement depuis Redis.",
        "status":           "completed",
    }

    col.insert_one(document)
    print(f"  OK MongoDB : document inséré pour {command_id}")
    print(f"  OK Synchronisation terminée avec succès.")
    return True

if __name__ == "__main__":
    synchroniser_livraison("c2")
