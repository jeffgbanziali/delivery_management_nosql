import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

def affecter_commande(r, command_id: str, driver_id: str):
    print(f"\n=== T3 : Affectation de {command_id} à {driver_id} (atomique) ===")

    # Vérifications préalables
    statut_actuel = r.hget(f"order:{command_id}", "statut")
    if statut_actuel != "en_attente":
        print(f"  ERREUR Impossible : la commande {command_id} est déjà '{statut_actuel}'")
        return False

    livreur_existe = r.exists(f"driver:{driver_id}")
    if not livreur_existe:
        print(f"  ERREUR Impossible : le livreur {driver_id} n'existe pas")
        return False

    # Pipeline = toutes les commandes envoyées d'un coup 
    pipe = r.pipeline()

    pipe.hset(f"order:{command_id}", "statut", "assignée")   # 1. Statut commande
    pipe.srem("orders:en_attente", command_id)                # 2. Retire du set en_attente
    pipe.sadd("orders:assignée",   command_id)                # 3. Ajoute au set assignée
    pipe.set(f"assignment:{command_id}", driver_id)           # 4. Enregistre l'affectation
    pipe.hincrby(f"driver:{driver_id}", "active_deliveries", 1)  # 5. Incrémente actives

    pipe.execute()  # Exécution atomique

    # Vérification
    nom = r.hget(f"driver:{driver_id}", "nom")
    print(f"  OK {command_id} affectée à {driver_id} ({nom}) avec succès")
    print(f"  OK Livraisons actives de {driver_id} : {r.hget(f'driver:{driver_id}', 'active_deliveries')}")
    return True

if __name__ == "__main__":
    r = get_redis()
    affecter_commande(r, "c1", "d3")
    affecter_commande(r, "c2", "d1") 
