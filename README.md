# 🛡️ StarBasto

**StarBasto** is a next-generation "Colmado-to-Customer" delivery ecosystem. It features a robust FastAPI backend protected by the **Star Defense Security Shield**, ensuring that price tampering and unauthorized orders are blocked at the source.

The project utilizes an **Adaptive Web-App** architecture, allowing a single codebase to serve as both a high-efficiency **Owner Dashboard** and a mobile-optimized **Customer Storefront**.



## 🚀 Key Features

* **🛡️ Star Defense Middleware**: A custom security layer that validates every transaction. If a customer attempts to modify prices via the browser console, the backend automatically intercepts and blocks the order.
* **📱 Adaptive UI**: A "Mobile-First" design built with **Tailwind CSS** that works seamlessly on iOS, Android, and Desktop browsers without needing separate apps.
* **⚡ Real-time Inventory**: Live search and catalog management enabling Colmado owners to update prices and stock instantly.
* **📦 Headless API Architecture**: Clean separation between the "Brain" (FastAPI) and the "Face" (HTML/JS), ready for future expansion into native React Native or Flutter apps.

---

## 🏗️ Project Structure

```text
StarBasto/
├── backend/                # The "Brain" (FastAPI)
│   ├── main.py             # Server entry & CORS configuration
│   ├── routes.py           # Owner & Client API endpoints
│   ├── database.py         # Source of Truth (Products & Orders)
│   ├── middleware.py       # 🛡️ Star Defense Security Shield
│   └── requirements.txt    # Python dependencies
└── frontend/               # The "Face" (Adaptive Web App)
    ├── index.html          # App Gateway / Entry Point
    ├── owner.html          # Admin & Inventory Dashboard
    └── customer.html       # Mobile-optimized Customer Storefront
```

## 🛠️ Setup & Installation
### 1. Start the Backend
Navigate to the backend folder and install the necessary dependencies:

```bash
cd backend
pip install -r requirements.txt
Run the server from the project root directory to ensure all modules are discovered:
```

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0
```
### 2. Launch the Frontend
Simply open `frontend/index.html` in any modern web browser.

> **📱 To test on Mobile**: Ensure your phone is on the same Wi-Fi. Replace `127.0.0.1` in your `.html` files with your Mac's **Local IP address** (e.g., `192.168.1.XX`).

---

## 🛡️ Star Defense Security Protocol
**StarBasto** operates on a **Zero-Trust Client** model. Every order submitted undergoes a rigorous **Price Integrity Check**:

* **Submission**: Customer submits a cart via the mobile web interface.
* **Interception**: The *Star Defense Middleware* intercepts the request before it reaches the database.
* **Validation**: The middleware cross-references submitted prices against the **Secure Server-Side Database**.
* **Enforcement**: If a mismatch is detected (even by 1 cent), the request is rejected with a `403 Forbidden` status.


---

## 📱 How to Use
* **Owner View**: Access the dashboard to manage stock levels, update product pricing, and monitor incoming orders in real-time.
* **Customer View**: Securely search the catalog, add items to the cart, and checkout with protected pricing.

---

## 📝 License
Proprietary - **StarBasto Security Systems 2026**.