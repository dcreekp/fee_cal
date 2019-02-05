# calculator.py

T12 = {
    1: 50,
    2: 90,
    3: 90,
    4: 115,
    5: 100,
    6: 120,
    7: 140,
    8: 160,
    9: 180,
    10: 200,
    11: 220,
    12: 240,
    13: 260,
    14: 280,
    15: 300,
    16: 320,
    17: 340,
    18: 360,
    19: 380,
    20: 400,
    21: 400,
    }

T24 = {
    1: 70,
    2: 100,
    3: 120,
    4: 160,
    5: 200,
    6: 240,
    7: 280,
    8: 320,
    9: 360,
    10: 400,
    11: 440,
    12: 480,
    13: 520,
    14: 560,
    15: 600,
    16: 640,
    17: 680,
    18: 720,
    19: 760,
    20: 800,
    21: 800,
    }


class FeeCalculator:

    TERMS = {
        12: T12,
        24: T24,
        }

    def __call__(self, loan, term):
        low, high = self.get_bounds(loan, term)
        raw_fee = self.interpolate(loan, low, high)
        fee = self.clean_fee(loan, raw_fee)
        return fee

    def get_bounds(self, loan, term):
        if not (1000 <= loan <= 20000):
            raise ValueError("loan must be 1000 <= loan <= 20000")
        t_key = loan // 1000
        try:
            low = self.TERMS[term][t_key]
        except KeyError:
            raise ValueError("term must be 12 or 24")
        high = self.TERMS[term][t_key + 1]
        return low, high

    def interpolate(self, loan, low, high):
        raw_fee = loan % 1000 / 1000 * (high - low) + low
        return raw_fee

    def clean_fee(self, loan, fee):
        total = loan + fee
        fee = self._round(total) - loan
        return round(fee, 2)

    def _round(self, amount, base=5):
        return base * round(float(amount)/base)
