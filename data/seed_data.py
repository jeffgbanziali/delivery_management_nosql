from datetime import datetime, timezone

# ── Livreurs de base ───────────────────────────────────
LIVREURS = [
    {"id": "d1", "nom": "Alice Dupont",    "region": "Paris",    "rating": 4.8},
    {"id": "d2", "nom": "Bob Martin",      "region": "Paris",    "rating": 4.5},
    {"id": "d3", "nom": "Charlie Lefevre", "region": "Banlieue", "rating": 4.9},
    {"id": "d4", "nom": "Diana Russo",     "region": "Banlieue", "rating": 4.3},
    {"id": "d5", "nom": "Emma Bernard",    "region": "Paris",    "rating": 4.7},
    {"id": "d6", "nom": "François Morel",  "region": "Paris",    "rating": 4.6},
    {"id": "d7", "nom": "Grace Petit",     "region": "Banlieue", "rating": 4.2},
    {"id": "d8", "nom": "Hugo Simon",      "region": "Banlieue", "rating": 4.8},
]

# ── Commandes de base ──────────────────────────────────
COMMANDES = [
    {"id": "c1", "client": "Client A", "destination": "Marais",    "montant": 25, "creee": "14:00"},
    {"id": "c2", "client": "Client B", "destination": "Belleville", "montant": 15, "creee": "14:05"},
    {"id": "c3", "client": "Client C", "destination": "Bercy",      "montant": 30, "creee": "14:10"},
    {"id": "c4", "client": "Client D", "destination": "Auteuil",    "montant": 20, "creee": "14:15"},
    {"id": "c5", "client": "Client E", "destination": "Marais",    "montant": 18, "creee": "14:20"},
    {"id": "c6", "client": "Client F", "destination": "Bercy",     "montant": 35, "creee": "14:25"},
]

# ── Livraisons historiques MongoDB ─────────────────────
LIVRAISONS = [
    {
        "command_id":       "c1",
        "client":           "Client A",
        "driver_id":        "d3",
        "driver_name":      "Charlie Lefevre",
        "pickup_time":      datetime(2025, 12, 6, 14,  5, tzinfo=timezone.utc),
        "delivery_time":    datetime(2025, 12, 6, 14, 25, tzinfo=timezone.utc),
        "duration_minutes": 20,
        "amount":           25,
        "region":           "Paris",
        "rating":           4.9,
        "review":           "Livraison rapide et soignée, très satisfait !",
        "status":           "completed",
    },
    {
        "command_id":       "c2",
        "client":           "Client B",
        "driver_id":        "d1",
        "driver_name":      "Alice Dupont",
        "pickup_time":      datetime(2025, 12, 6, 14, 10, tzinfo=timezone.utc),
        "delivery_time":    datetime(2025, 12, 6, 14, 25, tzinfo=timezone.utc),
        "duration_minutes": 15,
        "amount":           15,
        "region":           "Paris",
        "rating":           4.8,
        "review":           "Très professionnel, à recommander.",
        "status":           "completed",
    },
    {
        "command_id":       "c3",
        "client":           "Client C",
        "driver_id":        "d2",
        "driver_name":      "Bob Martin",
        "pickup_time":      datetime(2025, 12, 6, 14, 15, tzinfo=timezone.utc),
        "delivery_time":    datetime(2025, 12, 6, 14, 40, tzinfo=timezone.utc),
        "duration_minutes": 25,
        "amount":           30,
        "region":           "Banlieue",
        "rating":           4.5,
        "review":           "Correct, mais un peu de retard.",
        "status":           "completed",
    },
    {
        "command_id":       "c4",
        "client":           "Client D",
        "driver_id":        "d1",
        "driver_name":      "Alice Dupont",
        "pickup_time":      datetime(2025, 12, 6, 14, 20, tzinfo=timezone.utc),
        "delivery_time":    datetime(2025, 12, 6, 14, 38, tzinfo=timezone.utc),
        "duration_minutes": 18,
        "amount":           20,
        "region":           "Paris",
        "rating":           4.8,
        "review":           "Parfait, commande bien emballée.",
        "status":           "completed",
    },
]

# ── Coordonnées géo-spatiales ──────────────────────────
LIEUX_LIVRAISON = [
    {"nom": "Marais",    "region": "Paris",    "lon": 2.364, "lat": 48.861},
    {"nom": "Belleville","region": "Paris",    "lon": 2.379, "lat": 48.870},
    {"nom": "Bercy",     "region": "Paris",    "lon": 2.381, "lat": 48.840},
    {"nom": "Auteuil",   "region": "Paris",    "lon": 2.254, "lat": 48.851},
]

POSITIONS_LIVREURS = [
    {"id": "d1", "lon": 2.365, "lat": 48.862},
    {"id": "d2", "lon": 2.378, "lat": 48.871},
    {"id": "d3", "lon": 2.320, "lat": 48.920},
    {"id": "d4", "lon": 2.400, "lat": 48.750},
]
