class AVariant(dict):
    def modified_copy(self, *, variants=[], **kwargs):
        return AVariant(**{**self, "variants": variants, **kwargs})

    def get_variants(self):
        real_class = self["real_class"]
        ret = [real_class(**{k: v for k, v in self.items() if k not in ["variants", "real_class"]})]
        if self.get("variants") is not None:
            for v in self["variants"]:
                ret.extend(self.modified_copy(**v).get_variants())
        return ret
