def check_id_uniqueness(economy):
    for industry in economy.industries:
        for another_industry in economy.industries:
            assert (
                industry is another_industry or industry.id != another_industry.id
            ), f"Industries {industry.name} and {another_industry.name} have the same ID!"
