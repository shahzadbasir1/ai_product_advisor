# AI Product Advisor

An AI-powered application that analyzes product catalogs, identifies data quality issues, scores product completeness, and uses Large Language Models (LLMs) to generate high-quality product descriptions and SEO tags.

The application is designed to help e-commerce businesses improve catalog quality, increase search engine visibility, and prepare product data for online marketplaces.

---

# Features

## Catalog Upload

- Upload product catalogs in JSON format
- Automatic catalog validation
- Detect missing required fields
- Display upload summary

---

## Catalog Health Dashboard

Automatically analyzes the uploaded catalog and reports:

- Missing Images
- Missing URLs
- Missing Product Descriptions
- Missing Product Types
- Missing Inventory
- Missing SEO Tags
- Missing Vendors
- Missing Categories

---

## Catalog Quality Score

Generates an overall catalog quality score based on missing information.

Example:

```
Catalog Score: 50 / 100
★★★★☆ Good
```

---

## Product Quality Score

Each product receives an AI quality score based on:

- Image Quality
- Description Quality
- SEO Readiness
- Metadata Completeness
- Overall Product Completeness

Example:

```
Overall Product Score

33 / 100
```

---

## Product Recommendations

Automatically generates actionable recommendations such as:

- Upload a product image
- Improve the product description
- Generate SEO tags
- Complete product metadata
- Add a product URL

---

## AI Description Generator

Uses OpenAI to generate rich product descriptions based on product information.

Example workflow:

```
Select Product
        ↓
Generate AI Description
        ↓
Review Description
        ↓
Edit (optional)
        ↓
Save
```

---

## AI SEO Tag Generator

Generates SEO-friendly keyword tags using OpenAI.

Example:

```
hydrating shampoo
dry hair
hair care
moisture shampoo
professional salon shampoo
```

---

## Product Editing

Users can edit product information directly within the application.

Editable fields include:

- Description
- Product URL
- Inventory
- Product Type
- SEO Tags
- Product Image

Changes can be saved back to the catalog.

---

## Product Image Upload

Supports uploading product images.

Uploaded images are stored locally and linked to the product.

---

# Project Architecture

```
                    Streamlit UI
                          │
                          ▼
                  Business Logic Layer
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Catalog Health     Product Scoring    AI Services
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                  Repository Layer
                          │
                          ▼
                    JSON Catalog
```

---

# Project Structure

```
ai-product-advisor/

│
├── analysis/
│   ├── catalog_health.py
│   ├── catalog_score.py
│   ├── catalog_summary.py
│   ├── catalog_issues.py
│   └── product_score.py
│
├── models/
│   └── product.py
│
├── repositories/
│   └── catalog_repository.py
│
├── ai/
│   ├── description_generator.py
│   └── seo_generator.py
│
├── data/
│   ├── catalogs/
│   └── images/
│
├── app.py
│
└── requirements.txt
```

---

# Technologies Used

| Category | Technology |
|------------|----------------|
| Language | Python 3 |
| Frontend | Streamlit |
| AI | OpenAI GPT |
| Data Models | Pydantic |
| Storage | JSON |
| Version Control | Git |
| IDE | Visual Studio Code |

---

# AI Features

Current AI capabilities include:

- AI Product Description Generation
- AI SEO Tag Generation

Future enhancements may include:

- AI Product Categorization
- AI Image Analysis
- AI Product Type Detection
- AI Catalog Optimization
- AI Product Recommendations

---

# Product Scoring Model

Overall Product Score is calculated using five weighted categories.

| Category | Maximum Score |
|------------|--------------|
| Image | 20 |
| Description | 20 |
| SEO | 20 |
| Metadata | 20 |
| Completeness | 20 |

Maximum Score

```
100 / 100
```

---

# Catalog Health Checks

The application currently validates:

- Missing Images
- Missing URLs
- Missing Descriptions
- Missing Product Types
- Missing Inventory
- Missing SEO Tags
- Missing Vendors
- Missing Categories

---

# Installation

Clone the repository

```bash
git clone https://github.com/shahzadbasir1/ai_product_advisor.git
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

```bash
streamlit run app.py
```

---

# Sample Workflow

```
Upload Catalog
        ↓
Validate Catalog
        ↓
Generate Catalog Health
        ↓
Calculate Catalog Score
        ↓
Select Product
        ↓
Generate AI Description
        ↓
Generate SEO Tags
        ↓
Edit Product
        ↓
Upload Product Image
        ↓
Save Changes
        ↓
Recalculate Product Score
```

---

# Future Roadmap

- FastAPI Backend
- PostgreSQL Database
- User Authentication
- Bulk AI Product Description Generation
- Bulk SEO Tag Generation
- Image Quality Detection
- Product Image Background Removal
- Duplicate Product Detection
- Vector Database Search
- RAG-based Product Knowledge
- Multi-Agent AI Workflow
- Deployment to Azure or AWS

---

# Author

**Shahzad Basir**

AI Product Advisor was developed as part of an Agentic AI portfolio demonstrating practical applications of:

- Artificial Intelligence
- Large Language Models (LLMs)
- Product Data Quality
- E-commerce Catalog Optimization
- Streamlit Application Development
- Python Software Engineering