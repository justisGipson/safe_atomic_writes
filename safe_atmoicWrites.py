import json
import os
import shutil
import stat
import tempfile
import yaml


def copy_with_metadata(source, target):
    """
    Copy file with all its permissions and metadata

    pulled from https://stackoverflow.com/a/a43761127/2860309
    :param source: source file name
    :param target: target file name
    """

    # copy content, stat-info (and mode), timestamps
    shutil.copy2(source, target)
    # copy owner and group
    st = os.stat(source)
    os.chown(target, st[stat.ST_UID], st[stat.ST_GID])


def atomic_write(file_contents, target_file_path, mode="w"):
    """
    Write to a temp file and rename it to avoid file corruption

    Attribution @therightstuff, @deichrenner, @hrudham
    :param file_contents: contents to be written to file
    :param target_file_path: file to be created or replaced
    :param mode: file mode defaults to "w", only "w" & "a" are supported
    """

    # use same directory as destination file, so moving across
    # file systems does not cause issues
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, dir=os.path.dirname(target_file_path)
    )

    try:
        # preserve fetadata if it exists
        if os.path.exists(target_file_path):
            copy_with_metadata(target_file_path, temp_file.name)

        with open(temp_file.name, mode) as f:
            f.write(file_contents)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_file.name, target_file_path)

    finally:
        if os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except:
                pass


# example lifted from https://www.debugcn.com/en/article/37223857.html
data = [
    {
        "item": "Food_eat",
        "Food": {"foodNo": 42536216, "type": "fruit", "moreInfo": ["organic"]},
    }
]

yaml_content = yaml.safe_dump(data, default_flow_style=False)

atomic_write(yaml_content, "./sample.yaml")

json_content = json.dumps(data, indent=4)

atomic_write(json_content, "./sample.json")
