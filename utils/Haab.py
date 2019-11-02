haab_months = ["Pop", "Wo", "Sip", "Sotz", "Sek", "Xul", "Yaxkin", "Mol", "Chen",
                "Yax", "Sak", "Keh", "Mak", "Kankin", "Muwan", "Pax", "Kayab",
                "Kumku", "Wayeb"]

haab_idx_to_month = {idx:month for idx, month in enumerate(haab_months)}
haab_month_to_idx = {month:idx for idx, month in haab_idx_to_month.keys()}


class Haab:
    def __init__(self, month_name="Kumku", month_number=4):
        self.month_name = month_name
        self.month_number = month_number
