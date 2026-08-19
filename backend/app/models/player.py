from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String(3), unique=True, index=True, nullable=False)
    city = Column(String, nullable=False)
    name = Column(String, nullable=False)

    player_seasons = relationship("PlayerSeason", back_populates="team")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    position = Column(String(10))
    height_inches = Column(Integer)
    weight_lbs = Column(Integer)
    birth_date = Column(Date)
    is_active = Column(Boolean, default=True)

    seasons = relationship("PlayerSeason", back_populates="player")

class PlayerSeason(Base):
    __tablename__ = "player_seasons"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season = Column(String(7), nullable=False)
    
    games_played = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    points = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    rebounds = Column(Integer, default=0)

    player = relationship("Player", back_populates="seasons")
    team = relationship("Team", back_populates="player_seasons")