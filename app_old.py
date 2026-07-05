import streamlit as st
import pandas as pd
import os
import traceback
import json

from ingestion.json_loader import load_products_json
from validation.validators import validate_product
from analysis.catalog_summary import generate_catalog_summary
from analysis.catalog_health import analyze_catalog_health
import analysis.catalog_health as ch
from storage.catalog_repository import (
    save_catalog,
    save_uploaded_catalog
)
from analysis.product_score import (
    calculate_product_score
)
from tools.ai_description_generator import generate_description
from tools.ai_tag_generator import generate_tags
from tools.ai_image_search import get_image_search_url
from tools.ai_product_reviewer import review_product
from analysis.catalog_score import calculate_catalog_score
from datetime import datetime

import inspect
MASTER_CATALOG = "data/catalogs/master_catalog.json"

# print("=" * 60)
# print("Imported from:", inspect.getsourcefile(calculate_catalog_score))
# print("Signature   :", inspect.signature(calculate_catalog_score))
# print("First line  :", calculate_catalog_score.__code__.co_firstlineno)
# print("=" * 60)

# print("=" * 60)
# print("catalog_health module:")
# print(ch.__file__)
# print("=" * 60)

st.set_page_config(
    page_title="AI Product Advisor"
)
import analysis.catalog_score as cs

import sys
import os

import inspect
from analysis import catalog_health

# st.code(
#     inspect.getsource(catalog_health.analyze_catalog_health),
#     language="python"
# )

st.title("AI Product Advisor")

st.error("THIS IS THE APP.PY I AM EDITING")

uploaded_file = st.file_uploader(
    "Upload Catalog",
    type=["csv", "json"]
)

if uploaded_file:

    st.success(
        "File uploaded successfully"
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

            summary = generate_catalog_summary(
                products
            )

            health_summary, health_issues = analyze_catalog_health(
                products
            )

# #07/03/26
#             json_data = json.dumps(
#                 [product.model_dump() for product in products],
#                 indent=2,
#                 default=str
#             )

#             st.download_button(
#                 "⬇ Download Updated Catalog",
#                 data=json_data,
#                 file_name="updated_catalog.json",
#                 mime="application/json"
#             )
# #07/03/26
#07/05/26
            # # st.subheader("📈 Catalog Improvement Summary")

            # # average_score = (
            # #     sum(
            # #         calculate_product_score(product)["overall_score"]
            # #         for product in products
            # #     )
            # #     / len(products)
            # # )

            # # st.metric(
            # #     "Overall Catalog Score",
            # #     f"{average_score:.0f}/100"
            # # )

            # # ready_products = sum(
            # #     1
            # #     for product in products
            # #     if calculate_product_score(product)["overall_score"] >= 90
            # # )

            # # st.metric(
            # #     "Products Ready",
            # #     f"{ready_products} / {len(products)}"
            # # )    

            # # for i, issue in enumerate(health_issues):
            # #     st.write(i, issue)

            # # st.write(id(health_issues))                        
            # # critical_count = sum(
            # #     1
            # #     for issue in health_issues
            # #     if issue["severity"] == "Critical"
            # # )

            # # warning_count = sum(
            # #     1
            # #     for issue in health_issues
            # #     if issue["severity"] == "Warning"
            # # )            

            # # col1, col2 = st.columns(2)

            # # with col1:
            # #     st.metric(
            # #         "🔴 Critical Issues",
            # #         critical_count
            # #     )

            # # with col2:
            # #     st.metric(
            # #         "🟡 Warning Issues",
            # #         warning_count
            # #     )           

            # st.subheader("Highest Priorities")
            # if health_summary["missing_image"]:

            #     st.error(
            #         f"Upload images for "
            #         f"{health_summary['missing_image']} products."
            #     )

            # if health_summary["missing_url"]:

            #     st.error(
            #         f"Add Product URLs for "
            #         f"{health_summary['missing_url']} products."
            #     )

            # if health_summary["missing_tags"]:

            #     st.warning(
            #         f"Generate SEO Tags for "
            #         f"{health_summary['missing_tags']} products."
            #     )

            # if health_summary["missing_description"]:

            #     st.warning(
            #         f"Generate AI Descriptions for "
            #         f"{health_summary['missing_description']} products."
            #     )

            # if health_summary["missing_product_type"]:

            #     st.warning(
            #         f"Complete Product Type for "
            #         f"{health_summary['missing_product_type']} products."
            #     )

            # potential_score = min(
            #     average_score + 20,
            #     100
            # )

            # st.metric(
            #     "Potential Catalog Score",
            #     f"{potential_score:.0f}/100"
            # )    
#07/05/26

            import inspect


            import inspect

            try:
                result = calculate_catalog_score(health_summary)
            except Exception as e:
                st.error(e)

            import analysis.catalog_score as cs

            import inspect

            import inspect

            import analysis.catalog_score as cs

            import sys

            import dis

            catalog_score = calculate_catalog_score(
                health_summary
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

            st.subheader(
                f"Catalog Issues ({len(health_issues)})"
            )

            if health_issues:

                issues_df = pd.DataFrame(health_issues)

                st.dataframe(
                    issues_df,
                    use_container_width=True
                )
            else:

                st.success(
                    "No catalog issues found."
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
                        "Score": f"{calculate_product_score(product)['overall_score']}/100",
                        "Product URL": product.product_url or ""
                    }
                )

            df = pd.DataFrame(rows)

            st.subheader("Product List")

            st.dataframe(
                df,
                width="stretch"
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
                st.write(f"Vendor: {selected_product.vendor}")
                st.write(f"Category: {selected_product.category}")
                st.write(f"Price: {selected_product.price}")
                if selected_product.product_url:

                    st.link_button(
                        "🔗 Open Product",
                        selected_product.product_url
                    )
                    
                if selected_product.image_url:
                    st.caption(selected_product.image_url)

                st.subheader("Product Image")

                if selected_product.image_url:

                    st.image(
                        selected_product.image_url,
                        width=250
                    )

                else:

                    st.info("No image uploaded.")

                uploaded_image = st.file_uploader(
                    "Upload Product Image",
                    type=["jpg", "jpeg", "png"],
                    key=f"image_{selected_product.product_id}"
                )

                if uploaded_image is not None:

                    if st.button(
                        "Save Image",
                        key=f"save_image_{selected_product.product_id}"
                    ):

                        os.makedirs(
                            "data/images",
                            exist_ok=True
                        )

                        extension = uploaded_image.name.split(".")[-1]

                        image_path = (
                            f"data/images/"
                            f"{selected_product.product_id}.{extension}"
                        )

                        with open(image_path, "wb") as f:
                            f.write(uploaded_image.getbuffer())

                        selected_product.image_url = image_path
                        selected_product.updated_datetime = datetime.now()

                        save_catalog(
                            products,
                            catalog_path
                        )

                        st.success(
                            "Image uploaded successfully."
                        )

                        st.rerun()

                score = calculate_product_score(
                    selected_product
                )

                st.subheader("AI Product Advisor")

                st.progress(score["overall_score"] / 100)

                st.metric(
                    "Overall Product Score",
                    f"{score['overall_score']} / 100"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Images",
                        f"{score['image_score']} / 20"
                    )

                    st.metric(
                        "Description",
                        f"{score['description_score']} / 20"
                    )

                    st.metric(
                        "SEO",
                        f"{score['seo_score']} / 20"
                    )

                with col2:

                    st.metric(
                        "Metadata",
                        f"{score['metadata_score']} / 20"
                    )

                    st.metric(
                        "Completeness",
                        f"{score['completeness_score']} / 20"
                    )

                st.subheader(
                    "Recommendations"
                )

                for recommendation in score["recommendations"]:
                    st.warning(
                        recommendation
                    )

                generated_key = (
                    f"generated_desc_{selected_product.product_id}"
                )

                if generated_key in st.session_state:

                    st.subheader(
                        "AI Suggested Description"
                    )

                    st.text_area(
                        "",
                        value=st.session_state[generated_key],
                        height=180,
                        key=f"display_desc_{selected_product.product_id}"
                    )

                    if st.button(
                        "Accept Description",
                        key=f"accept_desc_{selected_product.product_id}"
                    ):

                        selected_product.description = (
                            st.session_state[generated_key]
                        )

                        st.success(
                            "Description updated. Click Save Changes."
                        )

                    if not selected_product.image_url:

                        st.subheader(
                            "Suggested Image Search"
                        )

                        st.link_button(
                            "Search Images",
                            get_image_search_url(selected_product)
                        )

                    if st.button(
                        "AI Review Product",
                        key=f"review_{selected_product.product_id}"
                    ):

                        try:

                            review = review_product(selected_product)

                        except Exception as e:

                            import traceback
                            st.exception(e)

                            st.code(
                                traceback.format_exc(),
                                language="python"
                            )

                        st.subheader(
                            review["rating"]
                        )

                        st.metric(
                            "Overall AI Review Score",
                            f"{review['score']} / 100"
                        )

                        st.subheader(
                            "Strengths"
                        )

                        for item in review["strengths"]:

                            st.success(item)

                        st.subheader(
                            "Needs Improvement"
                        )

                        for item in review["weaknesses"]:

                            st.warning(item)

                        st.subheader(
                            "AI Recommendations"
                        )

                        for item in review["recommendations"]:

                            st.info(item)
    
                        st.subheader(
                            "AI Suggestions"
                        )

#                        st.json(review)    

                ##################################################
                # AI Description Generator
                ##################################################

                description_key = (
                    f"description_{selected_product.product_id}"
                )

                tag_key = (
                    f"tags_{selected_product.product_id}"
                )

                if st.button(
                    "Generate AI Description",
                    key=f"generate_desc_{selected_product.product_id}"
                ):

                    with st.spinner(
                        "Generating AI description..."
                    ):

                        st.session_state[
                            description_key
                        ] = generate_description(
                            selected_product
                        )

                ##################################################
                # Show Suggested Description
                ##################################################

                if description_key in st.session_state:

                    st.subheader(
                        "AI Suggested Description"
                    )

                    description = st.text_area(
                        "Suggested Description",
                        value=st.session_state[description_key],
                        height=220,
                        key=f"ai_desc_{selected_product.product_id}"
                    )

                st.success("REACHED AI EDIT SECTION")

                if st.button(
                    "✨ Generate SEO Tags",
                    key=f"generate_tags_{selected_product.product_id}"
                ):

                    with st.spinner(
                        "Generating SEO tags..."
                    ):

                        temp_product = selected_product

                        temp_product.description = (
                            description
                            if "description" in locals()
                            else selected_product.description
                        )

                        st.session_state[tag_key] = generate_tags(
                            temp_product
                        )

                ##################################################
                # Product Edit Form
                ##################################################

                with st.form(
                    f"product_form_{selected_product.product_id}"
                ):

                    ##################################################
                    # Description
                    ##################################################

                    description = st.text_area(
                        "Description",
                        value=(
                            st.session_state.get(
                                description_key,
                                selected_product.description or ""
                            )
                        ),
                        height=220
                    )

                    ##################################################
                    # Product URL
                    ##################################################

                    new_url = st.text_input(
                        "URL",
                        value=selected_product.product_url or ""
                    )

                    ##################################################
                    # Inventory
                    ##################################################

                    new_inventory = st.number_input(
                        "Inventory Quantity",
                        min_value=0,
                        value=selected_product.inventory_qty or 0
                    )

                    ##################################################
                    # Product Type
                    ##################################################

                    new_product_type = st.text_input(
                        "Product Type",
                        value=selected_product.product_type or ""
                    )

                    ##################################################
                    # SEO Tags
                    ##################################################

                    tag_string = st.text_input(
                        "SEO Tags (comma separated)",
                        value=", ".join(

                            st.session_state.get(

                                tag_key,

                                selected_product.tags

                            )

                        )
                    )


                    ##################################################
                    # Save Button
                    ##################################################

                    submitted = st.form_submit_button(
                        "💾 Save Changes"
                    )

                    if submitted:
                        selected_product.description = description

                        #selected_product.product_url = new_url
                        ##################################################
                        # Product URL
                        ##################################################

                        selected_product.product_url = new_url.strip()

                        selected_product.inventory_qty = new_inventory

                        selected_product.product_type = new_product_type.strip()

                        selected_product.tags = [
                            tag.strip()
                            for tag in tag_string.split(",")
                            if tag.strip()
                        ]
                        selected_product.updated_datetime = datetime.now()
                        if selected_product.updated_datetime:
                            st.caption(
                                f"Last Updated: {selected_product.updated_datetime:%d %b %Y %I:%M %p}"
                            )


                        save_catalog(
                            products,
                            catalog_path
                        )

                        st.success(
                            "Product updated successfully."
                        )

                        st.rerun()

                if submitted:
                    ##################################################
                    # Description
                    ##################################################

                    selected_product.description = description.strip()

                    ##################################################
                    # URL
                    ##################################################

                    ##################################################
                    # Inventory
                    ##################################################

                    ##################################################
                    # Product Type
                    ##################################################

                    ##################################################
                    # SEO Tags
                    ##################################################
                    selected_product.updated_datetime = datetime.now()

                    selected_product.tags = [

                        tag.strip()

                        for tag in tag_string.split(",")

                        if tag.strip()

                    ]

                    ##################################################
                    # Save JSON
                    ##################################################
                    selected_product.updated_datetime = datetime.now()

                    save_catalog(
                        products,
                        catalog_path
                    )

                    if description_key in st.session_state:
                        del st.session_state[description_key]

                    if tag_key in st.session_state:
                        del st.session_state[tag_key]    

                    st.success(
                        f"Product saved for {selected_product.product_id}"
                    )

                    st.rerun()

        except Exception:
            st.exception(traceback.format_exc())