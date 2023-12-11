from agrf.variant import AVariant


class AMetaVehicle(AVariant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def name(self, string_manager, lang_id=0x7F):
        return get_translation(string_manager[f"STR_VEHICLE_NAME_{self.translation_name}"], lang_id)
