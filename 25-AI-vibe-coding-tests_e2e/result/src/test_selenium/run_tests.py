#!/usr/bin/env python
"""
Runner de Tests Selenium - Application Blog Simple
Script principal pour exécuter les tests et générer les rapports

Usage:
    python run_tests.py                           # Exécute tous les tests
    python run_tests.py --feature Users           # Tests de la feature Users
    python run_tests.py --feature Posts --priority Haute  # Posts priorité haute
    python run_tests.py --test-id TC-001-01       # Test spécifique
    python run_tests.py --help                    # Aide
"""
import os
import sys
import argparse
import subprocess
from datetime import datetime
import re


# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(SCRIPT_DIR, "reports")

# Mapping des features aux fichiers de test
FEATURE_FILES = {
    "users": "test_users.py",
    "posts": "test_posts.py",
    "statistics": "test_statistics.py"
}

# Mapping des priorités
PRIORITIES = ["haute", "moyenne", "basse"]


# =============================================================================
# Fonctions utilitaires
# =============================================================================

def ensure_reports_dir():
    """Crée le répertoire des rapports s'il n'existe pas"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)


def get_timestamp():
    """Retourne un timestamp formaté"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_report_name(feature=None, priority=None, test_id=None):
    """Génère le nom du rapport basé sur les filtres"""
    timestamp = get_timestamp()
    
    if test_id:
        return f"test_{test_id}_{timestamp}.md"
    elif feature and priority:
        return f"{feature}_{priority}_{timestamp}.md"
    elif feature:
        return f"{feature}_{timestamp}.md"
    else:
        return f"all_tests_{timestamp}.md"


def build_pytest_command(feature=None, priority=None, test_id=None, verbose=True):
    """Construit la commande pytest avec les filtres appropriés"""
    cmd = [sys.executable, "-m", "pytest"]
    
    # Verbose output
    if verbose:
        cmd.append("-v")
    
    # Output en temps réel
    cmd.append("-s")
    
    # Pas de capture pour voir l'output
    cmd.append("--tb=short")
    
    # Filtrer par feature (fichier de test)
    if feature:
        feature_lower = feature.lower()
        if feature_lower in FEATURE_FILES:
            cmd.append(FEATURE_FILES[feature_lower])
        else:
            print(f"⚠ Feature inconnue: {feature}")
            print(f"  Features disponibles: {', '.join(FEATURE_FILES.keys())}")
            return None
    
    # Filtrer par priorité (marqueur pytest)
    if priority:
        priority_lower = priority.lower()
        if priority_lower in PRIORITIES:
            cmd.extend(["-m", priority_lower])
        else:
            print(f"⚠ Priorité inconnue: {priority}")
            print(f"  Priorités disponibles: {', '.join(PRIORITIES)}")
            return None
    
    # Filtrer par test ID
    if test_id:
        # Convertir TC-001-01 en TC_001_01 pour correspondre au nom de fonction
        test_pattern = test_id.replace("-", "_")
        cmd.extend(["-k", test_pattern])
    
    return cmd


def run_tests(feature=None, priority=None, test_id=None, verbose=True):
    """Exécute les tests et capture les résultats"""
    ensure_reports_dir()
    
    # Construire la commande
    cmd = build_pytest_command(feature, priority, test_id, verbose)
    if cmd is None:
        return None, None, 1
    
    print("\n" + "="*70)
    print("🚀 EXÉCUTION DES TESTS SELENIUM")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if feature:
        print(f"📁 Feature: {feature}")
    if priority:
        print(f"⚡ Priorité: {priority}")
    if test_id:
        print(f"🎯 Test ID: {test_id}")
    print(f"📝 Commande: {' '.join(cmd)}")
    print("="*70 + "\n")
    
    # Changer vers le répertoire des tests
    original_dir = os.getcwd()
    os.chdir(SCRIPT_DIR)
    
    try:
        # Exécuter pytest
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True,
            env={**os.environ, "PYTHONPATH": SCRIPT_DIR}
        )
        
        return None, None, result.returncode
        
    finally:
        os.chdir(original_dir)


def run_tests_with_report(feature=None, priority=None, test_id=None, verbose=True):
    """Exécute les tests et génère un rapport Markdown"""
    ensure_reports_dir()
    
    # Construire la commande
    cmd = build_pytest_command(feature, priority, test_id, verbose)
    if cmd is None:
        return 1
    
    # Nom du rapport
    report_name = generate_report_name(feature, priority, test_id)
    report_path = os.path.join(REPORTS_DIR, report_name)
    
    print("\n" + "="*70)
    print("🚀 EXÉCUTION DES TESTS SELENIUM")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if feature:
        print(f"📁 Feature: {feature}")
    if priority:
        print(f"⚡ Priorité: {priority}")
    if test_id:
        print(f"🎯 Test ID: {test_id}")
    print(f"📝 Rapport: {report_path}")
    print("="*70 + "\n")
    
    # Changer vers le répertoire des tests
    original_dir = os.getcwd()
    os.chdir(SCRIPT_DIR)
    
    start_time = datetime.now()
    
    try:
        # Exécuter pytest avec capture de sortie pour le rapport
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": SCRIPT_DIR}
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Afficher la sortie en temps réel
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        # Générer le rapport
        generate_markdown_report(
            report_path,
            result.stdout,
            result.stderr,
            result.returncode,
            duration,
            feature,
            priority,
            test_id
        )
        
        print("\n" + "="*70)
        print(f"📊 RAPPORT GÉNÉRÉ: {report_path}")
        print("="*70)
        
        return result.returncode
        
    finally:
        os.chdir(original_dir)


def generate_markdown_report(report_path, stdout, stderr, return_code, duration, 
                            feature=None, priority=None, test_id=None):
    """Génère un rapport Markdown des résultats de test"""
    
    # Parser les résultats de pytest
    passed, failed, skipped, errors = parse_pytest_output(stdout)
    total = passed + failed + skipped + errors
    
    # Déterminer le statut global
    if return_code == 0:
        status = "✅ SUCCÈS"
        status_emoji = "🟢"
    else:
        status = "❌ ÉCHEC"
        status_emoji = "🔴"
    
    # Générer le contenu du rapport
    content = f"""# Rapport de Tests Selenium

## 📋 Informations Générales

| Élément | Valeur |
|---------|--------|
| **Date d'exécution** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **Statut global** | {status} |
| **Durée totale** | {duration:.2f} secondes |
| **Feature** | {feature or 'Toutes'} |
| **Priorité** | {priority or 'Toutes'} |
| **Test ID** | {test_id or 'Tous'} |

---

## 📊 Résumé des Résultats

| Métrique | Valeur |
|----------|--------|
| {status_emoji} **Total** | {total} |
| 🟢 **Passés** | {passed} |
| 🔴 **Échoués** | {failed} |
| 🟡 **Ignorés** | {skipped} |
| ⚠️ **Erreurs** | {errors} |
| **Taux de réussite** | {(passed/total*100) if total > 0 else 0:.1f}% |

---

## 📝 Détails de l'Exécution

### Sortie Standard

```
{stdout if stdout else 'Aucune sortie'}
```

"""

    if stderr:
        content += f"""### Erreurs

```
{stderr}
```

"""

    # Ajouter les tests échoués si présents
    failed_tests = extract_failed_tests(stdout)
    if failed_tests:
        content += """### Tests Échoués

| Test | Raison |
|------|--------|
"""
        for test, reason in failed_tests:
            content += f"| {test} | {reason[:100]}... |\n"
        content += "\n"

    content += f"""---

## 🔧 Configuration

- **Navigateur**: Chrome (par défaut)
- **Mode Headless**: {'Oui' if os.environ.get('SELENIUM_HEADLESS', 'false').lower() == 'true' else 'Non'}
- **Timeout par défaut**: 10 secondes

---

*Rapport généré automatiquement par le runner de tests Selenium*
"""

    # Écrire le rapport
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)


def parse_pytest_output(output):
    """Parse la sortie de pytest pour extraire les statistiques"""
    passed = failed = skipped = errors = 0
    
    if not output:
        return 0, 0, 0, 0
    
    # Chercher la ligne de résumé (ex: "5 passed, 2 failed, 1 skipped")
    summary_pattern = r'(\d+)\s+(passed|failed|skipped|error)'
    matches = re.findall(summary_pattern, output.lower())
    
    for count, status in matches:
        count = int(count)
        if status == 'passed':
            passed = count
        elif status == 'failed':
            failed = count
        elif status == 'skipped':
            skipped = count
        elif status == 'error':
            errors = count
    
    return passed, failed, skipped, errors


def extract_failed_tests(output):
    """Extrait les tests échoués et leurs raisons"""
    failed_tests = []
    
    if not output:
        return failed_tests
    
    # Pattern pour trouver les tests échoués
    # FAILED test_users.py::TestUsers::test_xxx - AssertionError: ...
    pattern = r'FAILED\s+(\S+)\s*-?\s*(.*?)(?=\n|$)'
    matches = re.findall(pattern, output)
    
    for test_name, reason in matches:
        # Nettoyer le nom du test
        test_name = test_name.split("::")[-1] if "::" in test_name else test_name
        failed_tests.append((test_name, reason.strip()))
    
    return failed_tests


def list_tests():
    """Liste tous les tests disponibles"""
    print("\n" + "="*70)
    print("📋 TESTS DISPONIBLES")
    print("="*70)
    
    for feature, file in FEATURE_FILES.items():
        print(f"\n📁 {feature.upper()} ({file})")
        print("-" * 40)
        
        file_path = os.path.join(SCRIPT_DIR, file)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Trouver tous les tests
            test_pattern = r'def\s+(test_\w+)'
            tests = re.findall(test_pattern, content)
            
            for test in tests:
                # Extraire les infos du nom
                parts = test.split('_')
                if len(parts) >= 4:
                    priority = parts[2]
                    test_id = '-'.join(parts[3:]).replace('_', '-')
                    print(f"  • {test_id} ({priority})")
        else:
            print(f"  ⚠ Fichier non trouvé")
    
    print("\n")


# =============================================================================
# Point d'entrée principal
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Runner de Tests Selenium - Application Blog Simple",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python run_tests.py                              # Tous les tests
  python run_tests.py --feature Users              # Tests Users
  python run_tests.py --feature Posts --priority Haute    # Posts haute priorité
  python run_tests.py --test-id TC-001-01          # Test spécifique
  python run_tests.py --list                       # Lister les tests
  python run_tests.py --no-report                  # Sans génération de rapport
        """
    )
    
    parser.add_argument(
        '--feature', '-f',
        choices=['Users', 'Posts', 'Statistics', 'users', 'posts', 'statistics'],
        help="Feature à tester (Users, Posts, Statistics)"
    )
    
    parser.add_argument(
        '--priority', '-p',
        choices=['Haute', 'Moyenne', 'Basse', 'haute', 'moyenne', 'basse'],
        help="Priorité des tests (Haute, Moyenne, Basse)"
    )
    
    parser.add_argument(
        '--test-id', '-t',
        help="ID du test spécifique (ex: TC-001-01)"
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help="Lister tous les tests disponibles"
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help="Ne pas générer de rapport Markdown"
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help="Mode silencieux (moins de sortie)"
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help="Exécuter en mode headless (sans interface graphique)"
    )
    
    parser.add_argument(
        '--browser', '-b',
        choices=['chrome', 'edge', 'firefox'],
        default='chrome',
        help="Navigateur à utiliser (défaut: chrome)"
    )
    
    args = parser.parse_args()
    
    # Configuration de l'environnement
    if args.headless:
        os.environ['SELENIUM_HEADLESS'] = 'true'
    
    os.environ['SELENIUM_BROWSER'] = args.browser
    
    # Lister les tests
    if args.list:
        list_tests()
        return 0
    
    # Normaliser les arguments
    feature = args.feature.capitalize() if args.feature else None
    priority = args.priority.capitalize() if args.priority else None
    
    # Exécuter les tests
    if args.no_report:
        _, _, return_code = run_tests(
            feature=feature,
            priority=priority,
            test_id=args.test_id,
            verbose=not args.quiet
        )
    else:
        return_code = run_tests_with_report(
            feature=feature,
            priority=priority,
            test_id=args.test_id,
            verbose=not args.quiet
        )
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())
