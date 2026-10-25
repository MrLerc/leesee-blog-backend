import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
        }


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + os.path.join(app.instance_path, "blog.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    @app.route("/api/posts", methods=["GET"])
    def get_posts():
        posts = Post.query.order_by(Post.id.desc()).all()
        return jsonify([post.to_dict() for post in posts])

    @app.route("/api/posts/<int:post_id>", methods=["GET"])
    def get_post(post_id):
        post = db.session.get(Post, post_id)

        if post is None:
            return jsonify({"error": "Article introuvable"}), 404

        return jsonify(post.to_dict())

    @app.route("/api/posts", methods=["POST"])
    def create_post():
        data = request.get_json(silent=True) or {}

        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        author = data.get("author", "").strip()

        if not title or not content or not author:
            return jsonify({"error": "Tous les champs sont obligatoires"}), 400

        if len(title) > 200 or len(author) > 100:
            return jsonify(
                {"error": "Le titre ou le nom de l'auteur est trop long"}
            ), 400

        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()

        return jsonify(post.to_dict()), 201

    @app.route("/api/posts/<int:post_id>", methods=["PUT"])
    def update_post(post_id):
        post = db.session.get(Post, post_id)

        if post is None:
            return jsonify({"error": "Article introuvable"}), 404

        data = request.get_json(silent=True) or {}

        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        author = data.get("author", "").strip()

        if not title or not content or not author:
            return jsonify({"error": "Tous les champs sont obligatoires"}), 400

        if len(title) > 200 or len(author) > 100:
            return jsonify(
                {"error": "Le titre ou le nom de l'auteur est trop long"}
            ), 400

        post.title = title
        post.content = content
        post.author = author

        db.session.commit()

        return jsonify(post.to_dict())

    @app.route("/api/posts/<int:post_id>", methods=["DELETE"])
    def delete_post(post_id):
        post = db.session.get(Post, post_id)

        if post is None:
            return jsonify({"error": "Article introuvable"}), 404

        db.session.delete(post)
        db.session.commit()

        return jsonify({"message": "Article supprimé"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)