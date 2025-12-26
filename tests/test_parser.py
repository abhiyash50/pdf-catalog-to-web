import re

from app.services.product_parser import PRICE_PATTERN, parse_products


SAMPLE_TEXT_BLOCKS = [
    """Product Alpha\n\nThis is a great item for daily use.\nPrice: Rs. 1,299""",
    """Beta Gadget\n\nCompact and lightweight. Only $49.99!""",
]


def test_price_regex_matches_various_formats():
    prices = [
        "Rs. 1,299",
        "INR 999",
        "$49.99",
        "€12.00",
        "1999",
    ]
    for price in prices:
        assert re.search(PRICE_PATTERN, price)


def test_parse_products_creates_entries():
    products = parse_products(SAMPLE_TEXT_BLOCKS, {0: ["/static/uploads/job/img1.png"]})
    assert len(products) == 2
    assert products[0].name == "Product Alpha"
    assert "great item" in products[0].description
    assert products[0].price is not None
    assert products[0].image_path is not None
    assert products[1].price == "$49.99"
