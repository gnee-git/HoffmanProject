import pydicom as dcm
import os

FOLDER = "D:\\Hoffman\\_Edinburgh\\#10_Hoff skull OSEM 3i24s 4mm 400 z1"

if not os.path.exists(FOLDER+"\\Frame1"):
    for i in range(1,7):
        os.mkdir(FOLDER+"\\Frame{}".format(i))

alist = [x for x in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, x))]

times = sorted(list(set([dcm.read_file(os.path.join(FOLDER, x)).AcquisitionTime for x in alist])))

timedict = {
    times[0]: os.path.join(FOLDER,"Frame1"),
    times[1]: os.path.join(FOLDER,"Frame2"),
    times[2]: os.path.join(FOLDER,"Frame3"),
    times[3]: os.path.join(FOLDER,"Frame4"),
    times[4]: os.path.join(FOLDER,"Frame5"),
    times[5]: os.path.join(FOLDER,"Frame6")
}

for f in alist:
    f = os.path.join(FOLDER, f)
    t = dcm.read_file(f).AcquisitionTime
    os.rename(f, os.path.join(timedict[t], os.path.basename(f)))
    