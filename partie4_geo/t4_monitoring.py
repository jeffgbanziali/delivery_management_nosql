
import sys, os, time, random, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.settings import get_redis

# Centre géographique de Paris
PARIS_CENTER_LON = 2.3488
PARIS_CENTER_LAT = 48.8534
ZONE_MAX_KM      = 5.0

def haversine(lon1, lat1, lon2, lat2) -> float:
    """Calcule la distance en km entre deux points GPS (formule de Haversine)."""
    R    = 6371  # rayon de la Terre en km
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a    = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def mettre_a_jour_position(r, driver_id: str, new_lon: float, new_lat: float):
    """Met à jour la position GPS d'un livreur dans Redis."""
    r.geoadd("drivers_locations", [new_lon, new_lat, driver_id])

def verifier_zone(r, driver_id: str) -> dict:
    """
    Vérifie si le livreur est dans la zone de service (< 5 km du centre de Paris).
    Retourne un dict avec distance et statut.
    """
    pos = r.geopos("drivers_locations", driver_id)
    if not pos or not pos[0]:
        return {"error": f"Livreur {driver_id} introuvable"}

    lon, lat = pos[0]
    dist = haversine(PARIS_CENTER_LON, PARIS_CENTER_LAT, lon, lat)
    hors_zone = dist > ZONE_MAX_KM

    return {
        "driver_id": driver_id,
        "lon":       lon,
        "lat":       lat,
        "distance":  round(dist, 2),
        "hors_zone": hors_zone,
    }

def simuler_deplacement(r, driver_id: str, nb_steps: int = 5, intervalle: float = 0.5):
    """
    Simule le déplacement d'un livreur sur nb_steps positions,
    avec une mise à jour toutes les `intervalle` secondes.
    Alerte si le livreur sort de sa zone.
    """
    nom = r.hget(f"driver:{driver_id}", "nom") or driver_id
    print(f"\n=== T4 : Monitoring de {driver_id} ({nom}) ===")
    print(f"  Zone de service : {ZONE_MAX_KM} km autour du centre de Paris\n")

    # Position de départ
    pos_actuelle = r.geopos("drivers_locations", driver_id)
    if not pos_actuelle or not pos_actuelle[0]:
        print(f"  ERREUR Position initiale de {driver_id} introuvable.")
        return

    lon, lat = pos_actuelle[0]

    for step in range(1, nb_steps + 1):
        # Déplacement aléatoire 
        lon += random.uniform(-0.012, 0.012)
        lat += random.uniform(-0.010, 0.010)

        # Met à jour dans Redis
        mettre_a_jour_position(r, driver_id, lon, lat)

        # Vérifie la zone
        info = verifier_zone(r, driver_id)
        statut = "HORS ZONE" if info["hors_zone"] else "En zone"

        print(f"  [Step {step:02d}] lon={lon:.4f}, lat={lat:.4f} | "
              f"dist centre : {info['distance']:.2f} km | {statut}")

        if info["hors_zone"]:
            envoyer_alerte(driver_id, nom, info["distance"])

        time.sleep(intervalle)

def envoyer_alerte(driver_id: str, nom: str, distance: float):
    """Simule l'envoi d'une alerte (log console, en production : email/SMS/webhook)."""
    print(f"\n  ALERTE : {driver_id} ({nom}) est à {distance:.2f} km du centre de Paris !")
    print(f"  ALERTE  Il dépasse la zone de service ({ZONE_MAX_KM} km). Notification envoyée.\n")

if __name__ == "__main__":
    r = get_redis()
    simuler_deplacement(r, "d1", nb_steps=8, intervalle=0.3)
