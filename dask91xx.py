import os
import platform
from ctypes import *

from definitions import ROOT_DIR


class Dask91xxLib:
    PCIe_9101 =52
    PCIe_9121 =53
    PCIe_9141 =54
    PCIe_9103 =55
    PCIe_9147 =57

 
    AD_B_10_V = 0x00000001
    AD_B_5_V = 0x00000002
    AD_B_2_5_V = 0x00000003
    AD_B_1_25_V = 0x00000004
    ASYNCH_OP = 2
    
# #-------------------------
# # Constants for PCIe-91xx 
# #-------------------------
# #
#   AI Constants
#  
# #Input Type
    P91xx_AI_SingEnded          =0x00
    P91xx_AI_Differential       =0x80
    P91xx_CH0					=0x0
    P91xx_CH1					=0x1
    P91xx_CH2					=0x2
    P91xx_CH3					=0x3
    P91xx_CH4					=0x4
    P91xx_CH5					=0x5
    P91xx_CH6					=0x6
    P91xx_CH7					=0x7
    P91xx_CH8					=0x8
    P91xx_CH9					=0x9
    P91xx_CH10					=0xa
    P91xx_CH11					=0xb
    P91xx_CH12					=0xc
    P91xx_CH13					=0xd
    P91xx_CH14					=0xe
    P91xx_CH15					=0xf
    #For 9103
    P91xx_CH16					=0x10
    P91xx_CH17					=0x11
    P91xx_CH18					=0x12
    P91xx_CH19					=0x13
    P91xx_CH20					=0x14
    P91xx_CH21					=0x15
    P91xx_CH22					=0x16
    P91xx_CH23					=0x17
    P91xx_CH24					=0x18
    P91xx_CH25					=0x19
    P91xx_CH26					=0x1a
    P91xx_CH27					=0x1b
    P91xx_CH28					=0x1c
    P91xx_CH29					=0x1d
    P91xx_CH30					=0x1e
    P91xx_CH31					=0x1f
    #Timbase and conversion settings for AI
    P91xx_AI_TIMEBASE_INT       =0x00
    P91xx_AI_TIMEBASE_EXT       =0x10
    P91xx_AI_CONVSRC_EXT        =0x20 
    #Trigger Mode
    P91xx_AI_TRGMOD_POST        =0x00
    P91xx_AI_TRGMOD_DELAY       =0x02
    P91xx_AI_TRGMOD_PRE         =0x04
    P91xx_AI_TRGMOD_MID         =0x05              
    #Trigger Source
    P91xx_AI_TRGSRC_SOFT        =0x00
    P91xx_AI_TRGSRC_EXTD        =0x10
    P91xx_AI_TRGSRC_AI          =0x20
    #Trigger Polarity
    P91xx_AI_TrgPositive        =0x000
    P91xx_AI_TrgNegative        =0x100
    #Delay Trigger with Samples
    P91xx_AI_DlyInTimebase      =0x000
    P91xx_AI_DlyInSamples       =0x200
    #Analog Trigger condition constants
    P91xx_Below_Low_level       =0x00
    P91xx_Above_High_Level      =0x10
    P91xx_Inside_Region         =0x20
    P91xx_High_Hysteresis       =0x30
    P91xx_Low_Hysteresis        =0x40
    
    #
    #  AO Constants
    # 
    #Timbase for AO
    P91xx_AO_TIMEBASE_INT       =0x00
    P91xx_AO_TIMEBASE_EXT       =0x01
    #Trigger Mode
    P91xx_AO_TRGMOD_POST        =0x00
    #Trigger Source
    P91xx_AO_TRGSRC_SOFT        =0x00
    P91xx_AO_TRGSRC_EXTD        =0x10
    #Trigger Polarity
    P91xx_AO_TrgPositive        =0x000
    P91xx_AO_TrgNegative        =0x100

    #
    #  DI Constants
    # 
    #Timbase and conversion settings for DI
    P91xx_DI_TIMEBASE_INT       =0x00
    P91xx_DI_TIMEBASE_EXT       =0x01
    P91xx_DI_CONVSRC_SYNC_IN    =0x02
    #Trigger Mode
    P91xx_DI_TRGMOD_POST        =0x00
    #Trigger Source
    P91xx_DI_TRGSRC_SOFT        =0x00
    P91xx_DI_TRGSRC_EXTD        =0x10
    #Trigger Polarity
    P91xx_DI_TrgPositive        =0x000
    P91xx_DI_TrgNegative        =0x100

    #
    #  DO Constants
    # 
    #Timbase for DO
    P91xx_DO_TIMEBASE_INT       =0x00
    P91xx_DO_TIMEBASE_EXT       =0x01
    #Trigger Mode
    P91xx_DO_TRGMOD_POST        =0x00
    #Trigger Source
    P91xx_DO_TRGSRC_SOFT        =0x00
    P91xx_DO_TRGSRC_EXTD        =0x10
    #Trigger Polarity
    P91xx_DO_TrgPositive        =0x000
    P91xx_DO_TrgNegative        =0x100

    P91xx_INFINITE_RETRIG       =0x0

    # 
    #   Encoder GPTC Constants
    #  
    P91xx_GPTC0                 =0x00
    P91xx_GPTC1                 =0x01
    P91xx_ENCODER0              =0x02
    P91xx_ENCODER1              =0x03    

    # 
    #   AI DMA with Encoder Feature
    #  
    AI_DMA_ENCODER_MODE         =0x10    

    #-------------------------------*/
    # General Purpose Timer/Counter */
    #-------------------------------*/
    #Counter Mode*/
    General_Counter         = 0x00
    Pulse_Generation        = 0x01
    #GPTC clock source*/
    GPTC_CLKSRC_EXT         = 0x08
    GPTC_CLKSRC_INT         = 0x00
    GPTC_GATESRC_EXT        = 0x10
    GPTC_GATESRC_INT        = 0x00
    GPTC_UPDOWN_SELECT_EXT  = 0x20
    GPTC_UPDOWN_SELECT_SOFT = 0x00
    GPTC_UP_CTR             = 0x40
    GPTC_DOWN_CTR           = 0x00
    GPTC_ENABLE             = 0x80
    GPTC_DISABLE            = 0x00


    #-----------------------------------------------------------*/
    # General Purpose Timer/Counter for PCI-922x/6202/PCIe-91xx */
    #-----------------------------------------------------------*/
    #Counter Mode*/
    SimpleGatedEventCNT       = 0x01
    SinglePeriodMSR           = 0x02
    SinglePulseWidthMSR       = 0x03
    SingleGatedPulseGen       = 0x04
    SingleTrigPulseGen        = 0x05
    RetrigSinglePulseGen      = 0x06
    SingleTrigContPulseGen    = 0x07
    ContGatedPulseGen         = 0x08
    SingleTrigContPulseGenPWM = 0x0a
    ContGatedPulseGenPWM      = 0x0b
    CW_CCW_Encoder            = 0x0c
    x1_AB_Phase_Encoder       = 0x0d
    x2_AB_Phase_Encoder       = 0x0e
    x4_AB_Phase_Encoder       = 0x0f
    Phase_Z                   = 0x10

    #GPTC clock source*/
    GPTC_CLK_SRC_Ext          = 0x01
    GPTC_CLK_SRC_Int          = 0x00
    GPTC_GATE_SRC_Ext         = 0x02
    GPTC_GATE_SRC_Int         = 0x00
    GPTC_UPDOWN_Int           = 0x00
    #GPTC clock polarity*/
    GPTC_CLKSRC_LACTIVE       = 0x01
    GPTC_CLKSRC_HACTIVE       = 0x00
    GPTC_GATE_LACTIVE         = 0x02
    GPTC_GATE_HACTIVE         = 0x00
    GPTC_UPDOWN_LACTIVE       = 0x04
    GPTC_UPDOWN_HACTIVE       = 0x00
    GPTC_OUTPUT_LACTIVE       = 0x08
    GPTC_OUTPUT_HACTIVE       = 0x00
    #GPTC OP Parameter*/
    IntGate                   = 0x0
    IntUpDnCTR                = 0x1
    IntENABLE                 = 0x2




    def __init__(self):
        self.MW_DLL_FILE_NAME_X64_WIN = "PCI-Dask64.dll"
        self.MW_DLL_FILE_NAME_X86_WIN = "PCI-dll"
        self.MW_DLL_FILE_NAME_X64_LINUX = "libAdMWCore64.so"
        self.MW_DLL_FILE_NAME_X86_LINUX = "libAdMWCore.so"
        self.strPlatform = platform.architecture()[0]
        self.strOS = platform.architecture()[1]

        if "Windows" in self.strOS:
            if '32' in self.strPlatform:
                print("System is Windows 32Bits")
                self.libHandle = windll.LoadLibrary(os.path.join(ROOT_DIR, "lib", self.MW_DLL_FILE_NAME_X86_WIN))
            else:
                print("System is Windows 64Bits")
                self.libHandle = windll.LoadLibrary(os.path.join(ROOT_DIR, "lib", self.MW_DLL_FILE_NAME_X64_WIN))
        else:
            if '32' in self.strPlatform:
                print("System is Linux 32Bits")
                self.libHandle = cdll.LoadLibrary(os.path.join(ROOT_DIR, "lib", self.MW_DLL_FILE_NAME_X86_LINUX))
            else:
                print("System is Linux 64Bits")
                self.libHandle = cdll.LoadLibrary(os.path.join(ROOT_DIR, "lib", self.MW_DLL_FILE_NAME_X64_LINUX))
        
    def Register_Card(self, card_type, card_num):
        return self.libHandle.Register_Card(card_type, card_num)
    
    def PCI_Buffer_Alloc (self,var_card, BufferSize):
        return self.libHandle.PCI_Buffer_Alloc (var_card, BufferSize)
    
    def AI_ContBufferSetup(self, var_card, RDBuffer, AI_READCOUNT, BufferId):
        return self.libHandle.AI_ContBufferSetup(var_card, RDBuffer, AI_READCOUNT, BufferId)
    
    def AI_Config(self,var_card, ConfigCtrl, TrigCtrl, TriggerCount, MidOrDlyScans, AutoResetBuf):
        return self.libHandle.AI_Config(var_card, ConfigCtrl, TrigCtrl, TriggerCount, MidOrDlyScans, AutoResetBuf)
    
    def AI_CounterInterval(self,var_card, ScanIntrv, SampIntrv):
        return self.libHandle.AI_CounterInterval(var_card, ScanIntrv, SampIntrv)
    
    def AI_AsyncDblBufferMode(self,var_card, Enable):
        return self.libHandle.AI_AsyncDblBufferMode(var_card, Enable)
    
    def AI_ContReadChannel(self,var_card, Channel, AdRange, BufferId, AI_READCOUNT, SampleRate, SyncMode):
        return self.libHandle.AI_ContReadChannel(var_card, Channel, AdRange, BufferId, AI_READCOUNT, SampleRate, SyncMode)
    
    def AI_AsyncCheck(self,var_card,Stopped=list(),AccessCnt=list()):
        bTemp0=c_bool(0)
        bTemp1=c_uint32(0)
        rtn=self.libHandle.AI_AsyncCheck(var_card,byref(bTemp0),byref(bTemp1))
        Stopped.clear()
        Stopped.append(bTemp0.value)
        AccessCnt.clear()
        AccessCnt.append(bTemp1.value)
        
        return rtn
    

    def AI_AsyncClear(self,var_card, AccessCnt=list()):
        bTemp=c_uint32(0)
        rtn=self.libHandle.AI_AsyncClear(var_card, byref(bTemp))
        AccessCnt.clear()
        AccessCnt.append(bTemp.value)
        
        return rtn
    
    def AI_ContVScale(self,var_card,adRange, RDBuffer,voltageArray=list() ,count=c_int32):
        VBuffer = (c_double*RDBuffer._length_)()
        cast(VBuffer, POINTER(c_double))
        rtn=self.libHandle.AI_ContVScale(var_card, adRange, RDBuffer, VBuffer, count)
        voltageArray.clear()
        voltageArray.append(VBuffer)
        return rtn
    
    def Release_Card(self,var_card):
        rtn=self.libHandle.Release_Card(var_card)
        return rtn
    
    def AI_ContBufferReset(self,var_card):
        rtn=self.libHandle.AI_ContBufferReset(var_card)
        return rtn
    
    def PCI_Buffer_Free(self,var_card,RDBuffer):
        rtn=self.libHandle.PCI_Buffer_Free(var_card,RDBuffer)
        return rtn
    
    def AI_ContReadMultiChannels(self,card, CHANNELCOUNT, Chans, AdRanges, BufferId, AI_READCOUNT, SampleRate, SyncMode):
        rtn =self.libHandle.AI_ContReadMultiChannels(card, CHANNELCOUNT, Chans, AdRanges, BufferId, AI_READCOUNT, SampleRate, SyncMode)
        return rtn
    
    def AI_AsyncDblBufferHalfReady(self,var_card,HalfReady=list(),Stopped=list()):
        bTemp0=c_bool(0)
        bTemp1=c_bool(0)
        rtn=self.libHandle.AI_AsyncDblBufferHalfReady(var_card,byref(bTemp0),byref(bTemp1))
        print(bTemp0.value)
        HalfReady.clear()
        HalfReady.append(bTemp0.value)
        Stopped.clear()
        Stopped.append(bTemp1.value)
        return rtn
    
    def AI_AsyncDblBufferHandled(self,card):
        rtn=self.libHandle.AI_AsyncDblBufferHandled(card)
        return rtn

    def AI_AsyncDblBufferOverrun(self,card, op, overrunFlag):
        if op==0:
            bTemp=c_bool(0)
            rtn=self.libHandle.AI_AsyncDblBufferOverrun(card, op, byref(bTemp))
            overrunFlag.clear()
            overrunFlag.append(bTemp.value)
            return rtn
        else:
            rtn=self.libHandle.AI_AsyncDblBufferOverrun(card, op, overrunFlag)
            return rtn
        
    def AI_AsyncReTrigNextReady(self,var_card, Ready=list(), StopFlag=list(), RdyTrigCnt=list()):
        bTemp0=c_bool(0)
        bTemp1=c_bool(0)
        bTemp2=c_int16(0)
        rtn=self.libHandle.AI_AsyncReTrigNextReady(var_card, byref(bTemp0), byref(bTemp1), byref(bTemp2))
        Ready.clear()
        StopFlag.clear()
        RdyTrigCnt.clear()
        Ready.append(bTemp0.value)
        StopFlag.append(bTemp1.value)
        RdyTrigCnt.append(bTemp2.value)
        return rtn
    
    def AI_AnalogTrig_Config_ByVoltage(self,var_card, TrigType, ThresholdHV, ThresholdLV, AdRange):
        fTemp0=c_double(ThresholdHV)
        fTemp1=c_double(ThresholdLV)
        rtn=self.libHandle.AI_AnalogTrig_Config_ByVoltage(var_card, TrigType, fTemp0,fTemp1, AdRange)
        return rtn
    
    def AI_ContScanChannels(self,var_card, CHANNELCOUNT , AdRange, BufferId, AI_READCOUNT, SampleRate, SyncMode):
        rtn=self.libHandle.AI_ContScanChannels(var_card, CHANNELCOUNT, AdRange, BufferId, AI_READCOUNT, SampleRate, SyncMode)
        return rtn
    
    def AI_ContReadMultiChannelsToFile(self,var_card, CHANNELCOUNT, Chans, AdRanges, FileName, AI_READCOUNT, SampleRate, SyncMode):
        rtn=self.libHandle.AI_ContReadMultiChannelsToFile(var_card, CHANNELCOUNT, Chans, AdRanges, FileName, AI_READCOUNT, SampleRate, SyncMode)
        return rtn
    
    def AI_AsyncDblBufferToFile(self,var_card):
        rtn=self.libHandle.AI_AsyncDblBufferToFile(var_card)
        return rtn
    
    def AI_ReadChannel(self,var_card, Channel, AdRange, Value=list()):
        bTemp=c_uint16(0)
        rtn=self.libHandle.AI_ReadChannel(var_card, Channel, AdRange, byref(bTemp))
        Value.clear()
        Value.append(bTemp.value)
        return rtn
    
    def AI_VoltScale(self,var_card, AdRange, Value, Voltage=list()):
        bTemp=c_double(0)
        rtn=self.libHandle.AI_VoltScale(var_card, AdRange, Value, byref(bTemp))
        Voltage.clear()
        Voltage.append(bTemp.value)
        return rtn
    
    def AO_Config(self,var_card, ConfigCtrl, TrigCtrl, TriggerCount, AutoResetBuf):
        rtn=self.libHandle.AO_Config(var_card, ConfigCtrl, TrigCtrl, TriggerCount, AutoResetBuf)
        return rtn
    
    def AO_Config(self,var_card, ConfigCtrl, TrigCtrl, TriggerCount, AutoResetBuf):
        rtn=self.libHandle.AO_Config(var_card, ConfigCtrl, TrigCtrl, TriggerCount, AutoResetBuf)
        return rtn
    
    def AO_AsyncDblBufferMode(self,var_card, Enable):
        rtn=self.libHandle.AO_AsyncDblBufferMode(var_card, Enable)
        return rtn
    
    def AO_ContBufferSetup(self,var_card,Buffer, WriteCount, BufferId=list()):
        bTemp=c_bool(0)
        rtn=self.libHandle.AO_ContBufferSetup(var_card,Buffer, WriteCount, byref(bTemp))
        BufferId.clear()
        BufferId.append(bTemp.value)
        return rtn
    
    def AO_ContWriteChannel(self,var_card, Channel, BufferId0, WriteCount, Iterations, Interval, definite, SyncMode):
        rtn=self.libHandle.AO_ContWriteChannel(var_card, Channel, BufferId0, WriteCount, Iterations, Interval, definite, SyncMode)
        return rtn
    
    def AO_ContBufferReset(self,var_card):
        rtn=self.libHandle.AO_ContBufferReset(var_card)
        return rtn
    
    def AO_AsyncClear(self,var_card, AccessCnt=list(), stop_mode=c_uint16):
        bTemp=c_uint32(0)
        rtn=self.libHandle.AO_AsyncClear(var_card, byref(bTemp), stop_mode)
        AccessCnt.clear()
        AccessCnt.append(bTemp.value)
        return rtn
    
    def AO_AsyncDblBufferHalfReady(self,var_card, HalfReady=list):
        bTemp=c_bool(0)
        rtn=self.libHandle.AO_AsyncDblBufferHalfReady(var_card, byref(bTemp))
        HalfReady.clear()
        HalfReady.append(bTemp.value)
        return rtn
    
    def AO_AsyncCheck(self,var_card, Stopped, AccessCnt): 
        bTemp0=c_bool(0)
        bTemp1=c_uint32(0)
        rtn=self.libHandle.AO_AsyncCheck(var_card, byref(bTemp0), byref(bTemp1))
        Stopped.clear()
        Stopped.append(bTemp0.value)
        AccessCnt.clear()
        AccessCnt.append(bTemp1.value)
        return rtn
    
    def AO_relay_EN(self,var_card, enable):
        rtn=self.libHandle.AO_relay_EN(var_card, enable)
        return rtn
    
    def AO_ContWriteMultiChannels(self,var_card, WRITECHNCNT, Chans, BufferId, WriteCount, Iterations, Interval, definite, SyncMode):
        rtn=self.libHandle.AO_ContWriteMultiChannels(var_card, WRITECHNCNT, Chans, BufferId, WriteCount, Iterations, Interval, definite, SyncMode)
        return rtn
    
    def AO_VWriteChannel(self,var_card, Channel, Voltage):
        fTemp0=c_double(Voltage)
        rtn=self.libHandle.AO_VWriteChannel(var_card, Channel,fTemp0)
        return rtn
    
    def AI_ContBufferReset(self,var_card):
        rtn=self.libHandle.AI_ContBufferReset(var_card)
        return rtn
    
    def DI_Config(self,var_card, ConfigCtrl, TrigCtrl, TRIG_COUNT, AutoResetBuf):
        rtn=self.libHandle.DI_Config(var_card, ConfigCtrl, TrigCtrl, TRIG_COUNT, AutoResetBuf)
        return rtn

    def DI_AsyncDblBufferMode(self,var_card, Enable):
        rtn=self.libHandle.DI_AsyncDblBufferMode(var_card, Enable)
        return rtn
    
    def DI_ContBufferSetup(self,var_card, RDBuffer, DI_READCOUNT, BufferId):
        rtn=self.libHandle.DI_ContBufferSetup(var_card, RDBuffer, DI_READCOUNT, BufferId)
        return rtn
    
    def DI_ContReadPort(self,var_card, Port, BufferId, DI_READCOUNT, SampleRate, SyncMode):
        fTemp=c_double(SampleRate)
        rtn=self.libHandle.DI_ContReadPort(var_card, Port, BufferId, DI_READCOUNT, fTemp, SyncMode)
        return rtn
    
    def DI_AsyncCheck(self,var_card, Stopped, AccessCnt):
        bTemp0=c_bool(0)
        bTemp1=c_uint32(0)
        rtn=self.libHandle.DI_AsyncCheck(var_card,byref(bTemp0),byref(bTemp1))
        Stopped.clear()
        Stopped.append(bTemp0.value)
        AccessCnt.clear()
        AccessCnt.append(bTemp1.value)
        return rtn
    
    def DI_AsyncClear(self,var_card,AccessCnt=list()):
        bTemp=c_uint32(0)
        rtn=self.libHandle.DI_AsyncClear(var_card,byref(bTemp))
        AccessCnt.clear()
        AccessCnt.append(bTemp.value)
        return rtn
    
    def DI_AsyncReTrigNextReady(self,var_card, Ready=list(), StopFlag=list(), RdyTrigCnt=list()):
        bTemp0=c_bool(0)
        bTemp1=c_bool(0)
        bTemp2=c_uint16(0)
        rtn=self.libHandle.DI_AsyncReTrigNextReady(var_card, byref(bTemp0), byref(bTemp1), byref(bTemp2))
        Ready.clear()
        StopFlag.clear()
        RdyTrigCnt.clear()
        Ready.append(bTemp0.value)
        StopFlag.append(bTemp1.value)
        RdyTrigCnt.append(bTemp2.value)
        return rtn
    
    def DI_AsyncDblBufferHalfReady(self,var_card, HalfReady=list()):
        bTemp=c_bool(0)
        rtn=self.libHandle.AI_AsyncDblBufferHalfReady(var_card,byref(bTemp))
        HalfReady.clear()
        HalfReady.append(bTemp.value)
        return rtn
    
    def DI_AsyncDblBufferOverrun(self,var_card, op, overrunFlag=list()):
        bTemp=c_bool(0)
        rtn=self.libHandle.DI_AsyncDblBufferOverrun(var_card, op, byref(bTemp))
        overrunFlag.clear()
        overrunFlag.append(bTemp)
        return rtn
    
    def DI_ReadPort(self,var_card, Port ,DI_Read=list()):
        bTemp=c_uint32(0)
        rtn=self.libHandle.DI_ReadPort(var_card, Port ,byref(bTemp))
        DI_Read.clear()
        DI_Read.append(bTemp.value)
        return rtn
    
    def DO_Config(self,var_card, ConfigCtrl, TrigCtrl, TrigCnt, AutoResetBuf):
        rtn=self.libHandle.DO_Config(var_card, ConfigCtrl, TrigCtrl, TrigCnt, AutoResetBuf)
        return rtn
    
    def DO_ContBufferSetup(self,var_card, W_Buffer, WriteCount, BufferId):
        rtn=self.libHandle.DO_ContBufferSetup(var_card, W_Buffer, WriteCount, BufferId)
        return rtn
    
    def DO_ContWritePort(self,var_card, Port, BufferId, WriteCount, Iterations, SampleRate, SyncMode):
        fTemp0=c_double(SampleRate)
        rtn=self.libHandle.DO_ContWritePort(var_card, Port, BufferId, WriteCount, Iterations, fTemp0, SyncMode)
        return rtn
    
    def DO_AsyncCheck(self,var_card, Stopped, AccessCnt):
        bTemp0=c_bool(0)
        bTemp1=c_uint32(0)
        rtn=self.libHandle.DO_AsyncCheck(var_card,byref(bTemp0),byref(bTemp1))
        Stopped.clear()
        Stopped.append(bTemp0.value)
        AccessCnt.clear()
        AccessCnt.append(bTemp1.value)
        return rtn

    def DO_AsyncClear(self,var_card, AccessCnt=list()):
        bTemp=c_uint32(0)
        rtn=self.libHandle.DO_AsyncClear(var_card, byref(bTemp))
        AccessCnt.clear()
        AccessCnt.append(bTemp.value)
        return rtn
    
    def DO_AsyncReTrigNextReady(self,var_card, Ready=list(), Stopped=list(), RdyTrigCnt=list()):
        bTemp0=c_bool(0)
        bTemp1=c_bool(0)
        bTemp2=c_int16(0)
        rtn=self.libHandle.DO_AsyncReTrigNextReady(var_card, byref(bTemp0), byref(bTemp1), byref(bTemp2))
        Ready.clear()
        Stopped.clear()
        RdyTrigCnt.clear()
        Ready.append(bTemp0.value)
        Stopped.append(bTemp1.value)
        RdyTrigCnt.append(bTemp2.value)
        return rtn
    
    def DO_AsyncDblBufferMode(self,var_card, Enable):
        rtn=self.libHandle.DO_AsyncDblBufferMode(var_card, Enable)
        return rtn

    def DO_AsyncDblBufferHalfReady(self,var_card, HalfReady):
        bTemp=c_bool(0)
        rtn=self.libHandle.DO_AsyncDblBufferHalfReady(var_card, byref(bTemp))
        HalfReady.clear()
        HalfReady.append(bTemp.value)
        return rtn
    
    def DO_WritePort(self,var_card, Port, DO_Write):
        fTemp0=c_uint32(DO_Write)
        rtn=self.libHandle.DO_WritePort(var_card, Port, fTemp0)
        return rtn
    
    def DO_ReadPort(self,var_card, Port, DO_Read=list()):
        bTemp=c_uint32(0)
        rtn=self.libHandle.DO_ReadPort(var_card, Port, byref(bTemp))
        DO_Read.clear()
        DO_Read.append(bTemp.value)
        return rtn
        
    def DIO_Mode_Config(self,var_card, dio_mode):
        rtn=self.libHandle.DIO_Mode_Config(var_card, dio_mode)
        return rtn       
    
    def GPTC_Clear(self,var_card, GCtr):
        rtn=self.libHandle.GPTC_Clear(var_card, GCtr)
        return rtn
    
    def GPTC_Setup(self,var_card, GCtr, Mode, SrcCtrl, PolCtrl, LReg1_Val, LReg2_Val):
        rtn=self.libHandle.GPTC_Setup(var_card, GCtr, Mode, SrcCtrl, PolCtrl, LReg1_Val, LReg2_Val)
        return rtn
    
    def GPTC_Control(self,var_card, GCtr, ParamID, Value):
        rtn=self.libHandle.GPTC_Control(var_card, GCtr, ParamID, Value)
        return rtn
    
    def GPTC_Status(self,var_card, GCtr, STAT=list()):
        bTemp=c_uint16(0)
        rtn=self.libHandle.GPTC_Status(var_card, GCtr, byref(bTemp))
        STAT.clear()
        STAT.append(bTemp.value)
        return rtn
    
    def GPTC_Read(self,var_card, GCtr, GPTC_Val):
        bTemp=c_uint32(0)
        rtn=self.libHandle.GPTC_Read(var_card, GCtr, byref(bTemp))
        GPTC_Val.clear()
        GPTC_Val.append(bTemp.value)
        return rtn
