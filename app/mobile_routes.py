from flask import Blueprint, render_template, request, jsonify, redirect, url_for

mobile_bp = Blueprint('mobile', __name__, url_prefix='/mobile')

@mobile_bp.route('/')
@mobile_bp.route('/main')
def main():
    """Mobile main page route"""
    return render_template('mobile/main_page.html')

@mobile_bp.route('/dashboard')
def dashboard():
    """Mobile dashboard route"""
    return render_template('mobile/dashboard.html')

@mobile_bp.route('/profile')
def profile():
    """Mobile profile route"""
    return render_template('mobile/profile.html')

# API endpoints for mobile
@mobile_bp.route('/api/stats')
def get_stats():
    """Get user stats for mobile UI"""
    # Mock data - in production, fetch from database
    stats = {
        "gamesPlayed": 42,
        "wins": 28,
        "winRate": "67%",
        "points": 1250,
        "recentGames": [
            {"name": "Adventure Quest", "result": "win", "date": "2 hours ago"},
            {"name": "Puzzle Master", "result": "loss", "date": "Yesterday"},
            {"name": "Space Invaders", "result": "win", "date": "3 days ago"}
        ]
    }
    return jsonify(stats)

@mobile_bp.route('/api/games')
def get_games():
    """Get available games for mobile UI"""
    # Mock data - in production, fetch from database
    games = [
        {"id": 1, "title": "Adventure Quest", "players": 4, "status": "active"},
        {"id": 2, "title": "Space Invaders", "players": 2, "status": "waiting"},
        {"id": 3, "title": "Puzzle Master", "players": 3, "status": "completed"}
    ]
    return jsonify({"games": games})

@mobile_bp.route('/api/profile', methods=['GET', 'POST'])
def update_profile():
    """Get or update user profile"""
    if request.method == 'POST':
        # In production, update profile in database
        data = request.json
        # Mock successful update
        return jsonify({"success": True, "message": "Profile updated successfully"})
    else:
        # Mock profile data
        profile = {
            "username": "alexj",
            "email": "alex@example.com",
            "location": "New York, USA",
            "bio": "Game enthusiast and competitive player. I love strategy games and puzzles!",
            "avatar": "https://via.placeholder.com/120"
        }
        return jsonify(profile)
