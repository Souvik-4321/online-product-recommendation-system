import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load product dataset
products = pd.read_csv("products.csv")


# Fill empty descriptions
products["description"] = products["description"].fillna("")


# Combine important product information
products["features"] = (
    products["category"] + " " +
    products["brand"] + " " +
    products["description"]
)


# Convert text into numerical vectors
vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(products["features"])


# Calculate similarity between products
similarity_matrix = cosine_similarity(tfidf_matrix)


def recommend_products(product_id, number_of_recommendations=5):

    # Find the index of selected product
    product_index = products[
        products["id"] == product_id
    ].index[0]

    # Get similarity scores
    similarity_scores = list(
        enumerate(similarity_matrix[product_index])
    )

    # Sort products according to similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected product
    similarity_scores = similarity_scores[1:]

    # Get top recommendations
    recommended_products = []

    for index, score in similarity_scores[
        :number_of_recommendations
    ]:

        product = products.iloc[index].copy()

        product["similarity"] = round(score, 3)

        recommended_products.append(product)

    return recommended_products


# Test the recommendation system
if __name__ == "__main__":

    recommendations = recommend_products(1)

    print("\nRecommendations for Samsung Galaxy S24:\n")

    for product in recommendations:
        print(
            product["name"],
            "Similarity:",
            product["similarity"]
        )
def personalized_recommendations(user_product_ids, products, top_n=6):

    if not user_product_ids:
        recommendations = products.head(top_n).copy()

        recommendations["score"] = recommendations["rating"] * 0.5

        recommendations["recommendation_reason"] = (
            "Popular product with a good rating"
        )

        return recommendations

    viewed_products = products[
        products["id"].isin(user_product_ids)
    ]

    if viewed_products.empty:
        recommendations = products.head(top_n).copy()

        recommendations["score"] = recommendations["rating"] * 0.5

        recommendations["recommendation_reason"] = (
            "Popular product with a good rating"
        )

        return recommendations

    # Find preferred category
    category_counts = viewed_products["category"].value_counts()
    preferred_category = category_counts.index[0]

    # Find preferred brand
    brand_counts = viewed_products["brand"].value_counts()
    preferred_brand = brand_counts.index[0]

    recommendations = products.copy()

    # Remove already viewed products
    recommendations = recommendations[
        ~recommendations["id"].isin(user_product_ids)
    ]

    # Create recommendation score
    recommendations["score"] = 0.0

    # Category preference
    recommendations.loc[
        recommendations["category"] == preferred_category,
        "score"
    ] += 3

    # Brand preference
    recommendations.loc[
        recommendations["brand"] == preferred_brand,
        "score"
    ] += 2

    # Rating contribution
    recommendations["score"] += recommendations["rating"] * 0.5

    # Create explanation
    def get_reason(row):

        reasons = []

        if row["category"] == preferred_category:
            reasons.append(
                f"you viewed {preferred_category} products"
            )

        if row["brand"] == preferred_brand:
            reasons.append(
                f"you showed interest in {preferred_brand}"
            )

        if row["rating"] >= 4.5:
            reasons.append(
                "it has a highly rated product"
            )

        if reasons:
            return "Recommended because " + " and ".join(reasons)

        return "Recommended based on your browsing activity"

    recommendations["recommendation_reason"] = recommendations.apply(
        get_reason,
        axis=1
    )

    recommendations = recommendations.sort_values(
        by="score",
        ascending=False
    ).head(top_n)

    return recommendations     