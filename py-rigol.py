"""
py-rigol.py

@author: https://github.com/willpatton
@created: Oct 22, 2019

REFERENCE
Hackaday.com PyVisa project
https://hackaday.com/2016/11/16/how-to-control-your-instruments-from-a-computer-its-easier-than-you-think/

LIBRARY
pyvisa

DOCS
https://pyvisa.readthedocs.io/en/stable/index.html

"""
#python3

import time
import visa

debug = False         #True or False - shows extra info

#INSTRUMENTS
DP832    = False      #power supply
DL3021   = True       #dc load
DM3068   = True       #multimeter
DG1022   = True       #signal generator
DS1054Z  = True       #oscilloscope (4 channel)
DS1102E  = False      #oscilloscope (2 channel)
  
#DELAYS
sm  = 0.5           #small delay 500ms sec
med = 1             #med delay 1 sec
lrg = 2             #lrg delay 2 sec


"""
SETUP
"""
#Create a resource manager using Py library
resources = visa.ResourceManager('@py')
if debug:
    print(resources.list_resources())


"""
LOOP
"""
while 1:
    
    #Rigol DL3021 DC Electronic Load 200W
    if DL3021:
        print('\nDC LOAD')
        dl = resources.open_resource('USB0::6833::3601::DL3A212100350::0::INSTR')
        time.sleep(sm)
        if debug:
            print('\n' + dl.query('*IDN?'),end='')
        
        #OFF
        time.sleep(sm)
        dl.write('INP OFF')
        time.sleep(med) #wait for bleed off
        
        #RESET
        dl.write('*RST')
        
        #SETTINGS
        time.sleep(sm)
        dl.write(':FUNC RES')
        dl.write(':RES 50')
        
        #ON
        dl.write(':INP ON')
        time.sleep(lrg) #wait for stable reading
        
        #MEAS
        vdc = str(dl.query(':MEAS:VOLT?').strip('H\n\r'))
        idc = str(dl.query(':MEAS:CURR?').strip('H\n\r'))
        res = str(dl.query(':MEAS:RES:DC?').strip('H\n\r'))
        pwr = str(dl.query(':MEAS:POW:DC?').strip('H\n\r'))
        #print
        print("Volts: " + vdc)
        print("Amps:  " + idc)
        print("Ohms:  " + res)
        print("Power: " + pwr)
        #OFF
        #dl.write('SOUR:INP:STAT 0')
        dl.close()
        time.sleep(sm)

    #Rigol DG1022 Signal Generator
    #('USB0::6833::1416::DG1D124004366\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::0::INSTR', 'ASRL/dev/ttyAMA0::INSTR')
    if DG1022:
        print('\nSIGNAL GENERATOR')
        sg = resources.open_resource('USB0::6833::1416::DG1D124004366\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::0::INSTR')
        if debug:
            time.sleep(sm)
            idn = str(sg.query('*IDN?'))
            print('\n' + idn.strip(' '),end='')
        
        time.sleep(sm)
        sg.write('*RST')        #causes crash ??
        time.sleep(sm)
        
        #SETTING
        sg.write('FUNC SIN')
        time.sleep(sm)
        sg.write('FREQ 1000')
        time.sleep(sm)
        sg.write('VOLT:UNIT VPP')
        time.sleep(sm)
        sg.write('VOLT 1.414')
        time.sleep(sm)
        sg.write('OUTP ON')
        time.sleep(sm)
        
        #READBACK
        print('Func: ' + sg.query('FUNC?'),end='')
        print('Freq: ' + sg.query('FREQ?'),end='')
        print('Ampl: ' + sg.query('VOLT?'),end='')
        print('Unit: ' + sg.query('VOLT:UNIT?'),end='')
        
        #CLOSE
        sg.close()
        time.sleep(sm)


    ##Rigol DM3068 DMM
    ##('USB0::6833::3220::DM3O140800083::0::INSTR', 'ASRL/dev/ttyAMA0::INSTR')
    if DM3068:
        print('\nMULTIMETER')
        dmm = resources.open_resource('USB0::6833::3220::DM3O140800083::0::INSTR')
        time.sleep(sm)
        if debug:
            print('\n' + dmm.query('*IDN?'), end='')
        time.sleep(sm)
        
        #RESET
        #dmm.write('*RST') #causes crash
        #time.sleep(med)
        
        #MEAS
        vdc = str(dmm.query('MEAS:VOLT:DC?'))
        print('VDC: ' + vdc,end='')
        time.sleep(sm)
        
        #CLOSE
        dmm.close()
        time.sleep(sm)


    #Rigol DS1102E 2 Channel 100MHz Oscilloscope
    #Assumes CH1 is connected to scope's squarewave output using a 10x probe
    if DS1102E:
        print('\nOSCILLOSCOPE')
        oscilloscope = resources.open_resource('USB0::6833::1416::DS1EB124907269\x00::0::INSTR')
        time.sleep(sm)
        if debug:
            print('\n' + ds.query('*IDN?'))
            time.sleep(sm)

        
        #RESET
        ds.write('*RST')
        time.sleep(sm)
        
        #CHAN
        ds.write(':CHAN1:DISP ON')
        ds.write(':CHAN2:DISP ON')
        ds.write(':CHAN1:BWL OFF')
        ds.write(':CHAN2:BWL OFF')
        ds.write(':CHAN1:SCAL 0.1')
        ds.write(':CHAN2:SCAL 1')
        ds.write(':CHAN1:PROB 10')
        ds.write(':CHAN2:PROB 1')
        ds.write(':CHANNEL1:OFFSET 0')
        ds.write(':CHANNEL2:OFFSET -2')
        ds.write(':CHAN1:COUP DC')
        ds.write(':CHAN2:COUP DC')
        
        #HORIZ
        ds.write(':TIM:MODE MAIN')
        ds.write(':TIM:FORM Y-T')
        ds.write(':TIM:OFFS 0')   #0.01
        ds.write(':TIM:SCAL 0.0005')
        
        #TRIG
        ds.write(':TRIG:EDGE:SOUR CHAN1')
        ds.write(':TRIG:EDGE:SLOP POS')
        ds.write(':TRIG:EDGE:LEV 1.65')
        #time.sleep(med)
        #ds.write(':Trig%50') #may need 1 sec setup time
        
        #RUN
        ds.write(':RUN')
        #ds.write(':AUT0')

        #READBACK
        print("VERT:  " + ds.query(':CHAN1:SCAL?'))
        print("HORIZ: " + ds.query(':TIM:SCAL?'))
        print("TRIG:  " + ds.query(':TRIG:EDGE:LEV?'))
        print("MODE:  " + ds.query(':ACQ:TYPE?'))
        
        #MEAS 
        vpp1 = ds.query(':MEAS:VPP? CHAN1')
        time.sleep(sm)
        print("CH1 Vpp: " + vpp1, end=' Freq: ')
        freq1 = ds.query(':MEAS:FREQ? CHAN1')
        time.sleep(sm)
        print(freq1 + " Hz")
        vpp2 = ds.query(':MEAS:VPP? CHAN2')
        time.sleep(sm)
        print("CH2 Vpp: " + vpp2, end=' Freq: ')
        freq2 = ds.query(':MEAS:FREQ? CHAN2')
        time.sleep(sm)
        print(freq2 + " Hz")
        
        #Extract the reading from the resulting string...
        #readinglines = fullreading.splitlines()
        # ...and convert it to a floating point value.
        #float(readinglines[0])
        #Send the reading to the terminal
        #print(reading)
        
        #CLOSE
        ds.close()
        time.sleep(sm)


    #Rigol DS1054Z 4 Channel 50MHz Oscilloscope
    #Assumes CH1 is connected to scope's squarewave output using a 10x probe
    if DS1054Z:
        print('\nOSCILLOSCOPE')
        ds = resources.open_resource('USB0::6833::1230::DS1ZA203615280::0::INSTR')
        time.sleep(sm)

        if debug:
            idn = str(ds.query('*IDN?')).strip('\r\n ')
            print('\n' + idn, end='')
            time.sleep(sm)
        
        #STOP
        ds.write(':STOP')
        ds.write('*CLE')
        
        #DOES NOT LIKE THIS - crashes on next query()
        #ds.write('*RST')
        #ds.write('*WAI')
        #time.sleep(sm)
                
        #CHAN
        time.sleep(sm)
        ds.write(':CHAN1:DISP ON')
        ds.write(':CHAN2:DISP ON')
        ds.write(':CHAN1:COUP DC')
        ds.write(':CHAN2:COUP DC')
        ds.write(':CHAN1:BWL OFF')
        ds.write(':CHAN2:BWL OFF')
        ds.write(':CHAN1:PROB 10')
        ds.write(':CHAN2:PROB 1')
        ds.write(':CHAN1:INV OFF')
        ds.write(':CHAN2:INV OFF')
        ds.write(':CHAN1:VERN OFF')
        ds.write(':CHAN2:VERN OFF')
        ds.write(':CHAN1:UNIT VOLT')
        ds.write(':CHAN2:UNIT VOLT')
        ds.write(':CHAN1:SCALE 1')
        ds.write(':CHAN2:SCALE 1')
        ds.write(':CHAN1:OFFSET 0')
        ds.write(':CHAN2:OFFSET -2')
              
        #HORIZ
        ds.write(':TIM:MODE MAIN')     #MAIN is YT mode
        ds.write(':TIM:DEL:ENAB OFF')
        #ds.write(':TIM:DEL:OFFS 0')
        #ds.write(':TIM:DEL:SCAL .001')
        ds.write(':TIM:MAIN:OFFS 0')   #0.01
        ds.write(':TIM:MAIN:SCAL 0.0005')

        #TRIG
        ds.write(':TRIG:EDGE:SOUR CHAN1')
        ds.write(':TRIG:EDGE:SLOP POS')
        ds.write(':TRIG:EDGE:LEV 1.65')
        ds.write(':TRIG:SWE NORM')
            
        #READBACK
        time.sleep(med)
        vert = str(ds.query(':CHAN1:SCAL?')).strip('\n\rO ')
        print("VERT:  " + vert)
        tim = str(ds.query(':TIM:SCAL?')).strip('\n\r ')
        print("HORIZ: " + tim)
        trig = str(ds.query(':TRIG:EDGE:LEV?')).strip('\n\r ')
        print("TRIG:  " + trig)
        swp = str(ds.query(':TRIG:SWE?')).strip('\n\r0 ')
        print("SWEEP: " + swp)
        
        #RUN
        ds.write(':RUN')
        #ds.write(':AUT0')
           
        #MEAS
        time.sleep(sm)
        vpp1 = str(ds.query(':MEAS:VPP? CHAN1')).strip('\n\r ')
        print("CH1 Vpp: " + vpp1, end=' Freq: ')
        freq1 = str(ds.query(':MEAS:FREQ? CHAN1')).strip('\n\r ')
        print(freq1 + " Hz")
        vpp2 = str(ds.query(':MEAS:VPP? CHAN2')).strip('\n\r ')
        print("CH2 Vpp: " + vpp2, end=' Freq: ')
        freq2 = str(ds.query(':MEAS:FREQ? CHAN2')).strip('\n\r ')
        print(freq2 + " Hz")
        
        #CLOSE
        ds.close()
        time.sleep(sm)    
      
    #<CR>  
    #print();
    
    #end while


