from flask import Flask
from flask_limiter import Limiter


def test_redis_storage_backend_initializes_without_remote_connection():
    app = Flask(__name__)
    limiter = Limiter(
        key_func=lambda: "qa-test",
        storage_uri="redis://127.0.0.1:6379/0",
        default_limits=[],
    )
    limiter.init_app(app)

    assert type(limiter.storage).__name__ == "RedisStorage"
