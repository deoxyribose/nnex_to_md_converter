This script converted notes in .nnex format (the NixNote format) to markdown files that can be read by e.g. Obsidian
This allows Linux users who have a backlog of Evernote notes to
    1. Log in to their user using NixNote
        `sudo apt-get install nixnote2`
    2. Export all notes to .nnex
    3. Run the script
        `python3 convert_nnex_to_md.py mynotes.nnex`
        which creates a folder `markdown_notes`
        which can be dragged & dropped in Obsidian