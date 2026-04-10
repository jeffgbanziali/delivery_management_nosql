import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from faker import Faker
import random
from datetime import datetime, timedelta, timezone
from config.settings import get_mongo
from data.seed_data import LIVRAISONS, LIVREURS

fake = Faker("fr_FR")

REVIEWS_POSITIFS = [
    "Livraison rapide et soignée, très satisfait !",
    "Parfait, commande bien emballée et livrée à l'heure.",
    "Excellent service, je recommande vivement.",
    "Très professionnel, à recommander sans hésiter.",
    "Super livreur, souriant et ponctuel !",
]
REVIEWS_NEUTRES = [
    "Correct, mais un peu de retard.",
    "La livraison s'est bien passée dans l'ensemble.",
    "Rien à signaler, service standard.",
]
REVIEWS_NEGATIFS = [
    "Colis abîmé à la réception, déçu.",
    "Livraison très en retard, sans prévenir.",
    "Peut mieux faire sur la communication.",
]

def generer_livraisons_aleatoires(nb=50):
    livreurs_data = LIVREURS
    regions       = ["Paris", "Banlieue"]
    destinations  = ["Marais", "Belleville", "Bercy", "Auteuil", "Nation", "Bastille", "Montmartre"]
    generated     = []

    for i in range(nb):
        livreur       = random.choice(livreurs_data)
        duration      = random.randint(10, 45)
        pickup        = datetime(2025, 12, 6, tzinfo=timezone.utc) + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59))
        delivery      = pickup + timedelta(minutes=duration)
        rating_value  = round(random.uniform(3.5, 5.0), 1)

        if rating_value >= 4.5:
            review = random.choice(REVIEWS_POSITIFS)
        elif rating_value >= 3.8:
            review = random.choice(REVIEWS_NEUTRES)
        else:
            review = random.choice(REVIEWS_NEGATIFS)

        generated.append({
            "command_id":       f"c{100 + i}",
            "client":           f"Client {fake.last_name()}",
            "driver_id":        livreur["id"],
            "driver_name":      livreur["nom"],
            "pickup_time":      pickup,
            "delivery_time":    delivery,
            "duration_minutes": duration,
            "amount":           random.randint(10, 70),
            "region":           livreur["region"],
            "rating":           rating_value,
            "review":           review,
            "status":           "completed",
        })
    return generated

def importer_historique(db):
    print("\n Importation de l'historique dans MongoDB ")

    col = db["deliveries"]
    col.drop()  # repart de zéro à chaque iniation du projet

    # Insère les livraisons de base
    col.insert_many(LIVRAISONS)
    print(f"  OK {len(LIVRAISONS)} livraisons de base insérées.")

    # Insère les livraisons générées
    extras = generer_livraisons_aleatoires(50)
    col.insert_many(extras)
    print(f"  OK {len(extras)} livraisons générées insérées.")

    total = col.count_documents({})
    print(f"\n  → Collection 'deliveries' : {total} documents au total.")
    return col

if __name__ == "__main__":
    db  = get_mongo()
    col = importer_historique(db)

    # Aperçu d'un document
    print("\n  Exemple de document :")
    doc = col.find_one({"command_id": "c1"}, {"_id": 0})
    for k, v in doc.items():
        print(f"    {k:<20} : {v}")
