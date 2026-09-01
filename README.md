# 🛍️ Online Product Recommendation System

A machine learning-based web application that recommends similar products to users based on product information such as category, brand, and description.

The system uses **TF-IDF Vectorization** and **Cosine Similarity** to analyze product features and generate relevant product recommendations.

## 🚀 Live Demo

The application is deployed online using Render and can be accessed from any device with an internet connection.

## 📌 Project Overview

The Online Product Recommendation System is designed to improve the online shopping experience by helping users discover products that are similar to the products they are interested in.

For example, if a user views a smartphone, the system analyzes its features and recommends other similar smartphones.

### Example

If a user views:

**Samsung Galaxy S24**

The system may recommend:

- Samsung Galaxy S23
- OnePlus 12
- Google Pixel 8
- iPhone 15

## ✨ Features

- 🔍 Product Search
- 📂 Category Filtering
- 🛍️ Product Listing
- 📱 Product Details
- ⭐ Product Ratings
- 🤖 Machine Learning-Based Recommendations
- 🔄 Similar Product Recommendations
- 📱 Responsive Web Design
- 🌐 Online Deployment

## 🧠 Recommendation Algorithm

The system currently uses a **Content-Based Filtering** approach.

### Working Process

```text
Product Information
        ↓
Feature Combination
        ↓
TF-IDF Vectorization
        ↓
Cosine Similarity
        ↓
Similarity Scores
        ↓
Top Similar Products
        ↓
Recommended Products
```
## TF-IDF

TF-IDF (Term Frequency-Inverse Document Frequency) converts the textual product information into numerical vectors that can be processed by the machine learning algorithm.

## Cosine Similarity

Cosine Similarity measures how similar two product vectors are.

A higher similarity score means the products have more similar features.

## 🛠️ Technologies Used
| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Backend programming       |
| Flask        | Web application framework |
| Pandas       | Data processing           |
| Scikit-learn | Machine learning          |
| HTML         | Web page structure        |
| CSS          | Website styling           |
| CSV          | Product dataset           |
| Git          | Version control           |
| GitHub       | Source code management    |
| Render       | Cloud deployment          |

## 📂 Project Structure

Online-Product-Recommendation-System/
│

├── app.py

├── recommendation.py

├── products.csv

├── requirements.txt

├── .gitignore

│
├── templates/

  │   ├── index.html

  │   └── product.html

│
└── static/

  └── style.css

## ⚙️ How to Run Locally
1. Clone the repository
   ```bash
   git clone https://github.com/Souvik-4321/online-product-recommendation-system.git
   ```
2. Open the project folder
   ```bash
   cd Online-Product-Recommendation-System
   ```
3. Create a virtual environment
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment

Windows:
```bash
venv\Scripts\activate
```
5. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
6. Run the Flask application
   ```bash
   python app.py
   ```
7. Open the application
   ```bash
   http://127.0.0.1:5000
   ```

## 📊 Dataset

The project currently uses a product dataset stored in:
```bash
products.csv
```
The dataset contains information such as:

* Product ID
* Product Name
* Category
* Brand
* Description
* Price
* Rating

## 🎯 Objectives

The main objectives of this project are:

* To develop an online product recommendation system.
* To apply machine learning techniques to product data.
* To recommend products based on similarity.
* To improve product discovery for users.
* To provide a simple and responsive web interface.
* To demonstrate the practical use of Python and machine learning in e-commerce.
  
## 🔮 Future Enhancements

The system can be further improved by adding:

* 👤 User Registration and Login
* 🗄️ MySQL/SQLite Database
* ⭐ User Ratings and Reviews
* ❤️ Wishlist
* 🛒 Shopping Cart
* 👀 Recently Viewed Products
* 🤝 Collaborative Filtering
* 🧠 Hybrid Recommendation System
* 👨‍💼 Admin Dashboard
* 📈 Recommendation Performance Analysis
* 👤 Personalized Recommendations

## 👨‍💻 Project Status

🚧 Currently in Development

Completed
 * Product dataset
 * Flask backend
 * Content-based recommendation system
 * TF-IDF implementation
 * Cosine similarity
 * Product search
 * Category filtering
 * Responsive UI
 * GitHub repository
 * Online deployment
   
Planned
 * User authentication
 * Database integration
 * Ratings and reviews
 * User activity tracking
 * Collaborative filtering
 * Hybrid recommendation system
 * Admin dashboard

## 📜 License

This project is developed for educational and academic purposes as a final-year project.
