import numpy as np
import matplotlib.pyplot as plt
import calc_footprint_FFP_climatology as myfootprint_clim
import calc_footprint_FFP as myfootprint
import pandas as pd
import csv

def FFPplot(xr, yr, datePrefix, dateList, meanFCH4List):
    print('REQUIRED INPUTS: xr, yr, datePrefix, dateList, meanFCH4List \n \
        xr & yr from FFP output, datePrefix e.g. "2017-12-", dateList e.g. ["09","10","11"]')
    """
    Inputs:
    1. xr --> x‐array for contour lines from FFP model
    2. yr --> y‐array for contour lines from FFP model
    4. datePrefix --> date string without the day (e.g. '2017-12-')
    3. dateList --> list of DAYS in FFP output (e.g. ['09','10','11'])

    Returns:
    1. outfile --> a list collection of "Directions" for each date.
                    (Directions = a dict of footprint quadrant info)
    2. a subplot of FFP contour

    """

    outfile = []
    Ndates = len(dateList)
    fig, ax = plt.subplots(1,Ndates,figsize = (15*Ndates,Ndates*3))
    # Categorizing footprint by quadrant occupation
    for timeStep in range(Ndates):
        north = []
        south = []
        east = []
        west = []
        NE = []
        SE = []
        SW = []
        NW = []

        # Determining North/South weighting
        for i in range(len(yr[timeStep])): # Selecting contour lines
            for j in range(len(yr[timeStep][i])): # selecting points within each contour

                # North/South
                if yr[timeStep][i][j] > 0:
                    north.append(yr[timeStep][i][j])
                else:
                    south.append(yr[timeStep][i][j])

                # East/West
                if xr[timeStep][i][j] > 0:
                    east.append(xr[timeStep][i][j])
                else:
                    west.append(xr[timeStep][i][j])

                # Northeast
                if yr[timeStep][i][j] > 0 and xr[timeStep][i][j] > 0:
                    NE.append(1), NE.append(1)
                # Southeast
                if yr[timeStep][i][j] < 0 and xr[timeStep][i][j] > 0:
                    SE.append(1), SE.append(1)
                # Southwest
                if yr[timeStep][i][j] < 0 and xr[timeStep][i][j] < 0:
                    SW.append(1), SW.append(1)
                # Northwest
                if yr[timeStep][i][j] > 0 and xr[timeStep][i][j] < 0:
                    NW.append(1), NW.append(1)

        allD = len(NE)+len(SE)+len(SW)+len(NW)
        Directions = {'date': datePrefix+dateList[timeStep],
                    'N': np.round(len(north)/(len(south)+len(north)),3),
                    'E': np.round(len(east)/(len(east)+len(west)),3),
                    'S': np.round(len(south)/(len(south)+len(north)),3),
                    'W': np.round(len(west)/(len(east)+len(west)),3),
                    'NE': np.round(len(NE)/allD,3),
                    'SE': np.round(len(SE)/allD,3),
                    'SW': np.round(len(SW)/allD,3),
                    'NW': np.round(len(NW)/allD,3)}

        outfile.append(Directions)
        # print(f'% at {datePrefix+dateList[timeStep]}:') 

        # print(f"N = {Directions['N']*100}%, E = {Directions['E']*100}%")
        # print(f"S = {Directions['S']*100}%, W = {Directions['W']*100}%")
        # print(f"Northeast = {Directions['NE']*100}%")
        # print(f"Southeast = {Directions['SE']*100}%")
        # print(f"Southwest = {Directions['SW']*100}%")
        # print(f"Northwest = {Directions['NW']*100}%\n")
        
        # Plotting contours
    
        # for i in range(len(xr)):
        for j in range(len(xr[timeStep])):
            ax[timeStep].plot(xr[timeStep][j],yr[timeStep][j])
        ax[timeStep].set_title(datePrefix+dateList[timeStep],fontsize = 40)
        ax[timeStep].axvline(0)
        ax[timeStep].axhline(0)
        ax[timeStep].set_xlim([-50,50])
        ax[timeStep].set_ylim([-50,50])
            

        ax[timeStep].set_xlabel(f"\nMean FCH4: {np.round(meanFCH4List[0][timeStep],5)}\n Median FCH4: {np.round(meanFCH4List[1][timeStep],5)}\n\n N = {Directions['N']}\n \
    S = {Directions['S']} \n E = {Directions['E']} \n  W = {Directions['W']} \n \
    Northeast = {Directions['NE']} \n Southeast = {Directions['SE']}\n Southwest = {Directions['SW']}\n \
    Northwest = {Directions['NW']}",fontsize = 40)

    return outfile, fig

# =======================================================================================


def FFPloop(csv_file, datePrefix, dateList):
    """
    Input:
    1. csv_file = eddypro csv data file
    2. datePrefix = year and month of observations (e.g. '2017-12-')
    3. dateList = list of days (e.g. ['23','24','25','26'])

    Returns:
    1. FFP model xr and yr contour outputs (see FFP readme)
    2. List of daily averaged CH4 flux
    """

    # CHECK IF DATA ARE ALL -9999 --> filter out.

    alldata = pd.read_csv(csv_file,header = 0)

    N = len(alldata['date'])

    WS = alldata['wind_speed']
    date = alldata['date']
    L = alldata['L']
    ustar = alldata['u*']
    sigmav = alldata['v_stddev']
    WD = alldata['wind_dir']
    FCH4 = alldata['ch4_flux']


    data = {} # Initializing dictionary.

    # dateList = ['23','24','25','26']
    # datePrefix = '2018-09-'
    # getting data

    for currentDate in dateList:
        listws = []
        listL = []
        listustar = []
        listsigmav = []
        listwd = []
        listch4 = []
        
        data[datePrefix+currentDate] = {}
        for i in range(N):
            if date[i] == datePrefix+currentDate:
                if WS[i] != -9999.0:
                    listws.append(WS[i])
                else:
                    listws.append(-999)
                    
                if L[i] != -9999.0:
                    listL.append(L[i])
                else:
                    listL.append(-999)
                    
                if ustar[i] != -9999.0:
                    listustar.append(ustar[i])
                else:
                    listustar.append(-999)
                    
                if sigmav[i] != -9999.0:
                    listsigmav.append(float(sigmav[i]))
                else:
                    listsigmav.append(-999)
                    
                if WD[i] != -9999.0:
                    listwd.append(WD[i])
                else:
                    listwd.append(-999)
                    
                if FCH4[i] != -9999.0:
                    listch4.append(FCH4[i])
                else:
                    listch4.append(np.nan)
                    
                data[datePrefix+currentDate]['ws'] = listws
                data[datePrefix+currentDate]['L'] = listL
                data[datePrefix+currentDate]['ustar'] = listustar
                data[datePrefix+currentDate]['sigmav'] = listsigmav
                data[datePrefix+currentDate]['wd'] = listwd
                data[datePrefix+currentDate]['FCH4'] = listch4
                
                
    # Removing dates that have arrays with ONLY NAN's
    tempDateList = []
    for currentDate in dateList: 
        thisData = data[datePrefix+currentDate]
        if np.all(np.array(thisData['ws'])==-999) or np.all(np.array(thisData['L'])==-999) or \
            np.all(np.array(thisData['ustar'])==-999) or np.all(np.array(thisData['sigmav'])==-999) or \
            np.all(np.array(thisData['wd'])==-999):
                data.pop(datePrefix+currentDate, None)
        else:
            tempDateList.append(currentDate)
    dateList = tempDateList
    Ndates = len(dateList)

    print(f'Available dates are: {dateList}')
    # Getting mean daily FCH4
    meanFCH4List = np.zeros((2,Ndates)) # FCH4 stats. [0] = mean, [1] = median
    for i in range(Ndates):
        meanFCH4List[0][i] = np.nanmean(data[datePrefix+dateList[i]]['FCH4'])
        meanFCH4List[1][i] = np.nanmedian(data[datePrefix+dateList[i]]['FCH4'])
    meanFCH4List

    z_measure = 1.599
    z_zero = 0.045
    xr = []
    yr = []

    for currentDate in dateList:
        dateidx = datePrefix+currentDate
        height = [4000]*len(data[dateidx]['ws'])
        FFP = myfootprint_clim.FFP_climatology(zm=z_measure,z0=z_zero,umean=data[dateidx]['ws'],
                                            h=height,ol=data[dateidx]['L'],sigmav=data[dateidx]['sigmav'],
                                            ustar=data[dateidx]['ustar'],wind_dir=data[dateidx]['wd'],rs=np.arange(10,100,10).tolist());
        xr.append(FFP['xr'])
        yr.append(FFP['yr'])
    return xr, yr, meanFCH4List

# =======================================================================================

def FFPsave_csv(outfile, meanFCH4List,name):
    csvcolumns = ['date','N','E','S','W','NE','SE','SW','NW','FCH4']

    filename = 'Directions_'+name+'.csv'


    with open(filename, 'w') as f:

        f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(csvcolumns[0],csvcolumns[1],csvcolumns[2],csvcolumns[3],csvcolumns[4],csvcolumns[5],csvcolumns[6],csvcolumns[7],csvcolumns[8],csvcolumns[9]))
        for i in range(len(outfile)):
            valcol = outfile[i]['date'],outfile[i]['N'],outfile[i]['E'],outfile[i]['S'],outfile[i]['W'],outfile[i]['NE'],outfile[i]['SE'],outfile[i]['SW'],outfile[i]['NW'],meanFCH4List[i]
            f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(valcol))

# =======================================================================================

def FFP_clim(csv_file, dateStart, dateEnd, site):
    """
    Simple flux footprint climatology via Kljun's model
    Input:
    1. csv_file = eddypro csv data file
    2. dateStart = year and month and date of start date (e.g. '2017-03-09')
    3. dateEnd =  year and month and date of start date (e.g. '2017-12-09')
    4) site = "BB1" or "BB2". Adjusts z_m and z0 parameters. BB1: zm=1.599, z0=0.045; BB2: zm=2.5, z0=0.125

    Returns:
    1. FFP model xr and yr contour outputs (see FFP readme)
    2. List of daily averaged CH4 flux
    """

    

    alldata = pd.read_csv(csv_file,header = 0)

    N = len(alldata['date'])

    WS = alldata['wind_speed']
    date = alldata['date']
    L = alldata['L']
    ustar = alldata['u*']
    sigmav = alldata['v_stddev']
    WD = alldata['wind_dir']

    if csv_file[:12] == 'Wilson_Field':
        date = []
        for d in alldata['date']:
            characters = []
            for j in range(len(d)):
                characters.append(d[j])
            first_slash = np.where(np.array(characters) == '/')[0][0]
            second_slash = np.where(np.array(characters) == '/')[0][1]
            if first_slash == 1:    # e.g. 1/23/2019
                this_month = '0'+d[0]
            if first_slash == 2:    # e.g. 10/23/2019
                this_month = d[:2]
            if first_slash == 1 and second_slash == 3:  # e.g. 1/2/2019
                this_day = '0'+d[2]
                this_year = d[4:8]
            if first_slash == 1 and second_slash == 4:  # e.g. 1/20/2019
                this_day = d[2:4]
                this_year = d[5:9]
            if first_slash == 2 and second_slash == 5:  # e.g. 11/20/2019
                this_day = d[3:5]
                this_year = d[6:10]

            this_date = this_year+'-'+this_month+'-'+this_day

            date.append(this_date)
        date = np.array(date)

    # making list of dates that run between dateStart and dateEnd
    start_idx = np.where(date == dateStart)[0][0]
    end_idx = np.where(date == dateEnd)[0][-1] + 1

    # Fixing indexing issue in upcoming for loop.
    if end_idx == len(WS):
        end_idx = end_idx-1


    # dateList = ['23','24','25','26']
    # datePrefix = '2018-09-'
    # getting data
    listws = []
    listL = []
    listustar = []
    listsigmav = []
    listwd = []

    for i in range(start_idx,end_idx+1):
        if WS[i] != -9999.0 and WS[i] != '#NUM!' and WS[i] != 'NA' and ~np.isnan(WS[i]):
            listws.append(WS[i])
        else:
            listws.append(-999)
                    
        if L[i] != -9999.0 and L[i] != '#NUM!' and L[i] != 'NA' and ~np.isnan(L[i]):
            listL.append(L[i])
        else:
            listL.append(-999)
                    
        if ustar[i] != -9999.0 and ustar[i] != '#NUM!' and ustar[i] != 'NA' and ~np.isnan(ustar[i]):
            listustar.append(ustar[i])
        else:
            listustar.append(-999)
                    
        # if sigmav[i] != -9999.0 and sigmav[i] != '#NUM!' and sigmav[i] != 'NA' and ~np.isnan(sigmav[i]):
        #     listsigmav.append(float(sigmav[i]))
        # else:
        #     listsigmav.append(-999)
        
        # BYPASSING ISSUE OF SIGMA_V HAVING #NUM! THAT DOESN'T WORK WITH np.isnan
        if sigmav[i] != -9999.0 and sigmav[i] != '#NUM!' and sigmav[i] != 'NA':
            listsigmav.append(float(sigmav[i]))
        else:
            listsigmav.append(-999)
                    
        if WD[i] != -9999.0 and WD[i] != '#NUM!' and WD[i] != 'NA' and ~np.isnan(WD[i]):
            listwd.append(WD[i])
        else:
            listwd.append(-999)
    
    # Removing dates that have arrays with ONLY NAN's to speed up climatology modelling
    for j in reversed(range(len(listws))): 
        if listws[j] == -999 and listL[j] == -999 and \
            listustar[j] == -999 and listsigmav[j] == -999 and \
            listwd == -999 or \
            listustar[j] < 0.1: # Kljun requirement of ustar >= 0.1
                listws.pop(j)
                listL.pop(j)
                listustar.pop(j)
                listsigmav.pop(j)
                listwd.pop(j)

    # # For faster FFP climatology modelling (removing )
    # ws_idx = np.where(WS != -9999.0)[0]
    # L_idx = np.where(L != -9999.0)[0]
    # ustar_idx = np.where(ustar != -9999.0)[0]
    # sigmav_idx = np.where(sigmav != -9999.0)[0]
    # wd_idx = p.where(WD != -9999.0)[0]

    print('length of dataset:',len(listws))
    if site == "BB1":
        z_measure = 1.599
        z_zero = 0.045
    elif site == "BB2":
        z_measure = 2.5 # BB2
        z_zero = 0.125 # BB2
    else:
        print("ERROR: Enter Site as 'BB1' or 'BB2'")
    print(f'site info: z_m = {z_measure}, z0 = {z_zero}')

    height = [4000]*len(listws)
    FFP = myfootprint_clim.FFP_climatology(zm=z_measure,z0=z_zero,umean=listws,
                                            h=height,ol=listL,sigmav=listsigmav,
                                            ustar=listustar,wind_dir=listwd,rs=np.arange(10,100,10).tolist());

    return FFP['xr'], FFP['yr']
