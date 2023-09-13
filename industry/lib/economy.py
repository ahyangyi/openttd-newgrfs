class Economy:
    def __init__(self, name, industries):
        self.name = name
        self.industries = [x.the_industry for x in industries]
