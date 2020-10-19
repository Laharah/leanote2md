# Exporting leanote notes to joplin

leanote exporting is a clusterfuck and you always lose creation times and media
resources. Here's the steps to export the notes so they can be imported correctly into
joplin markdown notes.

1. run export.py and download the leanote markdown notes (fill in config for convince)

2. import markdown directories into joplin

3. from leanote export each notebook 3 times to their same folder (leanote, evernote enex, and html)

4. run leanote_fixer.py on an exported notebook folder

5. use joplin to import the generated `full_notebook.enex` to import the notebook

6. merge the full_notebook notes into the downloaded markdown notebooks, and then delete
   the empty notebook afterward.

7. repeat steps 4-6 on remaining exported notebook folders.
