import json
import os


def save_catalog(products, file_path):

    print("=" * 80)
    print("Saving catalog...")
    print("File:", os.path.abspath(file_path))

    data = []

    for product in products:

        d = product.model_dump()

        print(d)

        data.append(d)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            default=str
        )

    print("File written successfully.")

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        print("Contents of file after write:")
        print(f.read())

    print("=" * 80)

def save_catalog_old(products, file_path):

    data = []

    for product in products:

        data.append(
            product.model_dump()
        )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def save_uploaded_catalog(
    uploaded_file
):


    print("=" * 80)
    print("save_uploaded_catalog() called")
    print("Uploading:", uploaded_file.name)
    print("=" * 80)
    
    os.makedirs(
        "data/catalogs",
        exist_ok=True
    )

    catalog_path = (
        f"data/catalogs/{uploaded_file.name}"
    )

    with open(
        catalog_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getvalue()
        )

    return catalog_path