from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import check_password_hash

from recommendation import (
    products,
    recommend_products
)

from database import (
    create_tables,
    add_user,
    get_user_by_email,
    add_activity,
    get_recently_viewed,
    
)


app = Flask(__name__)

# Secret key for sessions
app.secret_key = "change-this-secret-key"


# Create database tables
create_tables()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    search = request.args.get("search", "")

    category = request.args.get("category", "")

    filtered_products = products.copy()

    # Search
    if search:

        filtered_products = filtered_products[
            filtered_products["name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # Category filter
    if category:

        filtered_products = filtered_products[
            filtered_products["category"] == category
        ]

    categories = sorted(
        products["category"].unique()
    )

    return render_template(
        "index.html",

        products=filtered_products.to_dict(
            "records"
        ),

        categories=categories,

        search=search,

        selected_category=category
    )


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        if not name or not email or not password:

            flash("Please fill all fields.")

            return redirect(
                url_for("register")
            )

        user_id = add_user(
            name,
            email,
            password
        )

        if user_id is None:

            flash(
                "Email already registered."
            )

            return redirect(
                url_for("register")
            )

        flash(
            "Registration successful. Please login."
        )

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password."
        )

    return render_template("login.html")


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    recently_viewed_ids = (
        get_recently_viewed(user_id)
    )

    recently_viewed = []

    for row in recently_viewed_ids:

        product = products[
            products["id"] == row["product_id"]
        ]

        if not product.empty:

            recently_viewed.append(
                product.iloc[0].to_dict()
            )

    return render_template(
        "dashboard.html",

        user_name=session["user_name"],

        recently_viewed=recently_viewed
    )


# ==========================================
# PRODUCT DETAILS
# ==========================================

@app.route("/product/<int:product_id>")
def product(product_id):

    selected_product = products[
        products["id"] == product_id
    ]

    if selected_product.empty:

        return "Product not found", 404

    selected_product = (
        selected_product
        .iloc[0]
        .to_dict()
    )

    # Save view activity
    if "user_id" in session:

        add_activity(
            session["user_id"],
            product_id,
            "view"
        )

    # Generate recommendations
    recommendations = recommend_products(
        product_id
    )

    recommendations = [

        product.to_dict()

        for product in recommendations
    ]

    return render_template(
        "product.html",

        product=selected_product,

        recommendations=recommendations
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)