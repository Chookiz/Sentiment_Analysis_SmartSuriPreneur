from app.bmc import Bmc
from app.sentiment import Sentiment,ReviewBase
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Annotated
from fastapi import FastAPI, Request, HTTPException, Depends
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.models import Review

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1:8000"],  # Allow requests from localhost and your API port
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def index(request: Request):
    return {
            "message": "Welcome To Suripreneur Decision Support System FAST API. For developer guide please visit "+ str(request.url) + "docs"
        }

@app.get("/sentiment/{name}")
def read_items(name: str, db: db_dependency):
    items = db.query().with_entities(Review.name, Review.sentiment).filter(Review.name.like(f"%{name}%")).all()
    return [{"name": item.name, "sentiment": item.sentiment} for item in items]

@app.post("/sentiment")
async def create_item(review: ReviewBase, db: db_dependency):
    obj = Sentiment(comment=review.comment, name=review.name)
    sentiment = obj.main()
    review.sentiment = sentiment
    review.kategori = 'fcad4cd69cd9334a24f5efb8857eb9371'
    db_item = Review(**review.model_dump())
    db.add(db_item)
    db.commit()
    return {"success": True}

@app.get("/bmc/{input_request}")
def read_item(q: Union[str, None] = None): # type: ignore
    obj = Bmc(q)
    return obj.view()

