import cloudinary
from app.config import settings

from fastapi import FastAPI
from app import routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

cloudinary.config(
    cloud_name=settings.CLOUD_Name,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,
)

app.include_router(router=routers.employee.router)
app.include_router(router=routers.auth.router)
app.include_router(router=routers.upload_employees.router)
app.include_router(router=routers.category.router)
app.include_router(router=routers.product.router)
app.include_router(router=routers.pricelist.router)
app.include_router(router=routers.pricelist_line.router)
app.include_router(router=routers.program.router)
app.include_router(router=routers.program_item.router)
app.include_router(router=routers.customer.router)
app.include_router(router=routers.session.router)
app.include_router(router=routers.order.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello point of sale"}
