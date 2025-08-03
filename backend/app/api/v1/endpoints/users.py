from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserProfileCreate, UserProfileUpdate, UserProfileResponse, Token
from app.api.deps import get_current_user
from typing import Dict, Any

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    return user

@router.put("/me/profile", response_model=UserProfileResponse)
def update_profile(
    profile: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    
    # Get or create profile
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if db_profile:
        # Update existing profile
        for field, value in profile.dict(exclude_unset=True).items():
            setattr(db_profile, field, value)
    else:
        # Create new profile
        db_profile = UserProfile(
            user_id=user.id,
            **profile.dict(exclude_unset=True)
        )
        db.add(db_profile)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/me/profile", response_model=UserProfileResponse)
def get_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile 