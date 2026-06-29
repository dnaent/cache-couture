import os
import sys
import json
import requests

def print_banner():
    print("=" * 60)
    print("        CACHÉ COUTURE — SHOPIFY IMAGE UPLOADER RUNNER")
    print("=" * 60)

def upload_images():
    # Load configuration
    token = os.environ.get("SHOPIFY_ADMIN_API_TOKEN")
    if not token:
        print("[ERROR] SHOPIFY_ADMIN_API_TOKEN environment variable not set.")
        print("Please export/set the token:")
        print("  export SHOPIFY_ADMIN_API_TOKEN=shpat_...")
        sys.exit(1)

    store_domain = os.environ.get("SHOPIFY_STORE_DOMAIN", "hiddencache.myshopify.com")
    graphql_url = f"https://{store_domain}/admin/api/2024-04/graphql.json"
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    # Load manifest
    manifest_path = "docs/shopify_image_manifest.json"
    if not os.path.exists(manifest_path):
        print(f"[ERROR] Manifest file not found at {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    image_root = manifest.get("image_root", "shopify")
    products = manifest.get("products", [])

    print(f"[INFO] Loaded manifest containing {len(products)} products.")
    print(f"[INFO] Image root folder: {image_root}")
    print(f"[INFO] Target Shopify Store: {store_domain}\n")

    for product in products:
        product_id = product["productId"]
        title = product["title"]
        images = product.get("images", [])

        if not images:
            continue

        print(f"\n---> Processing Product: {title} ({product_id})")

        # 1. Fetch existing variants for this product to map media to variants later
        variants_query = """
        query getProductVariants($id: ID!) {
          product(id: $id) {
            variants(first: 50) {
              edges {
                node {
                  id
                  title
                }
              }
            }
          }
        }
        """
        try:
            v_res = requests.post(graphql_url, headers=headers, json={"query": variants_query, "variables": {"id": product_id}})
            v_res.raise_for_status()
            variants_data = v_res.json().get("data", {}).get("product", {}).get("variants", {}).get("edges", [])
            variant_map = {edge["node"]["title"].lower(): edge["node"]["id"] for edge in variants_data}
        except Exception as e:
            print(f"  [WARNING] Could not fetch variants for mapping: {e}")
            variant_map = {}

        for img in images:
            filename = img["file"]
            variant_name = img.get("variant")
            local_path = os.path.join(image_root, filename)

            if not os.path.exists(local_path):
                print(f"  [ERROR] Local image file does not exist: {local_path}")
                continue

            print(f"  * Uploading image '{filename}'...")

            # Determine mime type
            mime_type = "image/png" if filename.lower().endswith(".png") else "image/jpeg"

            # Step 1: Request Staged Upload Target
            staged_mutation = """
            mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
              stagedUploadsCreate(input: $input) {
                stagedTargets {
                  url
                  resourceUrl
                  parameters {
                    name
                    value
                  }
                }
                userErrors {
                  field
                  message
                }
              }
            }
            """
            staged_input = [{
                "resource": "IMAGE",
                "filename": filename,
                "mimeType": mime_type,
                "httpMethod": "POST"
            }]

            try:
                s_res = requests.post(graphql_url, headers=headers, json={"query": staged_mutation, "variables": {"input": staged_input}})
                s_res.raise_for_status()
                s_data = s_res.json()
                
                errors = s_data.get("data", {}).get("stagedUploadsCreate", {}).get("userErrors", [])
                if errors:
                    print(f"    [ERROR] stagedUploadsCreate failed: {errors}")
                    continue

                target = s_data["data"]["stagedUploadsCreate"]["stagedTargets"][0]
            except Exception as e:
                print(f"    [ERROR] API request failed: {e}")
                continue

            # Step 2: Upload Content to Staged Target URL (GCS)
            upload_url = target["url"]
            resource_url = target["resourceUrl"]
            params = target["parameters"]

            multipart_data = []
            for p in params:
                multipart_data.append((p["name"], (None, p["value"])))
            
            with open(local_path, "rb") as f_img:
                multipart_data.append(("file", (filename, f_img, mime_type)))
                try:
                    up_res = requests.post(upload_url, files=multipart_data)
                    up_res.raise_for_status()
                except Exception as e:
                    print(f"    [ERROR] Failed pushing image bytes to stage: {e}")
                    continue

            # Step 3: Create Media on Product
            media_mutation = """
            mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
              productCreateMedia(productId: $productId, media: $media) {
                media {
                  id
                  status
                  mediaContentType
                }
                mediaUserErrors {
                  field
                  message
                }
              }
            }
            """
            media_input = [{
                "mediaContentType": "IMAGE",
                "originalSource": resource_url
            }]

            try:
                m_res = requests.post(graphql_url, headers=headers, json={"query": media_mutation, "variables": {"productId": product_id, "media": media_input}})
                m_res.raise_for_status()
                m_data = m_res.json()

                m_errors = m_data.get("data", {}).get("productCreateMedia", {}).get("mediaUserErrors", [])
                if m_errors:
                    print(f"    [ERROR] productCreateMedia failed: {m_errors}")
                    continue

                media_id = m_data["data"]["productCreateMedia"]["media"][0]["id"]
                print(f"    [SUCCESS] Media created with ID: {media_id}")
            except Exception as e:
                print(f"    [ERROR] Failed creating product media link: {e}")
                continue

            # Step 4: Associate Media with Variant (if applicable)
            if variant_name and variant_map:
                v_key = variant_name.lower()
                variant_id = variant_map.get(v_key)
                if variant_id:
                    print(f"    Assigning to variant '{variant_name}'...")
                    variant_mutation = """
                    mutation productVariantUpdate($input: ProductVariantInput!) {
                      productVariantUpdate(input: $input) {
                        productVariant {
                          id
                        }
                        userErrors {
                          field
                          message
                        }
                      }
                    }
                    """
                    v_input = {
                        "id": variant_id,
                        "mediaIds": [media_id]
                    }
                    try:
                        v_res = requests.post(graphql_url, headers=headers, json={"query": variant_mutation, "variables": {"input": v_input}})
                        v_res.raise_for_status()
                        v_data = v_res.json()
                        v_errors = v_data.get("data", {}).get("productVariantUpdate", {}).get("userErrors", [])
                        if v_errors:
                            print(f"      [WARNING] Variant assignment failed: {v_errors}")
                        else:
                            print(f"      [SUCCESS] Associated with variant: {variant_id}")
                    except Exception as e:
                        print(f"      [WARNING] Variant assignment failed: {e}")
                else:
                    print(f"    [INFO] Variant '{variant_name}' not found on product variants map.")

    print("\n[COMPLETE] Shopify product images processing finished.")

if __name__ == "__main__":
    print_banner()
    upload_images()
