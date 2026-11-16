import sqlite3
from app import app
from extensions import db
from models.user import User
from models.category import Category
from models.product import Product
from models.order import Order, OrderItem

def init_db():
    with app.app_context():
        # 1. Create any missing tables
        db.create_all()

        # 2. Ensure Admin User
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            admin_user = User(
                user_name='admin',
                email='admin@watchshop.com',
                password='admin',
                role='admin',
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Created default admin user (admin / admin)")
        else:
            print(f"Existing admin user found: {admin_user.user_name}")

        # 4. Seed Watch Categories
        categories_data = [
            ("Luxury Watches", "luxury-watches"),
            ("Chronograph Watches", "chronograph-watches"),
            ("Smart Watches", "smart-watches"),
            ("Classic & Minimalist", "classic-minimalist"),
            ("Sport & Diver", "sport-diver"),
        ]
        cat_map = {}
        for title, slug in categories_data:
            cat = Category.query.filter_by(slug=slug).first()
            if not cat:
                cat = Category(title=title, slug=slug, is_active=True)
                db.session.add(cat)
                db.session.commit()
                print(f"Added category: {title}")
            cat_map[title] = cat.id

        # 5. Seed Watch Products if none exist or only few exist
        if Product.query.count() == 0:
            watches = [
                {
                    "name": "Rolex Submariner Date 41mm",
                    "price": 10250.00,
                    "description": "The benchmark among divers' watches. Crafted in Oystersteel with an Cerachrom ceramic bezel and black dial with large luminescent hour markers.",
                    "image": "/static/image/rolex_submariner.jpg",
                    "stock": 5,
                    "status": "Active",
                    "rating": 5.0,
                    "category_id": cat_map.get("Sport & Diver"),
                    "user_id": admin_user.id
                },
                {
                    "name": "Omega Speedmaster Professional Moonwatch",
                    "price": 7600.00,
                    "description": "The legendary chronograph that has been part of all six lunar missions. Powered by the Co-Axial Master Chronometer Calibre 3861 with sapphire crystal front and back.",
                    "image": "/static/image/omega_speedmaster.jpg",
                    "stock": 8,
                    "status": "Active",
                    "rating": 4.9,
                    "category_id": cat_map.get("Chronograph Watches"),
                    "user_id": admin_user.id
                },
                {
                    "name": "Tissot PRX Powermatic 80",
                    "price": 725.00,
                    "description": "Evoking retro 1970s elegance with a slim, integrated stainless steel bracelet and an impressive 80-hour power reserve automatic movement with Nivachron balance spring.",
                    "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                    "stock": 14,
                    "status": "Active",
                    "rating": 4.8,
                    "category_id": cat_map.get("Classic & Minimalist"),
                    "user_id": admin_user.id
                },
                {
                    "name": "TAG Heuer Carrera Chronograph",
                    "price": 5450.00,
                    "description": "A prestigious motor-racing chronograph with signature glassbox curved sapphire crystal, deep blue sunray dial, and in-house Calibre TH20-00 automatic movement.",
                    "image": "/static/image/rolex_submariner.jpg",
                    "stock": 6,
                    "status": "Active",
                    "rating": 4.9,
                    "category_id": cat_map.get("Chronograph Watches"),
                    "user_id": admin_user.id
                },
                {
                    "name": "Patek Philippe Calatrava Rose Gold",
                    "price": 28900.00,
                    "description": "The timeless archetype of the round dress watch. 18k rose gold case with hobnail patterned bezel (Clous de Paris) and manual-wind manufacture movement.",
                    "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
                    "stock": 2,
                    "status": "Active",
                    "rating": 5.0,
                    "category_id": cat_map.get("Luxury Watches"),
                    "user_id": admin_user.id
                },
                {
                    "name": "Apple Watch Ultra 2 Titanium",
                    "price": 799.00,
                    "description": "The ultimate sports and adventure smartwatch. Rugged 49mm aerospace-grade titanium case, precision dual-frequency GPS, up to 72 hours of battery life, and 3000 nits display.",
                    "image": "/static/image/apple_watch.jpg",
                    "stock": 20,
                    "status": "Active",
                    "rating": 4.8,
                    "category_id": cat_map.get("Smart Watches"),
                    "user_id": admin_user.id
                },
                {
                    "name": "Seiko Prospex 1965 Heritage Diver",
                    "price": 1250.00,
                    "description": "Faithful modern re-interpretation of Japan's first diver's watch from 1965. 300m water resistance, Lumibrite markers, and 72-hour power reserve 6R55 movement.",
                    "image": "https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?auto=format&fit=crop&w=800&q=80",
                    "stock": 11,
                    "status": "Active",
                    "rating": 4.7,
                    "category_id": cat_map.get("Sport & Diver"),
                    "user_id": admin_user.id
                },
                {
                    "name": "Nomos Glashütte Tangente 38",
                    "price": 2180.00,
                    "description": "A pure icon of Bauhaus design and German watchmaking excellence. Crisp typography, tempered blued steel hands, and in-house manual caliber Alpha.",
                    "image": "https://images.unsplash.com/photo-1533139502658-0198f920d8e8?auto=format&fit=crop&w=800&q=80",
                    "stock": 7,
                    "status": "Active",
                    "rating": 4.9,
                    "category_id": cat_map.get("Classic & Minimalist"),
                    "user_id": admin_user.id
                }
            ]
            for w in watches:
                prod = Product(**w)
                db.session.add(prod)
            db.session.commit()
            print("Seeded 8 watch products!")
        else:
            print(f"Products already in DB: {Product.query.count()}")

if __name__ == '__main__':
    init_db()
