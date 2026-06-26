import streamlit as st
import pandas as pd

from ingestion.json_loader import load_products_json
from validation.validators import validate_product
from analysis.catalog_summary import generate_catalog_summary
from analysis.catalog_health import analyze_catalog_health
from storage.catalog_repository import (
    save_catalog,
    save_uploaded_catalog
)

st.set_page_config(
    page_title="AI Product Advisor"
)

st.title("AI Product Advisor")

uploaded_file = st.file_uploader(
    "Upload Catalog",
    type=["csv", "json"]
)

if uploaded_file:

    st.success(
        "File uploaded successfully"
    )

    st.write(
        f"File Name: {uploaded_file.name}"
    )

    st.write(
        f"File Size: {uploaded_file.size} bytes"
    )

    if uploaded_file.name.endswith(".json"):

#Needs to be fixed
        if "catalog_path" not in st.session_state:

            st.session_state.catalog_path = (
                save_uploaded_catalog(
                    uploaded_file
                )
            )

        catalog_path = (
            st.session_state.catalog_path
        )

        st.write(
            f"Temporary File: {catalog_path}"
        )

        try:

            products = load_products_json(
                catalog_path,
                catalog_id="CAT001"
            )

            validation_errors = []


            for product in products:

                errors = validate_product(
                    product
                )

                validation_errors.extend(
                    errors
                )

            st.subheader(
                "Upload Results"
            )

            st.write(
                f"Products Loaded: {len(products)}"
            )

            st.write(
                f"Validation Errors: {len(validation_errors)}"
            )

            if validation_errors:

                st.error(
                    "Validation Errors Found"
                )

                for error in validation_errors:

                    st.write(error)

            summary = generate_catalog_summary(
                products
            )

            health_summary, health_issues = analyze_catalog_health(
                products
            )

            st.subheader(
                "Catalog Summary"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Products",
                    summary["total_products"]
                )

                st.metric(
                    "Vendors",
                    summary["vendors"]
                )

                st.metric(
                    "Categories",
                    summary["categories"]
                )

            with col2:

                st.metric(
                    "Product Types",
                    summary["product_types"]
                )

                st.metric(
                    "Inventory",
                    summary["inventory_total"]
                )

                st.metric(
                    "Max Price",
                    summary["max_price"]
                )

            st.subheader("Catalog Health")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Missing URLs",
                    health_summary["missing_url"]
                )

                st.metric(
                    "Missing Descriptions",
                    health_summary["missing_description"]
                )

                st.metric(
                    "Missing Vendors",
                    health_summary["missing_vendor"]
                )

                st.metric(
                    "Missing Categories",
                    health_summary["missing_category"]
                )

            with col2:

                st.metric(
                    "Missing Images",
                    health_summary["missing_image"]
                )

                st.metric(
                    "Missing Tags",
                    health_summary["missing_tags"]
                )

                st.metric(
                    "Missing Product Types",
                    health_summary["missing_product_type"]
                )

                st.metric(
                    "Missing Inventory",
                    health_summary["missing_inventory"]
                )

            st.subheader("Catalog Issues")

            if health_issues:

                issue_df = (
                    pd.DataFrame(health_issues)
                    .sort_values(
                        by=["Product ID", "Issue"]
                    )
                )

                st.dataframe(
                    issue_df,
                    width="stretch"
                )

            else:

                st.success(
                    "No catalog issues found."
                )
                
            st.subheader(
                f"Catalog Issues ({len(health_issues)})"
            )

            rows = []

            for product in products:

                rows.append(
                    {
                        "Product ID": product.product_id,
                        "Title": product.title,
                        "Vendor": product.vendor,
                        "Category": product.category,
                        "Price": product.price,
                        "Status": product.status,
                        "Product URL": product.product_url or ""
                    }
                )

            df = pd.DataFrame(rows)

            st.subheader("Product List")

            st.dataframe(
                df,
                width="stretch"
            )

            st.subheader(
                "Catalog Health"
            )

            #Begin
            
            # End       

            st.subheader("Select Product")

            selected_product_id = st.selectbox(
                "Product",
                df["Product ID"]
            )

            selected_product = next(
                (
                    p for p in products
                    if p.product_id == selected_product_id
                ),
                None
            )

            if selected_product:

                st.subheader("Product Detail")

                st.write(f"Product ID: {selected_product.product_id}")
                st.write(f"Title: {selected_product.title}")
                st.write(f"Description: {selected_product.description}")
                st.write(f"Vendor: {selected_product.vendor}")
                st.write(f"Category: {selected_product.category}")
                st.write(f"Price: {selected_product.price}")
                st.write(f"Status: {selected_product.status}")



                with st.form(f"product_form_{selected_product.product_id}"):

                    new_url = st.text_input(
                        "Product URL",
                        value=selected_product.product_url or ""
                    )

                    submitted = st.form_submit_button(
                        "Save URL"
                    )

                if submitted:

                    new_url = new_url.strip()

                    if new_url and not (
                        new_url.startswith("http://")
                        or new_url.startswith("https://")
                    ):
                        new_url = "https://" + new_url

                    # Update the Product object
                    selected_product.product_url = new_url

                    # Save to disk
                    save_catalog(
                        products,
                        catalog_path
                    )

                    # Reload the products from the saved file
                    products = load_products_json(
                        catalog_path,
                        catalog_id="CAT001"
                    )

                    st.success(
                        f"URL saved for {selected_product.product_id}"
                    )

        except Exception as e:

            st.error(
                f"Error loading catalog: {str(e)}"
            )