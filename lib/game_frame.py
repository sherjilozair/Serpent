import skimage.color
import skimage.measure
import skimage.transform
import skimage.filters
import skimage.morphology

import numpy as np


class GameFrameError(BaseException):
    pass


class GameFrame:

    def __init__(self, frame_array):
        self.frame_array = frame_array
        self.frame_variants = dict()

    @property
    def frame(self):
        return self.frame_array

    @property
    def half_resolution_frame(self):
        """ A quarter-sized version of the frame (half-width, half-height)"""

        if "half" not in self.frame_variants:
            self.frame_variants["half"] = self._to_half_resolution()

        return self.frame_variants["half"]

    @property
    def quarter_resolution_frame(self):
        """ A sixteenth-sized version of the frame (quarter-width, quarter-height)"""

        if "quarter" not in self.frame_variants:
            self.frame_variants["quarter"] = self._to_quarter_resolution()

        return self.frame_variants["quarter"]

    @property
    def grayscale_frame(self):
        """ A full-size grayscale version of the frame"""

        if "grayscale" not in self.frame_variants:
            self.frame_variants["grayscale"] = self._to_grayscale()

        return self.frame_variants["grayscale"]

    @property
    def ssim_frame(self):
        """ A 100x100 grayscale frame to be used for SSIM"""

        if "ssim" not in self.frame_variants:
            self.frame_variants["ssim"] = self._to_ssim()

        return self.frame_variants["ssim"]

    def compare_ssim(self, previous_game_frame):
        return skimage.measure.compare_ssim(previous_game_frame.ssim_frame, self.ssim_frame)

    def difference(self, previous_game_frame):
        current = skimage.filters.gaussian(self.grayscale_frame, 8)
        previous = skimage.filters.gaussian(previous_game_frame.grayscale_frame, 8)

        return current - previous

    def _to_half_resolution(self):
        shape = (
            self.frame_array.shape[0] // 2,
            self.frame_array.shape[1] // 2
        )

        return np.array(skimage.transform.resize(self.frame_array, shape, mode="reflect", order=1) * 255, dtype="uint8")

    def _to_quarter_resolution(self):
        shape = (
            self.frame_array.shape[0] // 4,
            self.frame_array.shape[1] // 4
        )

        return np.array(skimage.transform.resize(self.frame_array, shape, mode="reflect", order=1) * 255, dtype="uint8")

    def _to_grayscale(self):
        return np.array(skimage.color.rgb2gray(self.frame_array) * 255, dtype="uint8")

    def _to_ssim(self):
        grayscale = self.grayscale_frame
        return skimage.transform.resize(grayscale, (100, 100), mode="reflect", order=0)
