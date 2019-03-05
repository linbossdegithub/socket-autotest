#coding=utf8
'''
Created on 2018.10.24
@author: chenyongfa
'''
class Constant:

    ERROR = "ERROR"
    FAILED = "FAILED"
    NOAPPLY = "NOAPPLY"

    '''port'''
    UDP_HAND_LISTEN_PORT = 16600
    UDP_TERMINAL_LISTEN_PORT = 16601
    TCP_SCREEN_SERVER_PORT = 16603
    TCP_SYSSETTING_SERVER_PORT = 16605
    
    '''Packet type'''
    PACKET_RESPONSE = 0x5251  # 是指需要回应的一种包类型
    
    ''' type '''
    TYPE_VNNOX_PLAYERINFO = 0x02
    TYPE_VNNOX_BINDINFO = 0x01
    TYPE_MANUAL = 0x01
    TYPE_POLICY = 0x02
    TYPE_MODE = 0x03
    TYPE_CARE = 0x05
    TYPE_REBOOT = 0x01
    
    TYPE_VIDEO_CONTROL = 0x01
    TYPE_EDID = 0x02
    TYPE_CUSTOM_RESOLUTION = 0x10
    TYPE_CURRENT_RESOLUTION = 0x07
    TYPE_TIME_INFO = 0x00  #读取时间信息
    TYPE_SCREEN_ATTR = 0x01
    TYPE_WHAT_PLAYLIST = 0x03
    TYPE_MD5 = 0x01
    TYPE_EXISTED = 0x02
    TYPE_INSTALLED_PACKAGEINFOS = 0x01 #已安装的软件
    TYPE_FIREWARE = 0x02 #固件

    
    '''what'''
    WHAT_MONITOR = 0x21
    WHAT_SCREEN_POWER = 0x1F
    WHAT_VIDEO_CONTROL = 0x27  # 视频控制
    WHAT_SYS_ADVANCED = 0x16  # 高级设置
    WHAT_NET_TIMING = 0x32  #对时
    WHAT_TIME_ZONE = 0x10  #时间时区
    WHAT_PLAYER_BINDING = 0x20 #播放机绑定
    WHAT_SCREEN_ATTRIBUTE = 0x1B
    WHAT_PLAYLIST = 0x1E
    WHAT_SCREEN_SHOT = 0x17
    WHAT_UPLOAD_RUNNING_LOG = 0x60
    WHAT_ZIP_RUNNING_LOG = 0x59
    WHAT_GET_PATH = 0x44
    WHAT_LOG = 0x35
    WHAT_ENV_BRIGHTNESS= 0x1A
    WHAT_SCREEN_BRIGHTNESS = 0x18
    WHAT_VOLUME = 0x26  # 音量
    WHAT_UPDATE = 0x0C #升级
    WHAT_FILE = 0x02
    WHAT_VERSION = 0x01 #版本

    '''action'''
    ACTION_GET = 0x05
    ACTION_SET = 0x04
    ACTION_MODIFY = 0x01  #修改
    ACTION_START = 0x09
    ACTION_STOP = 0x0B
    ACTION_PAUSE = 0x0C
    ACTION_END = 0x0D
    ACTION_RESUME = 0x0A
    ACTION_NOTIFY = 0x0F
    ACTION_DELETE = 0x03
    ACTION_UPDATE = 0x08 #更新


    
    ''' error '''
    ERR_ACCOUNT_NOT_EXIST = 33
    ERR_SCREEN_NOT_CONFIG = 34
    ERR_NETWORK = 35
    
    '''videoMode'''
    MODE_HDMI_FIRST = 0  # HDMI优先
    MODE_MANUAL = 1   # 手动模式
    MODE_TIMING = 2  # 定时模式
    
    '''videoSource '''
    SOURCE_INSIDE = 0  # 内部视频源
    SOURCE_HDMI = 1   # HDMI
    
    ''' displayMode '''
    DISPLAY_INTERFACE_TV = 1  # TV
    
    '''SOURCE '''
    SOURCE_INSIDE = 0  # 内部视频源
    SOURCE_HDMI = 1   # HDMI
    
    
    
    