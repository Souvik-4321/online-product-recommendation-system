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
        