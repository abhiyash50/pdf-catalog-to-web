import re

from app.services.product_parser import PRICE_PATTERN, parse_products


SAMPLE_TEXT_BLOCKS = [
    (1, """Product Alpha\n\nThis is a great item for daily use.\nPrice: Rs. 1,299"""),
    (2, """Beta Gadget\n\nコンパクトで軽量です。 Only $49.99!"""),
]


def test_price_regex_matches_various_formats():
    prices = [
        "Rs. 1,299",
        "INR 999",
        "$49.99",
        "€12.00",
        "1999",
        "¥12,000",
        "12,000円",
    ]
    for price in prices:
        assert re.search(PRICE_PATTERN, price)


def test_parse_products_creates_entries():
    products = parse_products(
        SAMPLE_TEXT_BLOCKS,
        {
            1: ["/static/uploads/job/img1.png"],
            2: ["/static/uploads/job/img2.png"],
        },
    )
    assert len(products) == 2
    assert products[0].name == "Product Alpha"
    assert "great item" in products[0].description
    assert products[0].price is not None
    assert products[0].image_path is not None
    assert products[1].price == "$49.99"
    assert products[1].name == "Beta Gadget"


def test_parse_products_handles_japanese_text():
    japanese_block = (3, "商品名：テスト\n\nこれはサンプルの説明です。価格は12,000円です。")
    products = parse_products([japanese_block], {})
    assert products[0].name.startswith("商品名")
    assert products[0].price == "12,000円"
