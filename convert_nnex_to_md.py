import argparse
import os
import re
import xml.etree.ElementTree as ET

def convert_to_markdown(note_element, notebook_name):
    metadata = {}
    content_lines = []

    for child in note_element:
        if child.tag == 'Title':
            metadata['title'] = child.text
        elif child.tag == 'Content':
            content_lines.append(child.text.strip())
        elif child.tag == 'Created':
            metadata['created'] = child.text
        elif child.tag == 'Updated':
            metadata['updated'] = child.text
        elif child.tag == 'Attributes':
            for attr in child:
                metadata[attr.tag.lower()] = attr.text

    yaml_front_matter = "---\n" + "\n".join(f"{key}: {value}" for key, value in metadata.items()) + "\n---\n"
    markdown_content = "\n".join(content_lines)

    # Prepend notebook name to title
    title_with_notebook = f"{notebook_name}_{metadata['title']}"

    # Remove invalid characters from the filename
    title_with_notebook = re.sub(r'[\/:*?"<>|]', '_', title_with_notebook)

    return yaml_front_matter + f"# {title_with_notebook}\n\n{markdown_content}\n", title_with_notebook

def convert_nnex_to_markdown(nnex_file_path, output_folder):
    tree = ET.parse(nnex_file_path)
    root = tree.getroot()

    markdown_notes = []

    for child in root:
        if child.tag == 'Note':
            notebook_name = None

            for note_child in child:
                if note_child.tag == 'NotebookGuid':
                    # Get the notebook name from the GUID (you might need a mapping if GUID is not clear)
                    notebook_name = f"notebook_{note_child.text}"

            if notebook_name:
                note_content, note_title = convert_to_markdown(child, notebook_name)
                markdown_notes.append((note_content, note_title))

    return markdown_notes

def main():
    parser = argparse.ArgumentParser(description='Convert Evernote .nnex file to Markdown format')
    parser.add_argument('file_path', help='Path to the .nnex file')
    args = parser.parse_args()

    nnex_file_path = args.file_path

    # Check if the file exists
    if not os.path.isfile(nnex_file_path):
        print(f"Error: File '{nnex_file_path}' not found.")
        return

    # Create a folder for exported notes
    output_folder = "markdown_notes"
    os.makedirs(output_folder, exist_ok=True)

    markdown_notes = convert_nnex_to_markdown(nnex_file_path, output_folder)

    for note_content, title in markdown_notes:
        # Create a file path based on the title
        filename = os.path.join(output_folder, f"{title}.md")

        # Check for conflicts
        counter = 1
        while os.path.exists(filename):
            counter += 1
            filename = os.path.join(output_folder, f"{title}_{counter}.md")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(note_content)

if __name__ == "__main__":
    main()
