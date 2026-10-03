from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Transaction, User
from schemas import TransactionCreate, TransactionUpdate, TransactionOut
from auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("", response_model=TransactionOut, status_code=201)
def create_tx(tx: TransactionCreate,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    new_tx = Transaction(**tx.dict(), owner_id=user.id)
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx

@router.get("", response_model=list[TransactionOut])
def get_all(db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    return db.query(Transaction).filter(Transaction.owner_id == user.id).all()

@router.get("/filter", response_model=list[TransactionOut])
def filter_tx(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    minimum_amount: Optional[float] = Query(None),
    maximum_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Transaction).filter(Transaction.owner_id == user.id)
    if type:
        q = q.filter(Transaction.type == type)
    if category:
        q = q.filter(Transaction.category == category)
    if minimum_amount is not None:
        q = q.filter(Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        q = q.filter(Transaction.amount <= maximum_amount)
    return q.all()

@router.get("/{transaction_id}", response_model=TransactionOut)
def get_one(transaction_id: int,
            db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    tx = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == user.id
    ).first()
    if not tx:
        raise HTTPException(404, "Transaction not found")
    return tx

@router.put("/{transaction_id}", response_model=TransactionOut)
def update_tx(transaction_id: int,
              data: TransactionUpdate,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    tx = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == user.id
    ).first()
    if not tx:
        raise HTTPException(404, "Transaction not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(tx, field, value)
    db.commit()
    db.refresh(tx)
    return tx

@router.delete("/{transaction_id}")
def delete_tx(transaction_id: int,
              db: Session = Depends(get_db),
              user: User = Depends(get_current_user)):
    tx = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == user.id
    ).first()
    if not tx:
        raise HTTPException(404, "Transaction not found")
    db.delete(tx)
    db.commit()
    return {"message": "Transaction deleted successfully"}