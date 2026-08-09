*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Guide de test - API Flask Blog

Ce guide explique comment exécuter les tests unitaires et d'intégration de l'application API Flask Blog.

## Table des matières

1. [Prérequis](#prérequis)
2. [Structure du projet](#structure-du-projet)
3. [Installation](#installation)
4. [Exécution des tests](#exécution-des-tests)
5. [Catégories de tests](#catégories-de-tests)
6. [Rapports de test](#rapports-de-test)
7. [Couverture des cas de test](#couverture-des-cas-de-test)
8. [Dépannage](#dépannage)

---

## Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Environnement virtuel (recommandé)

## Structure du projet

```
25-AI-vibe-coding-tests/
└── result/
    └── test/
        ├── conftest.py           # Fixtures pytest partagées
        ├── pytest.ini            # Configuration pytest
        ├── requirements.txt      # Dépendances de test
        ├── run_tests.py          # Script d'exécution des tests
        ├── unit/                 # Tests unitaires
        │   ├── __init__.py
        │   ├── test_user_validation.py
        │   ├── test_post_validation.py
        │   └── test_response_shapes.py
        ├── integration/          # Tests d'intégration
        │   ├── __init__.py
        │   ├── test_health.py
        │   ├── test_users.py
        │   ├── test_posts.py
        │   ├── test_stats.py
        │   ├── test_cors.py
        │   └── test_error_handling.py
        └── reports/              # Rapports de test générés
```

## Installation

1. **Accéder au répertoire de tests :**

   ```bash
   cd 25-AI-vibe-coding-tests/result/test
   ```

2. **Créer et activer un environnement virtuel (recommandé) :**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

## Exécution des tests

### Utilisation du script d'exécution des tests

Le script `run_tests.py` offre un moyen pratique d'exécuter les tests avec diverses options :

```bash
# Exécuter TOUS les tests (unitaires + intégration)
python run_tests.py

# Exécuter uniquement les tests UNITAIRES
python run_tests.py --unit
# ou
python run_tests.py -u

# Exécuter uniquement les tests D'INTÉGRATION
python run_tests.py --integration
# ou
python run_tests.py -i

# Exécuter avec une sortie détaillée
python run_tests.py --verbose
# ou
python run_tests.py -v

# Exécuter sans générer de rapport Markdown
python run_tests.py --no-report
```

### Utilisation directe de pytest

Vous pouvez également utiliser pytest directement pour plus de contrôle :

```bash
# Exécuter tous les tests
pytest unit integration -v

# Exécuter uniquement les tests unitaires
pytest unit -v -m unit

# Exécuter uniquement les tests d'intégration
pytest integration -v -m integration

# Exécuter les tests d'une fonctionnalité spécifique (en utilisant les marqueurs)
pytest -m users -v        # Tests liés aux utilisateurs
pytest -m posts -v        # Tests liés aux articles
pytest -m stats -v        # Tests de statistiques
pytest -m health -v       # Tests de vérification de santé

# Exécuter un fichier de test spécifique
pytest integration/test_users.py -v

# Exécuter une classe de test spécifique
pytest integration/test_users.py::TestCreateUser -v

# Exécuter une méthode de test spécifique
pytest integration/test_users.py::TestCreateUser::test_create_user_with_valid_data -v
```

## Catégories de tests

### Tests unitaires (`unit/`)

Les tests unitaires valident la logique métier sans appels HTTP ni accès à la base de données :

| Fichier de test | Description |
|-----------|-------------|
| `test_user_validation.py` | Sérialisation du modèle utilisateur, gestion des mots de passe, logique de validation |
| `test_post_validation.py` | Sérialisation du modèle d'article, valeurs par défaut, logique de validation |
| `test_response_shapes.py` | Validation de la structure des réponses API |

### Tests d'intégration (`integration/`)

Les tests d'intégration valident les points de terminaison de l'API avec le client de test Flask et une base de données SQLite en mémoire :

| Fichier de test | Description |
|-----------|-------------|
| `test_health.py` | Point de terminaison de santé (HLTH-01) |
| `test_users.py` | Opérations CRUD utilisateur (USR-01 à USR-04) |
| `test_posts.py` | Opérations CRUD article (PST-01 à PST-06) |
| `test_stats.py` | Point de terminaison de statistiques (STS-01) |
| `test_cors.py` | Configuration CORS (NFR-02) |
| `test_error_handling.py` | Gestion des erreurs et réponses JSON (NFR-01, NFR-03) |

### Marqueurs de test

Les tests sont étiquetés avec des marqueurs pour une exécution sélective :

- `@pytest.mark.unit` - Tests unitaires
- `@pytest.mark.integration` - Tests d'intégration
- `@pytest.mark.health` - Tests de vérification de santé
- `@pytest.mark.users` - Tests de gestion des utilisateurs
- `@pytest.mark.posts` - Tests de gestion des articles
- `@pytest.mark.stats` - Tests de statistiques

## Rapports de test

Les rapports de test sont générés automatiquement dans le répertoire `reports/` :

### Emplacement des rapports

```
reports/
├── test_results_all_YYYYMMDD_HHMMSS.md      # Rapport de tous les tests
├── test_results_all_YYYYMMDD_HHMMSS.html    # Rapport HTML
├── test_results_unit_YYYYMMDD_HHMMSS.md     # Rapport des tests unitaires
├── test_results_unit_YYYYMMDD_HHMMSS.html   # Rapport HTML
├── test_results_integration_YYYYMMDD_HHMMSS.md   # Rapport des tests d'intégration
└── test_results_integration_YYYYMMDD_HHMMSS.html # Rapport HTML
```

### Contenu du rapport Markdown

Chaque rapport Markdown comprend :

- **Résumé** : Type de test, horodatage, statut global, nombre total/réussis/échoués
- **Configuration des tests** : Framework et référence au rapport HTML
- **Sortie console** : Sortie complète de pytest avec les résultats des tests
- **Analyse des tests échoués** : Détails sur les échecs éventuels (le cas échéant)

### Consultation des rapports

- **Markdown** : Ouvrez les fichiers `.md` dans un éditeur de texte ou un visualiseur Markdown
- **HTML** : Ouvrez les fichiers `.html` dans un navigateur web pour une visualisation interactive

## Couverture des cas de test

### Couverture des user stories

| ID de la story | Description | Type de test | Fichier de test |
|----------|-------------|-----------|-----------|
| HLTH-01 | Vérification de santé | Intégration | `test_health.py` |
| USR-01 | Créer un utilisateur | Les deux | `test_users.py`, `test_user_validation.py` |
| USR-02 | Lister les utilisateurs | Intégration | `test_users.py` |
| USR-03 | Consulter un utilisateur par ID | Intégration | `test_users.py` |
| USR-04 | Supprimer un utilisateur (en cascade) | Intégration | `test_users.py` |
| PST-01 | Créer un article | Les deux | `test_posts.py`, `test_post_validation.py` |
| PST-02 | Lister tous les articles | Intégration | `test_posts.py` |
| PST-03 | Lister les articles publiés | Intégration | `test_posts.py` |
| PST-04 | Consulter un article par ID | Intégration | `test_posts.py` |
| PST-05 | Mettre à jour un article | Intégration | `test_posts.py` |
| PST-06 | Supprimer un article | Intégration | `test_posts.py` |
| STS-01 | Consulter les statistiques | Intégration | `test_stats.py` |
| NFR-01 | Réponses JSON | Intégration | `test_error_handling.py` |
| NFR-02 | CORS activé | Intégration | `test_cors.py` |

### Matrice des cas de test

| ID du cas de test | Description | Méthode de test |
|--------------|-------------|-------------|
| TC-HLTH-01 | Vérification de santé retourne OK | `test_health_check_returns_200` |
| TC-USR-01 | Créer un utilisateur avec des données valides | `test_create_user_with_valid_data` |
| TC-USR-02 | Rejeter les champs manquants | `test_create_user_missing_*` |
| TC-USR-03 | Rejeter un nom d'utilisateur en double | `test_create_user_duplicate_username` |
| TC-USR-04 | Rejeter un email en double | `test_create_user_duplicate_email` |
| TC-USR-05 | Lister les utilisateurs retourne un tableau | `test_list_users_returns_array` |
| TC-USR-06 | Lister les utilisateurs (base vide) | `test_list_users_empty_database` |
| TC-USR-07 | Récupérer un utilisateur par ID valide | `test_get_user_by_valid_id` |
| TC-USR-08 | Utilisateur non trouvé | `test_get_user_not_found` |
| TC-USR-09 | Suppression d'utilisateur réussie | `test_delete_user_success` |
| TC-USR-10 | Suppression d'utilisateur en cascade sur les articles | `test_delete_user_cascade_posts` |
| TC-USR-11 | Suppression d'un utilisateur non trouvé | `test_delete_user_not_found` |
| TC-PST-01 | Créer un article avec des données valides | `test_create_post_with_valid_data` |
| TC-PST-02 | Créer un article avec des champs manquants | `test_create_post_missing_*` |
| TC-PST-03 | Créer un article pour un utilisateur non trouvé | `test_create_post_user_not_found` |
| TC-PST-04 | Lister les articles triés | `test_list_posts_ordered_by_created_at_desc` |
| TC-PST-05 | Lister les articles (base vide) | `test_list_posts_empty_database` |
| TC-PST-06 | Lister uniquement les articles publiés | `test_list_published_posts_only` |
| TC-PST-07 | Lister les articles publiés (base vide) | `test_list_published_posts_empty` |
| TC-PST-08 | Récupérer un article par ID valide | `test_get_post_by_valid_id` |
| TC-PST-09 | Article non trouvé | `test_get_post_not_found` |
| TC-PST-10 | Publier un article via mise à jour | `test_update_post_publish` |
| TC-PST-11 | Mettre à jour les champs d'un article | `test_update_post_title_and_content` |
| TC-PST-12 | Mise à jour d'un article non trouvé | `test_update_post_not_found` |
| TC-PST-13 | Suppression d'article réussie | `test_delete_post_success` |
| TC-PST-14 | Suppression d'un article non trouvé | `test_delete_post_not_found` |
| TC-STS-01 | Les statistiques retournent des zéros | `test_stats_empty_database` |
| TC-STS-02 | Les statistiques reflètent les données | `test_stats_reflect_created_data` |
| TC-STS-03 | Impact de la cascade sur les statistiques | `test_stats_cascade_impact` |

## Dépannage

### Problèmes courants

1. **ModuleNotFoundError: No module named 'app'**
   
   Assurez-vous d'exécuter les tests depuis le bon répertoire et que le chemin source est configuré dans `conftest.py`.

2. **Erreurs de connexion à la base de données**
   
   Les tests utilisent une base de données SQLite en mémoire. Aucune connexion MySQL n'est requise pour les tests.

3. **Erreurs d'import pour les dépendances Flask**
   
   Installez toutes les dépendances : `pip install -r requirements.txt`

4. **pytest introuvable**
   
   Assurez-vous que pytest est installé : `pip install pytest`

### Obtenir de l'aide

- Consultez la configuration des tests dans `pytest.ini`
- Vérifiez les fixtures dans `conftest.py`
- Examinez les fichiers de test individuels pour les implémentations de tests spécifiques

---

*Dernière mise à jour : mars 2026*

---

## 🇬🇧 English

# Flask Blog API Test Guide

This guide explains how to run the unit and integration tests for the Flask Blog API application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Running Tests](#running-tests)
5. [Test Categories](#test-categories)
6. [Test Reports](#test-reports)
7. [Test Cases Coverage](#test-cases-coverage)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Project Structure

```
25-AI-vibe-coding-tests/
└── result/
    └── test/
        ├── conftest.py           # Shared pytest fixtures
        ├── pytest.ini            # Pytest configuration
        ├── requirements.txt      # Test dependencies
        ├── run_tests.py          # Test runner script
        ├── unit/                 # Unit tests
        │   ├── __init__.py
        │   ├── test_user_validation.py
        │   ├── test_post_validation.py
        │   └── test_response_shapes.py
        ├── integration/          # Integration tests
        │   ├── __init__.py
        │   ├── test_health.py
        │   ├── test_users.py
        │   ├── test_posts.py
        │   ├── test_stats.py
        │   ├── test_cors.py
        │   └── test_error_handling.py
        └── reports/              # Generated test reports
```

## Installation

1. **Navigate to the test directory:**

   ```bash
   cd 25-AI-vibe-coding-tests/result/test
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Using the Test Runner Script

The `run_tests.py` script provides a convenient way to run tests with various options:

```bash
# Run ALL tests (unit + integration)
python run_tests.py

# Run only UNIT tests
python run_tests.py --unit
# or
python run_tests.py -u

# Run only INTEGRATION tests
python run_tests.py --integration
# or
python run_tests.py -i

# Run with verbose output
python run_tests.py --verbose
# or
python run_tests.py -v

# Run without generating Markdown report
python run_tests.py --no-report
```

### Using pytest Directly

You can also use pytest directly for more control:

```bash
# Run all tests
pytest unit integration -v

# Run only unit tests
pytest unit -v -m unit

# Run only integration tests
pytest integration -v -m integration

# Run tests for a specific feature (using markers)
pytest -m users -v        # User-related tests
pytest -m posts -v        # Post-related tests
pytest -m stats -v        # Statistics tests
pytest -m health -v       # Health check tests

# Run a specific test file
pytest integration/test_users.py -v

# Run a specific test class
pytest integration/test_users.py::TestCreateUser -v

# Run a specific test method
pytest integration/test_users.py::TestCreateUser::test_create_user_with_valid_data -v
```

## Test Categories

### Unit Tests (`unit/`)

Unit tests validate business logic without HTTP calls or database access:

| Test File | Description |
|-----------|-------------|
| `test_user_validation.py` | User model serialization, password handling, validation logic |
| `test_post_validation.py` | Post model serialization, default values, validation logic |
| `test_response_shapes.py` | API response structure validation |

### Integration Tests (`integration/`)

Integration tests validate API endpoints with Flask test client and in-memory SQLite database:

| Test File | Description |
|-----------|-------------|
| `test_health.py` | Health endpoint (HLTH-01) |
| `test_users.py` | User CRUD operations (USR-01 to USR-04) |
| `test_posts.py` | Post CRUD operations (PST-01 to PST-06) |
| `test_stats.py` | Statistics endpoint (STS-01) |
| `test_cors.py` | CORS configuration (NFR-02) |
| `test_error_handling.py` | Error handling and JSON responses (NFR-01, NFR-03) |

### Test Markers

Tests are tagged with markers for selective execution:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.health` - Health check tests
- `@pytest.mark.users` - User management tests
- `@pytest.mark.posts` - Post management tests
- `@pytest.mark.stats` - Statistics tests

## Test Reports

Test reports are automatically generated in the `reports/` directory:

### Report Locations

```
reports/
├── test_results_all_YYYYMMDD_HHMMSS.md      # All tests report
├── test_results_all_YYYYMMDD_HHMMSS.html    # HTML report
├── test_results_unit_YYYYMMDD_HHMMSS.md     # Unit tests report
├── test_results_unit_YYYYMMDD_HHMMSS.html   # HTML report
├── test_results_integration_YYYYMMDD_HHMMSS.md   # Integration tests report
└── test_results_integration_YYYYMMDD_HHMMSS.html # HTML report
```

### Markdown Report Contents

Each Markdown report includes:

- **Summary**: Test type, timestamp, overall status, total/passed/failed counts
- **Test Configuration**: Framework and HTML report reference
- **Console Output**: Full pytest output with test results
- **Failed Tests Analysis**: Details on any failures (if applicable)

### Viewing Reports

- **Markdown**: Open `.md` files in any text editor or Markdown viewer
- **HTML**: Open `.html` files in a web browser for interactive viewing

## Test Cases Coverage

### User Stories Coverage

| Story ID | Description | Test Type | Test File |
|----------|-------------|-----------|-----------|
| HLTH-01 | Health check | Integration | `test_health.py` |
| USR-01 | Create user | Both | `test_users.py`, `test_user_validation.py` |
| USR-02 | List users | Integration | `test_users.py` |
| USR-03 | View user by ID | Integration | `test_users.py` |
| USR-04 | Delete user (cascade) | Integration | `test_users.py` |
| PST-01 | Create post | Both | `test_posts.py`, `test_post_validation.py` |
| PST-02 | List all posts | Integration | `test_posts.py` |
| PST-03 | List published posts | Integration | `test_posts.py` |
| PST-04 | View post by ID | Integration | `test_posts.py` |
| PST-05 | Update post | Integration | `test_posts.py` |
| PST-06 | Delete post | Integration | `test_posts.py` |
| STS-01 | View statistics | Integration | `test_stats.py` |
| NFR-01 | JSON responses | Integration | `test_error_handling.py` |
| NFR-02 | CORS enabled | Integration | `test_cors.py` |

### Test Cases Matrix

| Test Case ID | Description | Test Method |
|--------------|-------------|-------------|
| TC-HLTH-01 | Health check returns OK | `test_health_check_returns_200` |
| TC-USR-01 | Create user with valid data | `test_create_user_with_valid_data` |
| TC-USR-02 | Reject missing fields | `test_create_user_missing_*` |
| TC-USR-03 | Reject duplicate username | `test_create_user_duplicate_username` |
| TC-USR-04 | Reject duplicate email | `test_create_user_duplicate_email` |
| TC-USR-05 | List users returns array | `test_list_users_returns_array` |
| TC-USR-06 | List users empty | `test_list_users_empty_database` |
| TC-USR-07 | Get user by valid ID | `test_get_user_by_valid_id` |
| TC-USR-08 | Get user not found | `test_get_user_not_found` |
| TC-USR-09 | Delete user success | `test_delete_user_success` |
| TC-USR-10 | Delete user cascades posts | `test_delete_user_cascade_posts` |
| TC-USR-11 | Delete user not found | `test_delete_user_not_found` |
| TC-PST-01 | Create post valid data | `test_create_post_with_valid_data` |
| TC-PST-02 | Create post missing fields | `test_create_post_missing_*` |
| TC-PST-03 | Create post user not found | `test_create_post_user_not_found` |
| TC-PST-04 | List posts ordered | `test_list_posts_ordered_by_created_at_desc` |
| TC-PST-05 | List posts empty | `test_list_posts_empty_database` |
| TC-PST-06 | List published only | `test_list_published_posts_only` |
| TC-PST-07 | List published empty | `test_list_published_posts_empty` |
| TC-PST-08 | Get post by valid ID | `test_get_post_by_valid_id` |
| TC-PST-09 | Get post not found | `test_get_post_not_found` |
| TC-PST-10 | Update post publish | `test_update_post_publish` |
| TC-PST-11 | Update post fields | `test_update_post_title_and_content` |
| TC-PST-12 | Update post not found | `test_update_post_not_found` |
| TC-PST-13 | Delete post success | `test_delete_post_success` |
| TC-PST-14 | Delete post not found | `test_delete_post_not_found` |
| TC-STS-01 | Stats returns zeros | `test_stats_empty_database` |
| TC-STS-02 | Stats reflect data | `test_stats_reflect_created_data` |
| TC-STS-03 | Stats cascade impact | `test_stats_cascade_impact` |

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'app'**
   
   Ensure you're running tests from the correct directory and the source path is configured in `conftest.py`.

2. **Database connection errors**
   
   Tests use SQLite in-memory database. No MySQL connection is required for testing.

3. **Import errors for Flask dependencies**
   
   Install all requirements: `pip install -r requirements.txt`

4. **pytest not found**
   
   Ensure pytest is installed: `pip install pytest`

### Getting Help

- Review the test configuration in `pytest.ini`
- Check the fixtures in `conftest.py`
- Examine individual test files for specific test implementations

---

*Last updated: March 2026*
