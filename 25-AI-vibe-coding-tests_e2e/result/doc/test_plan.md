# Plan de Test - Application Blog Simple

## 📋 Informations Générales

| Élément | Description |
|---------|-------------|
| **Projet** | Simple Web Blog |
| **Version** | 1.0 |
| **Date de création** | 18 février 2026 |
| **Auteur** | Équipe QA |
| **Type de tests** | Tests End-to-End (E2E) |

---

## 🎯 Objectif

Ce plan de test définit les scénarios de tests end-to-end pour l'application web de blog. L'application possède trois sections principales :

1. **Users** - Gestion des utilisateurs
2. **Posts** - Gestion des articles de blog
3. **Statistics** - Affichage des statistiques

Chaque section est couverte par une suite de tests complète incluant les user stories, critères d'acceptation et cas de test détaillés.

---

## 🔧 Environnement de Test

| Composant | Technologie |
|-----------|-------------|
| Backend | Flask REST API (Python) |
| Frontend | HTML/CSS/JavaScript |
| Base de données | SQLite (développement) / MySQL (production) |
| URL API | http://localhost:5000/api |

---

# Suite de Tests 1 : Gestion des Utilisateurs (Users)

## US-001 : Consultation de la liste des utilisateurs

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** voir la liste de tous les utilisateurs enregistrés,  
> **Afin de** gérer les membres de ma communauté.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-001-1 | La liste des utilisateurs s'affiche lors de la navigation vers la section "Users" | Haute |
| CA-001-2 | Chaque carte utilisateur affiche le nom d'utilisateur | Haute |
| CA-001-3 | Chaque carte utilisateur affiche l'adresse email | Haute |
| CA-001-4 | Chaque carte utilisateur affiche le nombre de posts | Moyenne |
| CA-001-5 | Chaque carte utilisateur affiche la date d'inscription | Moyenne |
| CA-001-6 | Un message approprié s'affiche si aucun utilisateur n'existe | Basse |

### Cas de Test

#### TC-001-01 : Affichage de la liste des utilisateurs
| Élément | Description |
|---------|-------------|
| **ID** | TC-001-01 |
| **Objectif** | Vérifier que la liste des utilisateurs s'affiche correctement |
| **Préconditions** | - L'application est démarrée<br>- Au moins un utilisateur existe dans la base de données |
| **Étapes** | 1. Ouvrir l'application dans le navigateur<br>2. Cliquer sur le lien "Users" dans la navigation |
| **Résultat attendu** | La section Users s'affiche avec toutes les cartes utilisateurs contenant username, email, nombre de posts et date d'inscription |
| **Priorité** | Haute |

#### TC-001-02 : Affichage état vide
| Élément | Description |
|---------|-------------|
| **ID** | TC-001-02 |
| **Objectif** | Vérifier l'affichage lorsqu'aucun utilisateur n'existe |
| **Préconditions** | - L'application est démarrée<br>- La base de données ne contient aucun utilisateur |
| **Étapes** | 1. Ouvrir l'application<br>2. Naviguer vers la section "Users" |
| **Résultat attendu** | Un message "No users yet. Create your first user!" s'affiche avec une icône 👤 |
| **Priorité** | Basse |

---

## US-002 : Création d'un nouvel utilisateur

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** pouvoir créer un nouvel utilisateur,  
> **Afin de** permettre à de nouvelles personnes de publier des articles.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-002-1 | Un bouton "+ New User" est visible dans la section Users | Haute |
| CA-002-2 | Un formulaire modal s'ouvre lors du clic sur le bouton | Haute |
| CA-002-3 | Le formulaire contient les champs username et email | Haute |
| CA-002-4 | Les champs username et email sont obligatoires | Haute |
| CA-002-5 | Une notification de succès s'affiche après création | Moyenne |
| CA-002-6 | Le nouvel utilisateur apparaît dans la liste | Haute |
| CA-002-7 | Un message d'erreur s'affiche si le username existe déjà | Haute |
| CA-002-8 | Un message d'erreur s'affiche si l'email existe déjà | Haute |

### Cas de Test

#### TC-002-01 : Création d'un utilisateur avec données valides
| Élément | Description |
|---------|-------------|
| **ID** | TC-002-01 |
| **Objectif** | Vérifier la création d'un utilisateur avec des données valides |
| **Préconditions** | - L'application est démarrée<br>- Section Users affichée |
| **Données de test** | - Username: "testuser_001"<br>- Email: "testuser001@example.com" |
| **Étapes** | 1. Cliquer sur le bouton "+ New User"<br>2. Saisir le username dans le champ approprié<br>3. Saisir l'email dans le champ approprié<br>4. Cliquer sur le bouton "Create User" |
| **Résultat attendu** | - Le modal se ferme<br>- Une notification "User created successfully" s'affiche<br>- L'utilisateur apparaît dans la liste |
| **Priorité** | Haute |

#### TC-002-02 : Création avec username en doublon
| Élément | Description |
|---------|-------------|
| **ID** | TC-002-02 |
| **Objectif** | Vérifier le comportement lors de la création avec un username existant |
| **Préconditions** | - Un utilisateur "existinguser" existe déjà |
| **Données de test** | - Username: "existinguser"<br>- Email: "new@example.com" |
| **Étapes** | 1. Cliquer sur "+ New User"<br>2. Saisir "existinguser" comme username<br>3. Saisir un email unique<br>4. Cliquer sur "Create User" |
| **Résultat attendu** | Une notification d'erreur "Username already exists" s'affiche |
| **Priorité** | Haute |

#### TC-002-03 : Création avec email en doublon
| Élément | Description |
|---------|-------------|
| **ID** | TC-002-03 |
| **Objectif** | Vérifier le comportement lors de la création avec un email existant |
| **Préconditions** | - Un utilisateur avec l'email "existing@example.com" existe |
| **Données de test** | - Username: "newuser"<br>- Email: "existing@example.com" |
| **Étapes** | 1. Cliquer sur "+ New User"<br>2. Saisir un username unique<br>3. Saisir l'email existant<br>4. Cliquer sur "Create User" |
| **Résultat attendu** | Une notification d'erreur "Email already exists" s'affiche |
| **Priorité** | Haute |

#### TC-002-04 : Annulation de la création
| Élément | Description |
|---------|-------------|
| **ID** | TC-002-04 |
| **Objectif** | Vérifier que l'annulation ferme le formulaire sans créer d'utilisateur |
| **Préconditions** | - Section Users affichée |
| **Étapes** | 1. Cliquer sur "+ New User"<br>2. Saisir des données dans les champs<br>3. Cliquer sur le bouton "Cancel" |
| **Résultat attendu** | Le modal se ferme et aucun utilisateur n'est créé |
| **Priorité** | Moyenne |

#### TC-002-05 : Validation des champs obligatoires
| Élément | Description |
|---------|-------------|
| **ID** | TC-002-05 |
| **Objectif** | Vérifier que les champs obligatoires sont validés |
| **Préconditions** | - Formulaire de création ouvert |
| **Étapes** | 1. Laisser les champs username et email vides<br>2. Cliquer sur "Create User" |
| **Résultat attendu** | Le formulaire ne se soumet pas et les champs obligatoires sont signalés |
| **Priorité** | Haute |

---

## US-003 : Consultation des détails d'un utilisateur

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** voir les détails complets d'un utilisateur,  
> **Afin de** consulter ses informations détaillées.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-003-1 | Un bouton "View" est disponible sur chaque carte utilisateur | Haute |
| CA-003-2 | Le clic sur "View" ouvre un modal avec les détails | Haute |
| CA-003-3 | Le modal affiche le username, email, nombre de posts et date d'inscription | Haute |
| CA-003-4 | Le modal peut être fermé via le bouton X | Moyenne |

### Cas de Test

#### TC-003-01 : Affichage des détails utilisateur
| Élément | Description |
|---------|-------------|
| **ID** | TC-003-01 |
| **Objectif** | Vérifier l'affichage correct des détails d'un utilisateur |
| **Préconditions** | - Au moins un utilisateur existe |
| **Étapes** | 1. Naviguer vers la section Users<br>2. Cliquer sur le bouton "View" d'une carte utilisateur |
| **Résultat attendu** | Un modal s'ouvre affichant : username, email, nombre de posts, date d'inscription |
| **Priorité** | Haute |

#### TC-003-02 : Fermeture du modal détails
| Élément | Description |
|---------|-------------|
| **ID** | TC-003-02 |
| **Objectif** | Vérifier la fermeture du modal de détails |
| **Préconditions** | - Modal de détails utilisateur ouvert |
| **Étapes** | 1. Cliquer sur le bouton X du modal |
| **Résultat attendu** | Le modal se ferme et la liste des utilisateurs reste visible |
| **Priorité** | Moyenne |

---

## US-004 : Suppression d'un utilisateur

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** pouvoir supprimer un utilisateur,  
> **Afin de** retirer les comptes inactifs ou indésirables.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-004-1 | Un bouton "Delete" est disponible sur chaque carte utilisateur | Haute |
| CA-004-2 | Une confirmation est demandée avant la suppression | Haute |
| CA-004-3 | L'utilisateur disparaît de la liste après suppression | Haute |
| CA-004-4 | Tous les posts de l'utilisateur sont également supprimés | Haute |
| CA-004-5 | Une notification de succès s'affiche après suppression | Moyenne |

### Cas de Test

#### TC-004-01 : Suppression d'un utilisateur confirmée
| Élément | Description |
|---------|-------------|
| **ID** | TC-004-01 |
| **Objectif** | Vérifier la suppression d'un utilisateur avec confirmation |
| **Préconditions** | - Un utilisateur "usertodelete" existe |
| **Étapes** | 1. Naviguer vers Users<br>2. Cliquer sur "Delete" pour l'utilisateur cible<br>3. Confirmer la suppression dans la boîte de dialogue |
| **Résultat attendu** | - L'utilisateur disparaît de la liste<br>- Notification "User deleted successfully" affichée |
| **Priorité** | Haute |

#### TC-004-02 : Annulation de la suppression
| Élément | Description |
|---------|-------------|
| **ID** | TC-004-02 |
| **Objectif** | Vérifier que l'annulation préserve l'utilisateur |
| **Préconditions** | - Un utilisateur existe dans la liste |
| **Étapes** | 1. Cliquer sur "Delete" pour un utilisateur<br>2. Cliquer sur "Cancel" dans la boîte de dialogue de confirmation |
| **Résultat attendu** | L'utilisateur reste dans la liste |
| **Priorité** | Moyenne |

#### TC-004-03 : Suppression en cascade des posts
| Élément | Description |
|---------|-------------|
| **ID** | TC-004-03 |
| **Objectif** | Vérifier que les posts de l'utilisateur sont supprimés |
| **Préconditions** | - Un utilisateur avec plusieurs posts existe |
| **Étapes** | 1. Noter le nombre de posts de l'utilisateur<br>2. Supprimer l'utilisateur<br>3. Naviguer vers la section Posts |
| **Résultat attendu** | Les posts de l'utilisateur supprimé ne sont plus visibles |
| **Priorité** | Haute |

---

# Suite de Tests 2 : Gestion des Articles (Posts)

## US-005 : Consultation de la liste des articles

### User Story
> **En tant que** visiteur du blog,  
> **Je veux** voir la liste de tous les articles publiés,  
> **Afin de** découvrir le contenu disponible.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-005-1 | La section Posts s'affiche par défaut au chargement | Haute |
| CA-005-2 | Les articles sont triés par date de création décroissante | Haute |
| CA-005-3 | Chaque carte article affiche le titre | Haute |
| CA-005-4 | Chaque carte article affiche l'auteur | Haute |
| CA-005-5 | Chaque carte article affiche un aperçu du contenu (max 150 caractères) | Moyenne |
| CA-005-6 | Chaque carte article affiche la date de création | Moyenne |
| CA-005-7 | La date de modification s'affiche si différente de la création | Basse |
| CA-005-8 | Un message approprié s'affiche si aucun article n'existe | Basse |

### Cas de Test

#### TC-005-01 : Affichage de la liste des articles
| Élément | Description |
|---------|-------------|
| **ID** | TC-005-01 |
| **Objectif** | Vérifier l'affichage correct de la liste des articles |
| **Préconditions** | - L'application est démarrée<br>- Au moins un article existe |
| **Étapes** | 1. Ouvrir l'application<br>2. Observer la section Posts (affichée par défaut) |
| **Résultat attendu** | Les cartes articles s'affichent avec titre, auteur, aperçu du contenu et date |
| **Priorité** | Haute |

#### TC-005-02 : Ordre de tri des articles
| Élément | Description |
|---------|-------------|
| **ID** | TC-005-02 |
| **Objectif** | Vérifier que les articles sont triés du plus récent au plus ancien |
| **Préconditions** | - Plusieurs articles existent avec des dates différentes |
| **Étapes** | 1. Naviguer vers la section Posts<br>2. Observer l'ordre des articles |
| **Résultat attendu** | Le premier article affiché est le plus récemment créé |
| **Priorité** | Moyenne |

#### TC-005-03 : Affichage état vide des posts
| Élément | Description |
|---------|-------------|
| **ID** | TC-005-03 |
| **Objectif** | Vérifier l'affichage lorsqu'aucun article n'existe |
| **Préconditions** | - La base de données ne contient aucun article |
| **Étapes** | 1. Naviguer vers la section Posts |
| **Résultat attendu** | Message "No posts yet. Create your first post!" avec icône 📝 |
| **Priorité** | Basse |

#### TC-005-04 : Troncature du contenu
| Élément | Description |
|---------|-------------|
| **ID** | TC-005-04 |
| **Objectif** | Vérifier que le contenu long est tronqué à 150 caractères |
| **Préconditions** | - Un article avec un contenu > 150 caractères existe |
| **Étapes** | 1. Observer la carte de l'article<br>2. Vérifier l'aperçu du contenu |
| **Résultat attendu** | Le contenu est tronqué avec "..." à la fin |
| **Priorité** | Moyenne |

---

## US-006 : Création d'un nouvel article

### User Story
> **En tant qu'** auteur du blog,  
> **Je veux** pouvoir créer un nouvel article,  
> **Afin de** partager du contenu avec les lecteurs.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-006-1 | Un bouton "+ New Post" est visible dans la section Posts | Haute |
| CA-006-2 | Un formulaire modal s'ouvre lors du clic | Haute |
| CA-006-3 | Le formulaire contient les champs titre, contenu et auteur | Haute |
| CA-006-4 | La liste des auteurs est disponible dans un menu déroulant | Haute |
| CA-006-5 | Tous les champs sont obligatoires | Haute |
| CA-006-6 | Une notification de succès s'affiche après création | Moyenne |
| CA-006-7 | Le nouvel article apparaît en premier dans la liste | Haute |

### Cas de Test

#### TC-006-01 : Création d'un article avec données valides
| Élément | Description |
|---------|-------------|
| **ID** | TC-006-01 |
| **Objectif** | Vérifier la création d'un article avec des données valides |
| **Préconditions** | - Au moins un utilisateur existe<br>- Section Posts affichée |
| **Données de test** | - Titre: "Mon premier article"<br>- Contenu: "Ceci est le contenu de mon article de test."<br>- Auteur: Utilisateur existant |
| **Étapes** | 1. Cliquer sur "+ New Post"<br>2. Saisir le titre<br>3. Saisir le contenu<br>4. Sélectionner un auteur<br>5. Cliquer sur "Save Post" |
| **Résultat attendu** | - Modal se ferme<br>- Notification "Post created successfully"<br>- Article apparaît en premier dans la liste |
| **Priorité** | Haute |

#### TC-006-02 : Création sans utilisateur disponible
| Élément | Description |
|---------|-------------|
| **ID** | TC-006-02 |
| **Objectif** | Vérifier le comportement quand aucun auteur n'est disponible |
| **Préconditions** | - Aucun utilisateur n'existe dans la base |
| **Étapes** | 1. Cliquer sur "+ New Post"<br>2. Observer le menu déroulant des auteurs |
| **Résultat attendu** | Le menu déroulant ne contient que l'option "Select an author" |
| **Priorité** | Moyenne |

#### TC-006-03 : Validation des champs obligatoires article
| Élément | Description |
|---------|-------------|
| **ID** | TC-006-03 |
| **Objectif** | Vérifier la validation des champs obligatoires |
| **Préconditions** | - Formulaire de création ouvert |
| **Étapes** | 1. Laisser un ou plusieurs champs vides<br>2. Cliquer sur "Save Post" |
| **Résultat attendu** | Le formulaire ne se soumet pas et les champs manquants sont signalés |
| **Priorité** | Haute |

#### TC-006-04 : Annulation de la création d'article
| Élément | Description |
|---------|-------------|
| **ID** | TC-006-04 |
| **Objectif** | Vérifier l'annulation de la création |
| **Préconditions** | - Formulaire de création ouvert |
| **Étapes** | 1. Saisir des données<br>2. Cliquer sur "Cancel" |
| **Résultat attendu** | Le modal se ferme et aucun article n'est créé |
| **Priorité** | Moyenne |

---

## US-007 : Consultation des détails d'un article

### User Story
> **En tant que** lecteur du blog,  
> **Je veux** voir le contenu complet d'un article,  
> **Afin de** lire l'intégralité de l'article qui m'intéresse.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-007-1 | Un bouton "View" est disponible sur chaque carte article | Haute |
| CA-007-2 | Le clic sur le titre ouvre également les détails | Moyenne |
| CA-007-3 | Le modal affiche le titre complet | Haute |
| CA-007-4 | Le modal affiche le contenu complet | Haute |
| CA-007-5 | Le modal affiche l'auteur et les dates | Haute |
| CA-007-6 | Le modal peut être fermé via le bouton X | Moyenne |

### Cas de Test

#### TC-007-01 : Affichage des détails via bouton View
| Élément | Description |
|---------|-------------|
| **ID** | TC-007-01 |
| **Objectif** | Vérifier l'affichage des détails d'un article |
| **Préconditions** | - Au moins un article existe |
| **Étapes** | 1. Naviguer vers Posts<br>2. Cliquer sur le bouton "View" d'un article |
| **Résultat attendu** | Modal affichant titre, contenu complet, auteur, date de création et mise à jour |
| **Priorité** | Haute |

#### TC-007-02 : Affichage des détails via titre
| Élément | Description |
|---------|-------------|
| **ID** | TC-007-02 |
| **Objectif** | Vérifier l'ouverture des détails en cliquant sur le titre |
| **Préconditions** | - Au moins un article existe |
| **Étapes** | 1. Cliquer sur le titre d'un article |
| **Résultat attendu** | Le modal de détails s'ouvre |
| **Priorité** | Moyenne |

#### TC-007-03 : Fermeture du modal détails article
| Élément | Description |
|---------|-------------|
| **ID** | TC-007-03 |
| **Objectif** | Vérifier la fermeture du modal |
| **Préconditions** | - Modal de détails ouvert |
| **Étapes** | 1. Cliquer sur le bouton X |
| **Résultat attendu** | Le modal se ferme |
| **Priorité** | Moyenne |

---

## US-008 : Modification d'un article

### User Story
> **En tant qu'** auteur du blog,  
> **Je veux** pouvoir modifier un article existant,  
> **Afin de** corriger ou mettre à jour son contenu.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-008-1 | Un bouton "Edit" est disponible sur chaque carte article | Haute |
| CA-008-2 | Le formulaire d'édition s'ouvre pré-rempli avec les données actuelles | Haute |
| CA-008-3 | Le titre peut être modifié | Haute |
| CA-008-4 | Le contenu peut être modifié | Haute |
| CA-008-5 | L'auteur ne peut pas être modifié | Haute |
| CA-008-6 | La date de mise à jour est actualisée après modification | Moyenne |
| CA-008-7 | Une notification de succès s'affiche après modification | Moyenne |

### Cas de Test

#### TC-008-01 : Modification du titre d'un article
| Élément | Description |
|---------|-------------|
| **ID** | TC-008-01 |
| **Objectif** | Vérifier la modification du titre |
| **Préconditions** | - Un article existe |
| **Données de test** | - Nouveau titre: "Titre modifié" |
| **Étapes** | 1. Cliquer sur "Edit" pour un article<br>2. Modifier le titre<br>3. Cliquer sur "Save Post" |
| **Résultat attendu** | - Modal se ferme<br>- Notification "Post updated successfully"<br>- Le nouveau titre s'affiche |
| **Priorité** | Haute |

#### TC-008-02 : Modification du contenu d'un article
| Élément | Description |
|---------|-------------|
| **ID** | TC-008-02 |
| **Objectif** | Vérifier la modification du contenu |
| **Préconditions** | - Un article existe |
| **Données de test** | - Nouveau contenu: "Contenu mis à jour" |
| **Étapes** | 1. Cliquer sur "Edit"<br>2. Modifier le contenu<br>3. Sauvegarder |
| **Résultat attendu** | Le contenu est mis à jour |
| **Priorité** | Haute |

#### TC-008-03 : Vérification auteur non modifiable
| Élément | Description |
|---------|-------------|
| **ID** | TC-008-03 |
| **Objectif** | Vérifier que l'auteur ne peut pas être changé |
| **Préconditions** | - Formulaire d'édition ouvert |
| **Étapes** | 1. Observer le champ auteur dans le formulaire d'édition |
| **Résultat attendu** | Le champ auteur est désactivé (disabled) |
| **Priorité** | Haute |

#### TC-008-04 : Vérification mise à jour de la date
| Élément | Description |
|---------|-------------|
| **ID** | TC-008-04 |
| **Objectif** | Vérifier que la date de mise à jour est actualisée |
| **Préconditions** | - Un article créé précédemment existe |
| **Étapes** | 1. Noter la date de création de l'article<br>2. Modifier l'article<br>3. Vérifier les dates dans les détails |
| **Résultat attendu** | La date "Updated" est différente de "Created" et correspond à l'heure de modification |
| **Priorité** | Moyenne |

---

## US-009 : Suppression d'un article

### User Story
> **En tant qu'** auteur du blog,  
> **Je veux** pouvoir supprimer un article,  
> **Afin de** retirer du contenu obsolète ou erroné.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-009-1 | Un bouton "Delete" est disponible sur chaque carte article | Haute |
| CA-009-2 | Une confirmation est demandée avant la suppression | Haute |
| CA-009-3 | L'article disparaît de la liste après suppression | Haute |
| CA-009-4 | Une notification de succès s'affiche après suppression | Moyenne |

### Cas de Test

#### TC-009-01 : Suppression d'un article confirmée
| Élément | Description |
|---------|-------------|
| **ID** | TC-009-01 |
| **Objectif** | Vérifier la suppression d'un article |
| **Préconditions** | - Un article existe |
| **Étapes** | 1. Cliquer sur "Delete" pour un article<br>2. Confirmer la suppression |
| **Résultat attendu** | - L'article disparaît de la liste<br>- Notification "Post deleted successfully" |
| **Priorité** | Haute |

#### TC-009-02 : Annulation de la suppression d'article
| Élément | Description |
|---------|-------------|
| **ID** | TC-009-02 |
| **Objectif** | Vérifier que l'annulation préserve l'article |
| **Préconditions** | - Un article existe |
| **Étapes** | 1. Cliquer sur "Delete"<br>2. Cliquer sur "Cancel" dans la confirmation |
| **Résultat attendu** | L'article reste dans la liste |
| **Priorité** | Moyenne |

---

# Suite de Tests 3 : Statistiques (Statistics)

## US-010 : Consultation des statistiques générales

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** voir les statistiques globales du blog,  
> **Afin de** comprendre l'activité de ma plateforme.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-010-1 | La section Statistics est accessible via la navigation | Haute |
| CA-010-2 | Le nombre total d'utilisateurs est affiché | Haute |
| CA-010-3 | Le nombre total d'articles est affiché | Haute |
| CA-010-4 | L'utilisateur le plus actif est identifié | Moyenne |
| CA-010-5 | Le nombre de posts par utilisateur est affiché | Moyenne |
| CA-010-6 | La liste des articles récents est affichée | Moyenne |

### Cas de Test

#### TC-010-01 : Affichage du nombre total d'utilisateurs
| Élément | Description |
|---------|-------------|
| **ID** | TC-010-01 |
| **Objectif** | Vérifier l'affichage du compteur d'utilisateurs |
| **Préconditions** | - Plusieurs utilisateurs existent |
| **Étapes** | 1. Naviguer vers la section Statistics |
| **Résultat attendu** | Le nombre total d'utilisateurs est affiché correctement |
| **Priorité** | Haute |

#### TC-010-02 : Affichage du nombre total d'articles
| Élément | Description |
|---------|-------------|
| **ID** | TC-010-02 |
| **Objectif** | Vérifier l'affichage du compteur d'articles |
| **Préconditions** | - Plusieurs articles existent |
| **Étapes** | 1. Naviguer vers Statistics |
| **Résultat attendu** | Le nombre total d'articles est affiché correctement |
| **Priorité** | Haute |

#### TC-010-03 : Identification de l'utilisateur le plus actif
| Élément | Description |
|---------|-------------|
| **ID** | TC-010-03 |
| **Objectif** | Vérifier l'identification du top contributeur |
| **Préconditions** | - Plusieurs utilisateurs avec des nombres de posts différents |
| **Étapes** | 1. Naviguer vers Statistics<br>2. Observer la section "Most Active" |
| **Résultat attendu** | L'utilisateur avec le plus de posts est identifié avec son nombre de posts |
| **Priorité** | Moyenne |

#### TC-010-04 : Affichage des posts par utilisateur
| Élément | Description |
|---------|-------------|
| **ID** | TC-010-04 |
| **Objectif** | Vérifier l'affichage de la répartition des posts |
| **Préconditions** | - Plusieurs utilisateurs avec des posts existent |
| **Étapes** | 1. Naviguer vers Statistics<br>2. Observer la liste "Posts per User" |
| **Résultat attendu** | Chaque utilisateur est listé avec son nombre de posts |
| **Priorité** | Moyenne |

#### TC-010-05 : Affichage des articles récents
| Élément | Description |
|---------|-------------|
| **ID** | TC-010-05 |
| **Objectif** | Vérifier l'affichage des derniers articles |
| **Préconditions** | - Au moins 5 articles existent |
| **Étapes** | 1. Naviguer vers Statistics<br>2. Observer la liste "Recent Posts" |
| **Résultat attendu** | Les 5 derniers articles sont listés avec titre et auteur |
| **Priorité** | Moyenne |

---

## US-011 : Rafraîchissement des statistiques

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** pouvoir rafraîchir les statistiques,  
> **Afin de** voir les données les plus récentes.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-011-1 | Un bouton "Refresh" est disponible dans la section Statistics | Haute |
| CA-011-2 | Les statistiques sont mises à jour lors du clic | Haute |
| CA-011-3 | Un indicateur de chargement s'affiche pendant la mise à jour | Basse |

### Cas de Test

#### TC-011-01 : Rafraîchissement des statistiques
| Élément | Description |
|---------|-------------|
| **ID** | TC-011-01 |
| **Objectif** | Vérifier le fonctionnement du rafraîchissement |
| **Préconditions** | - Section Statistics affichée |
| **Étapes** | 1. Noter les statistiques actuelles<br>2. Dans un autre onglet, créer un nouvel article<br>3. Revenir et cliquer sur le bouton "Refresh" |
| **Résultat attendu** | Les statistiques sont mises à jour pour refléter le nouvel article |
| **Priorité** | Haute |

#### TC-011-02 : Affichage du chargement
| Élément | Description |
|---------|-------------|
| **ID** | TC-011-02 |
| **Objectif** | Vérifier l'indicateur de chargement |
| **Préconditions** | - Section Statistics affichée |
| **Étapes** | 1. Cliquer sur "Refresh"<br>2. Observer l'interface pendant le chargement |
| **Résultat attendu** | Un message "Loading statistics" s'affiche brièvement |
| **Priorité** | Basse |

---

## US-012 : Gestion des états vides dans les statistiques

### User Story
> **En tant qu'** administrateur du blog,  
> **Je veux** voir des messages appropriés quand il n'y a pas de données,  
> **Afin de** comprendre l'état actuel de la plateforme.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-012-1 | Si aucun utilisateur n'existe, "N/A" est affiché pour l'utilisateur le plus actif | Moyenne |
| CA-012-2 | Si aucun post n'existe, "No posts yet" est affiché | Moyenne |
| CA-012-3 | Les compteurs affichent 0 quand approprié | Haute |

### Cas de Test

#### TC-012-01 : Statistiques avec base vide
| Élément | Description |
|---------|-------------|
| **ID** | TC-012-01 |
| **Objectif** | Vérifier l'affichage des statistiques sans données |
| **Préconditions** | - Base de données vide |
| **Étapes** | 1. Naviguer vers Statistics |
| **Résultat attendu** | - Total Users: 0<br>- Total Posts: 0<br>- Most Active: N/A<br>- Messages "No users yet" et "No posts yet" |
| **Priorité** | Moyenne |

#### TC-012-02 : Utilisateur le plus actif sans posts
| Élément | Description |
|---------|-------------|
| **ID** | TC-012-02 |
| **Objectif** | Vérifier l'affichage quand des utilisateurs existent mais sans posts |
| **Préconditions** | - Des utilisateurs existent mais aucun post |
| **Étapes** | 1. Naviguer vers Statistics |
| **Résultat attendu** | L'utilisateur le plus actif affiche "N/A" ou le premier utilisateur avec 0 posts |
| **Priorité** | Moyenne |

---

# Tests d'Intégration Cross-Sections

## US-013 : Cohérence des données entre sections

### User Story
> **En tant qu'** utilisateur de l'application,  
> **Je veux** que les données soient cohérentes entre toutes les sections,  
> **Afin de** avoir confiance dans l'intégrité des informations.

### Critères d'Acceptation
| ID | Critère | Priorité |
|----|---------|----------|
| CA-013-1 | La création d'un utilisateur met à jour le compteur dans Statistics | Haute |
| CA-013-2 | La création d'un post met à jour le compteur dans Statistics | Haute |
| CA-013-3 | La suppression d'un utilisateur met à jour Posts et Statistics | Haute |
| CA-013-4 | Le menu déroulant des auteurs se met à jour après création d'utilisateur | Haute |

### Cas de Test

#### TC-013-01 : Synchronisation création utilisateur
| Élément | Description |
|---------|-------------|
| **ID** | TC-013-01 |
| **Objectif** | Vérifier la mise à jour des statistiques après création d'utilisateur |
| **Préconditions** | - Application démarrée |
| **Étapes** | 1. Noter le nombre d'utilisateurs dans Statistics<br>2. Créer un nouvel utilisateur dans Users<br>3. Retourner à Statistics et rafraîchir |
| **Résultat attendu** | Le compteur d'utilisateurs est incrémenté de 1 |
| **Priorité** | Haute |

#### TC-013-02 : Synchronisation création post
| Élément | Description |
|---------|-------------|
| **ID** | TC-013-02 |
| **Objectif** | Vérifier la mise à jour des statistiques après création de post |
| **Préconditions** | - Au moins un utilisateur existe |
| **Étapes** | 1. Noter le nombre de posts dans Statistics<br>2. Créer un nouvel article dans Posts<br>3. Retourner à Statistics et rafraîchir |
| **Résultat attendu** | Le compteur de posts est incrémenté de 1 |
| **Priorité** | Haute |

#### TC-013-03 : Mise à jour du sélecteur d'auteurs
| Élément | Description |
|---------|-------------|
| **ID** | TC-013-03 |
| **Objectif** | Vérifier que les nouveaux utilisateurs apparaissent dans le sélecteur |
| **Préconditions** | - Section Posts affichée |
| **Étapes** | 1. Ouvrir le formulaire de création de post<br>2. Noter les auteurs disponibles<br>3. Créer un nouvel utilisateur<br>4. Ouvrir à nouveau le formulaire de création de post |
| **Résultat attendu** | Le nouvel utilisateur apparaît dans la liste des auteurs |
| **Priorité** | Haute |

---

# Annexe A : Matrice de Traçabilité

| User Story | Critères d'Acceptation | Cas de Test |
|------------|----------------------|-------------|
| US-001 | CA-001-1 à CA-001-6 | TC-001-01, TC-001-02 |
| US-002 | CA-002-1 à CA-002-8 | TC-002-01 à TC-002-05 |
| US-003 | CA-003-1 à CA-003-4 | TC-003-01, TC-003-02 |
| US-004 | CA-004-1 à CA-004-5 | TC-004-01 à TC-004-03 |
| US-005 | CA-005-1 à CA-005-8 | TC-005-01 à TC-005-04 |
| US-006 | CA-006-1 à CA-006-7 | TC-006-01 à TC-006-04 |
| US-007 | CA-007-1 à CA-007-6 | TC-007-01 à TC-007-03 |
| US-008 | CA-008-1 à CA-008-7 | TC-008-01 à TC-008-04 |
| US-009 | CA-009-1 à CA-009-4 | TC-009-01, TC-009-02 |
| US-010 | CA-010-1 à CA-010-6 | TC-010-01 à TC-010-05 |
| US-011 | CA-011-1 à CA-011-3 | TC-011-01, TC-011-02 |
| US-012 | CA-012-1 à CA-012-3 | TC-012-01, TC-012-02 |
| US-013 | CA-013-1 à CA-013-4 | TC-013-01 à TC-013-03 |

---

# Annexe B : Résumé des Suites de Tests

| Suite | Section | Nombre de US | Nombre de TC | Priorité |
|-------|---------|--------------|--------------|----------|
| Suite 1 | Users | 4 | 12 | Haute |
| Suite 2 | Posts | 5 | 15 | Haute |
| Suite 3 | Statistics | 3 | 9 | Moyenne |
| **Total** | - | **13** | **39** | - |

---

# Annexe C : Endpoints API Testés

| Méthode | Endpoint | Description | Suite |
|---------|----------|-------------|-------|
| GET | /api/users | Liste des utilisateurs | Suite 1 |
| GET | /api/users/{id} | Détails utilisateur | Suite 1 |
| POST | /api/users | Création utilisateur | Suite 1 |
| DELETE | /api/users/{id} | Suppression utilisateur | Suite 1 |
| GET | /api/posts | Liste des articles | Suite 2 |
| GET | /api/posts/{id} | Détails article | Suite 2 |
| POST | /api/posts | Création article | Suite 2 |
| PUT | /api/posts/{id} | Modification article | Suite 2 |
| DELETE | /api/posts/{id} | Suppression article | Suite 2 |
| GET | /api/stats | Statistiques | Suite 3 |
| GET | /api/health | Vérification santé | Toutes |
