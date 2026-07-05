import streamlit as st
import pandas as pd
import os
import traceback

from ingestion.json_loader import load_products_json
from validation.validators import validate_product
from analysis.catalog_summary import generate_catalog_summary
from analysis.catalog_health import analyze_catalog_health
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

import inspect

print("=" * 60)
print("Imported from:", inspect.getsourcefile(calculate_catalog_score))
print("Signature   :", inspect.signature(calculate_catalog_score))
print("First line  :", calculate_catalog_score.__code__.co_firstlineno)
print("=" * 60)

st.set_page_config(
    page_title="AI Product Advisor"
)
import analysis.catalog_score as cs

st.write(cs.__file__)

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

            st.write("Health Summary:")
            st.write(health_summary)

            st.write(type(health_summary))

            st.write("Keys:")
            st.write(list(health_summary.keys()))

            st.json(health_summary)

            print("HEALTH SUMMARY =", health_summary)
            print("TYPE =", type(health_summary))
            print("KEYS =", health_summary.keys())

            import inspect

            st.write("Function object:")
            st.write(calculate_catalog_score)

            st.write("Module:")
            st.write(calculate_catalog_score.__module__)

            st.write("Source file:")
            st.write(inspect.getsourcefile(calculate_catalog_score))

            st.write("Signature:")
            st.code(str(inspect.signature(calculate_catalog_score)))

            st.write("Actual source Python imported:")
            st.code(inspect.getsource(calculate_catalog_score))

            import inspect

            st.write("Signature:", inspect.signature(calculate_catalog_score))
            st.write("__signature__:", getattr(calculate_catalog_score, "__signature__", None))
            st.write("__defaults__:", calculate_catalog_score.__defaults__)
            st.write("Argument count:", calculate_catalog_score.__code__.co_argcount)
            st.write("Variable names:", calculate_catalog_score.__code__.co_varnames)

            st.write("Calling with ONE argument...")

            try:
                result = calculate_catalog_score(health_summary)
                st.success("One-argument call succeeded")
                st.write(result)
            except Exception as e:
                st.error(e)

            st.write("Calling with TWO arguments...")

            try:
                result = calculate_catalog_score(summary, health_summary)
                st.success("Two-argument call succeeded")
                st.write(result)
            except Exception as e:
                st.error(e)

            import analysis.catalog_score as cs

            st.write("Module object:")
            st.write(cs)

            st.write("Module dict entry:")
            st.write(cs.__dict__["calculate_catalog_score"])

            import inspect

            st.write("Source file:")
            st.write(inspect.getfile(cs.calculate_catalog_score))

            st.write("Source lines:")
            st.code(
                "".join(
                    inspect.getsourcelines(cs.calculate_catalog_score)[0]
                )
            )

            st.write(id(calculate_catalog_score))
            st.write(id(cs.calculate_catalog_score))

            import inspect

            st.write("Function object:", calculate_catalog_score)

            st.write("__signature__ exists:",
                    hasattr(calculate_catalog_score, "__signature__"))

            st.write("__signature__ value:",
                    getattr(calculate_catalog_score, "__signature__", None))

            st.write("__wrapped__ exists:",
                    hasattr(calculate_catalog_score, "__wrapped__"))

            st.write("__wrapped__:",
                    getattr(calculate_catalog_score, "__wrapped__", None))

            st.write("Code argcount:",
                    calculate_catalog_score.__code__.co_argcount)

            st.write("Code varnames:",
                    calculate_catalog_score.__code__.co_varnames)

            st.write("Defaults:",
                    calculate_catalog_score.__defaults__)

            import analysis.catalog_score as cs

            import sys

            st.write("Module ID:")
            st.write(id(cs))

            st.write("Module in sys.modules:")
            st.write(id(sys.modules["analysis.catalog_score"]))

            st.write("Same object?")
            st.write(cs is sys.modules["analysis.catalog_score"])

            st.write("Module file:")
            st.write(cs.__file__)

            import dis

            st.subheader("Disassembly")

            disassembly = dis.Bytecode(cs.calculate_catalog_score)

            for instruction in disassembly:
                st.text(instruction)            

            catalog_score = calculate_catalog_score(
                health_summary
            )

            st.write("After calculate_catalog_score")
            st.write(catalog_score)

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
                st.write(f"Product URL: {selected_product.product_url}")
                st.write(f"Inventory: {selected_product.inventory_qty}")
                st.write(f"Image: {selected_product.image_url}")
                st.write(f"Tags: {selected_product.tags}")

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

                            st.write("Type:", type(review))
                            st.write(review)

                        except Exception as e:

                            import traceback
                            st.exception(e)

                            st.code(
                                traceback.format_exc(),
                                language="python"
                            )

                        st.write("Function:", review_product)
                        st.write("Module:", review_product.__module__)

                        st.write(type(review))
                        st.write(review.keys())                        
                        st.write(review)
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

                        st.json(review)    

                ##################################################
                # AI Description Generator
                ##################################################

                description_key = (
                    f"generated_desc_{selected_product.product_id}"
                )

                tag_key = (
                    f"generated_tags_{selected_product.product_id}"
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

                if st.button(
                    "âœ¨ Generate SEO Tags",
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
                        "Product URL",
                        value=selected_product.product_url or ""
                    )

                    ##################################################
                    # Inventory
                    ##################################################

                    inventory = st.number_input(
                        "Inventory Quantity",
                        min_value=0,
                        value=selected_product.inventory_qty or 0,
                        step=1
                    )

                    ##################################################
                    # Product Type
                    ##################################################

                    product_type = st.text_input(
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
                        "Save Changes"
                    )

                if submitted:
                    ##################################################
                    # Description
                    ##################################################

                    selected_product.description = description.strip()

                    ##################################################
                    # URL
                    ##################################################

                    new_url = new_url.strip()

                    if (
                        new_url
                        and not new_url.startswith(("http://", "https://"))
                    ):
                        new_url = "https://" + new_url

                    selected_product.product_url = new_url

                    ##################################################
                    # Inventory
                    ##################################################

                    selected_product.inventory_qty = inventory

                    ##################################################
                    # Product Type
                    ##################################################

                    selected_product.product_type = product_type.strip()

                    ##################################################
                    # SEO Tags
                    ##################################################

                    selected_product.tags = [

                        tag.strip()

                        for tag in tag_string.split(",")

                        if tag.strip()

                    ]

                    ##################################################
                    # Save JSON
                    ##################################################

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