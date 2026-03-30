from core.database import db
from core.security import hash_password
from datetime import date
import logging

logger = logging.getLogger(__name__)


def seed_all():
    """Create demo data if not exists"""
    
    existing = db.run_one("MATCH (u:User {username:'admin'}) RETURN u")
    
    if existing:
        logger.info("📦 Seed already exists — skipping")
        return

    logger.info("🌱 Seeding data...")

    seed_admin()
    seed_doctors()
    seed_patients()

    logger.info("✅ Seed completed")
    logger.info("ADMIN → admin / admin123")


# ================= ADMIN =================
def seed_admin():
    db.run("""
    CREATE (u:User {
        username: 'admin',
        password: $pw,
        role: 'ADMIN',
        active: true,
        created_at: $today
    })
    """, pw=hash_password("admin123"), today=str(date.today()))


# ================= DOCTORS =================
def seed_doctors():
    doctors = [
        ("dr.aditi", "Dr. Aditi Roy", "Cardiology"),
        ("dr.karan", "Dr. Karan Mehta", "Orthopaedics"),
    ]

    for uname, name, dept in doctors:
        db.run("""
        CREATE (u:User {
            username: $u,
            password: $pw,
            role: 'DOCTOR',
            active: true,
            created_at: $today
        })
        CREATE (d:Doctor {
            username: $u,
            full_name: $name,
            department: $dept,
            active: true,
            created_at: $today
        })
        """,
        u=uname,
        pw=hash_password("doctor123"),
        name=name,
        dept=dept,
        today=str(date.today())
        )


# ================= PATIENTS =================
def seed_patients():
    patients = [
        ("meera.g", "Meera Gupta"),
        ("rahul.k", "Rahul Khanna"),
    ]

    for uname, name in patients:
        db.run("""
        CREATE (u:User {
            username: $u,
            password: $pw,
            role: 'PATIENT',
            active: true,
            created_at: $today
        })
        CREATE (p:Patient {
            username: $u,
            full_name: $name,
            status: 'ADMITTED',
            created_at: $today
        })
        """,
        u=uname,
        pw=hash_password("patient123"),
        name=name,
        today=str(date.today())
        )
