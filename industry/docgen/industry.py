import os


def gen_industry_doc(all_industries, string_manager):
    prefix = "docs/industry/industries"
    for i, industry in enumerate(all_industries):
        with open(os.path.join(prefix, f"{industry.translation_name}.md"), "w") as f:
            print(
                f"""# {industry.name(string_manager)}

# Datasheet
""",
                file=f,
            )
