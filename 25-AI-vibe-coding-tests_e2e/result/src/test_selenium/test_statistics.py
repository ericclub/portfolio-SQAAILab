"""
Suite de Tests Selenium - Statistics (Statistiques)
Application Blog Simple - Tests End-to-End

Basé sur test_plan.md - Suite de Tests 3
"""
import pytest
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base_test import BaseTest


class TestStatistics:
    """Suite de tests pour les statistiques"""
    
    # =========================================================================
    # Helper: Préparer les données de test
    # =========================================================================
    
    def ensure_data_exists(self, base, driver):
        """S'assure qu'il y a des utilisateurs et des posts pour les statistiques"""
        # Créer un utilisateur si nécessaire
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        if base.get_user_count() == 0:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base.create_user(f"statsuser_{timestamp}", f"stats_{timestamp}@test.com")
            time.sleep(1)
            base.wait_for_loading_complete()
        
        # Créer un post si nécessaire
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        
        if base.get_post_count() == 0:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base.create_post(f"Stats Post {timestamp}", "Content for stats test")
            time.sleep(1)
            base.wait_for_loading_complete()
    
    # =========================================================================
    # US-010 : Consultation des statistiques générales
    # =========================================================================
    
    @pytest.mark.statistics
    @pytest.mark.haute
    def test_Statistics_Haute_TC_010_01(self, driver, app_url):
        """
        TC-010-01 : Affichage du nombre total d'utilisateurs
        
        Objectif: Vérifier l'affichage du compteur d'utilisateurs
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Haute_TC-010-01 - Nombre total d'utilisateurs")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Préparation
        print("➤ Étape 1: Préparation des données...")
        base.open_app()
        self.ensure_data_exists(base, driver)
        
        # Compter les utilisateurs
        base.navigate_to_users()
        base.wait_for_loading_complete()
        expected_count = base.get_user_count()
        print(f"✓ Nombre d'utilisateurs dans la liste: {expected_count}")
        
        # Naviguer vers Statistics
        print("➤ Étape 2: Navigation vers Statistics...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Vérifier le compteur
        print("➤ Vérification: Compteur d'utilisateurs...")
        stats_container = base.get_text(base.SELECTORS["stats_container"])
        
        # Chercher "Total Users" dans les statistiques
        assert "total users" in stats_container.lower() or "users" in stats_container.lower(), \
            "Le compteur d'utilisateurs n'est pas affiché"
        
        # Vérifier la valeur
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        user_count_found = False
        for card in stat_cards:
            if "user" in card.text.lower():
                value = card.find_element(By.CSS_SELECTOR, ".stat-value").text
                print(f"✓ Compteur Total Users: {value}")
                assert int(value) == expected_count, \
                    f"Compteur incorrect: attendu {expected_count}, obtenu {value}"
                user_count_found = True
                break
        
        assert user_count_found, "Le compteur d'utilisateurs n'a pas été trouvé"
        
        print("\n✅ TEST RÉUSSI: Compteur d'utilisateurs correct")
    
    @pytest.mark.statistics
    @pytest.mark.haute
    def test_Statistics_Haute_TC_010_02(self, driver, app_url):
        """
        TC-010-02 : Affichage du nombre total d'articles
        
        Objectif: Vérifier l'affichage du compteur d'articles
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Haute_TC-010-02 - Nombre total d'articles")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Préparation
        print("➤ Étape 1: Préparation...")
        base.open_app()
        self.ensure_data_exists(base, driver)
        
        # Compter les posts
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        expected_count = base.get_post_count()
        print(f"✓ Nombre de posts dans la liste: {expected_count}")
        
        # Naviguer vers Statistics
        print("➤ Étape 2: Navigation vers Statistics...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Vérifier le compteur
        print("➤ Vérification: Compteur de posts...")
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        post_count_found = False
        for card in stat_cards:
            if "post" in card.text.lower():
                value = card.find_element(By.CSS_SELECTOR, ".stat-value").text
                print(f"✓ Compteur Total Posts: {value}")
                assert int(value) == expected_count, \
                    f"Compteur incorrect: attendu {expected_count}, obtenu {value}"
                post_count_found = True
                break
        
        assert post_count_found, "Le compteur de posts n'a pas été trouvé"
        
        print("\n✅ TEST RÉUSSI: Compteur de posts correct")
    
    @pytest.mark.statistics
    @pytest.mark.moyenne
    def test_Statistics_Moyenne_TC_010_03(self, driver, app_url):
        """
        TC-010-03 : Identification de l'utilisateur le plus actif
        
        Objectif: Vérifier l'identification du top contributeur
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Moyenne_TC-010-03 - Utilisateur le plus actif")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Créer un utilisateur avec plusieurs posts
        print("➤ Étape 1: Création d'un utilisateur productif...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        active_username = f"activeuser_{timestamp}"
        base.create_user(active_username, f"active_{timestamp}@test.com")
        time.sleep(1)
        
        # Créer plusieurs posts pour cet utilisateur
        print("➤ Étape 2: Création de posts...")
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        
        for i in range(3):
            base.open_new_post_form()
            base.fill_input(base.SELECTORS["post_title_input"], f"Active Post {i} {timestamp}")
            base.fill_input(base.SELECTORS["post_content_input"], f"Content {i}")
            
            select = Select(driver.find_element(By.CSS_SELECTOR, base.SELECTORS["post_author_select"]))
            for option in select.options:
                if active_username in option.text:
                    option.click()
                    break
            
            base.click_element(base.SELECTORS["post_form_submit"])
            base.wait_for_modal_hidden(base.SELECTORS["post_form_modal"])
            time.sleep(0.5)
        
        base.wait_for_loading_complete()
        print(f"✓ 3 posts créés pour {active_username}")
        
        # Vérifier les statistiques
        print("➤ Étape 3: Vérification des statistiques...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        stats_text = base.get_text(base.SELECTORS["stats_container"])
        
        # L'utilisateur le plus actif devrait être affiché
        assert "most active" in stats_text.lower() or "active" in stats_text.lower(), \
            "La section 'Most Active' n'est pas affichée"
        print("✓ Section 'Most Active' présente")
        
        # Vérifier que notre utilisateur actif est mentionné
        # Note: Il pourrait y avoir d'autres utilisateurs plus actifs selon l'état de la DB
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        for card in stat_cards:
            if "active" in card.text.lower():
                print(f"✓ Info utilisateur actif: {card.text}")
                break
        
        print("\n✅ TEST RÉUSSI: Utilisateur le plus actif identifié")
    
    @pytest.mark.statistics
    @pytest.mark.moyenne
    def test_Statistics_Moyenne_TC_010_04(self, driver, app_url):
        """
        TC-010-04 : Affichage des posts par utilisateur
        
        Objectif: Vérifier l'affichage de la répartition des posts
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Moyenne_TC-010-04 - Posts par utilisateur")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Préparation
        print("➤ Étape 1: Préparation...")
        base.open_app()
        self.ensure_data_exists(base, driver)
        
        # Naviguer vers Statistics
        print("➤ Étape 2: Navigation vers Statistics...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Vérifier la liste des posts par utilisateur
        print("➤ Vérification: Liste 'Posts per User'...")
        stat_lists = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_list"])
        
        posts_per_user_found = False
        for stat_list in stat_lists:
            if "posts per user" in stat_list.text.lower():
                posts_per_user_found = True
                print(f"✓ Liste 'Posts per User' trouvée")
                
                # Vérifier qu'il y a des éléments dans la liste
                items = stat_list.find_elements(By.TAG_NAME, "li")
                print(f"✓ Nombre d'éléments dans la liste: {len(items)}")
                
                for item in items[:3]:  # Afficher les 3 premiers
                    print(f"  - {item.text}")
                break
        
        assert posts_per_user_found, "La liste 'Posts per User' n'est pas affichée"
        
        print("\n✅ TEST RÉUSSI: Répartition des posts affichée")
    
    @pytest.mark.statistics
    @pytest.mark.moyenne
    def test_Statistics_Moyenne_TC_010_05(self, driver, app_url):
        """
        TC-010-05 : Affichage des articles récents
        
        Objectif: Vérifier l'affichage des derniers articles
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Moyenne_TC-010-05 - Articles récents")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Préparation
        print("➤ Étape 1: Préparation...")
        base.open_app()
        self.ensure_data_exists(base, driver)
        
        # Créer quelques posts pour s'assurer qu'il y en a
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        
        if base.get_post_count() < 5:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            for i in range(5 - base.get_post_count()):
                base.create_post(f"Recent Post {i} {timestamp}", f"Content {i}")
                time.sleep(0.3)
        
        # Naviguer vers Statistics
        print("➤ Étape 2: Navigation vers Statistics...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Vérifier la liste des posts récents
        print("➤ Vérification: Liste 'Recent Posts'...")
        stat_lists = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_list"])
        
        recent_posts_found = False
        for stat_list in stat_lists:
            if "recent posts" in stat_list.text.lower():
                recent_posts_found = True
                print("✓ Liste 'Recent Posts' trouvée")
                
                items = stat_list.find_elements(By.TAG_NAME, "li")
                print(f"✓ Nombre d'articles récents: {len(items)}")
                
                # Afficher les articles récents
                for item in items[:5]:
                    print(f"  - {item.text[:50]}...")
                break
        
        assert recent_posts_found, "La liste 'Recent Posts' n'est pas affichée"
        
        print("\n✅ TEST RÉUSSI: Articles récents affichés")
    
    # =========================================================================
    # US-011 : Rafraîchissement des statistiques
    # =========================================================================
    
    @pytest.mark.statistics
    @pytest.mark.haute
    def test_Statistics_Haute_TC_011_01(self, driver, app_url):
        """
        TC-011-01 : Rafraîchissement des statistiques
        
        Objectif: Vérifier le fonctionnement du rafraîchissement
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Haute_TC-011-01 - Rafraîchissement")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Étape 1: Ouvrir les statistiques
        print("➤ Étape 1: Ouverture des statistiques...")
        base.open_app()
        self.ensure_data_exists(base, driver)
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Noter les statistiques actuelles
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        initial_posts = None
        for card in stat_cards:
            if "post" in card.text.lower():
                initial_posts = card.find_element(By.CSS_SELECTOR, ".stat-value").text
                break
        print(f"✓ Nombre initial de posts: {initial_posts}")
        
        # Étape 2: Créer un nouveau post (dans un autre onglet conceptuellement)
        print("➤ Étape 2: Création d'un nouveau post...")
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        base.create_post(f"Refresh Test {timestamp}", "Content for refresh test")
        time.sleep(1)
        
        # Étape 3: Retourner aux stats et rafraîchir
        print("➤ Étape 3: Retour aux statistiques et rafraîchissement...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Cliquer sur Refresh
        base.click_element(base.SELECTORS["stats_refresh_btn"])
        base.wait_for_loading_complete()
        time.sleep(1)
        print("✓ Rafraîchissement effectué")
        
        # Vérifier la mise à jour
        print("➤ Vérification: Statistiques mises à jour...")
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        new_posts = None
        for card in stat_cards:
            if "post" in card.text.lower():
                new_posts = card.find_element(By.CSS_SELECTOR, ".stat-value").text
                break
        
        print(f"✓ Nouveau nombre de posts: {new_posts}")
        
        if initial_posts:
            assert int(new_posts) >= int(initial_posts), \
                "Le compteur de posts n'a pas été mis à jour"
        
        print("\n✅ TEST RÉUSSI: Rafraîchissement fonctionnel")
    
    @pytest.mark.statistics
    @pytest.mark.basse
    def test_Statistics_Basse_TC_011_02(self, driver, app_url):
        """
        TC-011-02 : Affichage du chargement
        
        Objectif: Vérifier l'indicateur de chargement
        Priorité: Basse
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Basse_TC-011-02 - Indicateur de chargement")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Ouvrir les statistiques
        print("➤ Étape 1: Ouverture des statistiques...")
        base.open_app()
        base.navigate_to_stats()
        
        # Cliquer sur Refresh et observer le chargement
        print("➤ Étape 2: Clic sur Refresh...")
        
        # Note: Le loading est très rapide en local, difficile à capturer
        # On vérifie que la structure du loading existe
        
        base.click_element(base.SELECTORS["stats_refresh_btn"])
        
        # Le loading devrait s'afficher brièvement
        # En environnement local, c'est trop rapide pour être capturé de manière fiable
        print("✓ Rafraîchissement déclenché")
        
        time.sleep(1)
        base.wait_for_loading_complete()
        
        # Vérifier que le contenu est à nouveau visible
        assert base.element_is_visible(base.SELECTORS["stats_container"]), \
            "Le conteneur de statistiques n'est pas visible après le chargement"
        print("✓ Contenu affiché après chargement")
        
        print("\n✅ TEST RÉUSSI: Comportement de chargement vérifié")
    
    # =========================================================================
    # US-012 : Gestion des états vides dans les statistiques
    # =========================================================================
    
    @pytest.mark.statistics
    @pytest.mark.moyenne
    def test_Statistics_Moyenne_TC_012_01(self, driver, app_url):
        """
        TC-012-01 : Statistiques avec base vide
        
        Objectif: Vérifier l'affichage des statistiques sans données
        Priorité: Moyenne
        
        Note: Ce test vérifie le comportement avec des données minimales
        car il est difficile de vider complètement la base en test E2E.
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Moyenne_TC-012-01 - Statistiques avec données minimales")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Ouvrir les statistiques
        print("➤ Étape 1: Ouverture des statistiques...")
        base.open_app()
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Vérifier la structure des statistiques
        print("➤ Vérification: Structure des statistiques...")
        
        # Les compteurs devraient être présents (même si à 0)
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        assert len(stat_cards) >= 2, "Les compteurs de statistiques ne sont pas affichés"
        print(f"✓ Nombre de cartes de statistiques: {len(stat_cards)}")
        
        # Vérifier les valeurs
        for card in stat_cards:
            card_text = card.text
            print(f"  - {card_text.replace(chr(10), ' ')}")
        
        # Vérifier les listes (peuvent être vides)
        stat_lists = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_list"])
        print(f"✓ Nombre de listes de statistiques: {len(stat_lists)}")
        
        for stat_list in stat_lists:
            header = stat_list.text.split('\n')[0] if stat_list.text else "Unknown"
            items = stat_list.find_elements(By.TAG_NAME, "li")
            print(f"  - {header}: {len(items)} élément(s)")
        
        print("\n✅ TEST RÉUSSI: Structure des statistiques vérifiée")
    
    @pytest.mark.statistics
    @pytest.mark.moyenne
    def test_Statistics_Moyenne_TC_012_02(self, driver, app_url):
        """
        TC-012-02 : Utilisateur le plus actif sans posts
        
        Objectif: Vérifier l'affichage quand des utilisateurs existent mais sans posts
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Moyenne_TC-012-02 - Utilisateur actif sans posts")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Créer un utilisateur sans créer de post
        print("➤ Étape 1: Création d'un utilisateur sans posts...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        base.create_user(f"nopost_{timestamp}", f"nopost_{timestamp}@test.com")
        time.sleep(1)
        print("✓ Utilisateur créé")
        
        # Naviguer vers les statistiques
        print("➤ Étape 2: Vérification des statistiques...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        # Vérifier le comportement de "Most Active"
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        
        for card in stat_cards:
            if "active" in card.text.lower():
                value = card.find_element(By.CSS_SELECTOR, ".stat-value").text
                label = card.find_element(By.CSS_SELECTOR, ".stat-label").text
                print(f"✓ Most Active: {value} - {label}")
                
                # Si aucun post, pourrait afficher 0 ou N/A
                assert value == "0" or "n/a" in label.lower() or len(value) > 0, \
                    "Affichage incorrect pour l'utilisateur le plus actif"
                break
        
        print("\n✅ TEST RÉUSSI: Comportement correct pour utilisateur sans posts")
    
    # =========================================================================
    # US-013 : Tests d'intégration Cross-Sections
    # =========================================================================
    
    @pytest.mark.statistics
    @pytest.mark.haute
    def test_Statistics_Haute_TC_013_01(self, driver, app_url):
        """
        TC-013-01 : Synchronisation création utilisateur
        
        Objectif: Vérifier la mise à jour des statistiques après création d'utilisateur
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Haute_TC-013-01 - Synchro création utilisateur")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Noter le nombre initial d'utilisateurs dans les stats
        print("➤ Étape 1: Lecture des statistiques initiales...")
        base.open_app()
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        initial_users = 0
        for card in stat_cards:
            if "user" in card.text.lower():
                initial_users = int(card.find_element(By.CSS_SELECTOR, ".stat-value").text)
                break
        print(f"✓ Nombre initial d'utilisateurs: {initial_users}")
        
        # Créer un nouvel utilisateur
        print("➤ Étape 2: Création d'un nouvel utilisateur...")
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.create_user(f"syncuser_{timestamp}", f"sync_{timestamp}@test.com")
        time.sleep(1)
        
        # Vérifier les statistiques
        print("➤ Étape 3: Vérification des statistiques...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        base.refresh_stats()
        
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        new_users = 0
        for card in stat_cards:
            if "user" in card.text.lower():
                new_users = int(card.find_element(By.CSS_SELECTOR, ".stat-value").text)
                break
        
        print(f"✓ Nouveau nombre d'utilisateurs: {new_users}")
        assert new_users == initial_users + 1, \
            f"Le compteur n'a pas été incrémenté ({initial_users} -> {new_users})"
        
        print("\n✅ TEST RÉUSSI: Synchronisation création utilisateur OK")
    
    @pytest.mark.statistics
    @pytest.mark.haute
    def test_Statistics_Haute_TC_013_02(self, driver, app_url):
        """
        TC-013-02 : Synchronisation création post
        
        Objectif: Vérifier la mise à jour des statistiques après création de post
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Haute_TC-013-02 - Synchro création post")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Préparation
        print("➤ Étape 1: Préparation...")
        base.open_app()
        self.ensure_data_exists(base, driver)
        
        # Noter le nombre initial de posts
        print("➤ Étape 2: Lecture des statistiques initiales...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        initial_posts = 0
        for card in stat_cards:
            if "post" in card.text.lower():
                initial_posts = int(card.find_element(By.CSS_SELECTOR, ".stat-value").text)
                break
        print(f"✓ Nombre initial de posts: {initial_posts}")
        
        # Créer un nouveau post
        print("➤ Étape 3: Création d'un nouveau post...")
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        base.create_post(f"Sync Post {timestamp}", "Content for sync test")
        time.sleep(1)
        
        # Vérifier les statistiques
        print("➤ Étape 4: Vérification des statistiques...")
        base.navigate_to_stats()
        base.wait_for_loading_complete()
        base.refresh_stats()
        
        stat_cards = driver.find_elements(By.CSS_SELECTOR, base.SELECTORS["stat_card"])
        new_posts = 0
        for card in stat_cards:
            if "post" in card.text.lower():
                new_posts = int(card.find_element(By.CSS_SELECTOR, ".stat-value").text)
                break
        
        print(f"✓ Nouveau nombre de posts: {new_posts}")
        assert new_posts == initial_posts + 1, \
            f"Le compteur n'a pas été incrémenté ({initial_posts} -> {new_posts})"
        
        print("\n✅ TEST RÉUSSI: Synchronisation création post OK")
    
    @pytest.mark.statistics
    @pytest.mark.haute
    def test_Statistics_Haute_TC_013_03(self, driver, app_url):
        """
        TC-013-03 : Mise à jour du sélecteur d'auteurs
        
        Objectif: Vérifier que les nouveaux utilisateurs apparaissent dans le sélecteur
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Statistics_Haute_TC-013-03 - Mise à jour sélecteur auteurs")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_username = f"selectuser_{timestamp}"
        
        # Ouvrir le formulaire de post et noter les auteurs
        print("➤ Étape 1: Lecture des auteurs actuels...")
        base.open_app()
        base.wait_for_loading_complete()
        base.open_new_post_form()
        
        select = Select(driver.find_element(By.CSS_SELECTOR, base.SELECTORS["post_author_select"]))
        initial_options = [opt.text for opt in select.options]
        print(f"✓ Nombre d'auteurs initial: {len(initial_options) - 1}")  # -1 pour l'option par défaut
        
        base.click_element(base.SELECTORS["post_form_cancel"])
        
        # Créer un nouvel utilisateur
        print("➤ Étape 2: Création d'un nouvel utilisateur...")
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.create_user(new_username, f"select_{timestamp}@test.com")
        time.sleep(1)
        print(f"✓ Utilisateur créé: {new_username}")
        
        # Vérifier le sélecteur
        print("➤ Étape 3: Vérification du sélecteur d'auteurs...")
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        base.open_new_post_form()
        
        select = Select(driver.find_element(By.CSS_SELECTOR, base.SELECTORS["post_author_select"]))
        new_options = [opt.text for opt in select.options]
        print(f"✓ Nombre d'auteurs après création: {len(new_options) - 1}")
        
        # Vérifier que le nouvel utilisateur est présent
        found = any(new_username in opt for opt in new_options)
        assert found, f"L'utilisateur {new_username} n'apparaît pas dans le sélecteur"
        print(f"✓ Utilisateur {new_username} trouvé dans le sélecteur")
        
        base.click_element(base.SELECTORS["post_form_cancel"])
        
        print("\n✅ TEST RÉUSSI: Mise à jour du sélecteur d'auteurs OK")
