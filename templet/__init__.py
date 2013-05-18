import tempita
import shutil


__all__ = ['handle_project']


def copy(src, dst):
    shutil.copy(src, dst)
    return dst


def move(src, dst):
    shutil.move(src, dst)
    return dst


def expand_vars_in_file(filepath, project_root, template_data):
    with open(filepath) as fp:
        tmpl = tempita.Template(fp.read())
    file_contents = tmpl.substitute(template_data)
    with open(filepath, 'w', encoding='utf8') as f:
        f.write(file_contents)


def expand_vars_in_file_name(filepath, template_data):
    tmpl = tempita.Template(os.path.basename(filepath))
    return tmpl.substitute(template_data)


def handle_project(src, dst, template_data):
    copy(src, dst)
    dirs_to_rename = []
    for root, dirs, files in os.walk(dst):
        for f in files:
            filepath = os.path.join(root, f)

            if os.path.isfile(filepath):
                expand_vars_in_file(filepath)

            if filepath.startswith('{{') and filepath.endswith('}}'):
                # expand vars in file name
                new_filepath = move(filepath, template_data)
                # expand vars in dir name, it should be done in the last turn
                if os.path.isdir(filepath):
                    move(filepath, template_data)
