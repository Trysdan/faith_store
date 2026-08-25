# config.py - Configuración global Faith Store
# ---------------------------------------------------------
# Paleta de colores (máximo 3 colores primarios)
COLOR_PRIMARY = "#1a1a2e"      # Azul oscuro - principal
COLOR_SECONDARY = "#16213e"    # Azul medio - secundario
COLOR_ACCENT = "#e94560"       # Rojo-acento - alertas

# Rutas de recursos
BASE_DIR = "."  # Directorio base de la aplicación
DB_PATH = "database/faith_store.db"
BACKUP_DIR = "backups"

# Configuración de tallas estándar
SIZES_STANDARD = ["S", "M", "L", "XL", "XXL"]
SHOE_SIZES = [38, 39, 40, 41, 42]

# Umbrales de stock (semáforo)
STOCK_GREEN = 20   # Alto
STOCK_YELLOW = 10  # Medio
STOCK_RED = 5      # Crítico

# Tasa BCV por defecto (ejemplo)
DEFAULT_BCV_RATE = 35.0
DEFAULT_USDT_RATE = 1.0