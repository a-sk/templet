import tempita
import shutil

def rename(src, template_data):
    if os.path.isfile(src):
        shutil.move(src,)


def expand_vars_in_file(filepath, project_root, template_data):
    with open(filepath) as fp:
        tmpl = tempita.Template(fp.read())
    file_contents = tmpl.substitute(template_data)
    with open(filepath, 'w', encoding='utf8') as f:
        f.write(file_contents)

def expand_vars_in_file_name(filepath, template_data):
    tmpl = tempita.Template(os.path.basename(filepath))
    return tmpl.substitute(template_data)


def handle_project(project_path, project_root, template_data):
    dirs_to_rename = []
    for root, dirs, files in os.walk(project_root):
        for f in files:
            filepath = os.path.join(root, f)

            if os.path.isfile(filepath):
                expand_vars_in_file(filepath)

            # expand files
            new_filepath = rename(filepath, template_data)
            # expand dirs
            if os.path.isdir(filepath) and filepath.startswith('{{') and filepath.endswith('}}'):
                rename(filepath, template_data)


def copy_template(src, dst):
    return dst

