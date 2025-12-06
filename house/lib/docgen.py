import os


def gen_docs(string_manager, houses):
    prefix = "docs/house/"
    for i, house in enumerate(houses):
        with open(os.path.join(prefix, f"{house.name}.md"), "w") as f:
            print(
                f"""# {house.name}
""",
                file=f,
            )
