*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Guide des tests E2E Selenium

## Aperçu

Cette suite de tests fournit des tests automatisés de bout en bout (E2E) pour l'interface d'administration du Flask Blog Admin UI à l'aide de Selenium WebDriver avec Python. Les tests suivent le patron **Page Object Model** pour en faciliter la maintenance et utilisent **pytest** comme framework de test.

## Cas de test

| ID de test | Story | Description |
|---------|-------|-------------|
| TC-E2E-01 | E2E-01 | L'UI se charge et affiche les statistiques (test de fumée) |
| TC-E2E-02 | E2E-01 | Le rafraîchissement des stats met à jour les valeurs affichées |
| TC-E2E-03 | E2E-02 | Flux de création d'un utilisateur → création d'un post en brouillon |
| TC-E2E-04 | E2E-02 | Variante de création d'un post publié |

Ces tests couvrent les user stories E2E critiques issues de `20-AI-QA-analysis-assistant/result/doc/user_stories.md`.

---

## Prérequis

### 1. Exigences logicielles

- **Python 3.8+** installé
- **Google Chrome** installé (dernière version recommandée)
- **Flask Blog API** en cours d'exécution sur `http://localhost:5000`

### 2. Configuration de l'application

Avant d'exécuter les tests, assurez-vous que le Flask Blog API est bien lancé :

```bash
# Se déplacer dans le répertoire de l'application
cd 10-AI-vibe-coding\result\src\app\backend

# Activer l'environnement virtuel (si utilisé)
..\..\.venv\Scripts\activate

# Lancer l'application
python app.py
```

L'application devrait être accessible sur `http://localhost:5000`.

---

## Installation

### 1. Se déplacer dans le répertoire des tests

```bash
cd 25-AI-vibe-coding-tests_e2e\result\selenium
```

### 2. Créer et activer un environnement virtuel (recommandé)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Ceci installe :
- `selenium` - Automatisation de navigateur
- `pytest` - Framework de test
- `pytest-html` - Génération de rapport HTML
- `webdriver-manager` - Gestion automatique de ChromeDriver

---

## Exécution des tests

### Utilisation de base

```bash
# Exécuter tous les tests avec navigateur visible (par défaut)
python run_tests.py

# Exécuter tous les tests en mode headless (sans fenêtre de navigateur)
python run_tests.py --headless
```

### Filtrage des tests

```bash
# Exécuter uniquement les tests de fumée
python run_tests.py --smoke

# Exécuter uniquement les tests de l'onglet statistiques
python run_tests.py --statistics

# Exécuter uniquement les tests liés aux utilisateurs
python run_tests.py --users

# Exécuter uniquement les tests liés aux posts
python run_tests.py --posts
```

### Options supplémentaires

```bash
# Exécuter avec sortie détaillée (verbose)
python run_tests.py --verbose

# Ignorer la génération du rapport Markdown
python run_tests.py --no-report

# Utiliser une URL de base différente
python run_tests.py --base-url http://localhost:8080

# Combiner les options
python run_tests.py --headless --smoke --verbose
```

### Utilisation directe de pytest

```bash
# Exécuter tous les tests
pytest tests/ -v

# Exécuter en mode headless
pytest tests/ -v --headless

# Exécuter un fichier de test spécifique
pytest tests/test_statistics.py -v

# Exécuter par marqueur
pytest tests/ -v -m smoke

# Exécuter un test spécifique
pytest tests/test_statistics.py::TestStatisticsDisplay::test_ui_loads_and_shows_stats -v
```

---

## Rapports de test

### Emplacement des rapports

Tous les rapports sont enregistrés dans le répertoire `reports/` :

```
selenium/
└── reports/
    ├── test_results_e2e_20260305_160000.html    # Rapport HTML
    ├── test_results_e2e_20260305_160000.md      # Rapport Markdown
    └── screenshots/                              # Captures d'écran en cas d'échec
        └── test_name_timestamp.png
```

### Convention de nommage des rapports

- Format : `test_results_e2e_{YYYYMMDD}_{HHMMSS}.{ext}`
- Exemple : `test_results_e2e_20260305_160000.html`

### Rapport HTML

Le rapport HTML fournit :
- Statistiques résumées (réussis/échoués/ignorés)
- Durée des tests
- Résultats détaillés pour chaque test
- Messages d'erreur et traces de pile

À ouvrir dans un navigateur web pour une meilleure expérience de visualisation.

### Rapport Markdown

Le rapport Markdown comprend :
- Tableau résumé avec les métriques clés
- Tableau du statut des cas de test
- Sortie console complète
- Analyse des tests échoués (le cas échéant)
- Informations sur la couverture de test

---

## Structure du projet

```
selenium/
├── conftest.py           # Fixtures pytest (driver, base_url, données de test)
├── pytest.ini            # Configuration pytest et marqueurs
├── requirements.txt      # Dépendances Python
├── run_tests.py          # Lanceur de test en ligne de commande avec génération de rapport
├── test_guide.md         # Cette documentation
├── pages/                # Classes du Page Object Model
│   ├── __init__.py
│   ├── base_page.py      # Classe de base avec méthodes communes
│   ├── statistics_page.py # Interactions avec l'onglet statistiques
│   ├── users_page.py     # Interactions avec l'onglet utilisateurs
│   └── posts_page.py     # Interactions avec l'onglet posts
├── tests/                # Modules de test
│   ├── __init__.py
│   ├── test_statistics.py    # TC-E2E-01, TC-E2E-02
│   └── test_user_post_flow.py # TC-E2E-03, TC-E2E-04
└── reports/              # Rapports générés (créés à l'exécution)
    ├── *.html
    ├── *.md
    └── screenshots/
```

---

## Configuration

### Options du navigateur

Les tests utilisent le navigateur Chrome par défaut. Options disponibles :

| Option | Description | Par défaut |
|--------|-------------|---------|
| `--headless` | Exécute sans fenêtre de navigateur visible | `False` |
| `--window-size` | Dimensions de la fenêtre du navigateur | `1920x1080` |
| Attente implicite | Temps d'attente par défaut pour les éléments | `10s` |

### URL de base

Par défaut : `http://localhost:5000`

À surcharger avec : `--base-url http://your-server:port`

### Marqueurs pytest

Marqueurs disponibles pour le filtrage des tests :

| Marqueur | Description |
|--------|-------------|
| `smoke` | Tests de fumée pour les fonctionnalités de base |
| `e2e` | Tests de navigateur de bout en bout |
| `statistics` | Tests de l'onglet statistiques |
| `users` | Tests de gestion des utilisateurs |
| `posts` | Tests de gestion des posts |

---

## Dépannage

### Problèmes courants

#### 1. Erreur « Connection refused »

**Problème** : Les tests échouent avec une connexion refusée sur localhost:5000

**Solution** : Assurez-vous que le Flask Blog API est en cours d'exécution :
```bash
cd 10-AI-vibe-coding\result\src\app\backend
python app.py
```

#### 2. Incompatibilité de version de ChromeDriver

**Problème** : « This version of ChromeDriver only supports Chrome version XX »

**Solution** : Le package `webdriver-manager` gère automatiquement ce problème. Si le problème persiste :
```bash
pip install --upgrade webdriver-manager
```

#### 3. Éléments introuvables

**Problème** : Les tests échouent avec « element not found » ou des erreurs de délai d'attente (timeout)

**Causes possibles** :
- Page pas complètement chargée (augmenter les temps d'attente)
- Structure de l'UI modifiée (mettre à jour les sélecteurs des page objects)
- Erreur applicative empêchant le rendu de la page

**Solution** : Vérifiez que l'application fonctionne correctement lors d'une session manuelle dans le navigateur.

#### 4. Les tests réussissent en local mais échouent en CI

**Problème** : Les tests fonctionnent sur la machine locale mais échouent en CI/CD

**Solution** : Assurez-vous que l'environnement CI dispose de :
- Chrome installé
- Le flag `--headless` utilisé
- Des temps d'attente suffisants pour les environnements plus lents
- L'application en cours d'exécution et accessible

### Capture d'écran en cas d'échec

Lorsqu'un test échoue, une capture d'écran est automatiquement prise et enregistrée dans :
```
reports/screenshots/test_name_timestamp.png
```

---

## Bonnes pratiques

### Pour les développeurs

1. **Garder les tests indépendants** : Chaque test doit pouvoir s'exécuter de manière isolée
2. **Utiliser des données de test uniques** : Générer des noms d'utilisateur/e-mails uniques à chaque exécution de test
3. **Nettoyer les données de test** : Envisager des stratégies de nettoyage pour l'état de la base de données
4. **Mettre à jour les page objects** : Lorsque l'UI change, mettre à jour les sélecteurs dans les classes de page
5. **Exécuter en headless en CI** : Utiliser `--headless` pour les pipelines automatisés

### Pour les ingénieurs QA

1. **Exécuter d'abord les tests de fumée** : Utiliser `--smoke` pour une validation rapide
2. **Vérifier les rapports** : Examiner les rapports HTML/Markdown après chaque exécution
3. **Vérifier les prérequis** : S'assurer que l'application est lancée avant l'exécution des tests
4. **Utiliser le mode visible pour le débogage** : Omettre `--headless` pour observer l'exécution des tests

---

## Couverture des user stories

### E2E-01 : L'UI d'administration se charge et affiche des statistiques en direct

**Critères d'acceptation** :
- L'UI se charge et affiche les statistiques provenant de l'API ✅
- Le rafraîchissement met à jour les statistiques affichées ✅

**Tests** :
- `test_ui_loads_and_shows_stats` (TC-E2E-01)
- `test_refresh_updates_stats` (TC-E2E-02)

### E2E-02 : L'administrateur peut créer un utilisateur puis créer un post via l'UI

**Critères d'acceptation** :
- Créer un utilisateur via l'UI et le voir apparaître dans la liste ✅
- Créer un post pour le nouvel utilisateur via l'UI et le voir apparaître dans la liste ✅
- Le badge « brouillon » est affiché pour les posts en brouillon ✅
- Le badge « publié » est affiché pour les posts publiés ✅

**Tests** :
- `test_create_user_and_draft_post` (TC-E2E-03)
- `test_create_published_post` (TC-E2E-04)

---

## Référence rapide

```bash
# Démarrage rapide (après installation)
python run_tests.py

# Mode headless pour CI/CD
python run_tests.py --headless

# Tests de fumée uniquement
python run_tests.py --smoke --headless

# Consulter les résultats
# Ouvrir reports/test_results_e2e_*.html dans un navigateur
```

---

*Dernière mise à jour : mars 2026*

---

## 🇬🇧 English

# E2E Selenium Test Guide

## Overview

This test suite provides end-to-end (E2E) automated tests for the Flask Blog Admin UI using Selenium WebDriver with Python. The tests follow the **Page Object Model** pattern for maintainability and use **pytest** as the test framework.

## Test Cases

| Test ID | Story | Description |
|---------|-------|-------------|
| TC-E2E-01 | E2E-01 | UI loads and displays statistics (smoke test) |
| TC-E2E-02 | E2E-01 | Stats refresh updates displayed values |
| TC-E2E-03 | E2E-02 | Create user → create draft post flow |
| TC-E2E-04 | E2E-02 | Create published post variant |

These tests cover the critical E2E user stories from `20-AI-QA-analysis-assistant/result/doc/user_stories.md`.

---

## Prerequisites

### 1. Software Requirements

- **Python 3.8+** installed
- **Google Chrome** browser installed (latest version recommended)
- **Flask Blog API** application running at `http://localhost:5000`

### 2. Application Setup

Before running tests, ensure the Flask Blog API is running:

```bash
# Navigate to the application directory
cd 10-AI-vibe-coding\result\src\app\backend

# Activate virtual environment (if using)
..\..\.venv\Scripts\activate

# Run the application
python app.py
```

The application should be accessible at `http://localhost:5000`.

---

## Installation

### 1. Navigate to the test directory

```bash
cd 25-AI-vibe-coding-tests_e2e\result\selenium
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `selenium` - Browser automation
- `pytest` - Test framework
- `pytest-html` - HTML report generation
- `webdriver-manager` - Automatic ChromeDriver management

---

## Running Tests

### Basic Usage

```bash
# Run all tests with visible browser (default)
python run_tests.py

# Run all tests in headless mode (no browser window)
python run_tests.py --headless
```

### Test Filtering

```bash
# Run only smoke tests
python run_tests.py --smoke

# Run only statistics tab tests
python run_tests.py --statistics

# Run only user-related tests
python run_tests.py --users

# Run only post-related tests
python run_tests.py --posts
```

### Additional Options

```bash
# Run with verbose output
python run_tests.py --verbose

# Skip Markdown report generation
python run_tests.py --no-report

# Use a different base URL
python run_tests.py --base-url http://localhost:8080

# Combine options
python run_tests.py --headless --smoke --verbose
```

### Using pytest directly

```bash
# Run all tests
pytest tests/ -v

# Run with headless mode
pytest tests/ -v --headless

# Run specific test file
pytest tests/test_statistics.py -v

# Run by marker
pytest tests/ -v -m smoke

# Run specific test
pytest tests/test_statistics.py::TestStatisticsDisplay::test_ui_loads_and_shows_stats -v
```

---

## Test Reports

### Report Location

All reports are saved to the `reports/` directory:

```
selenium/
└── reports/
    ├── test_results_e2e_20260305_160000.html    # HTML report
    ├── test_results_e2e_20260305_160000.md      # Markdown report
    └── screenshots/                              # Screenshots on failure
        └── test_name_timestamp.png
```

### Report Naming Convention

- Format: `test_results_e2e_{YYYYMMDD}_{HHMMSS}.{ext}`
- Example: `test_results_e2e_20260305_160000.html`

### HTML Report

The HTML report provides:
- Summary statistics (passed/failed/skipped)
- Test duration
- Detailed results for each test
- Error messages and stack traces

Open in a web browser for best viewing experience.

### Markdown Report

The Markdown report includes:
- Summary table with key metrics
- Test case status table
- Full console output
- Failed test analysis (if applicable)
- Test coverage information

---

## Project Structure

```
selenium/
├── conftest.py           # Pytest fixtures (driver, base_url, test data)
├── pytest.ini            # Pytest configuration and markers
├── requirements.txt      # Python dependencies
├── run_tests.py          # CLI test runner with report generation
├── test_guide.md         # This documentation
├── pages/                # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py      # Base class with common methods
│   ├── statistics_page.py # Statistics tab interactions
│   ├── users_page.py     # Users tab interactions
│   └── posts_page.py     # Posts tab interactions
├── tests/                # Test modules
│   ├── __init__.py
│   ├── test_statistics.py    # TC-E2E-01, TC-E2E-02
│   └── test_user_post_flow.py # TC-E2E-03, TC-E2E-04
└── reports/              # Generated reports (created on run)
    ├── *.html
    ├── *.md
    └── screenshots/
```

---

## Configuration

### Browser Options

The tests use Chrome browser by default. Options include:

| Option | Description | Default |
|--------|-------------|---------|
| `--headless` | Run without visible browser window | `False` |
| `--window-size` | Browser window dimensions | `1920x1080` |
| Implicit wait | Default wait time for elements | `10s` |

### Base URL

Default: `http://localhost:5000`

Override with: `--base-url http://your-server:port`

### Pytest Markers

Available markers for test filtering:

| Marker | Description |
|--------|-------------|
| `smoke` | Smoke tests for basic functionality |
| `e2e` | End-to-end browser tests |
| `statistics` | Statistics tab tests |
| `users` | User management tests |
| `posts` | Post management tests |

---

## Troubleshooting

### Common Issues

#### 1. "Connection refused" error

**Problem**: Tests fail with connection refused to localhost:5000

**Solution**: Ensure the Flask Blog API is running:
```bash
cd 10-AI-vibe-coding\result\src\app\backend
python app.py
```

#### 2. ChromeDriver version mismatch

**Problem**: "This version of ChromeDriver only supports Chrome version XX"

**Solution**: The `webdriver-manager` package automatically handles this. If issues persist:
```bash
pip install --upgrade webdriver-manager
```

#### 3. Elements not found

**Problem**: Tests fail with "element not found" or timeout errors

**Possible causes**:
- Page not fully loaded (increase wait times)
- UI structure changed (update page object selectors)
- Application error preventing page render

**Solution**: Check the application is working correctly in a manual browser session.

#### 4. Tests pass locally but fail in CI

**Problem**: Tests work on local machine but fail in CI/CD

**Solution**: Ensure CI environment has:
- Chrome browser installed
- `--headless` flag used
- Sufficient wait times for slower environments
- Application running and accessible

### Screenshot on Failure

When a test fails, a screenshot is automatically captured and saved to:
```
reports/screenshots/test_name_timestamp.png
```

---

## Best Practices

### For Developers

1. **Keep tests independent**: Each test should be able to run in isolation
2. **Use unique test data**: Generate unique usernames/emails per test run
3. **Clean up test data**: Consider cleanup strategies for database state
4. **Update page objects**: When UI changes, update selectors in page classes
5. **Run headless in CI**: Use `--headless` for automated pipelines

### For QA Engineers

1. **Run smoke tests first**: Use `--smoke` for quick validation
2. **Check reports**: Review HTML/Markdown reports after each run
3. **Verify prerequisites**: Ensure app is running before test execution
4. **Use visible mode for debugging**: Omit `--headless` to watch test execution

---

## User Story Coverage

### E2E-01: Admin UI loads and shows live statistics

**Acceptance Criteria**:
- UI loads and renders stats from the API ✅
- Refresh updates the displayed stats ✅

**Tests**:
- `test_ui_loads_and_shows_stats` (TC-E2E-01)
- `test_refresh_updates_stats` (TC-E2E-02)

### E2E-02: Admin can create user then create post via UI

**Acceptance Criteria**:
- Create a user via UI and see it listed ✅
- Create a post for the new user via UI and see it listed ✅
- Draft badge displayed for draft posts ✅
- Published badge displayed for published posts ✅

**Tests**:
- `test_create_user_and_draft_post` (TC-E2E-03)
- `test_create_published_post` (TC-E2E-04)

---

## Quick Reference

```bash
# Quick start (after installation)
python run_tests.py

# Headless mode for CI/CD
python run_tests.py --headless

# Smoke tests only
python run_tests.py --smoke --headless

# View results
# Open reports/test_results_e2e_*.html in browser
```

---

*Last updated: March 2026*
