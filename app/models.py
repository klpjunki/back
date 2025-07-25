from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, BigInteger, Float, ForeignKey
)
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String(64), nullable=True)

    coins = Column(BigInteger, default=0, nullable=False)
    energy = Column(Integer, default=6500, nullable=False)
    max_energy = Column(Integer, default=6500, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    total_clicks = Column(Integer, default=0, nullable=False)

    referral_code = Column(String(16), unique=True, nullable=False)
    referred_by = Column(String(16), nullable=True)
    milestone_5_friends_claimed = Column(Boolean, default=False, nullable=False)
    reward_5_friends_claimed = Column(Boolean, default=False, nullable=False)
    reward_10_friends_claimed = Column(Boolean, default=False, nullable=False)

    youtube_subscribed = Column(Boolean, default=False, nullable=False)
    youtube_reward_claimed = Column(Boolean, default=False, nullable=False)
    youtube_timer_started = Column(DateTime(timezone=True), nullable=True)

    telegram_subscribed = Column(Boolean, default=False, nullable=False)
    telegram_reward_claimed = Column(Boolean, default=False, nullable=False)
    telegram_timer_started = Column(DateTime(timezone=True), nullable=True)

    boost_expiry = Column(DateTime(timezone=True), nullable=True)
    boost_multiplier = Column(Integer, default=1, nullable=False)

    last_energy_update = Column(DateTime(timezone=True),
                                server_default=func.now(),
                                nullable=False)
    daily_streak = Column(Integer, default=0, nullable=False)
    last_daily_login = Column(DateTime(timezone=True), nullable=True)

    role = Column(String(20), default="player", nullable=False)

    genshin_balance = Column(Integer, default=0, nullable=False)
    honkai_balance = Column(Integer, default=0, nullable=False)
    zenless_balance = Column(Integer, default=0, nullable=False)

    locked_coins = Column(Integer, default=0, nullable=False)

class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    quest_type = Column(String(20))
    reward_type = Column(String(20))
    reward_value = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    url = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

class PromoCode(Base):
    __tablename__ = "promocodes"

    code = Column(String(32), primary_key=True)
    reward_type = Column(String(20))
    value = Column(Integer)
    expiry = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    uses_left = Column(Integer, default=1)

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_currency = Column(String(10), nullable=False)
    to_currency = Column(String(10), nullable=False)
    rate = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ExchangeRequest(Base):
    __tablename__ = "exchange_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=False)
    from_currency = Column(String(10), nullable=False)
    to_currency = Column(String(10), nullable=False)
    amount = Column(Integer, nullable=False)
    received_amount = Column(Integer, nullable=False)
    uid = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.now)
    processed_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="exchange_requests")
