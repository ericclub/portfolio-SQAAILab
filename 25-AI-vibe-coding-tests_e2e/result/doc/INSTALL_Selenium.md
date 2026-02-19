# Rapport d'Installation - Selenium pour Python

## 📋 Informations

| Élément | Valeur |
|---------|--------|
| **Date d'installation** | 18 février 2026 |
| **Python Version** | 3.14.2 |
| **Système** | Windows |

---

## 📦 Packages Installés

| Package | Description |
|---------|-------------|
| **selenium** | Framework d'automatisation de navigateur web |
| **webdriver-manager** | Gestion automatique des drivers de navigateurs (Chrome, Firefox, Edge) |
| **pytest** | Framework de tests Python |
| **pytest-html** | Plugin pytest pour génération de rapports HTML |

---

## ✅ Vérification de l'Installation

Pour vérifier que Selenium est correctement installé, exécutez :

```bash
python -c "import selenium; print(f'Selenium version: {selenium.__version__}')"
```

Pour vérifier pytest :

```bash
pytest --version
```

---

## 🔧 Configuration du WebDriver

Le package `webdriver-manager` gère automatiquement le téléchargement et la configuration des drivers de navigateurs.

### Exemple de Configuration Chrome

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuration automatique du driver Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

### Exemple de Configuration Edge

```python
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Configuration automatique du driver Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
```

### Exemple de Configuration Firefox

```python
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Configuration automatique du driver Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
```

---

## 📁 Structure des Tests

Les tests Selenium sont organisés dans le répertoire suivant :

```
DEMO/result/src/
├── test_selenium/
│   ├── __init__.py
│   ├── conftest.py              # Configuration pytest et fixtures
│   ├── base_test.py             # Classe de base pour les tests
│   ├── run_tests.py             # Script principal d'exécution
│   ├── test_users.py            # Suite de tests Users
│   ├── test_posts.py            # Suite de tests Posts
│   ├── test_statistics.py       # Suite de tests Statistics
│   └── reports/                 # Répertoire des rapports
│       └── *.md
```

---

## 🚀 Prérequis pour l'Exécution

### 1. Navigateur Web
Un navigateur compatible doit être installé :
- Google Chrome (recommandé)
- Microsoft Edge
- Mozilla Firefox

### 2. Backend de l'Application
L'application Flask doit être en cours d'exécution :

```bash
cd DEMO/result/src/app/backend
python app.py
```

### 3. Frontend de l'Application
Le frontend doit être accessible (servi par un serveur web ou ouvert directement).

---

## ⚠️ Notes Importantes

1. **Mode Headless** : Les tests peuvent être exécutés en mode headless (sans interface graphique) pour les environnements CI/CD.

2. **Timeouts** : Des timeouts appropriés sont configurés pour gérer les temps de chargement.

3. **Isolation** : Chaque test est isolé et ne dépend pas des données des autres tests.

---

## 📖 Documentation Complémentaire

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [pytest Documentation](https://docs.pytest.org/)
- [webdriver-manager Documentation](https://github.com/SergeyPirogov/webdriver_manager)
