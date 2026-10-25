import unittest

from app import create_app, db


class BlogApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        })
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_posts(self):
        response = self.client.get("/api/posts")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_post(self):
        response = self.client.post(
            "/api/posts",
            json={
                "title": "Mon premier article",
                "content": "Le contenu de mon article.",
                "author": "Alex",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["title"], "Mon premier article")

    def test_create_post_with_missing_fields(self):
        response = self.client.post(
            "/api/posts",
            json={"title": "Article incomplet"},
        )

        self.assertEqual(response.status_code, 400)

    def test_get_one_post(self):
        created = self.client.post(
            "/api/posts",
            json={
                "title": "Article à lire",
                "content": "Voici le contenu.",
                "author": "Alex",
            },
        )
        post_id = created.get_json()["id"]

        response = self.client.get(f"/api/posts/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["title"], "Article à lire")

    def test_update_post(self):
        created = self.client.post(
            "/api/posts",
            json={
                "title": "Ancien titre",
                "content": "Contenu",
                "author": "Alex",
            },
        )
        post_id = created.get_json()["id"]

        response = self.client.put(
            f"/api/posts/{post_id}",
            json={
                "title": "Nouveau titre",
                "content": "Contenu modifié",
                "author": "Alex",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["title"], "Nouveau titre")

    def test_delete_post(self):
        created = self.client.post(
            "/api/posts",
            json={
                "title": "Article à supprimer",
                "content": "Contenu",
                "author": "Alex",
            },
        )
        post_id = created.get_json()["id"]

        response = self.client.delete(f"/api/posts/{post_id}")

        self.assertEqual(response.status_code, 200)

        missing_post = self.client.get(f"/api/posts/{post_id}")
        self.assertEqual(missing_post.status_code, 404)


if __name__ == "__main__":
    unittest.main()