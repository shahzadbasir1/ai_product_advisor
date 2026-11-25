import streamlit as st
import pandas as pd
import os
import traceback
import requests

from ingestion.json_loader import load_products_json
from models.product import Product
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
from tools.ai_image_search import get_image_search_url
from tools.ai_product_reviewer import review_product
from analysis.catalog_score import calculate_catalog_score
from api_client import (
    generate_description_api,
    generate_tags_api,
    generate_product_type_api,
    upload_knowledge_document_api,
    list_knowledge_documents_api,
    load_shopify_products_api
)

import inspect

# print("=" * 60)
# print("Imported from:", inspect.getsourcefile(calculate_catalog_score))
# print("Signature   :", inspect.signature(calculate_catalog_score))
# print("First line  :", calculate_catalog_score.__code__.co_firstlineno)
# print("=" * 60)

st.set_page_config(
    page_title="AI Product Advisor"
)
import analysis.catalog_score as cs

#st.write(cs.__file__)

st.title("AI Product Advisor")

# ---------------------------------------------------------
# Merchant Knowledge Base
# ---------------------------------------------------------

st.subheader("Merchant Knowledge Base")

merchant_id = st.text_input(
    "Merchant ID (*)",
    placeholder="e.g. oribe"
)

knowledge_file = st.file_uploader(
    "Upload Knowledge Document",
    type=["txt", "pdf", "docx"],
    key="knowledge_document"
)

if st.button("Upload & Index Knowledge"):

    if not merchant_id.strip():
        st.warning("Please enter a Merchant ID.")

    elif knowledge_file is None:
        st.warning("Please select a knowledge document.")

    else:
        try:
            result = upload_knowledge_document_api(
                merchant_id.strip().lower(),
                knowledge_file
            )

            st.success(
                f"{result['document']} successfully indexed "
                f"({result['chunks_indexed']} chunks)."
            )

        except Exception as e:
            st.error(
                f"Knowledge document upload failed: {e}"
            )

# ---------------------------------------------------------
# Uploaded Knowledge
# ---------------------------------------------------------

if merchant_id.strip():

    try:
        knowledge_documents = list_knowledge_documents_api(
            merchant_id.strip().lower()
        )

        st.markdown("#### Uploaded Knowledge")

        if knowledge_documents:

            for document in knowledge_documents:
                st.write(
                    f"✓ {document['document']} "
                    f"— {document['chunks']} chunks"
                )

        else:
            st.info(
                "No knowledge documents indexed "
                "for this merchant."
            )

    except Exception as e:
        st.error(
            f"Unable to load knowledge documents: {e}"
        )

st.divider()

st.subheader("Catalog Source")

catalog_source = st.radio(
    "Choose catalog source",
    ["Upload Catalog", "Shopify Store"],
    horizontal=True
)

products = []
catalog_path = None

if catalog_source == "Upload Catalog":
    uploaded_file = st.file_uploader(
        "Upload Catalog",
        type=["csv", "json"]
    )

    if uploaded_file:
        st.success("File uploaded successfully")

        if uploaded_file.name.endswith(".json"):
            upload_key = f"{uploaded_file.name}:{uploaded_file.size}"

            if st.session_state.get("catalog_upload_key") != upload_key:
                st.session_state.catalog_path = save_uploaded_catalog(
                    uploaded_file
                )
                st.session_state.catalog_upload_key = upload_key

            catalog_path = st.session_state.catalog_path

            try:
                products = load_products_json(
                    catalog_path,
                    catalog_id="CAT001"
                )
            except Exception:
                st.exception(traceback.format_exc())

        else:
            st.warning(
                "CSV upload is listed in the UI but is not yet implemented. "
                "Please upload a JSON catalog."
            )

else:
    shopify_limit = st.number_input(
        "Number of Shopify products to load",
        min_value=1,
        max_value=250,
        value=50,
        step=1
    )

    if st.button("Load Shopify Products"):
        try:
            shopify_data = load_shopify_products_api(
                limit=int(shopify_limit)
            )
            st.session_state.shopify_products = [
                Product(**item)
                for item in shopify_data
            ]
            st.success(
                f"Loaded {len(st.session_state.shopify_products)} "
                "product(s) from Shopify."
            )
        except Exception as exc:
            st.error(f"Unable to load Shopify products: {exc}")

    products = st.session_state.get(
        "shopify_products",
        []
    )

    if products:
        st.caption(
            f"Shopify catalog loaded: {len(products)} product(s). "
            "Read-only integration."
        )

if products:
    try:
        validation_errors = []


        for product in products:

            errors = validate_product(
                product
            )

            validation_errors.extend(
                errors
            )

        # st.subheader(
        #     "Upload Results"
        # )

        # st.write(
        #     f"Products Loaded: {len(products)}"
        # )

        # st.write(
        #     f"Validation Errors: {len(validation_errors)}"
        # )

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

        # st.write("Health Summary:")
        # st.write(health_summary)

        # st.write(type(health_summary))

        # st.write("Keys:")
        # st.write(list(health_summary.keys()))

        # st.json(health_summary)

        # print("HEALTH SUMMARY =", health_summary)
        # print("TYPE =", type(health_summary))
        # print("KEYS =", health_summary.keys())

        # import inspect

        # st.write("Function object:")
        # st.write(calculate_catalog_score)

        # st.write("Module:")
        # st.write(calculate_catalog_score.__module__)

        # st.write("Source file:")
        # st.write(inspect.getsourcefile(calculate_catalog_score))

        # st.write("Signature:")
        # st.code(str(inspect.signature(calculate_catalog_score)))

        # st.write("Actual source Python imported:")
        # st.code(inspect.getsource(calculate_catalog_score))

        # import inspect

        # st.write("Signature:", inspect.signature(calculate_catalog_score))
        # st.write("__signature__:", getattr(calculate_catalog_score, "__signature__", None))
        # st.write("__defaults__:", calculate_catalog_score.__defaults__)
        # st.write("Argument count:", calculate_catalog_score.__code__.co_argcount)
        # st.write("Variable names:", calculate_catalog_score.__code__.co_varnames)

        # st.write("Calling with ONE argument...")

        try:
            result = calculate_catalog_score(health_summary)
            # st.success("One-argument call succeeded")
            # st.write(result)
        except Exception as e:
            st.error(e)

        #            st.write("Calling with TWO arguments...")

        #             try:
        #                 result = calculate_catalog_score(summary, health_summary)
        # #                st.success("Two-argument call succeeded")
        # #                st.write(result)
        #             except Exception as e:
        #                 st.error(e)

        import analysis.catalog_score as cs

        # st.write("Module object:")
        # st.write(cs)

        # st.write("Module dict entry:")
        # st.write(cs.__dict__["calculate_catalog_score"])

        # import inspect

        # st.write("Source file:")
        # st.write(inspect.getfile(cs.calculate_catalog_score))

        # st.write("Source lines:")
        # st.code(
        #     "".join(
        #         inspect.getsourcelines(cs.calculate_catalog_score)[0]
        #     )
        # )

        # st.write(id(calculate_catalog_score))
        # st.write(id(cs.calculate_catalog_score))

        # import inspect

        # st.write("Function object:", calculate_catalog_score)

        # st.write("__signature__ exists:",
        #         hasattr(calculate_catalog_score, "__signature__"))

        # st.write("__signature__ value:",
        #         getattr(calculate_catalog_score, "__signature__", None))

        # st.write("__wrapped__ exists:",
        #         hasattr(calculate_catalog_score, "__wrapped__"))

        # st.write("__wrapped__:",
        #         getattr(calculate_catalog_score, "__wrapped__", None))

        # st.write("Code argcount:",
        #         calculate_catalog_score.__code__.co_argcount)

        # st.write("Code varnames:",
        #         calculate_catalog_score.__code__.co_varnames)

        # st.write("Defaults:",
        #         calculate_catalog_score.__defaults__)

        import analysis.catalog_score as cs

        import sys

        # st.write("Module ID:")
        # st.write(id(cs))

        # st.write("Module in sys.modules:")
        # st.write(id(sys.modules["analysis.catalog_score"]))

        # st.write("Same object?")
        # st.write(cs is sys.modules["analysis.catalog_score"])

        # st.write("Module file:")
        # st.write(cs.__file__)

        # import dis

        # # st.subheader("Disassembly")

        # disassembly = dis.Bytecode(cs.calculate_catalog_score)

        # for instruction in disassembly:
        #     st.text(instruction)            

        catalog_score = calculate_catalog_score(
            health_summary
        )

        # st.write("After calculate_catalog_score")
        # st.write(catalog_score)

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

            issue_df = pd.DataFrame(health_issues)

            issue_df = issue_df.sort_values(
                by=["product_id", "severity", "issue"]
            )

            issue_df = issue_df.rename(
                columns={
                    "product_id": "Product ID",
                    "severity": "Severity",
                    "issue": "Issue"
                }
            )
            
            st.dataframe(
                issue_df,
                width="stretch"
            )

        else:

            st.success(
                "No catalog issues found."
            )

        # ---------------------------------------------------------
        # Product List - Bulk Selection
        # ---------------------------------------------------------

        rows = []

        for product in products:

            # Get all catalog issues for this product
            product_issues = [
                issue["issue"]
                for issue in health_issues
                if issue["product_id"] == product.product_id
            ]

            # Combine all issues into one column
            issues_text = (
                " · ".join(product_issues)
                if product_issues
                else "None"
            )

            # Create a short description preview
            description = product.description or ""

            if len(description) > 100:
                description_preview = description[:100] + "..."
            else:
                description_preview = description

            rows.append(
                {
                    "Select": False,
                    "Product ID": product.product_id,
                    "Title": product.title,
                    "Description": description_preview,
                    "Issues": issues_text
                }
            )
        df = pd.DataFrame(rows)

        st.subheader("Product List")

        edited_df = st.data_editor(
            df,
            width="stretch",
            hide_index=True,
            disabled=[
                "Product ID",
                "Title",
                "Description",
                "Issues"
            ],
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select product for bulk AI actions",
                    default=False
                ),
                "Product ID": None,
                "Title": st.column_config.TextColumn(
                    "Title"
                ),
                "Description": st.column_config.TextColumn(
                    "Description"
                ),
                "Issues": st.column_config.TextColumn(
                    "Issues"
                )
            },
            key="product_list_editor"
        )
        #Next step: capture the checked products

        #Immediately after the closing ) of st.data_editor(), add:
        selected_rows = edited_df[
            edited_df["Select"] == True
        ]

        selected_product_ids = selected_rows[
            "Product ID"
        ].tolist()

        selected_products = [
            product
            for product in products
            if product.product_id in selected_product_ids
        ]            

        #Begin
        #Added 08/28/26
        if st.button(
            "Generate AI Description for Selected Products",
            disabled=len(selected_products) == 0
        ):

            with st.spinner(
                f"Generating AI descriptions for "
                f"{len(selected_products)} selected product(s)..."
            ):

                for product in selected_products:

                    description_key = (
                        f"generated_desc_{product.product_id}"
                    )

                    st.session_state[
                        description_key
                    ] = generate_description_api(
                        product
                    )

            st.success(
                f"Generated AI descriptions for "
                f"{len(selected_products)} product(s)."
            )
        # 
        # Added 08/28/26      # End 
        # Added 08/29/26
        ##################################################
        # Bulk SEO Tag Generation
        ##################################################

        if st.button(
            "Generate SEO Tags for Selected Products",
            disabled=len(selected_products) == 0
        ):

            with st.spinner(
                f"Generating SEO tags for "
                f"{len(selected_products)} selected product(s)..."
            ):

                for product in selected_products:

                    tag_key = (
                        f"generated_tags_{product.product_id}"
                    )

                    st.session_state[
                        tag_key
                    ] = generate_tags_api(
                        product
                    )

            st.success(
                f"Generated SEO tags for "
                f"{len(selected_products)} product(s)."
            )
        # Added 08/29/26      # End
        # Added 08/29/26 II
        ##################################################
        # Generate Product Type for Selected Products
        ##################################################

        if st.button(
            "Generate Product Type for Selected Products",
            disabled=len(selected_products) == 0
        ):

            with st.spinner(
                f"Generating Product Types for "
                f"{len(selected_products)} selected product(s)..."
            ):

                for product in selected_products:

                    product_type_key = (
                        f"generated_product_type_{product.product_id}"
                    )

                    st.session_state[
                        product_type_key
                    ] = generate_product_type_api(
                        product
                    )

            st.success(
                f"Generated Product Types for "
                f"{len(selected_products)} product(s)."
            )
        # Added 08/29/26 II # End

        ##################################################
        # Product Detail / Product Selection
        ##################################################

        st.divider()

        product_options = {
            f"{p.product_id} | {p.title}": p.product_id
            for p in products
        }

        detail_col, product_col = st.columns([1, 2])

        with detail_col:
            st.subheader("Product Detail")

        with product_col:
            selected_display = st.selectbox(
                "Select Product",
                list(product_options.keys())
            )

        selected_product_id = product_options[selected_display]

        selected_product = next(
            (
                p for p in products
                if p.product_id == selected_product_id
            ),
            None
        )

        if selected_product:
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

            if uploaded_image is not None and catalog_source == "Upload Catalog":

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

                    review = review_product(selected_product)
                    st.subheader(
                        "AI Suggestions"
                    )
                    st.json(review)

                        # st.write("Type:", type(review))
                        # st.write(review)

                    # st.write("Function:", review_product)
                    # st.write("Module:", review_product.__module__)

                    # st.write(type(review))
                    # st.write(review.keys())                        
                    # st.write(review)
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

            description_draft_key = (
                f"description_draft_{selected_product.product_id}"
            )

            if description_draft_key not in st.session_state:
                st.session_state[description_draft_key] = (
                    selected_product.description or ""
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
                    ] = generate_description_api(
                        selected_product
                    )

            ##################################################
            # Show / Accept Suggested Description
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
                    "Accept Description",
                    key=f"accept_desc_{selected_product.product_id}"
                ):

                    accepted_description = description

                    ##08/29/26selected_product.description = accepted_description
                    st.session_state[
                        description_draft_key
                    ] = accepted_description

                    st.session_state[
                        f"description_{selected_product.product_id}"
                    ] = accepted_description

                    del st.session_state[description_key]

                    st.rerun()

            if st.button(
                "✨ Generate SEO Tags",
                key=f"generate_tags_{selected_product.product_id}"
            ):

                with st.spinner(
                    "Generating SEO tags..."
                ):

                    temp_product = selected_product.model_copy(deep=True)

                    temp_product.description = (
                        st.session_state.get(
                            description_key,
                            selected_product.description
                        )
                    )

                    st.session_state[tag_key] = generate_tags_api(
                        temp_product
                    )

                ##################################################
                # Product Edit Form
                ##################################################

                    # with st.form(
                    #     f"product_form_{selected_product.product_id}"
                    # ):

            ##################################################
            # Description
            ##################################################

            description_draft_key = (
                f"description_draft_{selected_product.product_id}"
            )

            if description_draft_key not in st.session_state:
                st.session_state[description_draft_key] = (
                    selected_product.description or ""
                )
        ##                description = st.text_area(
        ##                    "Description",
        ##                    value=selected_product.description or "",
        ##                    height=220,
        ##                    key=f"description_{selected_product.product_id}"
        ##                )
            description = st.text_area(
                "Description",
                value=st.session_state[description_draft_key],
                height=220,
                key=f"description_{selected_product.product_id}"
            )

            st.session_state[description_draft_key] = description
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

            product_type_key = (
                f"generated_product_type_{selected_product.product_id}"
            )

            editable_product_type_key = (
                f"product_type_{selected_product.product_id}"
            )

            ##################################################
            # Generate AI Product Type
            ##################################################

            if st.button(
                "✨ Generate Product Type",
                key=f"generate_product_type_{selected_product.product_id}"
            ):

                with st.spinner("Generating product type..."):

                    st.session_state[
                        product_type_key
                    ] = generate_product_type_api(
                        selected_product
                    )

            ##################################################
            # Show / Accept Suggested Product Type
            ##################################################

            if product_type_key in st.session_state:

                st.subheader("AI Suggested Product Type")

                suggested_product_type = st.session_state[
                    product_type_key
                ]

                st.write(suggested_product_type)

                if st.button(
                    "Accept Product Type",
                    key=f"accept_product_type_{selected_product.product_id}"
                ):

                    st.session_state[
                        editable_product_type_key
                    ] = suggested_product_type

                    del st.session_state[product_type_key]

                    st.rerun()

            ##################################################
            # Editable Product Type
            ##################################################

            product_type = st.text_input(
                "Product Type",
                value=selected_product.product_type or "",
                key=editable_product_type_key
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

            # submitted = st.form_submit_button(
            #     "Save Changes"
            # )

            col1, col2 = st.columns(2)

            ##################################################
            # Save / Download Buttons
            ##################################################

            if catalog_source == "Upload Catalog":
                col1, col2 = st.columns(2)

                with col1:
                    save_clicked = st.button(
                        "💾 Save Changes",
                        use_container_width=True
                    )

                with col2:
                    with open(catalog_path, "rb") as file:
                        st.download_button(
                            "⬇ Download Updated Catalog",
                            data=file,
                            file_name=os.path.basename(catalog_path),
                            mime="application/json",
                            use_container_width=True
                        )

                if save_clicked:
                    selected_product.description = description.strip()

                    new_url = new_url.strip()
                    if (
                        new_url
                        and not new_url.startswith(("http://", "https://"))
                    ):
                        new_url = "https://" + new_url

                    selected_product.product_url = new_url
                    selected_product.inventory_qty = inventory
                    selected_product.product_type = product_type.strip()
                    selected_product.tags = [
                        tag.strip()
                        for tag in tag_string.split(",")
                        if tag.strip()
                    ]

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

            else:
                st.info(
                    "Shopify catalog is connected in read-only mode. "
                    "AI suggestions can be generated and reviewed here, "
                    "but writing changes back to Shopify will be added in Phase 5."
                )

    except Exception:
        st.exception(traceback.format_exc())
