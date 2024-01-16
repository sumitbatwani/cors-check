from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # support for cookie credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

cors_config = {
    "allow_origins": ["https://gw4v6m.csb.app/"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

# Middleware function to apply CORS to a specific API endpoint
async def apply_cors(request, call_next):
    # Check if the request path matches the specific API endpoint
    if 'dummy' in request.url.path:
        # Apply CORS settings
        response = await call_next(request)

        # Set allow_origin header
        response.headers["Access-Control-Allow-Origin"] = cors_config["allow_origins"][0]

        # Handle allow_methods and allow_headers, which can be lists
        for key in ["allow_methods", "allow_headers"]:
            if key in cors_config:
                response.headers["Access-Control-" + key.title()] = ", ".join(cors_config[key])

        # Set allow_credentials
        if cors_config.get("allow_credentials", False):
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    # Continue without applying CORS
    return await call_next(request)

app.middleware("http")(apply_cors)

@app.get("/health-check")
def health_check():
    return {"status": "OK"}

@app.get("/")
def root():
    return {"message": "OK!"}

@app.get("/dummy")
def root():
    return {"message": "DUMMY OK!"}

