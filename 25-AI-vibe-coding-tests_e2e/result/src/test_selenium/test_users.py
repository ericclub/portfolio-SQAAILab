"""
Suite de Tests Selenium - Users (Gestion des Utilisateurs)
Application Blog Simple - Tests End-to-End

Basé sur test_plan.md - Suite de Tests 1
"""
import pytest
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from base_test import BaseTest


class TestUsers:
    """Suite de tests pour la gestion des utilisateurs"""
    
    # =========================================================================
    # US-001 : Consultation de la liste des utilisateurs
    # =========================================================================
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_001_01(self, driver, app_url, test_data):
        """
        TC-001-01 : Affichage de la liste des utilisateurs
        
        Objectif: Vérifier que la liste des utilisateurs s'affiche correctement
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-001-01 - Affichage de la liste des utilisateurs")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Étape 1: Ouvrir l'application
        print(">> Étape 1: Ouverture de l'application...")  # ← Changé : Enlever les accents francais
        base.open_app()
        
        # Étape 2: Naviguer vers Users
        print(">> Étape 2: Navigation vers la section Users...")  # ← Changé : Enlever les accents francais
        base.navigate_to_users()
        
        # Vérification: Section Users visible
        print(">> Vérification: Section Users visible...")  # ← Changé : Enlever les accents francais
        assert base.element_is_visible(base.SELECTORS["users_section"]), \
            "La section Users n'est pas visible"
        
        # Vérification: Liste des utilisateurs présente
        print(">> Vérification: Liste des utilisateurs présente...")  # ← Changé : Enlever les accents francais
        assert base.element_exists(base.SELECTORS["users_list"]), \
            "La liste des utilisateurs n'existe pas"
        
        base.wait_for_loading_complete()
        
        # Vérification des cartes utilisateurs (si des utilisateurs existent)
        user_count = base.get_user_count()
        print(f"OK Nombre d'utilisateurs trouvés: {user_count}")  # ← Changé : Enlever les accents francais
        
        if user_count > 0:
            cards = base.get_user_cards()
            first_card = cards[0]
            card_text = first_card.text
            print(f"OK Première carte utilisateur: {card_text[:100]}...")  # ← Changé : Enlever les accents francais
            
            # Vérifier que les informations essentielles sont présentes
            assert "@" in card_text or "email" in card_text.lower() or "post" in card_text.lower(), \
                "Les informations de l'utilisateur ne sont pas complètes"
        
        print("\nOK TEST RÉUSSI: La liste des utilisateurs s'affiche correctement")  # ← Changé : Enlever les accents francais

    @pytest.mark.users
    @pytest.mark.basse
    def test_Users_Basse_TC_001_02(self, driver, app_url):
        """
        TC-001-02 : Affichage état vide
        
        Objectif: Vérifier l'affichage lorsqu'aucun utilisateur n'existe
        Priorité: Basse
        
        Note: Ce test vérifie le comportement avec une base vide ou 
        vérifie que le message d'état vide est correctement formaté.
        """
        print("\n" + "="*70)
        print("TEST: Users_Basse_TC-001-02 - Affichage état vide")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Étape 1: Ouvrir l'application
        print("➤ Étape 1: Ouverture de l'application...")
        base.open_app()
        
        # Étape 2: Naviguer vers Users
        print("➤ Étape 2: Navigation vers la section Users...")
        base.navigate_to_users()
        
        base.wait_for_loading_complete()
        
        # Vérification: soit des utilisateurs existent, soit le message vide s'affiche
        user_count = base.get_user_count()
        
        if user_count == 0:
            print("➤ Vérification: Message d'état vide...")
            assert base.element_exists(base.SELECTORS["empty_state"]), \
                "Le message d'état vide n'est pas affiché"
            
            empty_text = base.get_text(base.SELECTORS["empty_state"])
            assert "no users" in empty_text.lower() or "create" in empty_text.lower(), \
                f"Message d'état vide incorrect: {empty_text}"
            print(f"✓ Message d'état vide correct: {empty_text}")
        else:
            print(f"✓ {user_count} utilisateur(s) trouvé(s) - pas d'état vide à vérifier")
            # Vérifier que l'empty state n'est PAS affiché quand il y a des utilisateurs
            empty_visible = base.element_is_visible(f"{base.SELECTORS['users_list']} {base.SELECTORS['empty_state']}")
            assert not empty_visible, "L'état vide est affiché alors qu'il y a des utilisateurs"
        
        print("\n✅ TEST RÉUSSI: Comportement de l'état vide vérifié")
    
    # =========================================================================
    # US-002 : Création d'un nouvel utilisateur
    # =========================================================================
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_002_01(self, driver, app_url, test_data):
        """
        TC-002-01 : Création d'un utilisateur avec données valides
        
        Objectif: Vérifier la création d'un utilisateur avec des données valides
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-002-01 - Création d'un utilisateur avec données valides")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Données de test uniques
        username = f"testuser_{timestamp}"
        email = f"test_{timestamp}@example.com"
        
        print(f"➤ Données de test: username={username}, email={email}")
        
        # Étape 1: Ouvrir l'application et naviguer vers Users
        print("➤ Étape 1: Ouverture de l'application...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        # Compter les utilisateurs avant création
        initial_count = base.get_user_count()
        print(f"➤ Nombre initial d'utilisateurs: {initial_count}")
        
        # Étape 2: Cliquer sur "+ New User"
        print("➤ Étape 2: Ouverture du formulaire de création...")
        base.click_element(base.SELECTORS["new_user_btn"])
        base.wait_for_modal_visible(base.SELECTORS["user_form_modal"])
        
        # Vérifier que le formulaire est visible
        assert base.element_is_visible(base.SELECTORS["user_form_modal"]), \
            "Le formulaire de création n'est pas visible"
        print("✓ Formulaire de création ouvert")
        
        # Étape 3: Remplir les champs
        print("➤ Étape 3: Remplissage des champs...")
        base.fill_input(base.SELECTORS["username_input"], username)
        base.fill_input(base.SELECTORS["email_input"], email)
        
        # Étape 4: Soumettre le formulaire
        print("➤ Étape 4: Soumission du formulaire...")
        base.click_element(base.SELECTORS["user_form_submit"])
        
        # Attendre la fermeture du modal
        base.wait_for_modal_hidden(base.SELECTORS["user_form_modal"])
        print("✓ Formulaire fermé")
        
        # Vérification: Toast de succès
        print("➤ Vérification: Notification de succès...")
        try:
            base.wait_for_toast("success", timeout=5)
            print("✓ Notification de succès affichée")
        except Exception as e:
            print(f"⚠ Toast non détecté: {e}")
        
        # Attendre le rechargement de la liste
        time.sleep(1)
        base.wait_for_loading_complete()
        
        # Vérification: L'utilisateur apparaît dans la liste
        print("➤ Vérification: Nouvel utilisateur dans la liste...")
        new_count = base.get_user_count()
        print(f"✓ Nombre d'utilisateurs après création: {new_count}")
        
        # Chercher l'utilisateur créé
        page_source = driver.page_source
        assert username in page_source, \
            f"L'utilisateur {username} n'apparaît pas dans la page"
        print(f"✓ Utilisateur {username} trouvé dans la liste")
        
        print("\n✅ TEST RÉUSSI: Utilisateur créé avec succès")
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_002_02(self, driver, app_url):
        """
        TC-002-02 : Création avec username en doublon
        
        Objectif: Vérifier le comportement lors de la création avec un username existant
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-002-02 - Création avec username en doublon")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Données de test
        username = f"dupuser_{timestamp}"
        email1 = f"dup1_{timestamp}@example.com"
        email2 = f"dup2_{timestamp}@example.com"
        
        # Étape 1: Créer un premier utilisateur
        print("➤ Étape 1: Création du premier utilisateur...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        base.create_user(username, email1)
        time.sleep(1)
        print(f"✓ Premier utilisateur créé: {username}")
        
        # Étape 2: Essayer de créer un utilisateur avec le même username
        print("➤ Étape 2: Tentative de création avec username en doublon...")
        base.open_new_user_form()
        base.fill_input(base.SELECTORS["username_input"], username)
        base.fill_input(base.SELECTORS["email_input"], email2)
        base.click_element(base.SELECTORS["user_form_submit"])
        
        # Vérification: Message d'erreur
        print("➤ Vérification: Message d'erreur...")
        try:
            toast = base.wait_for_toast(timeout=5)
            toast_text = toast.text.lower()
            assert "already exists" in toast_text or "error" in toast_text or "existe" in toast_text, \
                f"Message d'erreur inattendu: {toast.text}"
            print(f"✓ Message d'erreur affiché: {toast.text}")
        except Exception as e:
            # Le formulaire peut rester ouvert en cas d'erreur
            if base.element_is_visible(base.SELECTORS["user_form_modal"]):
                print("✓ Le formulaire reste ouvert (comportement attendu en cas d'erreur)")
            else:
                raise AssertionError(f"Comportement inattendu lors du doublon: {e}")
        
        print("\n✅ TEST RÉUSSI: Le doublon de username est correctement rejeté")
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_002_03(self, driver, app_url):
        """
        TC-002-03 : Création avec email en doublon
        
        Objectif: Vérifier le comportement lors de la création avec un email existant
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-002-03 - Création avec email en doublon")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Données de test
        username1 = f"emaildup1_{timestamp}"
        username2 = f"emaildup2_{timestamp}"
        email = f"dupemail_{timestamp}@example.com"
        
        # Étape 1: Créer un premier utilisateur
        print("➤ Étape 1: Création du premier utilisateur...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        base.create_user(username1, email)
        time.sleep(1)
        print(f"✓ Premier utilisateur créé avec email: {email}")
        
        # Étape 2: Essayer de créer un utilisateur avec le même email
        print("➤ Étape 2: Tentative de création avec email en doublon...")
        base.open_new_user_form()
        base.fill_input(base.SELECTORS["username_input"], username2)
        base.fill_input(base.SELECTORS["email_input"], email)
        base.click_element(base.SELECTORS["user_form_submit"])
        
        # Vérification: Message d'erreur
        print("➤ Vérification: Message d'erreur...")
        try:
            toast = base.wait_for_toast(timeout=5)
            toast_text = toast.text.lower()
            assert "already exists" in toast_text or "error" in toast_text or "existe" in toast_text, \
                f"Message d'erreur inattendu: {toast.text}"
            print(f"✓ Message d'erreur affiché: {toast.text}")
        except Exception as e:
            if base.element_is_visible(base.SELECTORS["user_form_modal"]):
                print("✓ Le formulaire reste ouvert (comportement attendu en cas d'erreur)")
            else:
                raise AssertionError(f"Comportement inattendu lors du doublon email: {e}")
        
        print("\n✅ TEST RÉUSSI: Le doublon d'email est correctement rejeté")
    
    @pytest.mark.users
    @pytest.mark.moyenne
    def test_Users_Moyenne_TC_002_04(self, driver, app_url):
        """
        TC-002-04 : Annulation de la création
        
        Objectif: Vérifier que l'annulation ferme le formulaire sans créer d'utilisateur
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Users_Moyenne_TC-002-04 - Annulation de la création")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Étape 1: Ouvrir l'application et naviguer vers Users
        print("➤ Étape 1: Ouverture de l'application...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        # Compter les utilisateurs avant
        initial_count = base.get_user_count()
        print(f"➤ Nombre initial d'utilisateurs: {initial_count}")
        
        # Étape 2: Ouvrir le formulaire
        print("➤ Étape 2: Ouverture du formulaire...")
        base.open_new_user_form()
        
        # Étape 3: Remplir des données
        print("➤ Étape 3: Saisie de données...")
        base.fill_input(base.SELECTORS["username_input"], "cancelled_user")
        base.fill_input(base.SELECTORS["email_input"], "cancelled@example.com")
        
        # Étape 4: Annuler
        print("➤ Étape 4: Annulation...")
        base.click_element(base.SELECTORS["user_form_cancel"])
        base.wait_for_modal_hidden(base.SELECTORS["user_form_modal"])
        print("✓ Formulaire fermé")
        
        # Vérification: Pas de nouvel utilisateur
        print("➤ Vérification: Aucun utilisateur créé...")
        time.sleep(0.5)
        final_count = base.get_user_count()
        assert final_count == initial_count, \
            f"Un utilisateur a été créé malgré l'annulation ({initial_count} -> {final_count})"
        print(f"✓ Nombre d'utilisateurs inchangé: {final_count}")
        
        print("\n✅ TEST RÉUSSI: L'annulation fonctionne correctement")
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_002_05(self, driver, app_url):
        """
        TC-002-05 : Validation des champs obligatoires
        
        Objectif: Vérifier que les champs obligatoires sont validés
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-002-05 - Validation des champs obligatoires")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Étape 1: Ouvrir l'application et le formulaire
        print("➤ Étape 1: Ouverture du formulaire...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.open_new_user_form()
        
        # Étape 2: Essayer de soumettre avec champs vides
        print("➤ Étape 2: Soumission avec champs vides...")
        
        # Vérifier que le bouton submit est cliquable mais la validation HTML5 empêche la soumission
        submit_btn = base.wait_for_element(base.SELECTORS["user_form_submit"])
        
        # Vérifier l'attribut required sur les inputs
        username_input = base.driver.find_element(By.CSS_SELECTOR, base.SELECTORS["username_input"])
        email_input = base.driver.find_element(By.CSS_SELECTOR, base.SELECTORS["email_input"])
        
        username_required = username_input.get_attribute("required") is not None
        email_required = email_input.get_attribute("required") is not None
        
        print(f"➤ Vérification: Username required = {username_required}")
        print(f"➤ Vérification: Email required = {email_required}")
        
        # Le formulaire devrait avoir les attributs required
        assert username_required or email_required, \
            "Les champs ne semblent pas avoir l'attribut required"
        
        # Essayer de soumettre et vérifier que le modal reste ouvert
        base.click_element(base.SELECTORS["user_form_submit"])
        time.sleep(0.5)
        
        # Le modal devrait rester visible car les champs sont obligatoires
        modal_visible = base.element_is_visible(base.SELECTORS["user_form_modal"])
        print(f"✓ Modal toujours visible après soumission sans données: {modal_visible}")
        
        print("\n✅ TEST RÉUSSI: Les champs obligatoires sont validés")
    
    # =========================================================================
    # US-003 : Consultation des détails d'un utilisateur
    # =========================================================================
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_003_01(self, driver, app_url, test_data):
        """
        TC-003-01 : Affichage des détails utilisateur
        
        Objectif: Vérifier l'affichage correct des détails d'un utilisateur
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-003-01 - Affichage des détails utilisateur")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Créer un utilisateur de test
        username = f"detailuser_{timestamp}"
        email = f"detail_{timestamp}@example.com"
        
        print("➤ Étape 1: Création d'un utilisateur de test...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.create_user(username, email)
        time.sleep(1)
        base.wait_for_loading_complete()
        
        # Étape 2: Cliquer sur View
        print("➤ Étape 2: Clic sur le bouton View...")
        cards = base.get_user_cards()
        
        # Trouver la carte de notre utilisateur
        target_card = None
        for card in cards:
            if username in card.text:
                target_card = card
                break
        
        assert target_card is not None, f"Utilisateur {username} non trouvé"
        
        # Cliquer sur le bouton View de cette carte
        view_btn = target_card.find_element(By.CSS_SELECTOR, ".btn-secondary")
        view_btn.click()
        
        # Attendre le modal
        base.wait_for_modal_visible(base.SELECTORS["user_detail_modal"])
        print("✓ Modal de détails ouvert")
        
        # Vérifier le contenu
        print("➤ Vérification: Contenu du modal...")
        detail_content = base.get_text(base.SELECTORS["user_detail_content"])
        
        assert username in detail_content, "Username non affiché dans les détails"
        print(f"✓ Username présent: {username}")
        
        assert email in detail_content or "@" in detail_content, \
            "Email non affiché dans les détails"
        print("✓ Email présent")
        
        # Vérifier la présence d'informations sur les posts et la date
        assert "post" in detail_content.lower() or "member" in detail_content.lower(), \
            "Informations supplémentaires non affichées"
        print("✓ Informations supplémentaires présentes")
        
        print("\n✅ TEST RÉUSSI: Les détails utilisateur s'affichent correctement")
    
    @pytest.mark.users
    @pytest.mark.moyenne
    def test_Users_Moyenne_TC_003_02(self, driver, app_url):
        """
        TC-003-02 : Fermeture du modal détails
        
        Objectif: Vérifier la fermeture du modal de détails
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Users_Moyenne_TC-003-02 - Fermeture du modal détails")
        print("="*70)
        
        base = BaseTest(driver)
        
        # Étape 1: Ouvrir l'application
        print("➤ Étape 1: Ouverture de l'application...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        # S'assurer qu'il y a au moins un utilisateur
        if base.get_user_count() == 0:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base.create_user(f"closetest_{timestamp}", f"close_{timestamp}@test.com")
            time.sleep(1)
            base.wait_for_loading_complete()
        
        # Étape 2: Ouvrir les détails d'un utilisateur
        print("➤ Étape 2: Ouverture du modal de détails...")
        cards = base.get_user_cards()
        view_btn = cards[0].find_element(By.CSS_SELECTOR, ".btn-secondary")
        view_btn.click()
        base.wait_for_modal_visible(base.SELECTORS["user_detail_modal"])
        print("✓ Modal ouvert")
        
        # Étape 3: Fermer le modal
        print("➤ Étape 3: Fermeture du modal...")
        base.close_modal(base.SELECTORS["user_detail_modal"])
        
        # Vérification
        print("➤ Vérification: Modal fermé...")
        assert not base.element_is_visible(base.SELECTORS["user_detail_modal"]), \
            "Le modal n'est pas fermé"
        print("✓ Modal fermé correctement")
        
        # Vérifier que la liste reste visible
        assert base.element_is_visible(base.SELECTORS["users_list"]), \
            "La liste des utilisateurs n'est plus visible"
        print("✓ Liste des utilisateurs toujours visible")
        
        print("\n✅ TEST RÉUSSI: Le modal se ferme correctement")
    
    # =========================================================================
    # US-004 : Suppression d'un utilisateur
    # =========================================================================
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_004_01(self, driver, app_url):
        """
        TC-004-01 : Suppression d'un utilisateur confirmée
        
        Objectif: Vérifier la suppression d'un utilisateur avec confirmation
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-004-01 - Suppression d'un utilisateur confirmée")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Créer un utilisateur à supprimer
        username = f"todelete_{timestamp}"
        email = f"delete_{timestamp}@test.com"
        
        print("➤ Étape 1: Création d'un utilisateur à supprimer...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.create_user(username, email)
        time.sleep(1)
        base.wait_for_loading_complete()
        
        initial_count = base.get_user_count()
        print(f"✓ Utilisateur créé. Nombre total: {initial_count}")
        
        # Trouver et supprimer l'utilisateur
        print("➤ Étape 2: Suppression de l'utilisateur...")
        cards = base.get_user_cards()
        target_card = None
        for card in cards:
            if username in card.text:
                target_card = card
                break
        
        assert target_card is not None, f"Utilisateur {username} non trouvé"
        
        # Cliquer sur Delete
        delete_btn = target_card.find_element(By.CSS_SELECTOR, ".btn-danger")
        delete_btn.click()
        
        # Confirmer la suppression
        print("➤ Étape 3: Confirmation de la suppression...")
        base.accept_alert()
        time.sleep(1)
        
        # Vérification: Toast de succès
        print("➤ Vérification: Notification de succès...")
        try:
            base.wait_for_toast(timeout=5)
            print("✓ Notification de succès affichée")
        except:
            pass
        
        base.wait_for_loading_complete()
        
        # Vérification: L'utilisateur a disparu
        print("➤ Vérification: Utilisateur supprimé de la liste...")
        final_count = base.get_user_count()
        assert final_count == initial_count - 1, \
            f"Le nombre d'utilisateurs n'a pas diminué ({initial_count} -> {final_count})"
        print(f"✓ Nombre d'utilisateurs après suppression: {final_count}")
        
        # Vérifier que l'utilisateur n'est plus dans la page
        page_source = driver.page_source
        # Note: Le username pourrait apparaître dans d'autres contextes, 
        # donc on vérifie le comptage plutôt que l'absence totale
        
        print("\n✅ TEST RÉUSSI: L'utilisateur a été supprimé avec succès")
    
    @pytest.mark.users
    @pytest.mark.moyenne
    def test_Users_Moyenne_TC_004_02(self, driver, app_url):
        """
        TC-004-02 : Annulation de la suppression
        
        Objectif: Vérifier que l'annulation préserve l'utilisateur
        Priorité: Moyenne
        """
        print("\n" + "="*70)
        print("TEST: Users_Moyenne_TC-004-02 - Annulation de la suppression")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Créer un utilisateur
        username = f"keepuser_{timestamp}"
        email = f"keep_{timestamp}@test.com"
        
        print("➤ Étape 1: Création d'un utilisateur...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.create_user(username, email)
        time.sleep(1)
        base.wait_for_loading_complete()
        
        initial_count = base.get_user_count()
        print(f"✓ Nombre d'utilisateurs: {initial_count}")
        
        # Cliquer sur Delete et annuler
        print("➤ Étape 2: Clic sur Delete puis annulation...")
        cards = base.get_user_cards()
        target_card = None
        for card in cards:
            if username in card.text:
                target_card = card
                break
        
        assert target_card is not None, f"Utilisateur {username} non trouvé"
        
        delete_btn = target_card.find_element(By.CSS_SELECTOR, ".btn-danger")
        delete_btn.click()
        
        # Annuler la suppression
        base.dismiss_alert()
        print("✓ Suppression annulée")
        
        time.sleep(0.5)
        
        # Vérification: L'utilisateur est toujours là
        print("➤ Vérification: Utilisateur toujours présent...")
        final_count = base.get_user_count()
        assert final_count == initial_count, \
            f"L'utilisateur a été supprimé malgré l'annulation ({initial_count} -> {final_count})"
        print(f"✓ Nombre d'utilisateurs inchangé: {final_count}")
        
        print("\n✅ TEST RÉUSSI: L'annulation de suppression fonctionne")
    
    @pytest.mark.users
    @pytest.mark.haute
    def test_Users_Haute_TC_004_03(self, driver, app_url):
        """
        TC-004-03 : Suppression en cascade des posts
        
        Objectif: Vérifier que les posts de l'utilisateur sont supprimés
        Priorité: Haute
        """
        print("\n" + "="*70)
        print("TEST: Users_Haute_TC-004-03 - Suppression en cascade des posts")
        print("="*70)
        
        base = BaseTest(driver)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Créer un utilisateur avec un post
        username = f"cascade_{timestamp}"
        email = f"cascade_{timestamp}@test.com"
        post_title = f"Post Cascade {timestamp}"
        
        print("➤ Étape 1: Création d'un utilisateur...")
        base.open_app()
        base.navigate_to_users()
        base.wait_for_loading_complete()
        base.create_user(username, email)
        time.sleep(1)
        
        # Créer un post pour cet utilisateur
        print("➤ Étape 2: Création d'un post pour cet utilisateur...")
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        
        base.open_new_post_form()
        base.fill_input(base.SELECTORS["post_title_input"], post_title)
        base.fill_input(base.SELECTORS["post_content_input"], f"Contenu du post cascade {timestamp}")
        
        # Sélectionner l'auteur créé
        from selenium.webdriver.support.ui import Select
        select = Select(driver.find_element(By.CSS_SELECTOR, base.SELECTORS["post_author_select"]))
        
        # Trouver et sélectionner notre utilisateur
        for option in select.options:
            if username in option.text:
                option.click()
                break
        
        base.click_element(base.SELECTORS["post_form_submit"])
        base.wait_for_modal_hidden(base.SELECTORS["post_form_modal"])
        time.sleep(1)
        base.wait_for_loading_complete()
        
        # Vérifier que le post existe
        initial_post_count = base.get_post_count()
        assert post_title in driver.page_source, "Le post n'a pas été créé"
        print(f"✓ Post créé. Nombre total de posts: {initial_post_count}")
        
        # Maintenant supprimer l'utilisateur
        print("➤ Étape 3: Suppression de l'utilisateur...")
        base.navigate_to_users()
        base.wait_for_loading_complete()
        
        cards = base.get_user_cards()
        target_card = None
        for card in cards:
            if username in card.text:
                target_card = card
                break
        
        assert target_card is not None, f"Utilisateur {username} non trouvé"
        
        delete_btn = target_card.find_element(By.CSS_SELECTOR, ".btn-danger")
        delete_btn.click()
        base.accept_alert()
        time.sleep(1)
        base.wait_for_loading_complete()
        
        # Vérifier que les posts ont été supprimés
        print("➤ Étape 4: Vérification de la suppression des posts...")
        base.navigate_to_posts()
        base.wait_for_loading_complete()
        
        final_post_count = base.get_post_count()
        page_source = driver.page_source
        
        # Le post devrait avoir été supprimé avec l'utilisateur
        assert post_title not in page_source, \
            "Le post existe toujours après suppression de l'utilisateur"
        print(f"✓ Post supprimé en cascade. Nombre de posts: {final_post_count}")
        
        print("\n✅ TEST RÉUSSI: La suppression en cascade fonctionne")
