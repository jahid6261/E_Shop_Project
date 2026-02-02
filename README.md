# 🛒 E-Shop – Full Stack E-Commerce Web Application

**Live Demo:** [https://e-shop-project-2.onrender.com/](https://e-shop-project-2.onrender.com/)

E-Shop is a **full-featured e-commerce web application** built with **Django** and follows **real-world backend and full-stack best practices**.  
It implements complete e-commerce workflows including authentication, product & category management, cart & order handling, payments, and Google social login.

---

## 🚀 Features

- **User authentication & authorization**
  - Email/password login
  - Google Social Login (OAuth)
- Product & category management
- Cart management (one cart per user)
- Order placement & order history
- Online payment via **SSLCommerz Payment Gateway**
- Product reviews & ratings
- Media support (Cloudinary image upload)
- Admin panel (Django Admin)

---

## 🧑‍💻 Tech Stack

### Backend
- Python, Django, Django ORM
- PostgreSQL (Production) / SQLite (Development)
- Django Allauth (Google OAuth)
- SSLCommerz (Payment Gateway)

### Frontend
- HTML, CSS, Tailwind, JavaScript
- Responsive UI

### Others
- Cloudinary (Media Storage)
- Render (Deployment)
- Git & GitHub

---

## ⚙️ Installation (Local)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/jahid6261/e-shop-project.git
cd e-shop-project
2️⃣ Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Environment Variables (.env)
Create a .env file in the project root and add:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=*

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# SSLCommerz
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASS=your_store_password
SSLCOMMERZ_PAYMENT_URL=https://sandbox.sslcommerz.com
5️⃣ Apply migrations
python manage.py migrate
6️⃣ Create superuser
python manage.py createsuperuser
7️⃣ Collect static files
python manage.py collectstatic
8️⃣ Run development server
python manage.py runserver
📂 Project Purpose
This project is built to:

Practice real-world full-stack e-commerce development

Demonstrate authentication, social login, and payment integration

Showcase skills for junior full-stack developer / backend roles

👨‍💻 Author
Jahid Alam
Junior Full Stack Developer

Skills: Python | Django | PostgreSQL | JavaScript | Tailwind | OAuth | Payment Gateway | REST API

🔗 GitHub: https://github.com/jahid6261
🔗 LinkedIn: https://www.linkedin.com/in/jahid-alam-0a8b64360