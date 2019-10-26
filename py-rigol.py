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

INSTALLATION
sudo pip install pyusb
sudo pip install pyvisa
sudo pip install pyvisa-py

HOST SBC
RaspberryPi (or similar)

NOTE:
This code contains equipment serial numbers.  Use your serial numbers instead.

"""
#python3

import time
import visa

debug = True        #True or False
sm  = 0.5           #small delay sm sec
med = 1             #med delay 1 sec
lrg = 2             #lrg delay 2 sec


#SETUP
#Create a resource manager using Py library
resources = visa.ResourceManager('@py')
if debug:
    print(resources.list_resources())

#LOOP
while 1:

    #Rigol DL3021 DC Electronic Load 200W
    if 1:
        dcload = resources.open_resource('USB0::6833::3601::DL3A212100350::0::INSTR')
        time.sleep(sm)
        print('\n' + dcload.query('*IDN?'),end='')
        dcload.write('*RST')
        time.sleep(sm)
        dcload.write(':FUNC RES')
        dcload.write(':RES 50')
        #ON
        dcload.write(':INP 1') 
        time.sleep(2)  
        #MEAS
        vdc = str(dcload.query(':MEAS:VOLT?').strip('H\n\r'))
        idc = str(dcload.query(':MEAS:CURR?').strip('H\n\r'))
        res = str(dcload.query(':MEAS:RES:DC?').strip('H\n\r'))
        pwr = str(dcload.query(':MEAS:POW:DC?').strip('H\n\r'))
        #print
        print("Volts: " + vdc)
        print("Amps:  " + idc)
        print("Ohms:  " + res)
        print("Power: " + pwr)
        #OFF
        #dcload.write('SOUR:INP:STAT 0')
        dcload.close()
        time.sleep(sm)

    #Rigol DG1022 Signal Generator
    #('USB0::6833::1416::DG1D124004366\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::0::INSTR', 'ASRL/dev/ttyAMA0::INSTR')
    if 1:
        sg = resources.open_resource('USB0::6833::1416::DG1D124004366\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00::0::INSTR')
        time.sleep(sm)
        idn = str(sg.query('*IDN?'))
        print('\n' + idn.strip(' '),end='')
        #time.sleep(1)
        #sg.write('*RST')        #causes crash ??
        #time.sleep(sm)
        #SETTING
        sg.write('FUNC SIN')
        sg.write('FREQ 1000')
        sg.write('VOLT 1.414')
        sg.write('OUTP ON')
        time.sleep(sm)
        #ECHO
        print('Func: ' + sg.query('FUNC?'),end='')
        print('Freq: ' + sg.query('FREQ?'),end='')
        print('Ampl: ' + sg.query('VOLT?'),end='')
        sg.close()
        time.sleep(sm)

    ##Rigol DM3068 DMM
    ##('USB0::6833::3220::DM3O140800083::0::INSTR', 'ASRL/dev/ttyAMA0::INSTR')
    if 1:
        dmm = resources.open_resource('USB0::6833::3220::DM3O140800083::0::INSTR')
        time.sleep(sm)
        print('\n' + dmm.query('*IDN?'), end='')
        time.sleep(sm)
        #
        #dmm.write('*RST') #causes crash
        #time.sleep(1)
        #MEAS
        vdc = str(dmm.query('MEAS:VOLT:DC?'))
        print('VDC: ' + vdc,end='')
        time.sleep(1)
        dmm.close()
        time.sleep(sm)


    #Rigol DS1102E 2 Channel 100MHz Oscilloscope
    if 1:
        oscilloscope = resources.open_resource('USB0::6833::1416::DS1EB124907269\x00::0::INSTR')
        time.sleep(sm)
        print('\n' + oscilloscope.query('*IDN?'))
        #print(oscilloscope.write('*OPC?'))
        #print(oscilloscope.query(':ACQ:TYPE?'))
        
        oscilloscope.write('*RST')
        time.sleep(sm)
        
        #ACQ
        #oscilloscope.write(':ACQ:MODE ETIM')
        #print(oscilloscope.query(':ACQ:SAMP? CHAN1'))
        
        #Select vert
        oscilloscope.write(':CHAN1:DISP ON')
        oscilloscope.write(':CHAN2:DISP ON')
        oscilloscope.write(':CHAN1:BWL OFF')
        oscilloscope.write(':CHAN2:BWL OFF')
        oscilloscope.write(':CHAN1:SCAL 0.1')
        oscilloscope.write(':CHAN2:SCAL 1')
        oscilloscope.write(':CHAN1:PROB 10')
        oscilloscope.write(':CHAN2:PROB 1')
        oscilloscope.write(':CHANNEL1:OFFSET 0')
        oscilloscope.write(':CHANNEL2:OFFSET -2')
        oscilloscope.write(':CHAN1:COUP DC')
        oscilloscope.write(':CHAN2:COUP DC')
        
        oscilloscope.write(':TRIG:EDGE:SOUR CHAN1')
        oscilloscope.write(':TRIG:EDGE:SLOP POS')
        #oscilloscope.write(':TRIG:EDGE:LEV 1.65')
        time.sleep(1)
        oscilloscope.write(':Trig%50') #may need 1 sec settling time
       
        #HORIZ
        oscilloscope.write(':TIM:MODE MAIN')
        oscilloscope.write(':TIM:FORM Y-T')
        oscilloscope.write(':TIM:OFFS 0')   #0.01
        oscilloscope.write(':TIM:SCAL 0.0005')
        
        #RUN
        oscilloscope.write(':RUN')
        #oscilloscope.write(':AUT0')

        #SETTINGS
        print("VERT:  " + oscilloscope.query(':CHAN1:SCAL?'))
        print("HORIZ: " + oscilloscope.query(':TIM:SCAL?'))
        print("TRIG:  " + oscilloscope.query(':TRIG:EDGE:LEV?'))
        print("MODE:  " + oscilloscope.query(':ACQ:TYPE?'))
        
        #MEAS 
        vpp1 = oscilloscope.query(':MEAS:VPP? CHAN1')
        print("CH1 Vpp: " + vpp1, end=' Freq: ')
        time.sleep(sm)
        freq1 = oscilloscope.query(':MEAS:FREQ? CHAN1')
        print(freq1 + " Hz")
        vpp2 = oscilloscope.query(':MEAS:VPP? CHAN2')
        print("CH2 Vpp: " + vpp2, end=' Freq: ')
        time.sleep(sm)
        freq2 = oscilloscope.query(':MEAS:FREQ? CHAN2')
        print(freq2 + " Hz")
        
        #Extract the reading from the resulting string...
        #readinglines = fullreading.splitlines()
        # ...and convert it to a floating point value.
        #float(readinglines[0])
        #Send the reading to the terminal
        #print(reading)
        #Close the connection
        oscilloscope.close()
        time.sleep(sm)
        
      
    #<CR>  
    #print();
    
    #end while


