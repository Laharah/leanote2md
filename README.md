# leanote2md
Export all you Markdown notes in Leanote (a.k.a 蚂蚁笔记) to local Markdown files.

## Prerequisite

- Python 3
- pip3
- git

## Dependencies
Use your pip tool to install the dependencies

- anytree
- requests

You can install these packages by this command

```shell
pip3 install anytree requests --user
```

## Usage
Clone this repo, and run the `exporter.py` script. You can easily do this by running the following command on your terminal

```python
git clone https://github.com/gaunthan/leanote2md.git
cd ./leanote2md
chmod +x exporter.py
./exporter.py
```

If you don't want to save your notes interactively, you need to modify `config.py` and run `exporter.py` with command argument `config.py`

```shell
./exporter.py config.py
```


# Exporting leanote notes to joplin

leanote exporting is a clusterfuck and you always lose creation times and media
resources. Here's the steps to export the notes so they can be imported correctly as
joplin markdown notes.

1. run export.py and download the leanote markdown notes (fill in config for convenience)

2. import markdown directories into joplin

3. from leanote export each notebook 3 times to their same folder (leanote, evernote enex, and html)

4. run leanote_fixer.py on an exported notebook folder

5. use joplin to import the generated `full_notebook.enex` to import the notebook

6. merge the full_notebook notes into the downloaded markdown notebooks, and then delete
   the empty notebook afterward.

7. repeat steps 4-6 on remaining exported notebook folders.
