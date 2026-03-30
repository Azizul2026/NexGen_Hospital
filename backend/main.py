from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging
import os

from core.database import db
from services.seed import seed_all

# ✅ ROUTERS
from routers import auth, admin, doctor, patient, ai

# ─────────────────────────────────────────────
# 🔹 LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("nexgen")

# ─────────────────────────────────────────────
# 🔹 STARTUP / SHUTDOWN
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🏥 Starting NexGen Hospital...")

    try:
        db.connect()
        seed_all()
        logger.info("✅ Database connected & seeded")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

    port = os.environ.get("PORT", "10000")
    logger.info(f"🚀 Running on port {port}")

    yield

    db.close()
    logger.info("👋 Shutdown complete")

# ─────────────────────────────────────────────
# 🔹 APP INIT
# ─────────────────────────────────────────────
app = FastAPI(
    title="NexGen Hospital API",
    version="3.0.0",
    description="Hospital Management System with AI + Analytics + Security",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# ─────────────────────────────────────────────
# 🔐 SECURITY HEADERS
# ─────────────────────────────────────────────
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    return response

# ─────────────────────────────────────────────
# 🌍 CORS (VERY IMPORTANT FOR VERCEL)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 change to your Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# 🔗 ROUTERS
# ─────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(ai.router)

# ─────────────────────────────────────────────
# 📁 FRONTEND SERVING (OPTIONAL LOCAL)
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

if os.path.isdir(FRONTEND_DIR):

    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

    js_dir = os.path.join(FRONTEND_DIR, "js")
    if os.path.isdir(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")

    def serve(page):
        return FileResponse(os.path.join(FRONTEND_DIR, page))

    @app.get("/")
    def root():
        return serve("login.html")

    @app.get("/login.html")
    def login():
        return serve("login.html")

    @app.get("/admin.html")
    def admin_page():
        return serve("admin.html")

    @app.get("/doctor.html")
    def doctor_page():
        return serve("doctor.html")

    @app.get("/patient.html")
    def patient_page():
        return serve("patient.html")

# ─────────────────────────────────────────────
# ❤️ HEALTH CHECK
# ─────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "NexGen Hospital API",
        "version": "3.0.0"
    }

# ─────────────────────────────────────────────
# ℹ️ INFO
# ─────────────────────────────────────────────
@app.get("/info")
def info():
    return {
        "name": "NexGen Hospital System",
        "version": "3.0.0",
        "features": [
            "JWT Authentication",
            "Admin Panel",
            "Doctor Dashboard",
            "Patient Portal",
            "AI Predictions",
            "Analytics Dashboard"
        ]
    }
