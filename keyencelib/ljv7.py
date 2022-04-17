import os.path as osp
from ctypes import *
from typing import List

import numpy as np

from keyencelib.exceptions import (CommunicationError, DllError,
                                   MeasurementError)

DLL_PATH = osp.join(osp.dirname(__file__), 'LJV7_IF.dll')


# Define.cs
class Define:
    DEVICE_ID = 0
    MAX_PROFILE_COUNT = 3200
    MEASURE_RANGE_FULL = 800


# NativeMethods.cs
class Rc:
    Ok = hex(0x0000)


class LJV7IF_MEASURE_DATA(Structure):
    _fields_ = [('byDataInfo', c_byte),
                ('byJudge', c_byte),
                ('reserve', c_byte * 2),
                ('fValue', c_float)]


class LJV7IF_PROFILE_INFO(Structure):
    _fields_ = [('byProfileCnt', c_byte),
                ('byEnvelope', c_byte),
                ('reserve', c_byte * 2),
                ('wProfDataCnt', c_short),
                ('reserve2', c_byte * 2),
                ('lXStart', c_int),
                ('lXPitch', c_int)]


class LJV7IF_PROFILE_HEADER(Structure):
    _fields_ = [('reserve', c_uint),
                ('dwTriggerCnt', c_uint),
                ('dwEncoderCnt', c_uint),
                ('reserve2', c_uint * 3)]


class LJV7IF_PROFILE_FOOTER(Structure):
    _fields_ = [('reserve', c_uint)]


class NativeMethods:
    dll = cdll.LoadLibrary(DLL_PATH)
    MeasurementDataCount = 16

    @classmethod
    def LJV7IF_Initialize(cls) -> int:
        return cls.dll.LJV7IF_Initialize()

    @classmethod
    def LJV7IF_Finalize(cls) -> int:
        return cls.dll.LJV7IF_Finalize()

    @classmethod
    def LJV7IF_UsbOpen(cls, lDeviceId: int) -> int:
        return cls.dll.LJV7IF_UsbOpen(lDeviceId)

    @classmethod
    def LJV7IF_CommClose(cls, lDeviceId: int) -> int:
        return cls.dll.LJV7IF_CommClose(lDeviceId)

    @classmethod
    def LJV7IF_GetProfileAdvance(
        cls, lDeviceId: int, pProfileInfo: 'LJV7IF_PROFILE_INFO',
        pdwProfileData: List[int], dwDataSize: c_uint,
        pMeasureData: List['LJV7IF_MEASURE_DATA']) -> int:
        return cls.dll.LJV7IF_GetProfileAdvance(
            lDeviceId, pProfileInfo, pdwProfileData, dwDataSize, pMeasureData)


# MainForm.cs
profileInfo = LJV7IF_PROFILE_INFO()
measureData = (LJV7IF_MEASURE_DATA * NativeMethods.MeasurementDataCount)()

headerSize = int(sizeof(LJV7IF_PROFILE_HEADER) / sizeof(c_int))
footerSize = int(sizeof(LJV7IF_PROFILE_FOOTER) / sizeof(c_int))

profileDataSize = Define.MAX_PROFILE_COUNT + headerSize + footerSize
receiveBuffer = (c_int * profileDataSize)()


def EstablishCommunication() -> None:
    rc = NativeMethods.LJV7IF_Initialize()
    if not CheckReturnCode(rc):
        raise DllError('Cannot initialize ljv7 dll')

    rc = NativeMethods.LJV7IF_UsbOpen(Define.DEVICE_ID)
    if not CheckReturnCode(rc):
        raise CommunicationError('Cannot connect to keyence device via USB')


def TerminateCommunication() -> None:
    rc = NativeMethods.LJV7IF_CommClose(Define.DEVICE_ID)
    if not CheckReturnCode(rc):
        raise CommunicationError('Cannot disconnect from keyence device')

    rc = NativeMethods.LJV7IF_Finalize()
    if not CheckReturnCode(rc):
        raise DllError('Cannot finalize ljv7 dll')


def GetProfileAdvance() -> np.ndarray:
    rc = NativeMethods.LJV7IF_GetProfileAdvance(
        Define.DEVICE_ID, profileInfo, receiveBuffer,
        c_uint(len(receiveBuffer) * sizeof(c_int)), measureData)
    if not CheckReturnCode(rc):
        raise MeasurementError('Cannot get profile')

    receivedArray = np.array(receiveBuffer)
    validArray = receivedArray[headerSize:headerSize+Define.MEASURE_RANGE_FULL]
    return validArray


def CheckReturnCode(rc: Rc) -> bool:
    rc = hex(rc)
    if rc == Rc.Ok:
        return True
    return False
