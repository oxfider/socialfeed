from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sources = db.Column(db.Text)  # JSON string with social media sources
    filters = db.Column(db.Text)  # JSON string with filter settings
    layout_config = db.Column(db.Text)  # JSON string with layout configuration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Feed {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'sources': json.loads(self.sources) if self.sources else [],
            'filters': json.loads(self.filters) if self.filters else {},
            'layout_config': json.loads(self.layout_config) if self.layout_config else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

    def set_sources(self, sources_list):
        self.sources = json.dumps(sources_list)

    def set_filters(self, filters_dict):
        self.filters = json.dumps(filters_dict)

    def set_layout_config(self, layout_dict):
        self.layout_config = json.dumps(layout_dict)

class SocialPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # instagram, twitter, facebook, etc.
    post_id = db.Column(db.String(100), nullable=False)  # original post ID from platform
    content = db.Column(db.Text)
    author = db.Column(db.String(100))
    author_avatar = db.Column(db.String(255))
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.String(50))  # image, video, text
    post_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_at = db.Column(db.DateTime)  # original post date from platform
    is_approved = db.Column(db.Boolean, default=True)
    is_hidden = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<SocialPost {self.platform}:{self.post_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'feed_id': self.feed_id,
            'platform': self.platform,
            'post_id': self.post_id,
            'content': self.content,
            'author': self.author,
            'author_avatar': self.author_avatar,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'post_url': self.post_url,
            'created_at': self.created_at.isoformat(),
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'is_approved': self.is_approved,
            'is_hidden': self.is_hidden
        }

