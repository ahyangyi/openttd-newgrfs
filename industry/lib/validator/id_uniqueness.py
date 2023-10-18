def check_id_uniqueness(economy):
    industry_ids = [industry.id for industry in economy.industries]
    assert len(industry_ids) == len(set(industry_ids))
