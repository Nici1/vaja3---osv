from matplotlib import pyplot as plt
import numpy  as np
import sys
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/nikola/test/osv')
from vaja_1.script2 import loadImage, displayImage

sys.path.insert(1, '/home/nikola/test/osv')
from vaja_2.script1 import computeHistogram, displayHistogram

if __name__ == '__main__':
    orig_size = [200,152]
    I = loadImage('/home/nikola/test/osv/vaja_3/pumpkin-200x152-08bit.raw',orig_size,np.uint8)
    displayImage(I,'Orginalna slika')
    

def interpolateImage ( iImage , iSize , iOrder ) :

    iOrder = int(iOrder) # ce uporabnik definira order kot float, ta vrstica je samo kot garancija

    oImage = np.zeros((iSize[1],iSize[0])) # alternativa: np.zeros(iSize[::-1])

    cols, rows = iSize
    step = [(iImage.shape[1]-1)/(iSize[0]-1),(iImage.shape[0]-1)/(iSize[1]-1)]
    


    for y in range(rows):
            for x in range(cols):
                pt = np.array([x,y])*np.array(step) # pt = point coordinates
                
                if iOrder ==0:
                    px=np.round(pt).astype(int) # px = indices(x,y)
                    s = iImage[px[1],px[0]] # intenziteto
                elif iOrder ==1:
                    #px je koordinata levega zg. piksla
                    px = np.floor(pt).astype(int)
                    a = abs(pt[0]-(px[0]+1))*abs(pt[1]-px[1])
                    b = abs(pt[0]-(px[0]))*abs(pt[1]-(px[1]))
                    c = abs(pt[0]-(px[0]+1))*abs(pt[1]-(px[1]+1))
                    d = abs(pt[0]-(px[0]))*abs(pt[1]-(px[1]+1))

                    sa = iImage[min(px[1]+1,iImage.shape[0]-1),px[0]]
                    sb = iImage[min(px[1]+1,iImage.shape[0]-1),min(px[0]+1,iImage.shape[1]-1)]
                    sc = iImage[px[1],px[0]]
                    sd = iImage[px[1],min(px[0]+1,iImage.shape[1]-1)]
                    s= sa*a+sb*b+sc*c+sd*d
                
                oImage[y,x] = s

    return oImage


def cropImage (iImage,iStart, iSize):
    oImage = iImage[iStart[1]:(iStart[1]+iSize[1]), iStart[0]:(iStart[0]+iSize[0])]
    return oImage

def min_maks_povp (normiran_hist):
    povp =0
    for i in range(len(normiran_hist)):
        povp=normiran_hist[i]*i+povp
    
    return np.amin(np.nonzero(normiran_hist)),np.amax(np.nonzero(normiran_hist)),povp

def displayImage2 ( iImage , iTitle, iGridX , iGridY ):
    
    plt.figure()
    plt.title(iTitle)
    plt.imshow(iImage,cmap=plt.cm.gray,vmin=0, vmax=255,extent = (iGridX[0], iImage.shape[1]/iGridX[1], iGridY[0], iImage.shape[0]/iGridY[1]),aspect = 'equal')
    plt.show()

if __name__ == '__main__':
    I0 = interpolateImage(I,iSize = np.array(orig_size)*2,iOrder=0)
    displayImage(I0,"Slika interpolirana z ničtim redom")
    I1 = interpolateImage(I,iSize = np.array(orig_size)*2,iOrder=1)
    displayImage(I1,"Slika interpolirana z prvim redom")
    plt.imshow

    c_size = [65,50]
    C = cropImage(I,iStart = [74,29],iSize=c_size)
    displayImage(C,"Obrezana slika")
    
    C = C.astype(np.uint8)
    h,p,cdf,l=computeHistogram(C)
    displayHistogram(h,l,"Histogram obrezane slike")
    print(min_maks_povp(p))

    print(''' 
    2. Kaj so prednosti in kaj slabosti interpolacije ničtega reda?

    Največja prednost interpolacije ničtega reda je da je bistveno hitreja v primerjavi z interpolaciji
    višjega reda. Njena slabost je da ne proizvaja najbolj podrobne slike zaradi načina na kateri deluje.
    ''')
    C0 = interpolateImage(C,iSize = [600,300],iOrder=0).astype(np.uint8)
    displayImage(C0,"Obrezana slika interpolirana z ničtim redom")
    
    C0 = C0.astype(np.uint8)
    h_0,p_0,cdf_0,l_0=computeHistogram(C0)
    displayHistogram(h_0,l_0,"Histogram obrezane slike")
    print(min_maks_povp(p_0))

    print(''' 
    3. Kaj so prednosti in slabosti interpolacije prvega reda?

    Interpolacija prvega reda dela počasi kot ničtega reda (rabi zračunati 4 uteži), ampak proizvaja 
    bolj podrobne slike.
    ''')

    C1 = interpolateImage(C,iSize = [600,300],iOrder=1)
    displayImage(C1,"Obrezana slika interpolirana z prvim redom")
    
    C1 = C1.astype(np.uint8)
    h_1,p_1,cdf_1,l_1=computeHistogram(C1)
    displayHistogram(h_1,l_1,"Histogram obrezane slike")
    print(min_maks_povp(p_1))

    print(''' 
    4. Kaj dosežemo z interpolacijami višjih redov, npr. z interpolacijo tretjega reda?

    Zvišujemo podrobnost slike za ceno hitrosti.
    ''')

    displayImage2(I,'Orginalna slika',[0,I.shape[1]],[0,I.shape[0]])
    displayImage2(I0,"Slika interpolirana z ničtim redom",[0,I.shape[1]],[0,I.shape[0]])
    displayImage2(I1,"Slika interpolirana z prvim redom",[0,I.shape[1]],[0,I.shape[0]])
    
    




    
