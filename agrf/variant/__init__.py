class AVariant:
    def __init__(self, *, variants=None, **kwargs):
        self.variants = variants
        self.kwargs = kwargs

    def modified_copy(self, *, variants=[], **kwargs):
        new_variant = AVariant(variants=self.variants, **self.kwargs)
        new_variant.variants = variants
        new_variant.kwargs.update(kwargs)
        return new_variant

    def get_variants(self):
        real_class = self.kwargs["real_class"]
        ret = [real_class(**{k: v for k, v in self.kwargs.items() if k not in ["real_class"]})]
        if self.variants is not None:
            for v in self.variants:
                ret.extend(self.modified_copy(**v).get_variants())
        return ret
