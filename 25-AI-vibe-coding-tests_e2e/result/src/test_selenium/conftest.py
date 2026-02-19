"""
Configuration pytest et fixtures pour les tests Selenium
Application Blog Simple - Tests End-to-End
"""
import pytest
import os
import sys
import io
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Forcer l'encodage UTF-8 pour la console Windows
# TODO - Tests executés avec la command python : Laisser ce bloc de code pour éviter les problèmes d'encodage sur Windows, surtout si les tests génèrent des logs avec des caractères spéciaux.
#        Tests exécutés avec pytest : Ce bloc doit être mis en commentaire ou supprimé, car pytest gère déjà l'encodage de la sortie et cela pourrait causer des problèmes d'affichage.
#        À voir plus tard si une solution plus élégante est possible pour gérer l'encodage de manière transparente dans les deux cas.
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# =============================================================================
# Configuration
# =============================================================================

# URL de l'application
FRONTEND_URL = "http://localhost:8080"  # Serveur frontend
BACKEND_URL = "http://localhost:5000"   # API Backend

# Timeout par défaut (secondes)
DEFAULT_TIMEOUT = 10

# Navigateur par défaut
DEFAULT_BROWSER = os.environ.get("SELENIUM_BROWSER", "chrome")

# Mode headless
HEADLESS_MODE = os.environ.get("SELENIUM_HEADLESS", "false").lower() == "true"


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def browser_name():
    """Retourne le nom du navigateur configuré"""
    return DEFAULT_BROWSER


# ...existing code...
# La correction pour utiliser ChromeDriver en local. 
# Assurez-vous que le chemin vers chromedriver.exe est correct et que la version de ChromeDriver correspond à votre version de Chrome installée. 
# Vous pouvez télécharger ChromeDriver depuis https://sites.google.com/chromium.org/driver/ et le placer dans le répertoire spécifié (C:\chromedriver\chromedriver.exe dans cet exemple).
# // TODO - Peux être qu'il faudra également effectuer une modification pour Edge et Firefox si vous souhaitez les utiliser en local sans WebDriverManager, mais pour l'instant nous allons nous concentrer sur Chrome.
@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture pour créer et gérer le WebDriver
    Crée une nouvelle instance pour chaque test
    """
    browser = DEFAULT_BROWSER.lower()
    driver = None
    
    try:
        if browser == "chrome":
            # from webdriver_manager.chrome import ChromeDriverManager  # ← Commenté
            options = ChromeOptions()
            if HEADLESS_MODE:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            # Utiliser le chemin local de ChromeDriver
            service = Service(r"C:\chromedriver\chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser == "edge":
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            options = EdgeOptions()
            if HEADLESS_MODE:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            
        elif browser == "firefox":
            from webdriver_manager.firefox import GeckoDriverManager
            options = FirefoxOptions()
            if HEADLESS_MODE:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
        else:
            raise ValueError(f"Navigateur non supporté: {browser}")
        
        driver.implicitly_wait(DEFAULT_TIMEOUT)
        driver.set_page_load_timeout(30)
        
        yield driver
        
    finally:
        if driver:
            driver.quit()

# ...existing code...


@pytest.fixture(scope="function")
def app_url():
    """Retourne l'URL de l'application frontend"""
    return FRONTEND_URL


@pytest.fixture(scope="function")
def api_url():
    """Retourne l'URL de l'API backend"""
    return BACKEND_URL


@pytest.fixture(scope="session")
def test_data():
    """Données de test partagées"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "user": {
            "username": f"testuser_{timestamp}",
            "email": f"testuser_{timestamp}@example.com"
        },
        "post": {
            "title": f"Test Article {timestamp}",
            "content": f"Contenu de test créé le {timestamp}. Ceci est un article de test pour les tests Selenium automatisés."
        },
        "timestamp": timestamp
    }


# =============================================================================
# Hooks pytest
# =============================================================================

def pytest_configure(config):
    """Configuration au démarrage de pytest"""
    # Créer le répertoire des rapports s'il n'existe pas
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Ajouter des marqueurs personnalisés
    config.addinivalue_line("markers", "users: Tests de la suite Users")
    config.addinivalue_line("markers", "posts: Tests de la suite Posts")
    config.addinivalue_line("markers", "statistics: Tests de la suite Statistics")
    config.addinivalue_line("markers", "haute: Tests de priorité haute")
    config.addinivalue_line("markers", "moyenne: Tests de priorité moyenne")
    config.addinivalue_line("markers", "basse: Tests de priorité basse")


def pytest_collection_modifyitems(config, items):
    """Modifier la collection des tests"""
    for item in items:
        # Ajouter automatiquement les marqueurs basés sur le nom du test
        test_name = item.name.lower()
        
        # Marqueurs de feature
        if "users" in test_name:
            item.add_marker(pytest.mark.users)
        elif "posts" in test_name:
            item.add_marker(pytest.mark.posts)
        elif "statistics" in test_name:
            item.add_marker(pytest.mark.statistics)
        
        # Marqueurs de priorité
        if "_haute_" in test_name:
            item.add_marker(pytest.mark.haute)
        elif "_moyenne_" in test_name:
            item.add_marker(pytest.mark.moyenne)
        elif "_basse_" in test_name:
            item.add_marker(pytest.mark.basse)


# =============================================================================
# Helpers pour les rapports
# =============================================================================

class TestResultCollector:
    """Collecteur de résultats de tests pour les rapports"""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = datetime.now()
        self.results = []
    
    def add_result(self, test_id, name, status, duration, message=""):
        self.results.append({
            "test_id": test_id,
            "name": name,
            "status": status,
            "duration": duration,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def finish(self):
        self.end_time = datetime.now()
    
    def get_summary(self):
        passed = len([r for r in self.results if r["status"] == "PASSED"])
        failed = len([r for r in self.results if r["status"] == "FAILED"])
        skipped = len([r for r in self.results if r["status"] == "SKIPPED"])
        total = len(self.results)
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "N/A"
        }


# Instance globale du collecteur
result_collector = TestResultCollector()


@pytest.fixture(scope="session", autouse=True)
def setup_result_collector():
    """Initialise le collecteur de résultats"""
    result_collector.start()
    yield
    result_collector.finish()
