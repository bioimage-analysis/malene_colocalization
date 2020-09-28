import javabridge
import bioformats
import numpy as np
import os
import time


def _metadata(path):
    xml = bioformats.get_omexml_metadata(path)
    md = bioformats.omexml.OMEXML(xml)

    meta={'AcquisitionDate': md.image().AcquisitionDate}
    meta['Name']=(md.image().Name).replace(" ", "")
    meta['SizeT']=md.image().Pixels.SizeT
    meta['SizeX']=md.image().Pixels.SizeX
    meta['SizeY']=md.image().Pixels.SizeY
    meta['PhysicalSizeX'] = md.image().Pixels.PhysicalSizeX
    meta['PhysicalSizeY'] = md.image().Pixels.PhysicalSizeY
    timepoint = []
    for planes in range(meta['SizeT']):
        timepoint.append(md.image().Pixels.Plane(planes).DeltaT)
    meta['Timepoint'] = np.asarray(timepoint)
    return(meta)

def load_data(path):
    meta = _metadata(path)

    image = np.empty((meta['SizeT'], meta['SizeX'], meta['SizeY']))
    with bioformats.ImageReader(path) as rdr:
        for t in range(0, meta['SizeT']):
            image[t,:,:]=rdr.read(c=0, z=0, t=t, series=None,
                                  index=None, rescale=False, wants_max_intensity=False,
                                  channel_names=None)

    return(np.squeeze(image), meta, _new_directory(path, meta))

def _new_directory(path, meta):


    directory = os.path.dirname(path) +"/"+"result"+'_'+meta["Name"]+'_'+ time.strftime('%m'+'_'+'%d'+'_'+'%Y')

    if os.path.exists(directory):
        expand = 0
        while True:
            expand += 1
            new_directory = directory+"_"+str(expand)
            if os.path.exists(new_directory):
                continue
            else:
                directory = new_directory
                os.makedirs(directory)
                break
    else:
        os.makedirs(directory)
    return(directory)
