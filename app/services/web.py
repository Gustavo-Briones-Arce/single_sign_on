from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.web import Web
from app.schemas.web import WebCreate, WebUpdate


class WebService():

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, skip: int, limit: int) -> list[Web]:
        return self.session.query(Web).offset(skip).limit(limit).all()

    def get_one(self, id: str):
        web = self.session.get(Web, id)
        if not web:
            raise HTTPException(status_code=404, detail='Website not found')
        return web

    def new_web(self, web: WebCreate):
        if self.session.query(Web).filter(Web.name == web.name).one_or_none():
            raise HTTPException(status_code=400, detail='Web name exists')

        db_web = Web(**web.dict())
        self.session.add(db_web)
        self.session.commit()
        self.session.refresh(db_web)
        return db_web

    def update_web(self, id: str, web: WebUpdate):
        db_web = self.session.get(Web, id)
        if not db_web:
            raise HTTPException(status_code=404, detail='Website not found')
        web_data = web.dict(exclude_unset=True)
        for key, value in web_data.items():
            setattr(db_web, key, value)
        setattr(db_web, 'on_updated', datetime.now())
        self.session.add(db_web)
        self.session.commit()
        self.session.refresh(db_web)
        return db_web

    def delete_web(self, id: str):
        db_web = self.session.get(Web, id)
        if not db_web:
            raise HTTPException(status_code=404, detail='Website not found')
        self.session.delete(db_web)
        self.session.commit()
        return JSONResponse(content='Website deleted', status_code=200)
