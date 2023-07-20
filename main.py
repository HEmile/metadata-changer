#!/usr/bin/python3
import os, frontmatter

keys = [] # key names
vault_path = "" # "absolute path to the vault"
exclude = "" # template path to exclude; leave empty if you don't want to exclude anything

def main():
    if len(vault_path) > 0 and len(keys) > 0:
        for dirpath, dirnames, files in os.walk(vault_path):
            # print(f"Found directory: {dirnames}, located here:{dirpath}")
            for file_name in files:
                if file_name.endswith(".md"):
                    if (len(exclude) == 0) or (len(exclude) > 0 and exclude not in dirpath):
                        normalised_path = os.path.normpath(dirpath + "/" + file_name)
                        print(normalised_path)
                        with open(normalised_path, "r") as f:
                            post = frontmatter.load(f)
                            change_keys(post, normalised_path)
        print("Done!")
    else:
        print("Set a vault path and/or add a key!")


def change_keys(post: frontmatter.Post, normPath: str):
    for key in keys:
        value = post.get(key)
        if value is not None:
            new_value = []
            if isinstance(value, list) and len(value) > 0:
                for el in value:
                    if el is not None and not isinstance(el, list) and el[0:2] != "[[":
                        new_value.append("[[" + el + "]]")
                        print("File: " + normPath)
                        print("Fixed value: '" + el + "' of key: '" + key + "'")
                    else:
                        new_value.append(el)
            elif isinstance(value, str):
                if value[0:2] != "[[":
                    new_value.append("[[" + value + "]]")
                    print("File: " + normPath)
                    print("Fixed value: '" + value + "' of key: '" + key + "'")
                else:
                    new_value.append(value)
            post.__setitem__(key, new_value)
    with open(normPath, "w") as f:
        f.write(frontmatter.dumps(post))


if __name__ == "__main__":
    main()