import pandas as pd
from PIL import Image #pip install pillow
import numpy
from numpy import array
import matplotlib.pyplot as plt #pip install matplotlib
import seaborn as sb #pip install seaborn
from scipy.interpolate import griddata

class ArpesUFMG:
    def __init__(self, msg='Job Done!'):
        self.msg = msg      
    
    def put_axes(self, image_path, resize=False, w=500, h=500, E_i=20.675, E_f=21.625, Chi_i=-10, Chi_f=10):  
        print('putting axes...')  
        a,b = E_f, E_i  #Energy Window - ERange[eV]
        c,d = Chi_i, Chi_f #chi (Accepted Angle) - aRange[deg]        
        img = Image.open(image_path).rotate(90, expand=True)
        if resize:
            img.thumbnail((w,h), Image.ANTIALIAS)
        m,n = img.size
        if resize:
            print(f'New Size: {m} x {n}')
        else:
            print(f'Original Size: {m} x {n}')
        df = array(img)
        df = pd.DataFrame(df)
        E = numpy.linspace(a,b,n)
        E = numpy.round(E,4)
        df['Energy (eV)']=E
        df.set_index('Energy (eV)', inplace=True)
        chi=numpy.round(numpy.linspace(c,d,m),3) #Acceptance angle array in dg    
        df.columns=chi
        df.interpolate(method='polynomial',order=3,inplace=True)
        fig = plt.figure(figsize=(8,8))
        sb.heatmap(df,cmap='gist_yarg_r')
        plt.xlabel('Accepted Angle (dg)')
        #plt.show()
        fig.savefig('ARPES_R90_new.png')
        print(self.msg)
        return df, m, n
    
    def k_warp(self, df,  m, n, phi=0, verbose=False):
        print('k warping...')
        worksheet = []
        for i in range(0,m):
            for j in range(0,n):
                chi2=float(df.columns[i])
                E2=float(df.index[j]) 
                count2=float(df.values[j][i])      
                kx=numpy.round(float(0.512*E2**(1/2)*numpy.sin(chi2*numpy.pi/180)*numpy.cos(phi*numpy.pi/180)),3)
                ky=numpy.round(float(0.512*E2**(1/2)*numpy.sin(chi2*numpy.pi/180)),3)*round(float(numpy.sin(phi*numpy.pi/180)),3)
                if chi2<0:
                    kp=-(kx**2+ky**2)**(1/2)
                elif chi2>=0:
                    kp=(kx**2+ky**2)**(1/2)
                worksheet.append((chi2,phi,kx,ky,kp,E2,count2))
                if verbose:
                    print(chi2,phi,kx,ky,kp,E2,count2)
        da=pd.DataFrame(worksheet,columns=['Chi','Phi','kx','ky','kp','Energy','Counts'])
        da.sort_values(by=['kp'],inplace=True)
        da.interpolate(method='polynomial',order=3,inplace=True)
        da.to_csv('Warped_new.dat', index=False)
        print(self.msg)
        return da
    
    def plot_k_warp(self, da):
        print('saving k warped file...')
        #from scipy.ndimage.filters import gaussian_filter
        x = (numpy.asarray(da['kp'])+0 ) #Deslocate kp
        y = (numpy.asarray(da['Energy'])-0) #Deslocate Energy
        z = (numpy.asarray(da['Counts'])**(1))# Change the expoent to best contrast
        fig = plt.figure(figsize=(5,8)); #Fig. Size
        plt.xlim(-0.3,0.3) #Kp Limits
        plt.ylim(19,22) # Energy Limits
        plt.xlabel('Parallel $\t{Momentum}$ ($\AA^{-1}$)') #kp Label (using LaTeX)
        plt.ylabel('Energy (eV)') #Energy label
        plt.tricontourf(x, y, z,100, cmap='gist_gray')
        #plt.show();
        fig.savefig('K-WARPED_new.png');
        print(self.msg);
        return None