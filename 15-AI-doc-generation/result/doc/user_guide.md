*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Flask Blog API – Guide utilisateur technique 

## Table des matières
1. Introduction
2. Aperçu du système
3. Architecture
4. Démarrage
5. Aperçu de l'interface utilisateur
   - Onglet Statistiques
   - Onglet Utilisateurs
   - Onglet Articles
6. Aperçu de l'API backend
7. Workflows CRUD
   - Gestion des utilisateurs
   - Gestion des articles
8. Gestion des erreurs et validation
9. Aperçu du modèle de données
10. Considérations de sécurité
11. Bon à savoir / bonnes pratiques

---

## 1. Introduction
Ce document est un **guide utilisateur** pour l'*interface d'administration Flask Blog API*.  
Il est destiné aux **clients, product owners, analystes QA et autres parties prenantes** souhaitant comprendre le fonctionnement fonctionnel du logiciel.

L'application fournit :
- Une API backend RESTful (Flask + SQLAlchemy)
- Une interface web d'administration légère (HTML + JavaScript)
- Des opérations CRUD complètes pour les utilisateurs et les articles de blog
- Un tableau de bord de statistiques globales

---

## 2. Aperçu du système
Le système est composé de deux parties principales :

- **Backend** : API REST Flask connectée à une base de données MySQL
- **Frontend** : Interface d'administration monopage communiquant via HTTP (JSON)

Cas d'usage typiques :
- Créer et gérer des utilisateurs
- Créer, publier et supprimer des articles de blog
- Consulter les statistiques globales de la plateforme

---

## 3. Architecture

**Frontend (Navigateur)**
- HTML + JavaScript
- Utilise `fetch()` pour appeler les endpoints REST
- Fonctionne indépendamment du backend

**Backend (API Flask)**
- Flask + ORM SQLAlchemy
- Base de données MySQL
- CORS activé pour l'accès du frontend

**Base de données**
- Table Users (utilisateurs)
- Table Posts (articles, liée aux utilisateurs)

---

## 4. Démarrage

### Prérequis
- Python 3.9+
- Base de données MySQL
- Navigateur (Chrome, Edge, Firefox)

### Démarrage du backend
1. Configurer la connexion à la base de données (variable d'environnement ou valeur par défaut)
2. Exécuter :
```bash
python app.py
```
3. Les tables de la base de données sont créées automatiquement au démarrage

### Démarrage du frontend
- Ouvrir `index.html` dans un navigateur
- Le backend doit être en cours d'exécution sur `http://localhost:5000`

---

## 5. Aperçu de l'interface utilisateur

### 📊 Onglet Statistiques
Affiche les métriques de la plateforme en temps réel :
- Nombre total d'utilisateurs
- Nombre total d'articles
- Articles publiés

**Actions**
- Actualiser les statistiques manuellement

**Objectif**
- Surveillance de haut niveau pour les parties prenantes

---

### 👥 Onglet Utilisateurs
Permet une gestion complète des utilisateurs.

**Fonctionnalités**
- Créer un utilisateur (nom d'utilisateur, email, mot de passe)
- Voir tous les utilisateurs
- Supprimer des utilisateurs

**Remarques**
- Le nom d'utilisateur et l'email doivent être uniques
- Supprimer un utilisateur supprime aussi ses articles

---

### 📝 Onglet Articles
Gère les articles de blog.

**Fonctionnalités**
- Créer des articles
- Assigner un auteur (ID utilisateur)
- Statut Brouillon ou Publié
- Voir la liste des articles
- Supprimer des articles

**Remarques**
- Un utilisateur doit exister avant de créer un article
- Seuls les articles publiés comptent comme contenu public

---

## 6. Aperçu de l'API backend

### Vérification de l'état de santé
`GET /api/health`

### Utilisateurs
- `POST /api/users`
- `GET /api/users`
- `GET /api/users/{id}`
- `DELETE /api/users/{id}`

### Articles
- `POST /api/posts`
- `GET /api/posts`
- `GET /api/posts/{id}`
- `PUT /api/posts/{id}`
- `DELETE /api/posts/{id}`

### Statistiques
- `GET /api/stats`

---

## 7. Workflows CRUD

### Utilisateur – Exemple CRUD

**Créer**
```json
POST /api/users
{
  "username": "john",
  "email": "john@email.com",
  "password": "secret"
}
```

**Lire**
```http
GET /api/users
```

**Supprimer**
```http
DELETE /api/users/1
```

---

### Article – Exemple CRUD

**Créer**
```json
POST /api/posts
{
  "title": "My First Post",
  "content": "Hello world",
  "user_id": 1,
  "published": true
}
```

**Lire**
```http
GET /api/posts
```

**Mettre à jour**
```json
PUT /api/posts/1
{
  "published": false
}
```

**Supprimer**
```http
DELETE /api/posts/1
```

---

## 8. Gestion des erreurs et validation
- Champs manquants → HTTP 400
- Nom d'utilisateur/email en double → HTTP 409
- Ressource introuvable → HTTP 404
- Erreur serveur → HTTP 500

Toutes les erreurs renvoient des réponses JSON.

---

## 9. Aperçu du modèle de données

### User (Utilisateur)
- id
- username (unique)
- email (unique)
- password_hash
- created_at

### Post (Article)
- id
- title
- content
- published
- created_at
- updated_at
- user_id (clé étrangère)

---

## 10. Considérations de sécurité
- Les mots de passe sont hachés (Werkzeug)
- Aucune couche d'authentification (prototype réservé aux administrateurs)
- CORS activé (mode développement)
- Pas prêt pour la production sans authentification ni HTTPS

---

## 11. Bon à savoir / bonnes pratiques
- Toujours créer les utilisateurs avant les articles
- Utiliser l'onglet Statistiques pour les tests de fumée (smoke testing)
- Projet idéal pour :
  - S'entraîner à l'automatisation QA
  - Les tests d'API
  - Les scénarios de validation CRUD
- Peut être étendu avec :
  - Authentification (JWT)
  - Contrôle d'accès basé sur les rôles
  - Pagination et recherche

---

**Fin du guide utilisateur**

---

## 🇬🇧 English


# Flask Blog API – Technical User Guide 

## Table of Contents
1. Introduction
2. System Overview
3. Architecture
4. Getting Started
5. User Interface Overview
   - Statistics Tab
   - Users Tab
   - Posts Tab
6. Backend API Overview
7. CRUD Workflows
   - User Management
   - Post Management
8. Error Handling & Validation
9. Data Model Overview
10. Security Considerations
11. Good to Know / Best Practices

---

## 1. Introduction
This document is a **User Guide** for the *Flask Blog API Admin Interface*.  
It is intended for **Clients, Product Owners, QA Analysts, and other stakeholders** who want to understand how the software works functionally.

The application provides:
- A RESTful backend API (Flask + SQLAlchemy)
- A lightweight admin web interface (HTML + JavaScript)
- Full CRUD operations for Users and Blog Posts
- Global statistics dashboard

---

## 2. System Overview
The system is composed of two main parts:

- **Backend**: Flask REST API connected to a MySQL database
- **Frontend**: Single-page admin interface communicating via HTTP (JSON)

Typical use cases:
- Create and manage users
- Create, publish, and delete blog posts
- View global platform statistics

---

## 3. Architecture

**Frontend (Browser)**
- HTML + JavaScript
- Uses `fetch()` to call REST endpoints
- Runs independently from backend

**Backend (Flask API)**
- Flask + SQLAlchemy ORM
- MySQL database
- CORS enabled for frontend access

**Database**
- Users table
- Posts table (linked to users)

---

## 4. Getting Started

### Prerequisites
- Python 3.9+
- MySQL database
- Browser (Chrome, Edge, Firefox)

### Backend Startup
1. Configure database connection (environment variable or default)
2. Run:
```bash
python app.py
```
3. Database tables are auto-created on startup

### Frontend Startup
- Open `index.html` in a browser
- Backend must be running at `http://localhost:5000`

---

## 5. User Interface Overview

### 📊 Statistics Tab
Displays real-time platform metrics:
- Total Users
- Total Posts
- Published Posts

**Actions**
- Refresh statistics manually

**Purpose**
- High-level monitoring for stakeholders

---

### 👥 Users Tab
Allows full user management.

**Features**
- Create user (username, email, password)
- View all users
- Delete users

**Notes**
- Username and email must be unique
- Deleting a user also deletes their posts

---

### 📝 Posts Tab
Manages blog posts.

**Features**
- Create posts
- Assign author (User ID)
- Draft or Published status
- View post list
- Delete posts

**Notes**
- A user must exist before creating a post
- Only published posts count as public content

---

## 6. Backend API Overview

### Health Check
`GET /api/health`

### Users
- `POST /api/users`
- `GET /api/users`
- `GET /api/users/{id}`
- `DELETE /api/users/{id}`

### Posts
- `POST /api/posts`
- `GET /api/posts`
- `GET /api/posts/{id}`
- `PUT /api/posts/{id}`
- `DELETE /api/posts/{id}`

### Statistics
- `GET /api/stats`

---

## 7. CRUD Workflows

### User – CRUD Example

**Create**
```json
POST /api/users
{
  "username": "john",
  "email": "john@email.com",
  "password": "secret"
}
```

**Read**
```http
GET /api/users
```

**Delete**
```http
DELETE /api/users/1
```

---

### Post – CRUD Example

**Create**
```json
POST /api/posts
{
  "title": "My First Post",
  "content": "Hello world",
  "user_id": 1,
  "published": true
}
```

**Read**
```http
GET /api/posts
```

**Update**
```json
PUT /api/posts/1
{
  "published": false
}
```

**Delete**
```http
DELETE /api/posts/1
```

---

## 8. Error Handling & Validation
- Missing fields → HTTP 400
- Duplicate username/email → HTTP 409
- Resource not found → HTTP 404
- Server error → HTTP 500

All errors return JSON responses.

---

## 9. Data Model Overview

### User
- id
- username (unique)
- email (unique)
- password_hash
- created_at

### Post
- id
- title
- content
- published
- created_at
- updated_at
- user_id (foreign key)

---

## 10. Security Considerations
- Passwords are hashed (Werkzeug)
- No authentication layer (admin-only prototype)
- CORS enabled (development mode)
- Not production-ready without auth & HTTPS

---

## 11. Good to Know / Best Practices
- Always create users before posts
- Use Statistics tab for smoke testing
- Ideal project for:
  - QA automation practice
  - API testing
  - CRUD validation scenarios
- Can be extended with:
  - Authentication (JWT)
  - Role-based access
  - Pagination & search

---

**End of User Guide**
