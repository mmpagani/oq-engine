"""
Module :mod:`nhe.msr.wc1994` implements :class:`WC1994MSR`.
"""
from math import log10
from nhe.msr.base import BaseMSR


class WC1994MSR(BaseMSR):
    """
    Wells and Coppersmith magnitude -- rupture area relationships,
    see 1994, Bull. Seism. Soc. Am., pages 974-2002.
    """
    def get_median_area(self, mag, rake):
        """
        The values are a function of both magnitude and rake.

        Setting the rake to ``None`` causes their "All" rupture-types
        to be applied.
        """
        assert rake is None or -180 <= rake <= 180
        if rake is None:
            # their "All" case
            return 10.0 ** (-3.49 + 0.91 * mag)
        elif (-45 <= rake <= 45) or (rake >= 135) or (rake <= -135):
            # strike slip
            return 10.0 ** (-3.42 + 0.90 * mag)
        elif rake > 0:
            # thrust/reverse
            return 10.0 ** (-3.99 + 0.98 * mag)
        else:
            # normal
            return 10.0 ** (-2.87 + 0.82 * mag)

    def get_std_dev_area(self, mag, rake):
        """
        Standard deviation for WC1994MSR. Mag is ignored.
        """
        assert rake is None or -180 <= rake <= 180
        if rake is None:
            # their "All" case
            return 0.24
        elif (-45 <= rake <= 45) or (rake >= 135) or (rake <= -135):
            # strike slip
            return 0.22
        elif rake > 0:
            # thrust/reverse
            return 0.26
        else:
            # normal
            return 0.22

    def get_std_dev_mag_from_area(self, rake):
        """
        Returns the standard deviation on the magnitude
        for the WC1994MSR area relation.

        :param rake:
            Rake angle (the rupture propagation direction) in degrees,
            from -180 to 180.
        """
        assert rake is None or -180 <= rake <= 180
        if rake is None:
            # their "All" case
            return 0.24
        elif (-45 <= rake <= 45) or (rake >= 135) or (rake <= -135):
            # strike slip
            return 0.23
        elif rake > 0:
            # thrust/reverse
            return 0.25
        else:
            # normal
            return 0.25

    def get_median_mag_from_area(self, area, rake):
        """
        Returns magnitude (Mw) given the area and rake.

        Setting the rake to ``None`` causes their "All" rupture-types
        to be applied.

        :param area:
            Area in square km.
        :param rake:
            Rake angle (the rupture propagation direction) in degrees,
            from -180 to 180.
        """
        assert rake is None or -180 <= rake <= 180
        if rake is None:
            # their "All" case
            return 4.07 + 0.98 * log10(area)
        elif (-45 <= rake <= 45) or (rake > 135) or (rake < -135):
            # strike slip
            return 3.98 + 1.02 * log10(area)
        elif rake > 0:
            # thrust/reverse
            return 4.33 + 0.90 * log10(area)
        else:
            # normal
            return 3.93 + 1.02 * log10(area)

    def get_mag_from_area(self, area, rake, epsilon=0.0):
        """
        Return the Moment magnitude given the area, rake
        and uncertainty epsilon.

        :param area:
            Area in square km.
        :param rake:
            Rake angle (the rupture propagation direction) in degrees,
            from -180 to 180.
        :param epsilon:
            Uncertainty residual, which identifies the number
            of standard deviations from the median.
        """
        median_mag = self.get_median_mag_from_area(area, rake)
        std_dev = self.get_std_dev_mag_from_area(rake)
        return median_mag + epsilon * std_dev
