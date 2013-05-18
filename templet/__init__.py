import os
import tempita
import shutil


__all__ = ['handle_project']


def copy(src, dst):
    if os.path.isfile(src):
        shutil.copy(src, dst)
    elif os.path.isdir(src):
        shutil.copytree(src, dst)
    return dst

def move(src, dst):
    shutil.move(src, dst)
    return dst

def maybe_rename(src, template_data):
    """Rename file or directory if it's name contains expandable variable"""
    if os.path.basename(src).startswith('{{') \
        and os.path.basename(src).endswith('}}'):

        new_path = expand_vars_in_file_name(src, template_data)
        move(src, new_path)

def expand_vars_in_file(filepath, project_root, template_data):
    with open(filepath) as fp:
        tmpl = tempita.Template(fp.read())
    file_contents = tmpl.substitute(template_data)
    with open(filepath, 'w') as f:
        f.write(file_contents)

def expand_vars_in_file_name(filepath, template_data):
    tmpl = tempita.Template(filepath)
    return tmpl.substitute(template_data)

def handle_project(src, dst, template_data):
    copy(src, dst)
    dirs_to_rename = []
    for root, dirs, files in os.walk(dst):
        for d in dirs:
            dirpath = os.path.join(root, d)
            maybe_rename(dirpath, template_data)

        for f in files:
            filepath = os.path.join(root, f)
            if os.path.isfile(filepath):
                expand_vars_in_file(filepath, dst, template_data)
            maybe_rename(filepath, template_data)

