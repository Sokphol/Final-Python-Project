# Final-Python-Project - Watch Shop E-Commerce

A modern, full-stack mini e-commerce web application built using Python, Flask, SQLite/SQLAlchemy, Tailwind CSS, and KHQR payment integration.

## Key Features

### 1. Customer Storefront
- **Home Page**: Interactive product grid with watch collections, price, full description, availability, and direct Add to Cart.
- **Product Detail**: High-resolution image showcase, complete specifications, real-time stock indicator, quantity selector, and one-click social share to **Facebook** and **Telegram**.
- **Shopping Cart**: Real-time shopping bag with item management, unit prices, dynamic quantity adjusters, subtotals, and total amount.
- **KHQR Checkout**: Guest checkout form (Full Name, Email, Phone, Shipping Address) with authentic **Bakong / KHQR** QR code generation for instant mobile banking payment.
- **Order Confirmation**: Receipt view with unique Order ID, customer information, line items, and total amount.

### 2. Administrative Interface
- **Watch Inventory Management**: Full CRUD (Create, Read, Update, Delete) for timepieces with Name, Description, Price, Stock Quantity, Status (Active/Inactive), and Image.
- **Customer Order History**: Comprehensive order tracking showing Order ID, Customer Name, Contact Number, Total Amount, Order Date, and Payment Status.
- **Order Details**: Full fulfillment breakdown displaying purchased watches, quantities, subtotals, and delivery address.

## Tech Stack
- **Backend**: Python 3.12, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-Limiter
- **Database**: SQLite / PostgreSQL compatible
- **Payments**: KHQR / Bakong Standard QR integration
- **Styling**: Tailwind CSS & Bootstrap Icons

## Setup & Running Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sokphol/Final-Python-Project.git
   cd Final-Python-Project
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database and seed data**:
   ```bash
   python init_watch_store.py
   ```

5. **Run the server**:
   ```bash
   python app.py
   ```

6. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
   - **Admin Login**: `admin` / `admin` at `/login`
