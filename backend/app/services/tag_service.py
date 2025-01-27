from typing import List, Optional
from app.models.tag import Tag
from app.extensions import db

def create_tag(name: str) -> Tag:
    """Create a new tag"""
    tag = Tag(name=name.lower())  # Store tags in lowercase for consistency
    db.session.add(tag)
    db.session.commit()
    return tag

def get_tag_by_name(name: str) -> Optional[Tag]:
    """Get a tag by its name"""
    return Tag.query.filter(Tag.name == name.lower()).first()

def get_tag_by_id(tag_id: int) -> Optional[Tag]:
    """Get a tag by its ID"""
    return Tag.query.get(tag_id)

def get_all_tags() -> List[Tag]:
    """Get all tags"""
    return Tag.query.all()

def delete_tag(tag_id: int) -> bool:
    """Delete a tag by its ID"""
    tag = get_tag_by_id(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        return True
    return False

def get_or_create_tags(tag_names: List[str]) -> List[Tag]:
    """Get existing tags or create new ones from a list of tag names"""
    tags = []
    for name in tag_names:
        name = name.lower().strip()
        if not name:
            continue
        
        tag = get_tag_by_name(name)
        if not tag:
            tag = create_tag(name)
        tags.append(tag)
    return tags
