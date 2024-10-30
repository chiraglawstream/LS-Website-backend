from fastapi.middleware.cors import CORSMiddleware

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://lawstream-web.vercel.app",
    "https://www.lawstream.in"
]

# CORS middleware setup function
def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )
