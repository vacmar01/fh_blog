"""
Image optimization script for the blog.
Converts PNG/JPG images to WebP and updates markdown references.
"""

import re
from pathlib import Path

from PIL import Image

# Files to skip (favicons, OG images, etc.)
BLACKLIST = [
    "favicon-16x16.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "og.png",
]

# Configuration
IMAGES_DIR = Path("public/images")
POSTS_DIR = Path("posts")
MAX_WIDTH = 1200
WEBP_QUALITY = 85  # For lossy compression (JPG sources)


def should_process(filename: str) -> bool:
    """Check if file should be processed."""
    if filename in BLACKLIST:
        return False
    return filename.lower().endswith((".png", ".jpg", ".jpeg"))


def optimize_image(source_path: Path) -> Path | None:
    """Convert image to WebP, resize if needed. Returns output path or None if skipped."""
    output_path = source_path.with_suffix(".webp")

    # Skip if WebP already exists and is newer than source
    if output_path.exists() and output_path.stat().st_mtime >= source_path.stat().st_mtime:
        return None

    with Image.open(source_path) as img:
        # Convert to RGB if necessary (for PNG with transparency, use RGBA)
        if img.mode in ("RGBA", "LA", "P"):
            # Keep alpha channel for PNGs
            if img.mode == "P":
                img = img.convert("RGBA")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Resize if wider than MAX_WIDTH
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        # Determine compression settings based on source format
        is_png = source_path.suffix.lower() == ".png"

        if is_png:
            # Lossless for PNGs (preserves screenshot text clarity)
            img.save(output_path, "WEBP", lossless=True)
        else:
            # Lossy for JPGs
            img.save(output_path, "WEBP", quality=WEBP_QUALITY)

    return output_path


def update_markdown_files(converted: dict[str, str]) -> int:
    """Update image references in markdown files. Returns count of files updated."""
    if not converted:
        return 0

    updated_count = 0

    for md_file in POSTS_DIR.glob("*.md"):
        content = md_file.read_text()
        original_content = content

        for old_name, new_name in converted.items():
            # Update inline markdown images: ![alt](/images/foo.png)
            content = re.sub(
                rf"(\!\[[^\]]*\]\(/images/){re.escape(old_name)}(\))",
                rf"\1{new_name}\2",
                content,
            )

            # Update frontmatter image field: image: foo.png
            content = re.sub(
                rf"^(image:\s*){re.escape(old_name)}(\s*)$",
                rf"\1{new_name}\2",
                content,
                flags=re.MULTILINE,
            )

        if content != original_content:
            md_file.write_text(content)
            updated_count += 1

    return updated_count


def main():
    print("Optimizing images...")

    # Find and process images
    converted = {}  # old_filename -> new_filename
    skipped = 0
    processed = 0

    for image_path in IMAGES_DIR.iterdir():
        if not image_path.is_file():
            continue

        if not should_process(image_path.name):
            continue

        result = optimize_image(image_path)

        if result:
            old_name = image_path.name
            new_name = result.name
            converted[old_name] = new_name
            processed += 1

            # Calculate size reduction
            old_size = image_path.stat().st_size
            new_size = result.stat().st_size
            reduction = (1 - new_size / old_size) * 100

            print(f"  {old_name} -> {new_name} ({reduction:+.1f}%)")
        else:
            skipped += 1

    # Update markdown files
    md_updated = update_markdown_files(converted)

    # Summary
    print()
    print(f"Processed: {processed} images")
    print(f"Skipped (up-to-date): {skipped} images")
    print(f"Markdown files updated: {md_updated}")


if __name__ == "__main__":
    main()
