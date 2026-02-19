# Guide d'Utilisation - Suite de Tests Selenium

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Structure des Tests](#structure-des-tests)
4. [Exécution des Tests](#exécution-des-tests)
5. [Options de Filtrage](#options-de-filtrage)
6. [Rapports de Tests](#rapports-de-tests)
7. [Configuration Avancée](#configuration-avancée)
8. [Dépannage](#dépannage)

---

## Introduction

Cette suite de tests Selenium automatise les tests end-to-end (E2E) de l'application Blog Simple. Les tests sont organisés en trois suites correspondant aux principales fonctionnalités de l'application :

- **Users** : Gestion des utilisateurs
- **Posts** : Gestion des articles
- **Statistics** : Affichage des statistiques

Les tests sont basés sur le plan de test défini dans `DEMO/result/doc/test_plan.md`.

---

## Prérequis

### 1. Python 3.8+
```bash
python --version
```

### 2. Packages Python
Les packages suivants doivent être installés :
```bash
pip install selenium webdriver-manager pytest pytest-html
```

### 3. Navigateur Web
Un des navigateurs suivants doit être installé :
- Google Chrome (recommandé)
- Microsoft Edge
- Mozilla Firefox

### 4. Application Blog en Cours d'Exécution

**Backend (API Flask):**
```bash
cd DEMO/result/src/app/backend
python app.py
```
Le serveur démarre sur `http://localhost:5000`

**Frontend:**
Le frontend peut être servi de plusieurs façons :

Option 1 - Serveur HTTP Python :
```bash
cd DEMO/result/src/app/frontend
python -m http.server 8080
```

Option 2 - Extension Live Server (VS Code)

---

## Structure des Tests

```
DEMO/result/src/test_selenium/
├── __init__.py              # Package Python
├── conftest.py              # Configuration pytest et fixtures
├── base_test.py             # Classe de base avec méthodes utilitaires
├── pytest.ini               # Configuration pytest
├── run_tests.py             # Script principal d'exécution
├── test_users.py            # Tests de la suite Users
├── test_posts.py            # Tests de la suite Posts
├── test_statistics.py       # Tests de la suite Statistics
└── reports/                 # Répertoire des rapports générés
    └── *.md
```

### Convention de Nommage des Tests

Les tests suivent la convention : `test_{FEATURE}_{PRIORITY}_{TC_ID}`

| Composant | Description | Exemple |
|-----------|-------------|---------|
| FEATURE | Nom de la suite | Users, Posts, Statistics |
| PRIORITY | Priorité du test | Haute, Moyenne, Basse |
| TC_ID | Identifiant du cas de test | TC_001_01 |

**Exemple:** `test_Users_Haute_TC_001_01`

---

## Exécution des Tests

### Méthode 1 : Via le Script run_tests.py (Recommandé)

Le script `run_tests.py` offre une interface simplifiée avec génération automatique de rapports.

```bash
cd DEMO/result/src/test_selenium

# Exécuter tous les tests
python run_tests.py

# Voir l'aide
python run_tests.py --help

# Lister tous les tests disponibles
python run_tests.py --list
```

### Méthode 2 : Via pytest Directement

```bash
cd DEMO/result/src/test_selenium

# Tous les tests
pytest

# Tests verbose
pytest -v

# Avec sortie en temps réel
pytest -v -s
```

---

## Options de Filtrage

### Par Feature (Suite de Tests)

```bash
# Tests Users uniquement
python run_tests.py --feature Users
python run_tests.py -f Users

# Tests Posts uniquement
python run_tests.py --feature Posts

# Tests Statistics uniquement
python run_tests.py --feature Statistics
```

Ou avec pytest :
```bash
pytest test_users.py
pytest test_posts.py
pytest test_statistics.py
```

### Par Priorité

```bash
# Tests de priorité haute uniquement
python run_tests.py --priority Haute
python run_tests.py -p Haute

# Tests de priorité moyenne
python run_tests.py --priority Moyenne

# Tests de priorité basse
python run_tests.py --priority Basse
```

Ou avec pytest :
```bash
pytest -m haute
pytest -m moyenne
pytest -m basse
```

### Par Feature ET Priorité

```bash
# Tests Users de haute priorité
python run_tests.py --feature Users --priority Haute
python run_tests.py -f Users -p Haute

# Tests Posts de priorité moyenne
python run_tests.py -f Posts -p Moyenne
```

Ou avec pytest :
```bash
pytest test_users.py -m haute
pytest test_posts.py -m moyenne
```

### Par Test ID Spécifique

```bash
# Exécuter un test spécifique par son ID
python run_tests.py --test-id TC-001-01
python run_tests.py -t TC-002-03
```

Ou avec pytest :
```bash
pytest -k "TC_001_01"
pytest -k "TC_002_03"
```

### Combinaisons Avancées

```bash
# Plusieurs tests spécifiques
pytest -k "TC_001_01 or TC_001_02"

# Tests contenant "create" dans le nom
pytest -k "create"

# Exclure certains tests
pytest -k "not TC_004"
```

---

## Rapports de Tests

### Génération Automatique

Par défaut, `run_tests.py` génère un rapport Markdown dans le répertoire `reports/`.

```bash
# Avec rapport (par défaut)
python run_tests.py

# Sans rapport
python run_tests.py --no-report
```

### Format du Nom de Rapport

Le nom du rapport suit le format : `{FEATURE}_{TIMESTAMP}.md`

| Filtre | Format du Rapport |
|--------|-------------------|
| Tous les tests | `all_tests_20260218_143052.md` |
| Feature Users | `Users_20260218_143052.md` |
| Users + Haute | `Users_Haute_20260218_143052.md` |
| Test spécifique | `test_TC-001-01_20260218_143052.md` |

### Contenu du Rapport

Chaque rapport inclut :
- Date et heure d'exécution
- Configuration utilisée (feature, priorité, navigateur)
- Résumé des résultats (passés, échoués, ignorés)
- Détails de la sortie
- Liste des tests échoués avec raisons

### Emplacement des Rapports

```
DEMO/result/src/test_selenium/reports/
├── all_tests_20260218_143052.md
├── Users_20260218_150000.md
├── Posts_Haute_20260218_151234.md
└── ...
```

---

## Configuration Avancée

### Variables d'Environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `SELENIUM_BROWSER` | Navigateur à utiliser | `chrome` |
| `SELENIUM_HEADLESS` | Mode sans interface | `false` |

### Options de Ligne de Commande

```bash
# Mode headless (sans interface graphique)
python run_tests.py --headless

# Choisir le navigateur
python run_tests.py --browser chrome
python run_tests.py --browser edge
python run_tests.py --browser firefox
python run_tests.py -b firefox

# Mode silencieux
python run_tests.py --quiet
python run_tests.py -q
```

### Configuration pytest.ini

Le fichier `pytest.ini` contient la configuration pytest :
- Marqueurs personnalisés (users, posts, statistics, haute, moyenne, basse)
- Options par défaut
- Filtres de warnings

### Personnaliser les URLs

Modifier `conftest.py` pour changer les URLs :

```python
FRONTEND_URL = "http://localhost:8080"
BACKEND_URL = "http://localhost:5000"
```

### Personnaliser les Timeouts

Dans `base_test.py` :

```python
DEFAULT_TIMEOUT = 10  # secondes
SHORT_TIMEOUT = 5
LONG_TIMEOUT = 30
```

---

## Dépannage

### Problèmes Courants

#### 1. "L'application n'est pas accessible"

**Solution:** Vérifiez que le backend et le frontend sont en cours d'exécution.

```bash
# Vérifier le backend
curl http://localhost:5000/api/health

# Vérifier le frontend
curl http://localhost:8080
```

#### 2. "WebDriver non trouvé"

**Solution:** Le webdriver-manager devrait le télécharger automatiquement. Sinon :

```bash
pip install --upgrade webdriver-manager
```

#### 3. "Element not found" / "Timeout"

**Solutions possibles:**
- Augmenter le timeout dans `base_test.py`
- Vérifier que le sélecteur CSS est correct
- S'assurer que l'élément est visible

#### 4. "Permission denied" sur Windows

**Solution:** Exécuter en tant qu'administrateur ou vérifier l'antivirus.

#### 5. Tests qui échouent aléatoirement

**Solutions:**
- Ajouter des `time.sleep()` après les actions
- Utiliser des waits explicites
- Vérifier la stabilité de l'application

### Mode Debug

Pour un débogage avancé :

```bash
# Afficher plus de détails
pytest -v -s --tb=long

# Arrêter au premier échec
pytest -x

# Afficher les logs du navigateur
# (modifier conftest.py pour activer les logs)
```

### Support des Navigateurs

| Navigateur | Status | Notes |
|------------|--------|-------|
| Chrome | ✅ Recommandé | Meilleure compatibilité |
| Edge | ✅ Supporté | Nécessite Edge Chromium |
| Firefox | ✅ Supporté | Peut être plus lent |

---

## Exemples d'Utilisation

### Scénario 1 : Exécution Complète

```bash
# Démarrer l'application
cd DEMO/result/src/app/backend
python app.py

# Dans un autre terminal
cd DEMO/result/src/app/frontend
python -m http.server 8080

# Dans un troisième terminal
cd DEMO/result/src/test_selenium
python run_tests.py
```

### Scénario 2 : Tests de Régression Rapide (Haute Priorité)

```bash
python run_tests.py --priority Haute
```

### Scénario 3 : Test d'une Nouvelle Fonctionnalité

```bash
# Tester uniquement la feature Users
python run_tests.py --feature Users

# Ou un test spécifique
python run_tests.py --test-id TC-002-01
```

### Scénario 4 : Exécution CI/CD (Headless)

```bash
python run_tests.py --headless --browser chrome
```

---

## Référence Rapide

| Commande | Description |
|----------|-------------|
| `python run_tests.py` | Tous les tests avec rapport |
| `python run_tests.py --list` | Lister les tests |
| `python run_tests.py -f Users` | Tests Users |
| `python run_tests.py -p Haute` | Tests haute priorité |
| `python run_tests.py -t TC-001-01` | Test spécifique |
| `python run_tests.py --headless` | Mode sans interface |
| `python run_tests.py --no-report` | Sans rapport |
| `pytest -v -s` | Pytest direct verbose |

---

*Documentation générée le 18 février 2026*
