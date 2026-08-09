*🇫🇷 Version française ci-dessous — la version anglaise suit plus bas. / 🇬🇧 English version follows further down.*

## 🇫🇷 Français

# Guide d'installation - API Blog Flask

### Prérequis

- Git 2.52.0  
- Visual Studio Code 1.107.1  
- Python (via python.org)  
- MySQL Installer 8.0 (Full)

### Étape 1 : Cloner le projet

```bash
cd \dev
git init
git clone https://github.com/ericclub/portfolio-SQAAILab.git
```

Ouvrez le dossier `\dev\portfolio-SQAAILab` dans Visual Studio Code et ouvrez un terminal.

### Étape 2 : Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate
```

Vous devriez voir `(venv)` dans le terminal.

### Étape 3 : Installer les dépendances

**requirements.txt**
```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-CORS==5.0.0
PyMySQL==1.1.1
python-dotenv==1.2.1
Werkzeug==3.1.4
cryptography==46.0.3
```

```bash
pip install -r requirements.txt
```

> Si `pip` n'est pas installé, copiez le message d'erreur dans GitHub Copilot Chat et relancez la commande après la configuration.

### Étape 4 : Configurer MySQL

```sql
CREATE DATABASE blog_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'blog_user'@'localhost'
  IDENTIFIED BY 'BlogPass2024!';

GRANT ALL PRIVILEGES ON blog_db.*
  TO 'blog_user'@'localhost';

FLUSH PRIVILEGES;
```

### Étape 5 : Créer le fichier `.env` (optionnel)

```env
DATABASE_URL=mysql+pymysql://blog_user:BlogPass2024!@localhost:3306/blog_db
SECRET_KEY=your-super-long-secret-key
FLASK_ENV=development
```

> Si omis, des valeurs par défaut sont utilisées.

### Étape 6 : Lancer l'application (back-end)

```bash
cd C:\dev\portfolio-SQAAILab\10-AI-vibe-coding\result\src\app\backend\
python app.py
```

Résultat attendu :
```
Database tables created!
* Running on http://0.0.0.0:5000
```

### Étape 7 : Lancer le front-end

Ouvrez :
```
C:\dev\portfolio-SQAAILab\10-AI-vibe-coding\result\src\app\frontend\index.html
```

### Vérifier l'installation

#### Vérification de l'état de santé

```bash
curl http://localhost:5000/api/health
```

Réponse attendue :
```json
{ "status": "ok", "message": "API is running" }
```

#### Créer un utilisateur

```bash
curl -X POST http://localhost:5000/api/users -H "Content-Type: application/json" -d '{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}'
```

#### Afficher les utilisateurs

```bash
curl http://localhost:5000/api/users
```

### Points de terminaison disponibles

#### Utilisateurs

| Méthode | Point de terminaison | Description |
|------|--------|------------|
| POST | /api/users | Créer un utilisateur |
| GET | /api/users | Lister les utilisateurs |
| GET | /api/users/{id} | Détails de l'utilisateur |
| DELETE | /api/users/{id} | Supprimer l'utilisateur |

#### Articles (Posts)

| Méthode | Point de terminaison | Description |
|------|--------|------------|
| POST | /api/posts | Créer un article |
| GET | /api/posts | Lister les articles |
| GET | /api/posts?published=true | Articles publiés uniquement |
| GET | /api/posts/{id} | Détails de l'article |
| PUT | /api/posts/{id} | Mettre à jour l'article |
| DELETE | /api/posts/{id} | Supprimer l'article |

#### Statistiques

| Méthode | Point de terminaison | Description |
|------|--------|------------|
| GET | /api/stats | Statistiques globales |

### Exemples d'utilisation

#### Créer un utilisateur

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secure123"
}
```

#### Créer un article

```json
{
  "title": "My First Article",
  "content": "This is the content of my article",
  "user_id": 1,
  "published": true
}
```

### Outils et concepts

- Flask & SQLAlchemy 2.0
- API REST (GET, POST, PUT, DELETE)
- CORS & sécurité
- MySQL avec utf8mb4
- Environnements virtuels
- Configuration `.env`
- Frontend HTML / CSS / JavaScript

### Capacités QA & IA

- Génération automatique de tests
- Création de données de test complexes
- 100 % de couverture des tests unitaires
- Vérifications de la qualité et de la maintenabilité du code
- Génération de documentation
- Analyse des logs et des données
- Rapports lisibles par des humains
- Prédiction des risques

---
**Félicitations ! Votre application Flask est prête pour les exercices QA + IA.**

---

## 🇬🇧 English

# Flask Blog API - Installation Guide

### Pre-requirements

- Git 2.52.0  
- Visual Studio Code 1.107.1  
- Python (via python.org)  
- MySQL Installer 8.0 (Full)

### Step 1: Clone the Project

```bash
cd \dev
git init
git clone https://github.com/ericclub/portfolio-SQAAILab.git
```

Open the folder `\dev\portfolio-SQAAILab` in Visual Studio Code and open a terminal.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in the terminal.

### Step 3: Install Dependencies

**requirements.txt**
```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-CORS==5.0.0
PyMySQL==1.1.1
python-dotenv==1.2.1
Werkzeug==3.1.4
cryptography==46.0.3
```

```bash
pip install -r requirements.txt
```

> If `pip` is not installed, copy the error message into GitHub Copilot Chat and re-run the command after setup.

### Step 4: Configure MySQL

```sql
CREATE DATABASE blog_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'blog_user'@'localhost'
  IDENTIFIED BY 'BlogPass2024!';

GRANT ALL PRIVILEGES ON blog_db.*
  TO 'blog_user'@'localhost';

FLUSH PRIVILEGES;
```

### Step 5: Create `.env` File (Optional)

```env
DATABASE_URL=mysql+pymysql://blog_user:BlogPass2024!@localhost:3306/blog_db
SECRET_KEY=your-super-long-secret-key
FLASK_ENV=development
```

> If omitted, default values are used.

### Step 6: Launch the Application (Back-End)

```bash
cd C:\dev\portfolio-SQAAILab\10-AI-vibe-coding\result\src\app\backend\
python app.py
```

Expected output:
```
Database tables created!
* Running on http://0.0.0.0:5000
```

### Step 7: Launch the Front-End

Open:
```
C:\dev\portfolio-SQAAILab\10-AI-vibe-coding\result\src\app\frontend\index.html
```

### Verify the Installation

#### Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{ "status": "ok", "message": "API is running" }
```

#### Create a User

```bash
curl -X POST http://localhost:5000/api/users -H "Content-Type: application/json" -d '{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}'
```

#### View Users

```bash
curl http://localhost:5000/api/users
```

### Available Endpoints

#### Users

| Method | Endpoint | Description |
|------|--------|------------|
| POST | /api/users | Create user |
| GET | /api/users | List users |
| GET | /api/users/{id} | User details |
| DELETE | /api/users/{id} | Delete user |

#### Posts (Articles)

| Method | Endpoint | Description |
|------|--------|------------|
| POST | /api/posts | Create post |
| GET | /api/posts | List posts |
| GET | /api/posts?published=true | Published only |
| GET | /api/posts/{id} | Post details |
| PUT | /api/posts/{id} | Update post |
| DELETE | /api/posts/{id} | Delete post |

#### Stats

| Method | Endpoint | Description |
|------|--------|------------|
| GET | /api/stats | Global statistics |

### Usage Examples

#### Create User

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secure123"
}
```

#### Create Post

```json
{
  "title": "My First Article",
  "content": "This is the content of my article",
  "user_id": 1,
  "published": true
}
```

### Tools & Concepts

- Flask & SQLAlchemy 2.0
- REST API (GET, POST, PUT, DELETE)
- CORS & security
- MySQL with utf8mb4
- Virtual environments
- `.env` configuration
- HTML / CSS / JavaScript frontend

### QA & AI Capabilities

- Automatic test generation
- Complex test data creation
- 100% unit test coverage
- Code quality & maintainability checks
- Documentation generation
- Log & data analysis
- Human-readable reports
- Risk prediction

---
**Congratulations! Your Flask application is ready for QA + AI exercises.**
