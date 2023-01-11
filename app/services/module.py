from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.models.module import Module
from app.models.web import Web
from app.schemas.module import ModuleCreate, ModuleUpdate


class ModuleService():
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.session.query(Module).offset(skip).limit(limit).all()

    def get_detail(self, id: str):
        module = self.session.get(Module, id)
        if not module:
            raise HTTPException(status_code=404, detail='Module not found')
        return module

    def create_module(self, module: ModuleCreate):
        web = self.session.get(Web, module.web_id)
        if not web:
            raise HTTPException(status_code=404, detail='Website not found')
        db_module = Module(**module.dict())
        self.session.add(db_module)
        self.session.commit()
        self.session.refresh(db_module)
        return db_module

    def update_module(self, id: str, module: ModuleUpdate):
        db_module = self.session.get(Module, id)
        if not db_module:
            raise HTTPException(status_code=404, detail='Module not found')
        if module.web_id:
            if not self.session.get(Web, module.web_id):
                raise HTTPException(
                    status_code=404, detail='Website not found')
            setattr(db_module, 'web_id', module.web_id)
        module_data = module.dict(exclude_unset=True)
        for key, value in module_data.items():
            setattr(db_module, key, value)
        setattr(db_module, 'on_updated', datetime.now())
        self.session.add(db_module)
        self.session.commit()
        self.session.refresh(db_module)
        return db_module

    def delete_module(self, id: str):
        db_module = self.session.get(Module, id)
        if not db_module:
            raise HTTPException(status_code=404, detail='Module not found')
        self.session.delete(db_module)
        self.session.commit()
        return JSONResponse(content='Website deleted', status_code=200)
