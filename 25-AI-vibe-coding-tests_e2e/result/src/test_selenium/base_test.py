"""
Classe de base pour les tests Selenium
Application Blog Simple - Tests End-to-End
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BaseTest:
    """Classe de base avec méthodes utilitaires pour les tests Selenium"""
    
    # URLs
    FRONTEND_URL = "http://localhost:8080"
    BACKEND_URL = "http://localhost:5000"
    
    # Timeouts
    DEFAULT_TIMEOUT = 10
    SHORT_TIMEOUT = 5
    LONG_TIMEOUT = 30
    
    # Sélecteurs CSS communs
    SELECTORS = {
        # Navigation
        "nav_posts": ".nav-links a[onclick*='posts']",
        "nav_users": ".nav-links a[onclick*='users']",
        "nav_stats": ".nav-links a[onclick*='stats']",
        
        # Sections
        "posts_section": "#posts-section",
        "users_section": "#users-section",
        "stats_section": "#stats-section",
        
        # Posts
        "posts_list": "#posts-list",
        "post_card": "#posts-list .card",
        "new_post_btn": "#posts-section .btn-primary",
        "post_form_modal": "#post-form-modal",
        "post_title_input": "#post-title-input",
        "post_content_input": "#post-content-input",
        "post_author_select": "#post-author-select",
        "post_form_submit": "#post-form button[type='submit']",
        "post_form_cancel": "#post-form .btn-secondary",
        "post_detail_modal": "#post-detail-modal",
        "post_detail_content": "#post-detail-content",
        
        # Users
        "users_list": "#users-list",
        "user_card": "#users-list .card",
        "new_user_btn": "#users-section .btn-primary",
        "user_form_modal": "#user-form-modal",
        "username_input": "#username-input",
        "email_input": "#email-input",
        "user_form_submit": "#user-form button[type='submit']",
        "user_form_cancel": "#user-form .btn-secondary",
        "user_detail_modal": "#user-detail-modal",
        "user_detail_content": "#user-detail-content",
        
        # Statistics
        "stats_container": "#stats-container",
        "stats_refresh_btn": "#stats-section .btn-secondary",
        "stat_card": ".stat-card",
        "stat_list": ".stat-list",
        
        # Toast notification
        "toast": "#toast",
        
        # Loading
        "loading": ".loading",
        
        # Empty state
        "empty_state": ".empty-state",
        
        # Modal close button
        "modal_close": ".modal .close",
        
        # Card actions
        "card_view_btn": ".card-actions .btn-secondary",
        "card_edit_btn": ".card-actions .btn-primary",
        "card_delete_btn": ".card-actions .btn-danger",
    }
    
    def __init__(self, driver):
        """Initialise avec le WebDriver"""
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
    
    # =========================================================================
    # Navigation
    # =========================================================================
    
    def open_app(self):
        """Ouvre l'application dans le navigateur"""
        self.driver.get(self.FRONTEND_URL)
        self.wait_for_page_load()
    
    def navigate_to_posts(self):
        """Navigue vers la section Posts"""
        self.click_element(self.SELECTORS["nav_posts"])
        self.wait_for_section_visible("posts")
    
    def navigate_to_users(self):
        """Navigue vers la section Users"""
        self.click_element(self.SELECTORS["nav_users"])
        self.wait_for_section_visible("users")
    
    def navigate_to_stats(self):
        """Navigue vers la section Statistics"""
        self.click_element(self.SELECTORS["nav_stats"])
        self.wait_for_section_visible("stats")
    
    # =========================================================================
    # Attentes
    # =========================================================================
    
    def wait_for_page_load(self):
        """Attend que la page soit complètement chargée"""
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(0.5)  # Petit délai pour les animations
    
    def wait_for_section_visible(self, section_name):
        """Attend qu'une section soit visible"""
        selector = self.SELECTORS.get(f"{section_name}_section")
        if selector:
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            time.sleep(0.3)
    
    def wait_for_element(self, selector, timeout=None):
        """Attend qu'un élément soit présent"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    
    def wait_for_element_visible(self, selector, timeout=None):
        """Attend qu'un élément soit visible"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    
    def wait_for_element_clickable(self, selector, timeout=None):
        """Attend qu'un élément soit cliquable"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    
    def wait_for_element_invisible(self, selector, timeout=None):
        """Attend qu'un élément disparaisse"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
    
    def wait_for_modal_visible(self, modal_selector):
        """Attend qu'un modal soit visible"""
        self.wait_for_element_visible(modal_selector)
        time.sleep(0.3)  # Animation du modal
    
    def wait_for_modal_hidden(self, modal_selector):
        """Attend qu'un modal soit caché"""
        self.wait_for_element_invisible(modal_selector)
        time.sleep(0.3)
    
    def wait_for_toast(self, expected_text=None, timeout=None):
        """Attend l'apparition d'un toast notification"""
        timeout = timeout or self.DEFAULT_TIMEOUT
        toast = self.wait_for_element_visible(self.SELECTORS["toast"], timeout)
        if expected_text:
            assert expected_text.lower() in toast.text.lower(), \
                f"Toast attendu '{expected_text}', reçu '{toast.text}'"
        return toast
    
    def wait_for_loading_complete(self):
        """Attend que le chargement soit terminé"""
        try:
            self.wait_for_element_invisible(self.SELECTORS["loading"], timeout=5)
        except TimeoutException:
            pass  # Le loading n'était peut-être pas affiché
        time.sleep(0.5)
    
    # =========================================================================
    # Interactions
    # =========================================================================
    
    def click_element(self, selector):
        """Clique sur un élément"""
        element = self.wait_for_element_clickable(selector)
        element.click()
    
    def fill_input(self, selector, value):
        """Remplit un champ de saisie"""
        element = self.wait_for_element_visible(selector)
        element.clear()
        element.send_keys(value)
    
    def select_option(self, selector, value=None, text=None):
        """Sélectionne une option dans un select"""
        element = self.wait_for_element_visible(selector)
        select = Select(element)
        if value:
            select.select_by_value(str(value))
        elif text:
            select.select_by_visible_text(text)
    
    def get_text(self, selector):
        """Récupère le texte d'un élément"""
        element = self.wait_for_element_visible(selector)
        return element.text
    
    def get_element_count(self, selector):
        """Compte le nombre d'éléments correspondant au sélecteur"""
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        return len(elements)
    
    def element_exists(self, selector):
        """Vérifie si un élément existe"""
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector)
            return True
        except NoSuchElementException:
            return False
    
    def element_is_visible(self, selector):
        """Vérifie si un élément est visible"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def element_is_enabled(self, selector):
        """Vérifie si un élément est activé"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.is_enabled()
        except NoSuchElementException:
            return False
    
    def get_input_value(self, selector):
        """Récupère la valeur d'un input"""
        element = self.wait_for_element(selector)
        return element.get_attribute("value")
    
    def accept_alert(self):
        """Accepte une alerte/confirmation JavaScript"""
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert.accept()
            return True
        except TimeoutException:
            return False
    
    def dismiss_alert(self):
        """Refuse une alerte/confirmation JavaScript"""
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert.dismiss()
            return True
        except TimeoutException:
            return False
    
    def close_modal(self, modal_selector):
        """Ferme un modal via le bouton X"""
        close_btn = f"{modal_selector} .close"
        self.click_element(close_btn)
        self.wait_for_modal_hidden(modal_selector)
    
    # =========================================================================
    # Actions spécifiques - Users
    # =========================================================================
    
    def open_new_user_form(self):
        """Ouvre le formulaire de création d'utilisateur"""
        self.click_element(self.SELECTORS["new_user_btn"])
        self.wait_for_modal_visible(self.SELECTORS["user_form_modal"])
    
    def create_user(self, username, email):
        """Crée un nouvel utilisateur"""
        self.open_new_user_form()
        self.fill_input(self.SELECTORS["username_input"], username)
        self.fill_input(self.SELECTORS["email_input"], email)
        self.click_element(self.SELECTORS["user_form_submit"])
        self.wait_for_modal_hidden(self.SELECTORS["user_form_modal"])
    
    def get_user_cards(self):
        """Récupère toutes les cartes utilisateur"""
        return self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS["user_card"])
    
    def get_user_count(self):
        """Compte le nombre d'utilisateurs affichés"""
        return self.get_element_count(self.SELECTORS["user_card"])
    
    # =========================================================================
    # Actions spécifiques - Posts
    # =========================================================================
    
    def open_new_post_form(self):
        """Ouvre le formulaire de création de post"""
        self.click_element(self.SELECTORS["new_post_btn"])
        self.wait_for_modal_visible(self.SELECTORS["post_form_modal"])
    
    def create_post(self, title, content, author_index=1):
        """Crée un nouveau post"""
        self.open_new_post_form()
        self.fill_input(self.SELECTORS["post_title_input"], title)
        self.fill_input(self.SELECTORS["post_content_input"], content)
        
        # Sélectionner un auteur (index 1 = premier auteur réel)
        select = Select(self.driver.find_element(By.CSS_SELECTOR, self.SELECTORS["post_author_select"]))
        if len(select.options) > author_index:
            select.select_by_index(author_index)
        
        self.click_element(self.SELECTORS["post_form_submit"])
        self.wait_for_modal_hidden(self.SELECTORS["post_form_modal"])
    
    def get_post_cards(self):
        """Récupère toutes les cartes post"""
        return self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS["post_card"])
    
    def get_post_count(self):
        """Compte le nombre de posts affichés"""
        return self.get_element_count(self.SELECTORS["post_card"])
    
    # =========================================================================
    # Actions spécifiques - Statistics
    # =========================================================================
    
    def refresh_stats(self):
        """Rafraîchit les statistiques"""
        self.click_element(self.SELECTORS["stats_refresh_btn"])
        self.wait_for_loading_complete()
    
    def get_stat_value(self, label):
        """Récupère une valeur de statistique par son label"""
        stat_cards = self.driver.find_elements(By.CSS_SELECTOR, self.SELECTORS["stat_card"])
        for card in stat_cards:
            if label.lower() in card.text.lower():
                value_elem = card.find_element(By.CSS_SELECTOR, ".stat-value")
                return value_elem.text
        return None
    
    # =========================================================================
    # Utilitaires de capture
    # =========================================================================
    
    def take_screenshot(self, name):
        """Prend une capture d'écran"""
        import os
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        filepath = os.path.join(screenshots_dir, f"{name}.png")
        self.driver.save_screenshot(filepath)
        return filepath
    
    def log_current_state(self):
        """Log l'état actuel pour le débogage"""
        print(f"URL actuelle: {self.driver.current_url}")
        print(f"Titre: {self.driver.title}")
