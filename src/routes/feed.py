from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.feed import Feed, SocialPost
from datetime import datetime
import json

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/feeds', methods=['GET'])
def get_feeds():
    """Obter todos os feeds do usuário"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id é obrigatório'}), 400
    
    feeds = Feed.query.filter_by(user_id=user_id, is_active=True).all()
    return jsonify([feed.to_dict() for feed in feeds])

@feed_bp.route('/feeds', methods=['POST'])
def create_feed():
    """Criar um novo feed"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('user_id'):
        return jsonify({'error': 'Nome e user_id são obrigatórios'}), 400
    
    feed = Feed(
        user_id=data['user_id'],
        name=data['name'],
        description=data.get('description', ''),
    )
    
    if data.get('sources'):
        feed.set_sources(data['sources'])
    
    if data.get('filters'):
        feed.set_filters(data['filters'])
    
    if data.get('layout_config'):
        feed.set_layout_config(data['layout_config'])
    
    db.session.add(feed)
    db.session.commit()
    
    return jsonify(feed.to_dict()), 201

@feed_bp.route('/feeds/<int:feed_id>', methods=['GET'])
def get_feed(feed_id):
    """Obter um feed específico"""
    feed = Feed.query.get_or_404(feed_id)
    return jsonify(feed.to_dict())

@feed_bp.route('/feeds/<int:feed_id>', methods=['PUT'])
def update_feed(feed_id):
    """Atualizar um feed"""
    feed = Feed.query.get_or_404(feed_id)
    data = request.get_json()
    
    if data.get('name'):
        feed.name = data['name']
    if data.get('description'):
        feed.description = data['description']
    if data.get('sources'):
        feed.set_sources(data['sources'])
    if data.get('filters'):
        feed.set_filters(data['filters'])
    if data.get('layout_config'):
        feed.set_layout_config(data['layout_config'])
    
    feed.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(feed.to_dict())

@feed_bp.route('/feeds/<int:feed_id>', methods=['DELETE'])
def delete_feed(feed_id):
    """Deletar um feed (soft delete)"""
    feed = Feed.query.get_or_404(feed_id)
    feed.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Feed deletado com sucesso'})

@feed_bp.route('/feeds/<int:feed_id>/posts', methods=['GET'])
def get_feed_posts(feed_id):
    """Obter posts de um feed"""
    feed = Feed.query.get_or_404(feed_id)
    posts = SocialPost.query.filter_by(
        feed_id=feed_id, 
        is_approved=True, 
        is_hidden=False
    ).order_by(SocialPost.posted_at.desc()).all()
    
    return jsonify([post.to_dict() for post in posts])

@feed_bp.route('/feeds/<int:feed_id>/posts', methods=['POST'])
def add_post_to_feed(feed_id):
    """Adicionar um post ao feed (simulação de dados de mídia social)"""
    feed = Feed.query.get_or_404(feed_id)
    data = request.get_json()
    
    required_fields = ['platform', 'post_id', 'content', 'author']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios: platform, post_id, content, author'}), 400
    
    post = SocialPost(
        feed_id=feed_id,
        platform=data['platform'],
        post_id=data['post_id'],
        content=data['content'],
        author=data['author'],
        author_avatar=data.get('author_avatar'),
        media_url=data.get('media_url'),
        media_type=data.get('media_type', 'text'),
        post_url=data.get('post_url'),
        posted_at=datetime.fromisoformat(data['posted_at']) if data.get('posted_at') else datetime.utcnow()
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@feed_bp.route('/feeds/<int:feed_id>/posts/<int:post_id>/moderate', methods=['PUT'])
def moderate_post(feed_id, post_id):
    """Moderar um post (aprovar/rejeitar/ocultar)"""
    post = SocialPost.query.filter_by(id=post_id, feed_id=feed_id).first_or_404()
    data = request.get_json()
    
    if 'is_approved' in data:
        post.is_approved = data['is_approved']
    if 'is_hidden' in data:
        post.is_hidden = data['is_hidden']
    
    db.session.commit()
    
    return jsonify(post.to_dict())

@feed_bp.route('/feeds/<int:feed_id>/embed', methods=['GET'])
def get_embed_code(feed_id):
    """Gerar código de incorporação para o feed"""
    feed = Feed.query.get_or_404(feed_id)
    
    # Código JavaScript para incorporação
    embed_code = f"""
<!-- Social Media Feed Widget -->
<div id="social-feed-{feed_id}"></div>
<script>
(function() {{
    var feedId = {feed_id};
    var apiUrl = window.location.protocol + '//' + window.location.host;
    
    function loadSocialFeed() {{
        fetch(apiUrl + '/api/feeds/' + feedId + '/posts')
            .then(response => response.json())
            .then(posts => {{
                var container = document.getElementById('social-feed-' + feedId);
                if (!container) return;
                
                var html = '<div class="social-feed-container">';
                posts.forEach(function(post) {{
                    html += '<div class="social-post">';
                    html += '<div class="post-header">';
                    if (post.author_avatar) {{
                        html += '<img src="' + post.author_avatar + '" alt="' + post.author + '" class="author-avatar">';
                    }}
                    html += '<span class="author-name">' + post.author + '</span>';
                    html += '<span class="platform">' + post.platform + '</span>';
                    html += '</div>';
                    html += '<div class="post-content">' + post.content + '</div>';
                    if (post.media_url && post.media_type === 'image') {{
                        html += '<img src="' + post.media_url + '" alt="Post image" class="post-media">';
                    }}
                    if (post.post_url) {{
                        html += '<a href="' + post.post_url + '" target="_blank" class="post-link">Ver original</a>';
                    }}
                    html += '</div>';
                }});
                html += '</div>';
                
                container.innerHTML = html;
                
                // Adicionar CSS básico se não existir
                if (!document.getElementById('social-feed-styles')) {{
                    var style = document.createElement('style');
                    style.id = 'social-feed-styles';
                    style.textContent = `
                        .social-feed-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            font-family: Arial, sans-serif;
                        }}
                        .social-post {{
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            margin-bottom: 16px;
                            padding: 16px;
                            background: white;
                        }}
                        .post-header {{
                            display: flex;
                            align-items: center;
                            margin-bottom: 12px;
                        }}
                        .author-avatar {{
                            width: 40px;
                            height: 40px;
                            border-radius: 50%;
                            margin-right: 12px;
                        }}
                        .author-name {{
                            font-weight: bold;
                            margin-right: 8px;
                        }}
                        .platform {{
                            color: #666;
                            font-size: 12px;
                            text-transform: uppercase;
                        }}
                        .post-content {{
                            margin-bottom: 12px;
                            line-height: 1.4;
                        }}
                        .post-media {{
                            max-width: 100%;
                            height: auto;
                            border-radius: 4px;
                            margin-bottom: 12px;
                        }}
                        .post-link {{
                            color: #1976d2;
                            text-decoration: none;
                            font-size: 14px;
                        }}
                        .post-link:hover {{
                            text-decoration: underline;
                        }}
                    `;
                    document.head.appendChild(style);
                }}
            }})
            .catch(error => console.error('Erro ao carregar feed:', error));
    }}
    
    // Carregar feed quando o DOM estiver pronto
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', loadSocialFeed);
    }} else {{
        loadSocialFeed();
    }}
}})();
</script>
"""
    
    return jsonify({
        'feed_id': feed_id,
        'embed_code': embed_code.strip(),
        'instructions': 'Copie e cole este código no seu website onde deseja exibir o feed de mídias sociais.'
    })

