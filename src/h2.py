'''
Copyright 2015 Stefan Andrei Chelariu
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import smbus2 as smbus
from time import *

#TODO: Implement Data Ready feature

class HMC5883L:
    bus        = None
    auto_range = False
    meas_res   = None
    '''
    *I2C Address
    '''
    DEV_ADDR = 0x1E
    '''
    *Register Map
    '''
    REG_CFG_A = 0
    REG_CFG_B = 1
    REG_MODE  = 2
    REG_X_MSB = 3
    REG_X_LSB = 4
    REG_Z_MSB = 5
    REG_Z_LSB = 6
    REG_Y_MSB = 7
    REG_Y_LSB = 8
    REG_STAT  = 9
    REG_ID_A  = 10
    REG_ID_B  = 11
    REG_ID_C  = 12
    '''
    *Settings
    '''
    SAMPLE_AVG  = { 0:1, 32:2, 64:4, 96:8 }
    OUTPUT_RATE = { 0:0.75, 4:1.5, 8:3, 12:7.5, 16:15, 20:30, 24:75, 28:0 }
    BIAS_MODE   = { 0:"normal", 1:"pos_bias", 2:"neg_bias" }
    GAIN        = { 0:1370, 32:1090, 64:820, 96:660, 128:440, 160:390, 192:330, 224:230 }
    RESOLUTION  = { 0:0.73, 32:0.92, 64:1.22, 96:1.52, 128:2.27, 160:2.56, 192:3.03, 224:4.35 }
    I2C_SPEED   = { 0:"normal", 128:"high" }
    MEAS_MODE   = { 0:"continuous", 1:"single", 2:"idle", 3:"idle" }
    PARAM_DIC   = { 'sample_avg':SAMPLE_AVG,
        'output_rate':OUTPUT_RATE, 
        'bias_mode':BIAS_MODE, 
        'gain':GAIN, 
        'resolution':RESOLUTION, 
        'i2c_speed':I2C_SPEED, 
        'meas_mode':MEAS_MODE }
    REGISTER    = { 'sample_avg':REG_CFG_A, 
        'output_rate':REG_CFG_A, 
        'bias_mode':REG_CFG_A, 
        'gain':REG_CFG_B, 
        'resolution':REG_CFG_B, 
        'i2c_speed':REG_MODE, 
        'meas_mode':REG_MODE }
    OFFSET      = { 'sample_avg':0b10011111,
        'output_rate':0b11100011,
        'bias_mode':0b11111100,
        'gain':0b00011111,
        'resolution':0b00011111, 
        'i2c_speed':0b01111111, 
        'meas_mode':0b11111100 }

    #Private Utility Functions
    def _two_comp_to_dec(self, b):
        if b & 0x8000:
            b = -(0x010000 - b)
        return b

    #Public Functions
    def set_parameter(self, parameter, value):
        if self.PARAM_DIC[parameter] != None:
            _param_dic = self.PARAM_DIC[parameter]
            _reg       = self.REGISTER[parameter]
            _offset    = self.OFFSET[parameter]
            _val = next((i for i,j in _param_dic.items() if j == value), None)
            if _val != None:
                _byte = self.bus.read_byte_data(self.DEV_ADDR, _reg)
                _byte &= _offset
                _byte |= _val
                self.bus.write_byte_data(self.DEV_ADDR, _reg, _byte)
                if self.bus.read_byte_data(self.DEV_ADDR, _reg) != _byte:
                    return False
            else:
                #if resolution is changed we need to update 
                #the class property
                if parameter == "resolution":
                    self.meas_res = value
                elif parameter == "gain":
                    self.meas_res = self.RESOLUTION[_val]
                else:
                    return False
        else:
            return False

        return True

    def get_parameter(self, parameter):
        if self.PARAM_DIC[parameter] != None:
            _param_dic = self.PARAM_DIC[parameter]
            _reg 	   = self.REGISTER[parameter]
            _offset    = self.OFFSET[parameter] ^ 0xFF
            _val = self.bus.read_byte_data(self.DEV_ADDR, _reg)
            _val &= _offset
            return _param_dic[_val]
        else:
            return None
    
    def get_field_x(self):
        _x = self.bus.read_byte_data(self.DEV_ADDR, self.REG_X_MSB) << 8 | self.bus.read_byte_data(self.DEV_ADDR, self.REG_X_LSB)
        _x = self._two_comp_to_dec(_x)
        return _x*self.meas_res
        

    def get_field_y(self):
        _y = self.bus.read_byte_data(self.DEV_ADDR, self.REG_Y_MSB) << 8 | self.bus.read_byte_data(self.DEV_ADDR, self.REG_Y_LSB)
        _y = self._two_comp_to_dec(_y)		
        return _y*self.meas_res
    
    def get_field_z(self):
        _z = self.bus.read_byte_data(self.DEV_ADDR, self.REG_Z_MSB) << 8 | self.bus.read_byte_data(self.DEV_ADDR, self.REG_Z_LSB)
        _z = self._two_comp_to_dec(_z)
        return _z*self.meas_res

    def get_field_xyz(self):
        return {'x':self.get_field_x(), 'y':self.get_field_y(), 'z':self.get_field_z()}
    
    def __init__(self, i2c_module):
        self.bus = smbus.SMBus(i2c_module)
        self.meas_res = self.get_parameter("resolution") 