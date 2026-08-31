from flask import Flask, render_template, request
from recommendation import products, recommend_products


app = Flask(__name__)


@app.route("/")
def home():

    # Get search query
    search = request.args.get("search", "")

    # Get selected category
    category = request.args.get("category", "")

    filtered_products = products.copy()

    # Search products
    if search:
        filtered_products = filtered_products[
            filtered_products["name"]
            .str.contains(search, case=False, na=False)
        ]

    # Filter by category
    if category:
        filtered_products = filtered_products[
            filtered_products["category"] == category
        ]

    # Get all categories
    categories = sorted(
        products["category"].unique()
    )

    return render_template(
        "index.html",
        products=filtered_products.to_dict("records"),
        categories=categories,
        search=search,
        selected_category=category
    )


@app.route("/product/<int:product_id>")
def product(product_id):

    selected_product = products[
        products["id"] == product_id
    ]

    if selected_product.empty:
        return "Product not found", 404

    selected_product = selected_product.iloc[0].to_dict()

    recommendations = recommend_products(product_id)

    recommendations = [
        product.to_dict()
        for product in recommendations
    ]

    return render_template(
        "product.html",
        product=selected_product,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)