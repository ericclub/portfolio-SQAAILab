*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# SQAAILab – User Stories (API Blog Flask + Interface d'administration)

## Table des matières
1. [Périmètre du produit](#périmètre-du-produit)
2. [Personas](#personas)
3. [Hypothèses et contraintes](#hypothèses-et-contraintes)
4. [Correspondance avec la pyramide de tests (recommandée)](#correspondance-avec-la-pyramide-de-tests-recommandée)
5. [Fonctionnalité : Santé de l'API](#fonctionnalité--santé-de-lapi)
6. [Fonctionnalité : Utilisateurs (CRUD)](#fonctionnalité--utilisateurs-crud)
7. [Fonctionnalité : Articles (CRUD)](#fonctionnalité--articles-crud)
8. [Fonctionnalité : Tableau de bord des statistiques (lecture)](#fonctionnalité--tableau-de-bord-des-statistiques-lecture)
9. [Fonctionnalité : Interface d'administration (E2E)](#fonctionnalité--interface-dadministration-e2e)
10. [Critères d'acceptation non fonctionnels / transversaux](#critères-dacceptation-non-fonctionnels--transversaux)

---

## Périmètre du produit
Le système fournit :
- Une API REST pour gérer les Utilisateurs et les Articles (billets de blog).
- Une interface d'administration légère (page HTML unique + JavaScript) qui appelle l'API.
- Une vue Statistiques résumant les totaux.

## Personas
- **Administrateur** : gère les utilisateurs et les articles via l'interface d'administration.
- **Consommateur de l'API (QA/Développeur)** : teste directement l'API REST (curl/Postman/automatisation).
- **Partie prenante (Stakeholder)** : consulte les statistiques globales pour valider l'activité de la plateforme.

## Hypothèses et contraintes
- Le backend s'exécute sur `http://localhost:5000`.
- Chemin de base de l'API : `/api`.
- Les tables de la base de données sont créées automatiquement au démarrage du backend.
- Aucune authentification/autorisation n'est implémentée (prototype réservé à l'administrateur).
- Validation implémentée :
  - Champs requis manquants → HTTP 400
  - Nom d'utilisateur/email en doublon → HTTP 409
  - Ressource introuvable → HTTP 404
  - Erreur serveur → HTTP 500
- Règles de données :
  - `User.username` est unique.
  - `User.email` est unique.
  - `Post.user_id` doit référencer un utilisateur existant.
  - La suppression d'un utilisateur supprime ses articles (cascade).

---

## Correspondance avec la pyramide de tests (recommandée)
Le **principe de la pyramide de tests** suggère : **beaucoup de tests unitaires**, **moins de tests d'intégration**, et **très peu de tests de bout en bout (e2e)**.

- **Tests unitaires** : tests rapides pour la validation/sérialisation/règles métier pures (pas de HTTP, pas de vraie base de données).
- **Tests d'intégration** : route Flask + requête/réponse + comportement de la base de données (couvre la majorité des stories ici).
- **Tests E2E** : flux de l'interface d'administration basé sur le navigateur, appelant la vraie API (les plus lents, à garder minimal).

| Story / NFR | Type de test principal recommandé | Également utile (à garder léger) |
|---|---|---|
| HLTH-01 — Vérifier la disponibilité de l'API | Intégration (contrat HTTP : `/api/health`) | Unitaire (le gestionnaire de santé retourne la forme JSON attendue) |
| USR-01 — Créer un utilisateur | Intégration (POST + BD + unicité + mot de passe non retourné) | Unitaire (validation des champs requis ; la sérialisation de la réponse exclut le mot de passe/hash) |
| USR-02 — Lister les utilisateurs | Intégration (GET + lignes BD → JSON) | Unitaire (sérialisation/ordre des utilisateurs si implémenté séparément) |
| USR-03 — Consulter un utilisateur par ID | Intégration (GET + comportement 200/404) | Unitaire (parsing d'ID / mapping non-trouvé si implémenté comme helpers) |
| USR-04 — Supprimer un utilisateur (cascade sur les articles) | Intégration (DELETE + cascade BD + comportement 404) | Unitaire (aucun requis au-delà de la logique des helpers ; la cascade est une préoccupation BD/intégration) |
| PST-01 — Créer un article | Intégration (POST + FK utilisateur existant + écriture BD) | Unitaire (validation des champs requis ; logique de valeur par défaut de « published » ; forme de sérialisation) |
| PST-02 — Lister tous les articles | Intégration (GET + ordre BD) | Unitaire (fonction de tri si extraite) |
| PST-03 — Lister uniquement les articles publiés | Intégration (GET avec paramètre de requête + filtre BD) | Unitaire (parsing du paramètre de requête ; prédicat de filtre si extrait) |
| PST-04 — Consulter un article par ID | Intégration (GET + comportement 200/404) | Unitaire (mapping non-trouvé si extrait) |
| PST-05 — Mettre à jour un article | Intégration (PUT + mise à jour BD + `updated_at` rafraîchi) | Unitaire (logique de fusion/patch pour les champs autorisés si implémentée séparément) |
| PST-06 — Supprimer un article | Intégration (DELETE + suppression BD + comportement 404) | Unitaire (aucun requis au-delà de la logique des helpers) |
| STS-01 — Consulter les statistiques globales | Intégration (GET + les agrégats reflètent l'état de la BD) | Unitaire (fonction d'agrégation des statistiques si séparée de la couche BD) |
| NFR-01 — Réponses JSON et codes HTTP | Intégration (contrat de fumée sur tous les endpoints) | Unitaire (le gestionnaire d'erreurs mappe les exceptions → JSON + statut corrects) |
| NFR-02 — CORS activé pour l'interface d'administration | Intégration (vérifier les en-têtes CORS sur les réponses de l'API) | E2E (un seul test navigateur prouvant que l'UI peut appeler l'API) |
| NFR-03 — La gestion des erreurs ne corrompt pas la session | Intégration (forcer une erreur en cours de transaction ; vérifier le rollback) | Unitaire (le wrapper de transaction appelle rollback en cas d'exception si extrait) |

La couverture E2E est volontairement limitée à deux stories de chemin critique :
- E2E-01 — L'interface d'administration se charge et affiche les statistiques en direct
- E2E-02 — L'administrateur peut créer un utilisateur puis créer un article via l'interface

---

## Fonctionnalité : Santé de l'API

### Story HLTH-01 — Vérifier la disponibilité de l'API
**User Story**
En tant que Consommateur de l'API (QA/Développeur), je veux vérifier le endpoint de santé, afin de confirmer que l'API est en cours d'exécution avant d'exécuter des tests.

**Critères d'acceptation**
Scénario : Le contrôle de santé retourne une réponse OK
- Étant donné que le serveur backend est en cours d'exécution
- Quand j'envoie une requête GET vers `/api/health`
- Alors le code de statut de la réponse est 200
- Et le corps de la réponse contient `status: "ok"` et un `message` non vide

**Cas de test**
- TC-HLTH-01 (Positif) : Démarrer le backend ; appeler `GET /api/health` ; attendre 200 et les clés JSON `status`, `message`.
- TC-HLTH-02 (Négatif) : Arrêter le backend ; appeler `GET /api/health` ; attendre un échec réseau/de connexion côté client.

---

## Fonctionnalité : Utilisateurs (CRUD)

### Story USR-01 — Créer un utilisateur
**User Story**
En tant qu'Administrateur, je veux créer un utilisateur avec un nom d'utilisateur, un email et un mot de passe, afin que l'utilisateur puisse être référencé comme auteur d'articles.

**Critères d'acceptation**
Scénario : Créer un utilisateur avec une saisie valide
- Étant donné un nom d'utilisateur et un email qui n'existent pas déjà
- Quand j'envoie une requête POST vers `/api/users` avec `username`, `email` et `password`
- Alors le code de statut de la réponse est 201
- Et la réponse contient un objet `user` avec un `id`, `username`, `email`, et `created_at`
- Et l'utilisateur retourné n'expose pas le mot de passe ni son hash

Scénario : Rejeter les champs requis manquants
- Étant donné que la charge utile de la requête ne contient pas `username`, `email` ou `password`
- Quand j'envoie une requête POST vers `/api/users`
- Alors le code de statut de la réponse est 400
- Et la réponse contient `error: "Missing required fields"`

Scénario : Rejeter un nom d'utilisateur en double
- Étant donné qu'un utilisateur existe déjà avec le même nom d'utilisateur
- Quand j'envoie une requête POST vers `/api/users` en utilisant ce nom d'utilisateur
- Alors le code de statut de la réponse est 409
- Et la réponse contient `error: "Username already exists"`

Scénario : Rejeter un email en double
- Étant donné qu'un utilisateur existe déjà avec le même email
- Quand j'envoie une requête POST vers `/api/users` en utilisant cet email
- Alors le code de statut de la réponse est 409
- Et la réponse contient `error: "Email already exists"`

**Cas de test**
- TC-USR-01 (Positif) : POST un JSON utilisateur valide ; attendre 201 et les champs utilisateur retournés ; s'assurer qu'aucun champ de mot de passe n'est présent.
- TC-USR-02 (Négatif) : POST `{username,email}` sans password ; attendre 400 et l'erreur correcte.
- TC-USR-03 (Négatif) : Créer l'utilisateur A ; POST l'utilisateur B avec le même nom d'utilisateur ; attendre 409.
- TC-USR-04 (Négatif) : Créer l'utilisateur A ; POST l'utilisateur B avec le même email ; attendre 409.

---

### Story USR-02 — Lister les utilisateurs
**User Story**
En tant qu'Administrateur, je veux consulter une liste d'utilisateurs, afin de confirmer qui existe dans le système et d'utiliser leurs ID pour les articles.

**Critères d'acceptation**
Scénario : Récupérer tous les utilisateurs
- Étant donné que le serveur backend est en cours d'exécution
- Quand j'envoie une requête GET vers `/api/users`
- Alors le code de statut de la réponse est 200
- Et la réponse contient un tableau `users`
- Et chaque élément utilisateur contient `id`, `username`, `email`, `created_at`

**Cas de test**
- TC-USR-05 (Positif) : GET `/api/users` ; attendre 200 et le tableau `users`.
- TC-USR-06 (Limite) : Avec zéro utilisateur en BD ; GET `/api/users` ; attendre 200 et `users: []`.

---

### Story USR-03 — Consulter un utilisateur par ID
**User Story**
En tant qu'Administrateur, je veux consulter les détails d'un utilisateur par ID, afin de vérifier que le bon utilisateur existe avant de gérer les articles associés.

**Critères d'acceptation**
Scénario : Récupérer les détails d'un utilisateur avec un ID valide
- Étant donné qu'un utilisateur existe avec l'ID `X`
- Quand j'envoie une requête GET vers `/api/users/X`
- Alors le code de statut de la réponse est 200
- Et la réponse contient `user.id = X`

Scénario : L'utilisateur n'existe pas
- Étant donné qu'aucun utilisateur n'existe avec l'ID `X`
- Quand j'envoie une requête GET vers `/api/users/X`
- Alors le code de statut de la réponse est 404
- Et la réponse contient `error: "Not found"`

**Cas de test**
- TC-USR-07 (Positif) : Créer un utilisateur ; GET `/api/users/{id}` ; attendre 200 et l'id correspondant.
- TC-USR-08 (Négatif) : GET `/api/users/999999` ; attendre 404 et le corps d'erreur.

---

### Story USR-04 — Supprimer un utilisateur
**User Story**
En tant qu'Administrateur, je veux supprimer un utilisateur, afin de retirer les comptes obsolètes et leurs données associées.

**Critères d'acceptation**
Scénario : Supprimer un utilisateur
- Étant donné qu'un utilisateur existe avec l'ID `X`
- Quand j'envoie une requête DELETE vers `/api/users/X`
- Alors le code de statut de la réponse est 200
- Et la réponse contient `message: "User deleted"`

Scénario : Suppression en cascade des articles de l'utilisateur
- Étant donné qu'un utilisateur existe avec l'ID `X` et qu'il a des articles
- Quand je supprime l'utilisateur avec DELETE `/api/users/X`
- Alors l'utilisateur est retiré
- Et les articles de l'utilisateur sont retirés de la base de données

Scénario : Supprimer un utilisateur inexistant
- Étant donné qu'aucun utilisateur n'existe avec l'ID `X`
- Quand j'envoie une requête DELETE vers `/api/users/X`
- Alors le code de statut de la réponse est 404

**Cas de test**
- TC-USR-09 (Positif) : Créer un utilisateur ; DELETE `/api/users/{id}` ; attendre 200 ; puis GET `/api/users/{id}` retourne 404.
- TC-USR-10 (Intégrité des données) : Créer un utilisateur ; créer un article pour cet utilisateur ; supprimer l'utilisateur ; puis GET `/api/posts/{postId}` retourne 404.
- TC-USR-11 (Négatif) : DELETE `/api/users/999999` ; attendre 404.

---

## Fonctionnalité : Articles (CRUD)

### Story PST-01 — Créer un article
**User Story**
En tant qu'Administrateur, je veux créer un article avec un titre, un contenu, un auteur (ID utilisateur), et un indicateur de publication, afin d'ajouter du contenu de blog au système.

**Critères d'acceptation**
Scénario : Créer un article avec une saisie valide
- Étant donné qu'un utilisateur existe avec l'ID `U`
- Quand j'envoie une requête POST vers `/api/posts` avec `title`, `content`, et `user_id = U`
- Alors le code de statut de la réponse est 201
- Et la réponse contient un objet `post` avec `id`, `title`, `content`, `published`, `author`, `created_at`, `updated_at`

Scénario : Rejeter les champs requis manquants
- Étant donné que la charge utile de la requête ne contient pas `title`, `content` ou `user_id`
- Quand j'envoie une requête POST vers `/api/posts`
- Alors le code de statut de la réponse est 400
- Et la réponse contient `error: "Missing required fields"`

Scénario : Rejeter un auteur inconnu
- Étant donné qu'aucun utilisateur n'existe avec l'ID `U`
- Quand j'envoie une requête POST vers `/api/posts` avec `user_id = U`
- Alors le code de statut de la réponse est 404
- Et la réponse contient `error: "User not found"`

**Cas de test**
- TC-PST-01 (Positif) : Créer un utilisateur ; POST un JSON d'article valide ; attendre 201 et le nom d'utilisateur de l'auteur retourné.
- TC-PST-02 (Négatif) : POST sans titre ; attendre 400.
- TC-PST-03 (Négatif) : POST avec un user_id absent de la BD ; attendre 404 et `User not found`.

---

### Story PST-02 — Lister tous les articles
**User Story**
En tant qu'Administrateur, je veux lister tous les articles (brouillons et publiés), afin de revoir le contenu et de gérer les suppressions.

**Critères d'acceptation**
Scénario : Récupérer tous les articles
- Étant donné que le serveur backend est en cours d'exécution
- Quand j'envoie une requête GET vers `/api/posts`
- Alors le code de statut de la réponse est 200
- Et la réponse contient un tableau `posts` trié par `created_at` décroissant

**Cas de test**
- TC-PST-04 (Positif) : Créer 2 articles à des moments différents ; GET `/api/posts` ; attendre le plus récent en premier.
- TC-PST-05 (Limite) : Avec zéro article ; GET `/api/posts` ; attendre 200 et `posts: []`.

---

### Story PST-03 — Lister uniquement les articles publiés
**User Story**
En tant que Partie prenante, je veux lister uniquement les articles publiés, afin de revoir ce qui est considéré comme du contenu public.

**Critères d'acceptation**
Scénario : Filtrer sur les articles publiés
- Étant donné qu'il existe à la fois des articles brouillons et publiés
- Quand j'envoie une requête GET vers `/api/posts?published=true`
- Alors le code de statut de la réponse est 200
- Et chaque article retourné a `published = true`

**Cas de test**
- TC-PST-06 (Positif) : Créer un brouillon et un article publié ; GET `/api/posts?published=true` ; attendre uniquement le publié.
- TC-PST-07 (Limite) : S'il n'existe aucun article publié ; GET `/api/posts?published=true` ; attendre `posts: []`.

---

### Story PST-04 — Consulter un article par ID
**User Story**
En tant qu'Administrateur, je veux consulter un article par ID, afin de vérifier son contenu et son statut.

**Critères d'acceptation**
Scénario : Récupérer les détails d'un article avec un ID valide
- Étant donné qu'un article existe avec l'ID `P`
- Quand j'envoie une requête GET vers `/api/posts/P`
- Alors le code de statut de la réponse est 200
- Et la réponse contient `post.id = P`

Scénario : L'article n'existe pas
- Étant donné qu'aucun article n'existe avec l'ID `P`
- Quand j'envoie une requête GET vers `/api/posts/P`
- Alors le code de statut de la réponse est 404
- Et la réponse contient `error: "Not found"`

**Cas de test**
- TC-PST-08 (Positif) : Créer un article ; GET `/api/posts/{id}` ; attendre 200 et l'id correspondant.
- TC-PST-09 (Négatif) : GET `/api/posts/999999` ; attendre 404.

---

### Story PST-05 — Mettre à jour un article
**User Story**
En tant qu'Administrateur, je veux mettre à jour le titre/contenu/statut de publication d'un article, afin de corriger le contenu et de gérer la publication.

**Critères d'acceptation**
Scénario : Mettre à jour un ou plusieurs champs
- Étant donné qu'un article existe avec l'ID `P`
- Quand j'envoie une requête PUT vers `/api/posts/P` avec un ou plusieurs de `title`, `content`, `published`
- Alors le code de statut de la réponse est 200
- Et l'article retourné reflète les champs mis à jour
- Et `updated_at` est rafraîchi

Scénario : Mettre à jour un article inexistant
- Étant donné qu'aucun article n'existe avec l'ID `P`
- Quand j'envoie une requête PUT vers `/api/posts/P`
- Alors le code de statut de la réponse est 404

**Cas de test**
- TC-PST-10 (Positif) : Créer un article en brouillon ; PUT `/api/posts/{id}` `{published:true}` ; attendre 200 et published à true.
- TC-PST-11 (Positif) : PUT met à jour le titre et le contenu ; attendre que les champs soient modifiés.
- TC-PST-12 (Négatif) : PUT `/api/posts/999999` ; attendre 404.

---

### Story PST-06 — Supprimer un article
**User Story**
En tant qu'Administrateur, je veux supprimer un article, afin de retirer un contenu obsolète ou incorrect.

**Critères d'acceptation**
Scénario : Supprimer un article
- Étant donné qu'un article existe avec l'ID `P`
- Quand j'envoie une requête DELETE vers `/api/posts/P`
- Alors le code de statut de la réponse est 200
- Et la réponse contient `message: "Post deleted"`

Scénario : Supprimer un article inexistant
- Étant donné qu'aucun article n'existe avec l'ID `P`
- Quand j'envoie une requête DELETE vers `/api/posts/P`
- Alors le code de statut de la réponse est 404

**Cas de test**
- TC-PST-13 (Positif) : Créer un article ; DELETE `/api/posts/{id}` ; attendre 200 ; puis GET `/api/posts/{id}` retourne 404.
- TC-PST-14 (Négatif) : DELETE `/api/posts/999999` ; attendre 404.

---

## Fonctionnalité : Tableau de bord des statistiques (lecture)

### Story STS-01 — Consulter les statistiques globales
**User Story**
En tant que Partie prenante, je veux consulter les compteurs globaux d'utilisateurs et d'articles, afin d'évaluer rapidement l'activité de la plateforme.

**Critères d'acceptation**
Scénario : Récupérer les statistiques globales
- Étant donné que le serveur backend est en cours d'exécution
- Quand j'envoie une requête GET vers `/api/stats`
- Alors le code de statut de la réponse est 200
- Et la réponse contient les champs numériques `total_users`, `total_posts`, `published_posts`

Scénario : Les statistiques reflètent les données actuelles
- Étant donné que je crée ou supprime des utilisateurs/articles
- Quand je demande `/api/stats`
- Alors les totaux retournés correspondent à l'état de la base de données

**Cas de test**
- TC-STS-01 (Positif) : Avec une BD vide ; GET `/api/stats` ; attendre des zéros.
- TC-STS-02 (Exactitude des données) : Créer 2 utilisateurs, 3 articles (2 publiés) ; GET `/api/stats` ; attendre les totaux (2, 3, 2).
- TC-STS-03 (Impact de la cascade) : Créer un utilisateur + un article ; supprimer l'utilisateur ; GET `/api/stats` ; attendre des compteurs diminués en conséquence.

---

## Fonctionnalité : Interface d'administration (E2E)

Ces stories de bout en bout restent volontairement **très peu nombreuses** (selon la pyramide de tests). La majorité du comportement doit être validée via des **tests d'intégration** sur l'API ; l'E2E est réservé pour prouver que l'interface d'administration peut piloter le chemin critique dans un vrai navigateur.

### Story E2E-01 — L'interface d'administration se charge et affiche les statistiques en direct
**User Story**
En tant qu'Administrateur/Partie prenante, je veux ouvrir l'interface d'administration et voir les statistiques en direct, afin de confirmer rapidement que le chemin UI-vers-API fonctionne.

**Critères d'acceptation**
Scénario : L'UI se charge et affiche les statistiques provenant de l'API
- Étant donné que le serveur backend est en cours d'exécution sur `http://localhost:5000`
- Et que l'interface d'administration `index.html` est ouverte dans un navigateur
- Quand l'onglet Statistiques est actif
- Alors l'UI demande `GET /api/stats`
- Et elle affiche des valeurs numériques pour Utilisateurs, Total des articles, et Articles publiés

Scénario : Le rafraîchissement met à jour les statistiques affichées
- Étant donné que l'onglet Statistiques est actif
- Quand je clique sur le bouton Rafraîchir
- Alors l'UI redemande `GET /api/stats`
- Et les valeurs affichées correspondent à la dernière réponse de l'API

**Cas de test (E2E)**
- TC-E2E-01 (Fumée) : Démarrer le backend ; ouvrir `index.html` ; attendre que les cartes Statistiques affichent des nombres (pas « Loading error »).
- TC-E2E-02 (Rafraîchissement) : Créer ou supprimer des données via l'API (ou via l'UI dans un autre onglet) ; cliquer sur Rafraîchir ; attendre que les valeurs des statistiques changent en conséquence.

---

### Story E2E-02 — L'administrateur peut créer un utilisateur puis créer un article via l'interface
**User Story**
En tant qu'Administrateur, je veux créer un utilisateur puis créer un article pour cet utilisateur dans l'interface d'administration, afin de compléter le flux principal de création de contenu.

**Critères d'acceptation**
Scénario : Créer un utilisateur via l'UI et le voir listé
- Étant donné que le serveur backend est en cours d'exécution
- Quand j'ouvre l'onglet Utilisateurs
- Et que je soumets le formulaire de création d'utilisateur avec un nom d'utilisateur, un email et un mot de passe uniques
- Alors l'UI affiche un message de succès
- Et le nouvel utilisateur apparaît dans la liste des utilisateurs avec un ID visible

Scénario : Créer un article pour le nouvel utilisateur via l'UI et le voir listé
- Étant donné que l'utilisateur existe
- Quand j'ouvre l'onglet Articles
- Alors la liste déroulante Auteur contient l'utilisateur créé
- Quand je soumets le formulaire de création d'article avec le titre/contenu/auteur et un statut sélectionné
- Alors l'UI affiche un message de succès
- Et le nouvel article apparaît dans la liste des articles avec le titre correct et le badge Publié/Brouillon

**Cas de test (E2E)**
- TC-E2E-03 (Chemin critique) : Ouvrir l'UI ; créer un utilisateur ; naviguer vers Articles ; créer un article en Brouillon ; vérifier qu'il apparaît avec le badge Brouillon.
- TC-E2E-04 (Variante Publié) : Créer un article en Publié ; vérifier qu'il apparaît avec le badge Publié.

---

## Critères d'acceptation non fonctionnels / transversaux
Ces critères s'appliquent à l'ensemble des stories de l'API ci-dessus.

### NFR-01 — Réponses JSON et codes HTTP
Scénario : Tous les endpoints retournent du JSON
- Étant donné qu'une requête API est traitée
- Quand l'API répond
- Alors le type de contenu de la réponse est JSON
- Et le code de statut correspond au comportement documenté (200/201/400/404/409/500)

### NFR-02 — CORS activé pour l'interface d'administration
Scénario : Un frontend basé sur navigateur peut appeler l'API
- Étant donné que l'interface d'administration est ouverte dans un navigateur
- Quand elle appelle l'API sur `http://localhost:5000/api/...`
- Alors le navigateur ne bloque pas les requêtes à cause de CORS

### NFR-03 — La gestion des erreurs ne corrompt pas la session
Scénario : Une erreur interne déclenche un rollback
- Étant donné qu'une erreur serveur interne se produit pendant une transaction BD
- Quand le serveur retourne HTTP 500
- Alors la session BD est annulée (rollback)

---

## 🇬🇧 English

# SQAAILab – User Stories (Flask Blog API + Admin Interface)

## Table of Contents
1. [Product Scope](#product-scope)
2. [Personas](#personas)
3. [Assumptions & Constraints](#assumptions--constraints)
4. [Test Pyramid Mapping (Recommended)](#test-pyramid-mapping-recommended)
5. [Feature: API Health](#feature-api-health)
6. [Feature: Users (CRUD)](#feature-users-crud)
7. [Feature: Posts (CRUD)](#feature-posts-crud)
8. [Feature: Statistics Dashboard (Read)](#feature-statistics-dashboard-read)
9. [Feature: Admin UI (E2E)](#feature-admin-ui-e2e)
10. [Non-Functional / Cross-Cutting Acceptance Criteria](#non-functional--cross-cutting-acceptance-criteria)

---

## Product Scope
The system provides:
- A REST API to manage Users and Posts (blog articles).
- A lightweight Admin UI (single-page HTML + JavaScript) that calls the API.
- A Statistics view summarizing totals.

## Personas
- **Admin**: manages users and posts using the Admin UI.
- **API Consumer (QA/Developer)**: tests the REST API directly (curl/Postman/automation).
- **Stakeholder**: checks global statistics to validate platform activity.

## Assumptions & Constraints
- Backend runs at `http://localhost:5000`.
- API base path: `/api`.
- Database tables are auto-created on backend startup.
- No authentication/authorization is implemented (admin-only prototype).
- Validation implemented:
  - Missing required fields → HTTP 400
  - Duplicate username/email → HTTP 409
  - Resource not found → HTTP 404
  - Server error → HTTP 500
- Data rules:
  - `User.username` is unique.
  - `User.email` is unique.
  - `Post.user_id` must reference an existing user.
  - Deleting a user deletes their posts (cascade).

---

## Test Pyramid Mapping (Recommended)
The **Test Pyramid Principle** suggests: **many unit tests**, **fewer integration tests**, and **very few end-to-end (e2e) tests**.

- **Unit tests**: fast tests for pure validation/serialization/business rules (no HTTP, no real DB).
- **Integration tests**: Flask route + request/response + database behavior (covers most stories here).
- **E2E tests**: browser-based Admin UI flow calling the real API (slowest, keep minimal).

| Story / NFR | Recommended primary test type | Also valuable (keep lean) |
|---|---|---|
| HLTH-01 — Check API availability | Integration (HTTP contract: `/api/health`) | Unit (health handler returns expected JSON shape) |
| USR-01 — Create a user | Integration (POST + DB + uniqueness + password not returned) | Unit (required-field validation; response serialization excludes password/hash) |
| USR-02 — List users | Integration (GET + DB rows → JSON) | Unit (user serialization/ordering if implemented separately) |
| USR-03 — View a user by ID | Integration (GET + 200/404 behavior) | Unit (ID parsing / not-found mapping if implemented as helpers) |
| USR-04 — Delete a user (cascade posts) | Integration (DELETE + DB cascade + 404 behavior) | Unit (none required beyond helper logic; cascade is a DB/integration concern) |
| PST-01 — Create a post | Integration (POST + FK user exists + DB write) | Unit (required-field validation; published default logic; serialization shape) |
| PST-02 — List all posts | Integration (GET + DB ordering) | Unit (ordering function if extracted) |
| PST-03 — List published posts only | Integration (GET with query param + DB filter) | Unit (query-param parsing; filter predicate if extracted) |
| PST-04 — View a post by ID | Integration (GET + 200/404 behavior) | Unit (not-found mapping if extracted) |
| PST-05 — Update a post | Integration (PUT + DB update + `updated_at` refreshed) | Unit (merge/patch logic for allowed fields if implemented separately) |
| PST-06 — Delete a post | Integration (DELETE + DB delete + 404 behavior) | Unit (none required beyond helper logic) |
| STS-01 — View global statistics | Integration (GET + aggregates reflect DB state) | Unit (stat aggregation function if separated from DB layer) |
| NFR-01 — JSON responses and HTTP codes | Integration (smoke contract across endpoints) | Unit (error handler maps exceptions → correct JSON + status) |
| NFR-02 — CORS enabled for Admin UI | Integration (assert CORS headers on API responses) | E2E (single browser test proving UI can call API) |
| NFR-03 — Error handling does not corrupt session | Integration (force error mid-transaction; assert rollback) | Unit (transaction wrapper calls rollback on exception if extracted) |

E2E coverage is intentionally limited to two critical-path stories:
- E2E-01 — Admin UI loads and shows live statistics
- E2E-02 — Admin can create user then create post via UI

---

## Feature: API Health

### Story HLTH-01 — Check API availability
**User Story**
As an API Consumer (QA/Developer), I want to check the health endpoint, so that I can confirm the API is running before executing tests.

**Acceptance Criteria**
Scenario: Health check returns an OK response
- Given the backend server is running
- When I send a GET request to `/api/health`
- Then the response status code is 200
- And the response body contains `status: "ok"` and a non-empty `message`

**Test Cases**
- TC-HLTH-01 (Positive): Start backend; call `GET /api/health`; expect 200 and JSON keys `status`, `message`.
- TC-HLTH-02 (Negative): Stop backend; call `GET /api/health`; expect network/connection failure at client.

---

## Feature: Users (CRUD)

### Story USR-01 — Create a user
**User Story**
As an Admin, I want to create a user with username, email, and password, so that the user can be referenced as an author for posts.

**Acceptance Criteria**
Scenario: Create user with valid input
- Given a username and email that do not already exist
- When I send a POST request to `/api/users` with `username`, `email`, and `password`
- Then the response status code is 201
- And the response contains a `user` object with an `id`, `username`, `email`, and `created_at`
- And the returned user does not expose the password or password hash

Scenario: Reject missing required fields
- Given the request payload is missing `username` or `email` or `password`
- When I send a POST request to `/api/users`
- Then the response status code is 400
- And the response contains `error: "Missing required fields"`

Scenario: Reject duplicate username
- Given a user already exists with the same username
- When I send a POST request to `/api/users` using that username
- Then the response status code is 409
- And the response contains `error: "Username already exists"`

Scenario: Reject duplicate email
- Given a user already exists with the same email
- When I send a POST request to `/api/users` using that email
- Then the response status code is 409
- And the response contains `error: "Email already exists"`

**Test Cases**
- TC-USR-01 (Positive): POST valid user JSON; expect 201 and returned user fields; ensure no password fields present.
- TC-USR-02 (Negative): POST `{username,email}` missing password; expect 400 and correct error.
- TC-USR-03 (Negative): Create user A; POST user B with same username; expect 409.
- TC-USR-04 (Negative): Create user A; POST user B with same email; expect 409.

---

### Story USR-02 — List users
**User Story**
As an Admin, I want to view a list of users, so that I can confirm who exists in the system and use their IDs for posts.

**Acceptance Criteria**
Scenario: Retrieve all users
- Given the backend server is running
- When I send a GET request to `/api/users`
- Then the response status code is 200
- And the response contains a `users` array
- And each user item contains `id`, `username`, `email`, `created_at`

**Test Cases**
- TC-USR-05 (Positive): GET `/api/users`; expect 200 and `users` array.
- TC-USR-06 (Edge): With zero users in DB; GET `/api/users`; expect 200 and `users: []`.

---

### Story USR-03 — View a user by ID
**User Story**
As an Admin, I want to view user details by ID, so that I can verify the correct user exists before managing related posts.

**Acceptance Criteria**
Scenario: Retrieve user details by valid ID
- Given a user exists with ID `X`
- When I send a GET request to `/api/users/X`
- Then the response status code is 200
- And the response contains `user.id = X`

Scenario: User does not exist
- Given no user exists with ID `X`
- When I send a GET request to `/api/users/X`
- Then the response status code is 404
- And the response contains `error: "Not found"`

**Test Cases**
- TC-USR-07 (Positive): Create a user; GET `/api/users/{id}`; expect 200 and matching id.
- TC-USR-08 (Negative): GET `/api/users/999999`; expect 404 and error body.

---

### Story USR-04 — Delete a user
**User Story**
As an Admin, I want to delete a user, so that I can remove obsolete accounts and their related data.

**Acceptance Criteria**
Scenario: Delete a user
- Given a user exists with ID `X`
- When I send a DELETE request to `/api/users/X`
- Then the response status code is 200
- And the response contains `message: "User deleted"`

Scenario: Cascade delete user posts
- Given a user exists with ID `X` and they have posts
- When I delete the user with DELETE `/api/users/X`
- Then the user is removed
- And the user’s posts are removed from the database

Scenario: Delete a non-existent user
- Given no user exists with ID `X`
- When I send a DELETE request to `/api/users/X`
- Then the response status code is 404

**Test Cases**
- TC-USR-09 (Positive): Create user; DELETE `/api/users/{id}`; expect 200; then GET `/api/users/{id}` returns 404.
- TC-USR-10 (Data integrity): Create user; create post for that user; delete user; then GET `/api/posts/{postId}` returns 404.
- TC-USR-11 (Negative): DELETE `/api/users/999999`; expect 404.

---

## Feature: Posts (CRUD)

### Story PST-01 — Create a post
**User Story**
As an Admin, I want to create a post with a title, content, author (user ID), and published flag, so that I can add blog content to the system.

**Acceptance Criteria**
Scenario: Create post with valid input
- Given a user exists with ID `U`
- When I send a POST request to `/api/posts` with `title`, `content`, and `user_id = U`
- Then the response status code is 201
- And the response contains a `post` object with `id`, `title`, `content`, `published`, `author`, `created_at`, `updated_at`

Scenario: Reject missing required fields
- Given the request payload is missing `title` or `content` or `user_id`
- When I send a POST request to `/api/posts`
- Then the response status code is 400
- And the response contains `error: "Missing required fields"`

Scenario: Reject unknown author
- Given no user exists with ID `U`
- When I send a POST request to `/api/posts` with `user_id = U`
- Then the response status code is 404
- And the response contains `error: "User not found"`

**Test Cases**
- TC-PST-01 (Positive): Create user; POST valid post JSON; expect 201 and author username returned.
- TC-PST-02 (Negative): POST missing title; expect 400.
- TC-PST-03 (Negative): POST with user_id not in DB; expect 404 and `User not found`.

---

### Story PST-02 — List all posts
**User Story**
As an Admin, I want to list all posts (draft and published), so that I can review content and manage deletions.

**Acceptance Criteria**
Scenario: Retrieve all posts
- Given the backend server is running
- When I send a GET request to `/api/posts`
- Then the response status code is 200
- And the response contains a `posts` array ordered by `created_at` descending

**Test Cases**
- TC-PST-04 (Positive): Create 2 posts at different times; GET `/api/posts`; expect newest first.
- TC-PST-05 (Edge): With zero posts; GET `/api/posts`; expect 200 and `posts: []`.

---

### Story PST-03 — List published posts only
**User Story**
As a Stakeholder, I want to list only published posts, so that I can review what is considered public content.

**Acceptance Criteria**
Scenario: Filter to published posts
- Given there are both draft and published posts
- When I send a GET request to `/api/posts?published=true`
- Then the response status code is 200
- And every returned post has `published = true`

**Test Cases**
- TC-PST-06 (Positive): Create one draft and one published post; GET `/api/posts?published=true`; expect only published.
- TC-PST-07 (Edge): If no published posts exist; GET `/api/posts?published=true`; expect `posts: []`.

---

### Story PST-04 — View a post by ID
**User Story**
As an Admin, I want to view a post by ID, so that I can verify its content and status.

**Acceptance Criteria**
Scenario: Retrieve post details by valid ID
- Given a post exists with ID `P`
- When I send a GET request to `/api/posts/P`
- Then the response status code is 200
- And the response contains `post.id = P`

Scenario: Post does not exist
- Given no post exists with ID `P`
- When I send a GET request to `/api/posts/P`
- Then the response status code is 404
- And the response contains `error: "Not found"`

**Test Cases**
- TC-PST-08 (Positive): Create post; GET `/api/posts/{id}`; expect 200 and matching id.
- TC-PST-09 (Negative): GET `/api/posts/999999`; expect 404.

---

### Story PST-05 — Update a post
**User Story**
As an Admin, I want to update a post’s title/content/published status, so that I can correct content and manage publication.

**Acceptance Criteria**
Scenario: Update one or more fields
- Given a post exists with ID `P`
- When I send a PUT request to `/api/posts/P` with any of `title`, `content`, `published`
- Then the response status code is 200
- And the returned post reflects the updated fields
- And `updated_at` is refreshed

Scenario: Update non-existent post
- Given no post exists with ID `P`
- When I send a PUT request to `/api/posts/P`
- Then the response status code is 404

**Test Cases**
- TC-PST-10 (Positive): Create post as draft; PUT `/api/posts/{id}` `{published:true}`; expect 200 and published true.
- TC-PST-11 (Positive): PUT update title and content; expect fields changed.
- TC-PST-12 (Negative): PUT `/api/posts/999999`; expect 404.

---

### Story PST-06 — Delete a post
**User Story**
As an Admin, I want to delete a post, so that I can remove outdated or incorrect content.

**Acceptance Criteria**
Scenario: Delete a post
- Given a post exists with ID `P`
- When I send a DELETE request to `/api/posts/P`
- Then the response status code is 200
- And the response contains `message: "Post deleted"`

Scenario: Delete non-existent post
- Given no post exists with ID `P`
- When I send a DELETE request to `/api/posts/P`
- Then the response status code is 404

**Test Cases**
- TC-PST-13 (Positive): Create post; DELETE `/api/posts/{id}`; expect 200; then GET `/api/posts/{id}` returns 404.
- TC-PST-14 (Negative): DELETE `/api/posts/999999`; expect 404.

---

## Feature: Statistics Dashboard (Read)

### Story STS-01 — View global statistics
**User Story**
As a Stakeholder, I want to view global counts of users and posts, so that I can quickly assess platform activity.

**Acceptance Criteria**
Scenario: Retrieve global statistics
- Given the backend server is running
- When I send a GET request to `/api/stats`
- Then the response status code is 200
- And the response contains numeric fields `total_users`, `total_posts`, `published_posts`

Scenario: Stats reflect current data
- Given I create or delete users/posts
- When I request `/api/stats`
- Then the returned totals match the database state

**Test Cases**
- TC-STS-01 (Positive): With empty DB; GET `/api/stats`; expect zeros.
- TC-STS-02 (Data accuracy): Create 2 users, 3 posts (2 published); GET `/api/stats`; expect totals (2, 3, 2).
- TC-STS-03 (Cascade impact): Create user+post; delete user; GET `/api/stats`; expect counts decreased accordingly.

---

## Feature: Admin UI (E2E)

These end-to-end stories intentionally remain **very small in number** (per the Test Pyramid). Most behavior should be validated via **integration tests** against the API; E2E is reserved for proving the Admin UI can drive the critical path in a real browser.

### Story E2E-01 — Admin UI loads and shows live statistics
**User Story**
As an Admin/Stakeholder, I want to open the Admin UI and see live statistics, so that I can quickly confirm the UI-to-API path is working.

**Acceptance Criteria**
Scenario: UI loads and renders stats from the API
- Given the backend server is running at `http://localhost:5000`
- And the Admin UI `index.html` is opened in a browser
- When the Statistics tab is active
- Then the UI requests `GET /api/stats`
- And it renders numeric values for Users, Total Posts, and Published Posts

Scenario: Refresh updates the displayed stats
- Given the Statistics tab is active
- When I click the Refresh button
- Then the UI re-requests `GET /api/stats`
- And the rendered values match the latest API response

**Test Cases (E2E)**
- TC-E2E-01 (Smoke): Start backend; open `index.html`; expect Stats cards to show numbers (not “Loading error”).
- TC-E2E-02 (Refresh): Create or delete data via API (or via UI in another tab); click Refresh; expect stats values to change accordingly.

---

### Story E2E-02 — Admin can create user then create post via UI
**User Story**
As an Admin, I want to create a user and then create a post for that user in the Admin UI, so that I can complete the primary authoring workflow.

**Acceptance Criteria**
Scenario: Create a user via UI and see it listed
- Given the backend server is running
- When I open the Users tab
- And I submit the Create User form with a unique username, email, and password
- Then the UI shows a success message
- And the new user appears in the User List with a visible ID

Scenario: Create a post for the new user via UI and see it listed
- Given the user exists
- When I open the Posts tab
- Then the Author dropdown contains the created user
- When I submit the Create Post form with title/content/author and a selected status
- Then the UI shows a success message
- And the new post appears in the Post List with the correct title and Published/Draft badge

**Test Cases (E2E)**
- TC-E2E-03 (Critical path): Open UI; create a user; navigate to Posts; create a post as Draft; verify it appears with Draft badge.
- TC-E2E-04 (Published variant): Create a post as Published; verify it appears with Published badge.

---

## Non-Functional / Cross-Cutting Acceptance Criteria
These criteria apply across the API stories above.

### NFR-01 — JSON responses and HTTP codes
Scenario: All endpoints return JSON
- Given any API request is processed
- When the API responds
- Then the response content type is JSON
- And the status code matches the documented behavior (200/201/400/404/409/500)

### NFR-02 — CORS enabled for Admin UI
Scenario: Browser-based frontend can call the API
- Given the Admin UI is opened in a browser
- When it calls the API at `http://localhost:5000/api/...`
- Then the browser does not block requests due to CORS

### NFR-03 — Error handling does not corrupt session
Scenario: Internal error triggers rollback
- Given an internal server error occurs during a DB transaction
- When the server returns HTTP 500
- Then the DB session is rolled back
