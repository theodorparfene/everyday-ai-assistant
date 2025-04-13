from sqlalchemy import Column, Integer, String, Text
from db import Base

class KnowledgeEntry(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(100), index=True)  # e.g. cleaning, cooking, tinkering
    title = Column(String(255))              # Short title
    content = Column(Text)                   # The actual info
    tags = Column(String(255))               # Comma-separated keywords
    source = Column(String(255), nullable=True)  # Optional origin or link
