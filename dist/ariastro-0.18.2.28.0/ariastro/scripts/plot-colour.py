import pyfits
import numpy
from .RGBImage import *


if __name__ == "__main__":
    p = pyfits.open('../../results/3115_out5_3c_n4_c_ba_r2_n2_n2.fits')

    med = [numpy.median(x) for x in [p['INPUT_J'].data,p['INPUT_H'].data,p['INPUT_K'].data]]

    img = RGBImage(p['INPUT_K'].data-med[2],p['INPUT_H'].data-med[1],p['INPUT_J'].data-med[0], scales=[0.11,0.09,0.1], mapping=map_Lupton04, beta=2.0)
    img.show()
    img.save_as('img.jpg')

    model = RGBImage(p['MODEL_K'].data-med[2],p['MODEL_H'].data-med[1],p['MODEL_J'].data-med[0], scales=[0.11,0.09,0.1], mapping=map_Lupton04, beta=2.0)
    model.show()
    model.save_as('model_3115_5_3c.n4_c_ba_r2_n2_n2.jpg')

    res = RGBImage(p['RESIDUAL_K'].data,p['RESIDUAL_H'].data,p['RESIDUAL_J'].data, scales=[0.1,0.09,0.1], mapping=map_Lupton04, beta=0.01)
    res.show()
    res.save_as('res_3115_5_3c.n4_c_ba_r2_n2_n2.jpg')

    negres = RGBImage(-p['RESIDUAL_K'].data,-p['RESIDUAL_H'].data,-p['RESIDUAL_J'].data, scales=[0.11,0.09,0.3], mapping=map_Lupton04, beta=0.01)
    negres.show()
    negres.save_as('negres_3115_5_3c.n4_c_ba_r2_n2_n2.jpg')
