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
#!/usr/bin/python3

from datetime import date
import time
import visa           #Python instrument library

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

#TEST PARAMS
volts = 5.0
frequency = 1000.0
amplitude = 1.414

#TIMERS/COUNTERS
loop_count = 0


#is float
def is_numeric(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

"""
SETUP
"""
print('Begin: ' + time.ctime())

#Create a resource manager using Py library
resources = visa.ResourceManager('@py')
if debug:
    print(resources.list_resources())


"""
LOOP
"""
def loop():
    #TODO
    print('hello')
    
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
        print('INPUT: OFF',end='')
        dl.write('INP OFF')
        time.sleep(med) #wait for bleed off
        
        #RESET
        dl.write('*RST')
        
        #SETTINGS
        time.sleep(sm)
        dl.write(':FUNC RES')
        dl.write(':RES 50')
        
        #ON
        print('...ON')
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
    if DG1022:
        """
        Does not have a reliable SCPI interface
        """
        print('\nSIGNAL GENERATOR')
        sg = resources.open_resource('USB0::6833::1416::DG1D124004366\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::0::INSTR')
        if debug:
            time.sleep(sm)
            idn = str(sg.query('*IDN?'))
            print('\n' + idn.strip(' '),end='')
        
        time.sleep(med)
        print('OUTPUT: OFF', end='')
        sg.write('OUTP OFF')
        time.sleep(sm)
        sg.write('*RST')        #causes crash ??
        time.sleep(sm)
        
        #SETTING
        sg.write('FUNC SIN')
        time.sleep(med)      #needs extra time here ??
        sg.write('FREQ ' + str(frequency))
        time.sleep(sm)
        sg.write('VOLT:UNIT VPP')
        time.sleep(sm)
        sg.write('VOLT ' + str(amplitude))
        time.sleep(sm)
        print('...ON')
        sg.write('OUTP ON')
           
        #READBACK
        """
        Requires a lengthy delay (>1.2 sec) between query() to prevent crashes
        """
        if False:
            dly = 0.8
            time.sleep(dly)
            print('Func: ' + sg.query('FUNC?'),end='')
            time.sleep(dly)
            print('Freq: ',end='')
            print(float(sg.query('FREQ?')))
            time.sleep(dly)
            print('Ampl: ',end='')
            print(float(sg.query('VOLT?')))
            #time.sleep(3)
            #print('Unit: ' + sg.query('VOLT:UNIT?'),end='')
        else:
            print('No query mode.')
            
        #CLOSE
        time.sleep(sm) #ensure setup time for the close cmd
        sg.close()
        time.sleep(sm)


    #Rigol DM3068 DMM
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
        print('VDC: ',end='')
        print(float(vdc))
        time.sleep(sm)
        
        #CLOSE
        dmm.close()
        time.sleep(sm)


    #Rigol DS1102E 2 Channel 100MHz Oscilloscope
    if DS1102E:
        """
        Assumes CH1 is connected to scope's squarewave output using a 10x probe
        """
        print('\nOSCILLOSCOPE')
        oscilloscope = resources.open_resource('USB0::6833::1416::DS1EB124907269\x00::0::INSTR')
        time.sleep(sm)
        if debug:
            print('\n' + ds.query('*IDN?'))
            time.sleep(sm)
     
        #STOP
        ds.write(':STOP')
        
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
        
        #CLOSE
        ds.close()
        time.sleep(sm)


    #Rigol DS1054Z 4 Channel 50MHz Oscilloscope
    if DS1054Z:
        """
        Assumes CH1 is connected to scope's squarewave output using a 10x probe
        """
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
        print('VERT:  ', float(vert), end=' V/div\n')
        horiz = str(ds.query(':TIM:SCAL?')).strip('\n\r ')
        print('HORIZ: ', float(horiz), end=' s/div\n')
        trig = str(ds.query(':TRIG:EDGE:LEV?')).strip('\n\r ')
        print('TRIG:  ', float(trig), end=' V\n')
        swp = str(ds.query(':TRIG:SWE?')).strip('\n\r0 ')
        print('SWEEP:  ' + swp)
        
        #RUN
        ds.write(':RUN')
           
        #MEAS
        time.sleep(sm)
        vpp1 = str(ds.query(':MEAS:VPP? CHAN1')).strip('\n\r ')
        print('CH1:    ', end='')
        if is_numeric(vpp1):
            #signal
            print(float(vpp1), end=' Vpp  ')
        else:
            #no signal
            print('Vpp=*****', end=' ')
        freq1 = str(ds.query(':MEAS:FREQ? CHAN1')).strip('\n\r ')
        if is_numeric(freq1):
            #signal
            print('Freq: ', float(freq1), end=' Hz\n')
        else:
            #no signal
            print()
        vpp2 = str(ds.query(':MEAS:VPP? CHAN2')).strip('\n\r ')
        print('CH2:    ', end='')
        if is_numeric(vpp2):
            #signal
            print(float(vpp2), end=' Vpp  ')
        else:
            #no signal
            print('Vpp=*****', end=' ')
        freq2 = str(ds.query(':MEAS:FREQ? CHAN2')).strip('\n\r ')
        if is_numeric(freq2):
            #signal
            print('Freq: ',float(freq2), end=' Hz\n')
        else:
            #no signal
            print()
        
        #IMG
        if 0:
            #TODO
            ds.write(':STOP')
            time.sleep(sm)
            #ds.query(':DISP:DATA?')
            time.sleep(sm)
            ds.write(':RUN')
             
        #CLOSE
        ds.close()
        time.sleep(sm)    
      


    #end of loop stuff here    
    loop_count = loop_count + 1
    print('\nLOOP: ', loop_count)
    
    #end while
 
