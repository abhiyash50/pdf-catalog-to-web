from app.services.image_export import build_web_image_path
from app.services import product_parser


def test_web_image_path_prefers_static_upload_prefix():
    web_path = build_web_image_path("abc123", "page1_img1.png")

    assert web_path.startswith("/static/uploads/abc123/")
    assert "/app/" not in web_path
    assert "D:" not in web_path


def test_web_image_path_normalizes_backslashes():
    web_path = build_web_image_path("job456", r"nested\\page1_img1.png")

    assert "\\" not in web_path
    assert web_path.endswith("/page1_img1.png")


def test_parsed_products_store_web_paths():
    job_id = "job789"
    web_path = build_web_image_path(job_id, "page1_img1.png")

    products = product_parser.parse_products([(1, "Widget\n$10")], {1: [web_path]})

    assert products[0].image_path == web_path
    assert products[0].image_path.startswith("/static/uploads/")
