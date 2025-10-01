from pathlib import Path

IMAGE_SIZE = 200
CATS_PER_ROW = 3

SITTING_CATS_IMAGE_FOLDER_NAME = "cats"
STANDING_CATS_IMAGE_FOLDER_NAME = "cats_2"

SITTING_CATS_IMAGE_FOLDER_PATH = Path(__file__).parent.parent.resolve() / SITTING_CATS_IMAGE_FOLDER_NAME
STANDING_CATS_IMAGE_FOLDER_PATH = Path(__file__).parent.parent.resolve() / STANDING_CATS_IMAGE_FOLDER_NAME
README_FILE_PATH = Path(__file__).parent.parent.resolve() / "README.md"

SITTING_CATS_IMAGE_PREFIX = "cat_sitting_"
STANDING_CATS_IMAGE_PREFIX = "cat_standing_"
PNG_EXTENSION = ".png"

# Percentage width per image to keep ~3 across on desktop but wrap on mobile
# 32% is a practical safe value to avoid accidental wrapping at desktop widths
IMG_PERCENT_PER_ITEM = max(1, min(100, (100 // CATS_PER_ROW) - 1))  # typically 32 for 3 per row

def group_list(ungrouped_list: list[str], elements_per_group: int) -> list[list[str]]:
    return [
        ungrouped_list[i : i + elements_per_group]
        for i in range(0, len(ungrouped_list), elements_per_group)
    ]

def get_cat_name(image_prefix: str, filename: str) -> str:
    # This assumes that filename contains image_prefix, no check done for this
    return Path(filename).stem[len(image_prefix):]

def get_image_item_html(image_prefix: str, image_folder_name: str, filename: str) -> str:
    """
    One gallery item: clickable image + caption beneath it.
    Uses percentage width so images lay out 3-across on desktop and wrap on smaller screens.
    """
    name = get_cat_name(image_prefix, filename)
    src = f"{image_folder_name}/{filename}"
    # Anchor wraps image and caption so each item stays logically grouped
    return (
        f'<a href="{src}" title="{name}">'
        f'<img src="{src}" alt="{name}" width="{IMG_PERCENT_PER_ITEM}%"/>'
        f'<br><sub>{name}</sub>'
        f'</a>'
    )

def generate_gallery_block(image_prefix: str, image_folder_name: str, filenames: list[str]) -> str:
    if len(filenames) == 0:
        return ""
    # Group to encourage 3-per-row on desktop; items still wrap naturally on mobile
    grouped = group_list(ungrouped_list=filenames, elements_per_group=CATS_PER_ROW)
    rows = []
    for group in grouped:
        items_html = "".join([get_image_item_html(image_prefix, image_folder_name, fn) for fn in group])
        # Center the row; no CSS classes or styles required
        rows.append(f'<p align="center">{items_html}</p>')
    return "\n".join(rows)

def update_cat_gallery_in_readme(markdown_filepath: Path, sitting_cat_gallery_markdown_str: str, standing_cat_gallery_markdown_str: str) -> None:
    """
    Updates the contents in the 'Cat Gallery' section in provided markdown file
    """
    text = markdown_filepath.read_text(encoding="utf-8")
    gallery_heading = R"### Cat gallery."
    idx = text.find(gallery_heading)
    updated_text = text[: idx + len(gallery_heading)] + "\n" + "___\n" + "#### Sitting Cat gallery.\n" + sitting_cat_gallery_markdown_str.strip() + '\n'
    updated_text +=  "___" + "\n#### Standing Cat gallery.\n\n" + standing_cat_gallery_markdown_str.strip() + '\n'
    markdown_filepath.write_text(updated_text)

def main() -> None:
    sitting_cat_image_filenames = [
        file_path.name
        for file_path in sorted(SITTING_CATS_IMAGE_FOLDER_PATH.iterdir())
        if (file_path.is_file() and (file_path.suffix == PNG_EXTENSION))
    ]

    standing_cat_image_filenames = [
        file_path.name
        for file_path in sorted(STANDING_CATS_IMAGE_FOLDER_PATH.iterdir())
        if (file_path.is_file() and (file_path.suffix == PNG_EXTENSION))
    ]

    print(f"Detected {len(sitting_cat_image_filenames)} sitting cats.")
    print(f"Detected {len(standing_cat_image_filenames)} standing cats.")

    sitting_cat_image_filenames.sort()
    standing_cat_image_filenames.sort()

    print("Updating README.md...")

    sitting_cats_block = generate_gallery_block(SITTING_CATS_IMAGE_PREFIX, SITTING_CATS_IMAGE_FOLDER_NAME, sitting_cat_image_filenames)
    standing_cats_block = generate_gallery_block(STANDING_CATS_IMAGE_PREFIX, STANDING_CATS_IMAGE_FOLDER_NAME, standing_cat_image_filenames)

    update_cat_gallery_in_readme(README_FILE_PATH, sitting_cats_block, standing_cats_block)

    print("Updated README.md.")

if __name__ == "__main__":
    main()