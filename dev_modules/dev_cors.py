"""
========= FOR DEV PORPOISES ONLY - ALLOW ALL CORS =========
"""

from fastapi.middleware.cors import CORSMiddleware #for dev porpoises!

def allow_all_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



"""
========= END FOR DEV PORPOISES ONLY - ALLOW ALL CORS =========
"""