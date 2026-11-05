# uncompyle6 version 3.9.3
# -*- coding: utf-8 -*-
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.13.15 (tags/v3.13.15:4061bc4, Aug  5 2026, 13:05:39) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: xbxxz_helper.py
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView
import os, socket, time, binascii, struct, threading, requests, uuid, sys, json, hashlib, urllib2, configparser, base64, json, random, pkgutil, traceback
from Crypto.Hash import MD5, SHA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
from browser import BrowserDialog
import local_auth
local_auth.install()   # 本地授权层：拦截作者服务器请求，脱离 211.159.180.131（见 docs/07）
import qt_main, icon, xbxxz_pb2, game, op
local_auth.patch_game(game)   # 本地授权状态：覆写 make_self_obj（到期检查，见 docs/07 §9）
QTextCodec.setCodecForTr(QTextCodec.codecForName('utf8'))
lijichonglian = False
zidongchonglian = False
chonglianjiange = 15
xiaomi_deviceId = ''

def getCoding(strInput):
    if isinstance(strInput, unicode):
        return 'unicode'
    try:
        strInput.decode('utf8')
        return 'utf8'
    except:
        pass

    try:
        strInput.decode('gbk')
        return 'gbk'
    except:
        pass

    return


def get_string(data, start, end):
    if not data or not start or not end:
        return ''
    if data.find(start) == -1:
        return ''
    temp = data[data.find(start) + len(start):]
    if data.find(end) == -1:
        return ''
    value = temp[:temp.find(end)]
    return value


def rf(filename):
    fp = open(filename, 'rb')
    data = fp.read()
    fp.close()
    return data


def wf(filename, data):
    fp = open(filename, 'wb')
    fp.write(data)
    fp.close()
    return


def rf_lines(filename):
    fp = open(filename, 'a+')
    lines = fp.readlines()
    fp.close()
    ret = []
    for line in lines:
        ret.append(line.strip())

    return ret


def wf_lines(filename, lines):
    fp = open(filename, 'w')
    fp.write(('\n').join(lines))
    fp.close()
    return


def cfg_set(section, key, value, config_file='settings.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    config.write(open(config_file, 'w'))
    return


def cfg_get(section, key, config_file='settings.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        return config.get(section, key)
    except Exception as e:
        if key == 'zidongmenpailiangong':
            cfg_set(section, key, '2', config_file)
            return '2'
        else:
            if key == 'chonglianjiange':
                cfg_set(section, key, '15', config_file)
                return '15'
            if key == 'mijing':
                cfg_set(section, key, '0,1,2,3,7,8,9,10,96,97', config_file)
                return '0,1,2,3,7,8,9,10,96,97'
            if key == 'skill_order':
                cfg_set(section, key, '2,1,5,4,13,10,3,12', config_file)
                return '2,1,5,4,13,10,3,12'
            if key == 'shoulie_place_index':
                cfg_set(section, key, '0,0,0', config_file)
                return '0,0,0'
            if key == 'dier_shentong_order':
                cfg_set(section, key, '0,1,2', config_file)
                return '0,1,2'
            if key == 'haoganrenwu':
                cfg_set(section, key, '0,0,0,0,0,0,0,0,0', config_file)
                return '0,0,0,0,0,0,0,0,0'
            if key == 'index_haishoutansuo':
                cfg_set(section, key, '11', config_file)
                return '11'
            if key == 'index_hunyuanwudao':
                cfg_set(section, key, '1', config_file)
                return '1'
            cfg_set(section, key, '0', config_file)
            return '0'

    return


game_obj = None

def trans_utf8(tt):
    return unicode(QtCore.QString(tt).toUtf8(), 'utf-8', 'ignore').encode('utf8')


def trans_unicode(tt):
    return unicode(QtCore.QString(tt).toUtf8(), 'utf-8', 'ignore')


class XbxxzDialog(QDialog):
    step_status = {}

    def __init__(self, parent=None):
        super(XbxxzDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        game.obj_tmp = game.init_get_serversjson()
        self.ui = qt_main.Ui_Dialog()
        self.ui.setupUi(self)
        self.icon = QIcon(':icon/icon.ico')
        self.setWindowIcon(self.icon)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.show()
        self.tray_menu = QMenu(QApplication.desktop())
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show)
        self.tray_menu.addAction(self.RestoreAction)
        self.tray.setContextMenu(self.tray_menu)
        self.webdialog = WebDialog()
        self.comboBox_danyaoleixing_list = [
         None, self.ui.comboBox_danyaoleixing, self.ui.comboBox_danyaoleixing2, self.ui.comboBox_danyaoleixing3, self.ui.comboBox_danyaoleixing4, self.ui.comboBox_danyaoleixing5, self.ui.comboBox_danyaoleixing6]
        self.comboBox_danyaojibie_list = [None, self.ui.comboBox_danyaojibie, self.ui.comboBox_danyaojibie2, self.ui.comboBox_danyaojibie3, self.ui.comboBox_danyaojibie4, self.ui.comboBox_danyaojibie5, self.ui.comboBox_danyaojibie6]
        self.comboBox_danlujibie_list = [None, self.ui.comboBox_danlujibie, self.ui.comboBox_danlujibie2, self.ui.comboBox_danlujibie3, self.ui.comboBox_danlujibie4, self.ui.comboBox_danlujibie5, self.ui.comboBox_danlujibie6]
        self.server_id_list = []
        self.server_id = 0
        self.last_pingtaileixing = 0
        self.imei = 0
        self.phonenum = ''
        self.gongde = {}
        self.last_status = 0
        self.initGameParam()
        self.ui.label_tip_2.setVisible(False)
        self.ui.label_tuzi_tips_yueka.setVisible(False)
        self.ui.label_tuzi_tips_putong.setVisible(False)
        self.ui.label_tuzi_tips_shoushua.setVisible(False)
        self.ui.label_tuzi_tips_yueka.setGeometry(0, 20, 640, 640)
        self.ui.label_tuzi_tips_putong.setGeometry(0, 20, 640, 640)
        self.ui.label_tuzi_tips_shoushua.setGeometry(0, 0, 463, 697)
        self.ui.lineEdit_shuatucishu.setVisible(False)
        self.ui.pushButton_kanjineng.setVisible(False)
        self.ui.pushButton_lijichonglian.setVisible(False)
        self.ui.listWidget_shuatu.itemClicked.connect(self.listWidget_shuatu_clicked)
        self.ui.listWidget_auto_info.itemClicked.connect(self.listWidget_auto_info_clicked)
        self.ui.listWidget_skillorder.itemClicked.connect(self.skill_order_clicked)
        self.ui.pushButton_login.clicked.connect(self.loginGame)
        self.ui.pushButton_save_openid.clicked.connect(self.save_openid)
        self.ui.pushButton_lijichonglian.clicked.connect(self.lijichonglian)
        self.ui.pushButton_sendverifynum.clicked.connect(self.sendverifynum)
        self.ui.pushButton_startguaji.clicked.connect(self.startGuaji)
        self.ui.pushButton_stopguaji.clicked.connect(self.stopGuaji)
        self.ui.pushButton_starttoutu.clicked.connect(self.starttoutu)
        self.ui.pushButton_stoptoutu.clicked.connect(self.stoptoutu)
        self.ui.pushButton_longgu.clicked.connect(self.longgu)
        self.ui.pushButton_fengchi.clicked.connect(self.fengchi)
        self.ui.pushButton_xiaolingshan.clicked.connect(self.xiaolingshan)
        self.ui.pushButton_kunlunmijing.clicked.connect(self.kunlunmijing)
        self.ui.pushButton_xianshoudao.clicked.connect(self.xianshoudao)
        self.ui.pushButton_wangshengchi.clicked.connect(self.wangshengchi)
        self.ui.pushButton_modian.clicked.connect(self.modian)
        self.ui.pushButton_chakanzishenshuxing.clicked.connect(self.chakanzishenshuxing)
        self.ui.pushButton_tiaozhanwangxianlou.clicked.connect((lambda : self.tiaozhanwangxianlou(10)))
        self.ui.pushButton_tiaozhanwangxianlou_20.clicked.connect((lambda : self.tiaozhanwangxianlou(20)))
        self.ui.pushButton_tiaozhanwangxianlou_50.clicked.connect((lambda : self.tiaozhanwangxianlou(50)))
        self.ui.pushButton_tiaozhanwangxianlou_100.clicked.connect((lambda : self.tiaozhanwangxianlou(100)))
        self.ui.pushButton_tuiyan_daotu.clicked.connect(self.tuiyan_daotu)
        self.ui.pushButton_xidaotong20.clicked.connect(self.xidaotong20)
        self.ui.pushButton_xidaotong6w.clicked.connect(self.xidaotong6w)
        self.ui.pushButton_xidaotong6w_30ci.clicked.connect(self.xidaotong6w_30ci)
        self.ui.pushButton_fuzhichongzhiid.clicked.connect(self.fuzhichongzhiid)
        self.ui.pushButton_start_xuefutu.clicked.connect(self.start_xuefutu)
        self.ui.pushButton_shengji_zifu.clicked.connect(self.shengji_zifu)
        self.ui.pushButton_dajieyin.clicked.connect(self.dajieyin)
        self.ui.pushButton_jieyinhuangongde.clicked.connect(self.jieyinhuangongde)
        self.ui.pushButton_maiwangxianlouxinwu.clicked.connect(self.maiwangxianlouxinwu)
        self.ui.pushButton_songli_longgu.clicked.connect(self.songli_longgu)
        self.ui.pushButton_songli_fengchi.clicked.connect(self.songli_fengchi)
        self.ui.pushButton_songli_dijun.clicked.connect(self.songli_dijun)
        self.ui.pushButton_xidaotongutil.clicked.connect(self.xidaotongutil)
        self.ui.pushButton_qingkongrizhi.clicked.connect(self.qingkongrizhi)
        self.ui.pushButton_chakanchidan.clicked.connect(self.chakanchidan)
        self.ui.pushButton_chakandanfang.clicked.connect(self.chakandanfang)
        self.ui.pushButton_xijiezhenbaoge1.clicked.connect(self.xijiezhenbaoge1)
        self.ui.pushButton_xijiexianshufang1.clicked.connect(self.xijiexianshufang1)
        self.ui.pushButton_xijiexianshufang2.clicked.connect(self.xijiexianshufang2)
        self.ui.pushButton_yijianshoudaotong.clicked.connect(self.yijianshoudaotong)
        self.ui.pushButton_yijianshoudaotong2.clicked.connect(self.yijianshoudaotong2)
        self.ui.pushButton_yijianshoudaotong3.clicked.connect(self.yijianshoudaotong3)
        self.ui.pushButton_startliandan.clicked.connect(self.startLiandan)
        self.ui.pushButton_stopliandan.clicked.connect(self.stopLiandan)
        self.ui.pushButton_startlianqi.clicked.connect(self.startLianqi)
        self.ui.pushButton_stoplianqi.clicked.connect(self.stopLianqi)
        self.ui.pushButton_kaishitiaozhan.clicked.connect(self.startTiaozhan)
        self.ui.pushButton_tingzhitiaozhan.clicked.connect(self.stopTiaozhan)
        self.ui.pushButton_study_xinfa.clicked.connect(self.study_xinfa)
        self.ui.pushButton_study_gongjue.clicked.connect(self.study_gongjue)
        self.ui.pushButton_gongji_xingjun_11.clicked.connect(self.gongji_xingjun_11)
        self.ui.pushButton_gongji_xingjun_12.clicked.connect(self.gongji_xingjun_12)
        self.ui.pushButton_gongji_xingjun_13.clicked.connect(self.gongji_xingjun_13)
        self.ui.pushButton_gongji_xingjun_14.clicked.connect(self.gongji_xingjun_14)
        self.ui.pushButton_gongji_xingjun_15.clicked.connect(self.gongji_xingjun_15)
        self.ui.pushButton_gongji_xingjun_16.clicked.connect(self.gongji_xingjun_16)
        self.ui.pushButton_gongji_xingjun_17.clicked.connect(self.gongji_xingjun_17)
        self.ui.pushButton_gongji_xingjun_18.clicked.connect(self.gongji_xingjun_18)
        self.ui.pushButton_gongji_xingjun_19.clicked.connect(self.gongji_xingjun_19)
        self.ui.pushButton_gongji_xingjun_20.clicked.connect(self.gongji_xingjun_20)
        self.ui.pushButton_gongji_xingjun_21.clicked.connect(self.gongji_xingjun_21)
        self.ui.pushButton_gongji_xingjun_22.clicked.connect(self.gongji_xingjun_22)
        self.ui.pushButton_gongji_xingjun_23.clicked.connect(self.gongji_xingjun_23)
        self.ui.pushButton_gongji_lingmai6.clicked.connect(self.gongji_lingmai6)
        self.ui.pushButton_gongji_lingmai5.clicked.connect(self.gongji_lingmai5)
        self.ui.pushButton_gongji_lingmai4.clicked.connect(self.gongji_lingmai4)
        self.ui.pushButton_gongji_lingmai3.clicked.connect(self.gongji_lingmai3)
        self.ui.pushButton_gongji_lingmai2.clicked.connect(self.gongji_lingmai2)
        self.ui.pushButton_gongji_lingmai1.clicked.connect(self.gongji_lingmai1)
        self.ui.pushButton_gongji_tianshen11.clicked.connect(self.gongji_tianshen_11)
        self.ui.pushButton_gongji_tianshen12.clicked.connect(self.gongji_tianshen_12)
        self.ui.pushButton_gongji_tianshen13.clicked.connect(self.gongji_tianshen_13)
        self.ui.pushButton_gongji_tianshen14.clicked.connect(self.gongji_tianshen_14)
        self.ui.pushButton_gongji_tianshen15.clicked.connect(self.gongji_tianshen_15)
        self.ui.pushButton_gongji_tianshen16.clicked.connect(self.gongji_tianshen_16)
        self.ui.pushButton_gongji_tianshen17.clicked.connect(self.gongji_tianshen_17)
        self.ui.pushButton_gongji_tianshen18.clicked.connect(self.gongji_tianshen_18)
        self.ui.pushButton_gongji_tianshen19.clicked.connect(self.gongji_tianshen_19)
        self.ui.pushButton_gongji_tianshen20.clicked.connect(self.gongji_tianshen_20)
        self.ui.pushButton_addmijing.clicked.connect(self.addmijing)
        self.ui.pushButton_delmijing.clicked.connect(self.delmijing)
        self.ui.pushButton_addmap.clicked.connect(self.addmap)
        self.ui.pushButton_modifymap.clicked.connect(self.modifymap)
        self.ui.pushButton_delmap.clicked.connect(self.delmap)
        self.ui.pushButton_help_tongyong.clicked.connect(self.help_tongyong)
        self.ui.pushButton_help_shuatutoutu.clicked.connect(self.help_shuatutoutu)
        self.ui.pushButton_help_liandanlianqi.clicked.connect(self.help_liandanlianqi)
        self.ui.pushButton_help_dongfu.clicked.connect(self.help_dongfu)
        self.ui.pushButton_help_jiezhujiangli.clicked.connect(self.help_jiezhujiangli)
        self.ui.pushButton_help_chongwujineng.clicked.connect(self.help_chongwujineng)
        self.ui.pushButton_help_ditudiaoluo.clicked.connect(self.help_ditudiaoluo)
        self.ui.pushButton_help_daotong.clicked.connect(self.help_daotong)
        self.ui.pushButton_help_tongguantiaozhan.clicked.connect(self.help_tongguantiaozhan)
        self.ui.pushButton_help_gongdeche.clicked.connect(self.help_gongdeche)
        self.ui.pushButton_help_xingjunlingmai.clicked.connect(self.help_xingjunlingmai)
        self.ui.pushButton_help_zhongtianfudan.clicked.connect(self.help_zhongtianfudan)
        self.ui.pushButton_settings_on.clicked.connect(self.settings_on_clicked)
        self.ui.pushButton_settings_off.clicked.connect(self.settings_off_clicked)
        self.ui.pushButton_skill_order_up.clicked.connect(self.skill_order_up)
        self.ui.pushButton_skill_order_down.clicked.connect(self.skill_order_down)
        self.ui.pushButton_skill_order_delete.clicked.connect(self.skill_order_delete)
        self.ui.pushButton_skill_order_reset.clicked.connect(self.skill_order_reset)
        self.ui.pushButton_startshilian.clicked.connect(self.startshilian)
        self.ui.pushButton_stopshilian.clicked.connect(self.stopshilian)
        self.ui.pushButton_shilian_gongdeduihuan.clicked.connect(self.gongdeduihuanlingli)
        self.ui.pushButton_shilian_shanglingduihuan.clicked.connect(self.shanglingduihuanlingli)
        self.ui.pushButton_add_shenmo_shijian.clicked.connect(self.add_shenmo_shijian)
        self.ui.pushButton_remove_shenmo_shijian.clicked.connect(self.remove_shenmo_shijian)
        self.ui.pushButton_set_zhandouchongwu.clicked.connect(self.set_zhandouchongwu)
        self.ui.pushButton_set_luxingchongwu.clicked.connect(self.set_luxingchongwu)
        self.ui.pushButton_set_feixingchongwu.clicked.connect(self.set_feixingchongwu)
        self.ui.pushButton_set_yuhaichongwu.clicked.connect(self.set_yuhaichongwu)
        self.ui.pushButton_quxiao_zhandouchongwu.clicked.connect(self.quxiao_zhandouchongwu)
        self.ui.pushButton_quxiao_luxingchongwu.clicked.connect(self.quxiao_luxingchongwu)
        self.ui.pushButton_quxiao_feixingchongwu.clicked.connect(self.quxiao_feixingchongwu)
        self.ui.pushButton_quxiao_yuhaichongwu.clicked.connect(self.quxiao_yuhaichongwu)
        self.ui.pushButton_chuzhan.clicked.connect(self.chongwu_chuzhan)
        self.ui.pushButton_qicheng.clicked.connect(self.chongwu_qicheng)
        self.ui.pushButton_xiuxi.clicked.connect(self.chongwu_xiuxi)
        self.ui.pushButton_kanjineng.clicked.connect(self.kanjineng)
        self.ui.pushButton_jinmenpai.clicked.connect(self.jinmenpai)
        self.ui.pushButton_tuimenpai.clicked.connect(self.tuimenpai)
        self.ui.pushButton_maijineng.clicked.connect(self.maijineng)
        self.ui.pushButton_show_all.clicked.connect(self.show_all)
        self.ui.pushButton_show_hundunshoulie.clicked.connect(self.show_hundunshoulie)
        self.ui.pushButton_show_hundunshengling_fight.clicked.connect(self.show_hundunshengling_fight)
        self.ui.pushButton_show_hundunshengling_exchange.clicked.connect(self.show_hundunshengling_exchange)
        self.ui.pushButton_show_jiezhu.clicked.connect(self.show_jiezhu)
        self.ui.pushButton_show_pk.clicked.connect(self.show_pk)
        self.ui.pushButton_show_npc.clicked.connect(self.show_npc)
        self.ui.comboBox_hundunhai_shoulie_place_1.activated.connect(self.hundunhai_shoulie_place_change)
        self.ui.comboBox_hundunhai_shoulie_place_2.activated.connect(self.hundunhai_shoulie_place_change)
        self.ui.comboBox_hundunhai_shoulie_place_3.activated.connect(self.hundunhai_shoulie_place_change)
        self.ui.comboBox_dier_shentong_1.activated.connect(self.dier_shentong_change)
        self.ui.comboBox_dier_shentong_2.activated.connect(self.dier_shentong_change)
        self.ui.comboBox_dier_shentong_3.activated.connect(self.dier_shentong_change)
        self.hundunhai_button_list = [self.ui.pushButton_1, self.ui.pushButton_1, self.ui.pushButton_2, self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5, self.ui.pushButton_6, self.ui.pushButton_7, self.ui.pushButton_8, self.ui.pushButton_9, self.ui.pushButton_10, self.ui.pushButton_11, self.ui.pushButton_12, self.ui.pushButton_13, self.ui.pushButton_14, self.ui.pushButton_15, self.ui.pushButton_16, self.ui.pushButton_17, self.ui.pushButton_18, self.ui.pushButton_19, self.ui.pushButton_20, self.ui.pushButton_21, self.ui.pushButton_22, self.ui.pushButton_23, self.ui.pushButton_24, self.ui.pushButton_25, self.ui.pushButton_26, self.ui.pushButton_27, self.ui.pushButton_28, self.ui.pushButton_29, self.ui.pushButton_30, self.ui.pushButton_31, self.ui.pushButton_32, self.ui.pushButton_33, self.ui.pushButton_34, self.ui.pushButton_35, self.ui.pushButton_36, self.ui.pushButton_37, self.ui.pushButton_38, self.ui.pushButton_39, self.ui.pushButton_40, self.ui.pushButton_41, self.ui.pushButton_42, self.ui.pushButton_43, self.ui.pushButton_44, self.ui.pushButton_45, self.ui.pushButton_46, self.ui.pushButton_47, self.ui.pushButton_48, self.ui.pushButton_49, self.ui.pushButton_50, self.ui.pushButton_51, self.ui.pushButton_52, self.ui.pushButton_53, self.ui.pushButton_54, self.ui.pushButton_55, self.ui.pushButton_56, self.ui.pushButton_57, self.ui.pushButton_58, self.ui.pushButton_59, self.ui.pushButton_60, self.ui.pushButton_61, self.ui.pushButton_62, self.ui.pushButton_63, self.ui.pushButton_64, self.ui.pushButton_65, self.ui.pushButton_66, self.ui.pushButton_67, self.ui.pushButton_68, self.ui.pushButton_69, self.ui.pushButton_70, self.ui.pushButton_71, self.ui.pushButton_72, self.ui.pushButton_73, self.ui.pushButton_74, self.ui.pushButton_75, self.ui.pushButton_76, self.ui.pushButton_77, self.ui.pushButton_78, self.ui.pushButton_79, self.ui.pushButton_80, self.ui.pushButton_81, self.ui.pushButton_82, self.ui.pushButton_83, self.ui.pushButton_84, self.ui.pushButton_85, self.ui.pushButton_86, self.ui.pushButton_87, self.ui.pushButton_88, self.ui.pushButton_89, self.ui.pushButton_90, self.ui.pushButton_91, self.ui.pushButton_92, self.ui.pushButton_93, self.ui.pushButton_94, self.ui.pushButton_95, self.ui.pushButton_96, self.ui.pushButton_97, self.ui.pushButton_98, self.ui.pushButton_99, self.ui.pushButton_100, self.ui.pushButton_101, self.ui.pushButton_102, self.ui.pushButton_103, self.ui.pushButton_104, self.ui.pushButton_105, self.ui.pushButton_106, self.ui.pushButton_107, self.ui.pushButton_108, self.ui.pushButton_109, self.ui.pushButton_110, self.ui.pushButton_111, self.ui.pushButton_112, self.ui.pushButton_113, self.ui.pushButton_114, self.ui.pushButton_115, self.ui.pushButton_116, self.ui.pushButton_117, self.ui.pushButton_118, self.ui.pushButton_119, self.ui.pushButton_120, self.ui.pushButton_121, self.ui.pushButton_122, self.ui.pushButton_123, self.ui.pushButton_124, self.ui.pushButton_125, self.ui.pushButton_126, self.ui.pushButton_127, self.ui.pushButton_128, self.ui.pushButton_129, self.ui.pushButton_130, self.ui.pushButton_131, self.ui.pushButton_132, self.ui.pushButton_133, self.ui.pushButton_134, self.ui.pushButton_135, self.ui.pushButton_136, self.ui.pushButton_137, self.ui.pushButton_138, self.ui.pushButton_139, self.ui.pushButton_140, self.ui.pushButton_141, self.ui.pushButton_142, self.ui.pushButton_143, self.ui.pushButton_144, self.ui.pushButton_145, self.ui.pushButton_146, self.ui.pushButton_147, self.ui.pushButton_148, self.ui.pushButton_149, self.ui.pushButton_150, self.ui.pushButton_151, self.ui.pushButton_152, self.ui.pushButton_153, self.ui.pushButton_154, self.ui.pushButton_155, self.ui.pushButton_156, self.ui.pushButton_157, self.ui.pushButton_158, self.ui.pushButton_159, self.ui.pushButton_160, self.ui.pushButton_161, self.ui.pushButton_162, self.ui.pushButton_163, self.ui.pushButton_164, self.ui.pushButton_165, self.ui.pushButton_166, self.ui.pushButton_167, self.ui.pushButton_168, self.ui.pushButton_169, self.ui.pushButton_170, self.ui.pushButton_171, self.ui.pushButton_172, self.ui.pushButton_173, self.ui.pushButton_174, self.ui.pushButton_175, self.ui.pushButton_176, self.ui.pushButton_177, self.ui.pushButton_178, self.ui.pushButton_179, self.ui.pushButton_180, self.ui.pushButton_181, self.ui.pushButton_182, self.ui.pushButton_183, self.ui.pushButton_184, self.ui.pushButton_185, self.ui.pushButton_186, self.ui.pushButton_187, self.ui.pushButton_188, self.ui.pushButton_189, self.ui.pushButton_190, self.ui.pushButton_191, self.ui.pushButton_192, self.ui.pushButton_193, self.ui.pushButton_194, self.ui.pushButton_195, self.ui.pushButton_196, self.ui.pushButton_197, self.ui.pushButton_198, self.ui.pushButton_199, self.ui.pushButton_200, self.ui.pushButton_201, self.ui.pushButton_202, self.ui.pushButton_203, self.ui.pushButton_204, self.ui.pushButton_205, self.ui.pushButton_206, self.ui.pushButton_207, self.ui.pushButton_208, self.ui.pushButton_209, self.ui.pushButton_210, self.ui.pushButton_211, self.ui.pushButton_212, self.ui.pushButton_213, self.ui.pushButton_214, self.ui.pushButton_215, self.ui.pushButton_216, self.ui.pushButton_217, self.ui.pushButton_218, self.ui.pushButton_219, self.ui.pushButton_220, self.ui.pushButton_221, self.ui.pushButton_222, self.ui.pushButton_223, self.ui.pushButton_224, self.ui.pushButton_225, self.ui.pushButton_226, self.ui.pushButton_227, self.ui.pushButton_228, self.ui.pushButton_229, self.ui.pushButton_230, self.ui.pushButton_231, self.ui.pushButton_232, self.ui.pushButton_233, self.ui.pushButton_234, self.ui.pushButton_235, self.ui.pushButton_236, self.ui.pushButton_237, self.ui.pushButton_238, self.ui.pushButton_239, self.ui.pushButton_240, self.ui.pushButton_241, self.ui.pushButton_242, self.ui.pushButton_243, self.ui.pushButton_244, self.ui.pushButton_245, self.ui.pushButton_246, self.ui.pushButton_247, self.ui.pushButton_248, self.ui.pushButton_249, self.ui.pushButton_250, self.ui.pushButton_251, self.ui.pushButton_252, self.ui.pushButton_253, self.ui.pushButton_254, self.ui.pushButton_255, self.ui.pushButton_256, self.ui.pushButton_257, self.ui.pushButton_258, self.ui.pushButton_259, self.ui.pushButton_260, self.ui.pushButton_261, self.ui.pushButton_262, self.ui.pushButton_263, self.ui.pushButton_264, self.ui.pushButton_265, self.ui.pushButton_266, self.ui.pushButton_267, self.ui.pushButton_268, self.ui.pushButton_269, self.ui.pushButton_270, self.ui.pushButton_271, self.ui.pushButton_272, self.ui.pushButton_273, self.ui.pushButton_274, self.ui.pushButton_275, self.ui.pushButton_276, self.ui.pushButton_277, self.ui.pushButton_278, self.ui.pushButton_279, self.ui.pushButton_280, self.ui.pushButton_281, self.ui.pushButton_282, self.ui.pushButton_283, self.ui.pushButton_284, self.ui.pushButton_285, self.ui.pushButton_286, self.ui.pushButton_287, self.ui.pushButton_288, self.ui.pushButton_289, self.ui.pushButton_290, self.ui.pushButton_291, self.ui.pushButton_292, self.ui.pushButton_293, self.ui.pushButton_294, self.ui.pushButton_295, self.ui.pushButton_296, self.ui.pushButton_297, self.ui.pushButton_298, self.ui.pushButton_299, self.ui.pushButton_300, self.ui.pushButton_301, self.ui.pushButton_302, self.ui.pushButton_303, self.ui.pushButton_304, self.ui.pushButton_305, self.ui.pushButton_306, self.ui.pushButton_307, self.ui.pushButton_308, self.ui.pushButton_309, self.ui.pushButton_310, self.ui.pushButton_311, self.ui.pushButton_312, self.ui.pushButton_313, self.ui.pushButton_314, self.ui.pushButton_315, self.ui.pushButton_316, self.ui.pushButton_317, self.ui.pushButton_318, self.ui.pushButton_319, self.ui.pushButton_320, self.ui.pushButton_321, self.ui.pushButton_322, self.ui.pushButton_323, self.ui.pushButton_324, self.ui.pushButton_325, self.ui.pushButton_326, self.ui.pushButton_327, self.ui.pushButton_328, self.ui.pushButton_329, self.ui.pushButton_330, self.ui.pushButton_331, self.ui.pushButton_332, self.ui.pushButton_333, self.ui.pushButton_334, self.ui.pushButton_335, self.ui.pushButton_336, self.ui.pushButton_337, self.ui.pushButton_338, self.ui.pushButton_339, self.ui.pushButton_340, self.ui.pushButton_341, self.ui.pushButton_342, self.ui.pushButton_343, self.ui.pushButton_344, self.ui.pushButton_345, self.ui.pushButton_346, self.ui.pushButton_347, self.ui.pushButton_348, self.ui.pushButton_349, self.ui.pushButton_350, self.ui.pushButton_351, self.ui.pushButton_352, self.ui.pushButton_353, self.ui.pushButton_354, self.ui.pushButton_355, self.ui.pushButton_356, self.ui.pushButton_357, self.ui.pushButton_358, self.ui.pushButton_359, self.ui.pushButton_360, self.ui.pushButton_361, self.ui.pushButton_362, self.ui.pushButton_363, self.ui.pushButton_364, self.ui.pushButton_365, self.ui.pushButton_366, self.ui.pushButton_367, self.ui.pushButton_368, self.ui.pushButton_369, self.ui.pushButton_370, self.ui.pushButton_371, self.ui.pushButton_372, self.ui.pushButton_373, self.ui.pushButton_374, self.ui.pushButton_375, self.ui.pushButton_376, self.ui.pushButton_377, self.ui.pushButton_378]
        self.tansuo_name = [u' ', u'1|迷乱星海', u'1|紫晶湖', u'2|角木海眼', u'5|风雷谷', u'5|太金宫', u'8|北离域', 
         u'8|长寿山', u'8|戊土海眼', u'10|亶爰山', u'12|天璇域', u'12|申金海眼', u'20|亢金海眼', 
         u'20|赤火域', u'25|柜山', u'25|氐土海眼', u'25|无定峰', u'30|午火海眼', u'30|明轮域', 
         u'30|尾火海眼', u'35|尧光宫', u'35|云峰', u'40|赤龙窟', u'45|箕水海眼', u'50|乙木海眼', 
         u'50|绝空谷', u'50|碧海', u'55|祷过山', u'60|苦海', u'70|斗木海眼', u'75|玉鼎山', 
         u'80|七色山', u'80|九灵墟', u'90|酉金海眼', u'100|辰火海眼', u'110|神蚕岭', 
         u'130|血岩谷', u'140|亥水海眼', u'140|牛金海眼', u'145|令丘山', u'150|兑泽海眼', 
         u'170|太华域', u'180|千幻域', u'200|坤地海眼', u'200|黑炎海', u'200|卯土海眼', 
         u'220|女土海眼', u'220|太华宫', u'230|寅土海眼', u'240|无光山', u'250|巽风海眼', 
         u'260|子水海眼', u'260|广寒域', u'280|天吴海', u'280|皋涂山', u'290|百香山', 
         u'300|艮山海眼', u'300|绝凶谷', u'310|室火海眼', u'330|寿华域', u'330|邽山', 
         u'340|璧水海眼', u'350|震雷海眼', u'350|辰金海眼', u'350|奇荒域', u'360|神铆峰', 
         u'360|奎木海眼', u'370|巳火海眼', u'390|厄目宫', u'390|幻沙海', u'400|寅木海眼', 
         u'400|未土海眼', u'410|明光殿', u'420|元极域', u'420|神梦谷', u'420|申木海眼', 
         u'430|幽元宫', u'450|离火海眼', u'450|三圣宫', u'460|焱岩域', u'470|娄金海眼', 
         u'470|胃土海眼', u'480|酉火海眼', u'490|羽寰域', u'500|乾阳海眼', u'510|寒冬宫', 
         u'510|雷鸣山', u'520|觜火海眼', u'530|无望峰', u'540|戌水海眼', u'540|参水海眼', 
         u'550|乾水海眼', u'550|乾洋', u'560|玉泉宫', u'570|罗天域', u'570|子土海眼', 
         u'580|千变峰', u'590|翼望山', u'600|离木海眼', u'600|鬼金海眼', u'600|金焰山', 
         u'600|英鞮山', u'610|不基山', u'630|紫元域', u'640|亥木海眼', u'650|泽风海眼', 
         u'650|凤宣湖', u'650|巳水海眼', u'660|化莲池', u'660|翼火海眼', u'680|血雨谷', 
         u'690|真龙池', u'690|崦嵫山', u'700|坤火海眼', u'700|星台宫', u'710|章尾山', 
         u'710|青霜域', u'720|邪冥域', u'720|峰渊', u'720|青岩域', u'750|坎水海眼', 
         u'750|金鼎域', u'750|戌火海眼', u'780|轸水海眼', u'800|风雷海眼', u'850|辰土海眼', 
         u'900|乾天海眼', u'970|云浪谷', u'980|无名宫', u'990|青溟海眼', u'1000|灵幻海眼', 
         u'1010|青空海眼', u'1015|灵象海眼', u'1020|银月宫', u'1025|九珑域', u'1030|天尽崖', 
         u'1040|画宫', u'1050|灵风海眼', u'1055|幻莺宫', u'1065|火天宫', u'1075|荒神域', 
         u'1080|焱麟宫', u'1085|七剑峰', u'1090|碧波宫', u'1095|灵意海眼', u'1100|匡御海眼', 
         u'1110|银光域', u'1110|灵极海眼', u'1120|雷仙宫', u'1130|青涛海', u'1140|白月山', 
         u'1145|青玄海眼', u'1150|空生海眼', u'1160|青安海眼', u'1175|梵风宫', u'1180|闇云域', 
         u'1190|青和海眼', u'1195|青元海眼', u'1200|真所海眼', u'1205|灵清海眼', u'1215|独羽宫', 
         u'1220|九浊宫', u'1225|真火域', u'1240|灵英海眼', u'1250|玄图海眼', u'1260|霓霞山', 
         u'1260|巨焰宫', u'1270|光元宫', u'1275|玄溪域', u'1280|青意海眼', u'1285|飞霜域', 
         u'1300|灵文海眼', u'1305|洗剑山', u'1320|冰牙宫', u'1325|灵真海眼', u'1330|天人宫', 
         u'1335|闇驭宫', u'1345|青根域', u'1350|青成海眼', u'1350|精极海眼', u'1355|赤月崖', 
         u'1370|龙目宫', u'1390|金灯山', u'1390|青云海眼', u'1400|灵玄海眼', u'1400|神表海眼', 
         u'1400|易道域', u'1405|锦绣宫', u'1415|止虚山', u'1420|梵空宫', u'1435|白云宫', 
         u'1450|华阳海眼', u'1455|灵天海眼', u'1460|炎金宫', u'1465|易化海眼', u'1470|丹元海眼', 
         u'1475|赤追宫', u'1485|弥天域', u'1500|雪苍山', u'1500|明灵海眼', u'1520|碧藤宫', 
         u'1530|炎古宫', u'1530|青兰域', u'1535|邪冥宫', u'1540|碧元海眼', u'1540|易元海眼', 
         u'1545|玉龙山', u'1550|易玄海眼', u'1550|灵奥海眼', u'1565|初元海眼', u'1595|溟水域', 
         u'1600|易生海眼', u'1600|古雷海', u'1600|百咏海眼', u'1605|飘絮宫', u'1610|妙元海眼', 
         u'1610|烟罗域', u'1615|东元域', u'1630|九印山', u'1650|灵鬼宫', u'1650|天长海眼', 
         u'1665|化元海眼', u'1670|斩情宫', u'1675|雨霖域', u'1680|易风海眼', u'1680|星风宫', 
         u'1700|大有海眼', u'1715|凌天峰', u'1725|易浩海眼', u'1730|九暗宫', u'1735|清元海眼', 
         u'1740|青叶域', u'1745|玄雾海', u'1750|十方海眼', u'1750|苍元海眼', u'1750|郁秀海眼', 
         u'1760|易极海眼', u'1790|奈何宫', u'1800|福禄宫', u'1805|剑临域', u'1810|北龙宫', 
         u'1810|易宏海眼', u'1820|幽元宫', u'1825|浩元海眼', u'1845|易阳海眼', u'1850|神极海眼', 
         u'1855|弥阳域', u'1860|九重宫', u'1865|九阴宫', u'1870|天元海眼', u'1875|天隐域', 
         u'1880|宝花谷', u'1900|承天海眼', u'1980|寿元宫', u'1990|灵交海眼', u'1970|苍空岛', 
         u'2025|花雨谷', u'2050|至阳海眼', u'2010|冰火谷', u'2000|百凶山', u'2020|千山峰', 
         u'2030|天突海眼', u'2090|玄木峰', u'2115|沧澜域', u'2075|宏玄海眼', u'2050|章莪山', 
         u'2040|天山海', u'2065|宏元海眼', u'2100|天府海眼', u'2095|鹿吴山', u'2155|宏意海眼', 
         u'2180|杻阳山', u'2150|紫宫海眼', u'2120|黑渊', u'2055|紫雷域', u'2110|玉堂海眼', 
         u'2130|金池', u'2150|宏成海眼', u'2160|青洪域', u'2220|九金山', u'2245|玄铜谷', 
         u'2215|关元海眼', u'2190|青水谷', u'2120|云天宫', u'2180|陆玄域', u'2200|上星海眼', 
         u'2215|玉玄域', u'2225|天曲山', u'2285|宏清海眼', u'2250|五灵海眼', u'2280|天虫宫', 
         u'2260|炎魂域', u'2190|宏真海眼', u'2250|宏苍海眼', u'2260|侠白海眼', u'2280|流波山', 
         u'2290|宏丹海眼', u'2350|大赫海眼', u'2375|灵彩山', u'2340|宏冲海眼', u'2330|商曲海眼', 
         u'2260|石湖', u'2350|天冲海眼', u'2325|太神域', u'2340|九荒山', u'2300|神门海眼', 
         u'2415|橙海', u'2440|气冲海眼', u'2405|阴风谷', u'2400|天鼎海眼', u'2330|神雷墟', 
         u'2390|碧元海', u'2390|少商海眼', u'2405|金雷山', u'2420|玄阳域', u'2400|久灵海眼', 
         u'2450|中极海眼', u'2505|星宏域', u'2470|都载山', u'2470|无光宫', u'2460|南翼泽', 
         u'2455|截脉峰', u'2470|通谷海眼', u'2485|久运海眼', u'2545|久承海眼', u'2550|天武海眼', 
         u'2535|云门海眼', u'2540|神风山', u'2500|天光海眼', u'2530|战穹域', u'2520|风灵殿', 
         u'2535|赤北山', u'2550|灵凶谷', u'2610|青曜域', u'2635|天池海眼', u'2600|北岳峰', 
         u'2610|苍焱峰', u'2540|曲泽海眼', u'2600|玉元宫', u'2600|紫云海眼', u'2600|血涛域', 
         u'2615|火灵山', u'2650|七玄海眼', u'2700|玉光山', u'2665|金光殿', u'2700|天华海眼', 
         u'2610|葬水山', u'2670|久极海眼', u'2650|中冲海眼', u'2665|石海', u'2680|久华海眼', 
         u'2780|七彩宫', u'2765|久清海眼', u'2730|少府海眼', u'2750|灵缈园', u'2680|玄木域', 
         u'2740|咽火山', u'2715|幻雪峰', u'2730|天残山', u'2750|云庭海眼', u'2845|天泉海眼', 
         u'2850|天机海眼', u'2795|金钟谷', u'2820|鱼龙宫', u'2750|久辰海眼', u'2810|折桂宫', 
         u'2800|灵业海眼', u'2795|久合海眼', u'2810|渡业谷', u'2890|南炎山', u'2895|清风域', 
         u'2860|久元海眼', u'2890|聚宝宫', u'2820|烈阳谷', u'2880|少海海眼', u'2845|少咸山', 
         u'2860|血焱域', u'2875|极泉海眼', u'2900|真皇海眼']
        for xid in range(1, len(self.tansuo_name)):
            self.hundunhai_button_list[xid].installEventFilter(self)
            self.ui.comboBox_hundunhai_cur_tansuo.addItem(self.tansuo_name[xid])
            self.ui.comboBox_hundunhai_next_tansuo.addItem(self.tansuo_name[xid])

        self.ui.pushButton_1.clicked.connect((lambda : self.hundunhai_tansuo(1)))
        self.ui.pushButton_2.clicked.connect((lambda : self.hundunhai_tansuo(2)))
        self.ui.pushButton_3.clicked.connect((lambda : self.hundunhai_tansuo(3)))
        self.ui.pushButton_4.clicked.connect((lambda : self.hundunhai_tansuo(4)))
        self.ui.pushButton_5.clicked.connect((lambda : self.hundunhai_tansuo(5)))
        self.ui.pushButton_6.clicked.connect((lambda : self.hundunhai_tansuo(6)))
        self.ui.pushButton_7.clicked.connect((lambda : self.hundunhai_tansuo(7)))
        self.ui.pushButton_8.clicked.connect((lambda : self.hundunhai_tansuo(8)))
        self.ui.pushButton_9.clicked.connect((lambda : self.hundunhai_tansuo(9)))
        self.ui.pushButton_10.clicked.connect((lambda : self.hundunhai_tansuo(10)))
        self.ui.pushButton_11.clicked.connect((lambda : self.hundunhai_tansuo(11)))
        self.ui.pushButton_12.clicked.connect((lambda : self.hundunhai_tansuo(12)))
        self.ui.pushButton_13.clicked.connect((lambda : self.hundunhai_tansuo(13)))
        self.ui.pushButton_14.clicked.connect((lambda : self.hundunhai_tansuo(14)))
        self.ui.pushButton_15.clicked.connect((lambda : self.hundunhai_tansuo(15)))
        self.ui.pushButton_16.clicked.connect((lambda : self.hundunhai_tansuo(16)))
        self.ui.pushButton_17.clicked.connect((lambda : self.hundunhai_tansuo(17)))
        self.ui.pushButton_18.clicked.connect((lambda : self.hundunhai_tansuo(18)))
        self.ui.pushButton_19.clicked.connect((lambda : self.hundunhai_tansuo(19)))
        self.ui.pushButton_20.clicked.connect((lambda : self.hundunhai_tansuo(20)))
        self.ui.pushButton_21.clicked.connect((lambda : self.hundunhai_tansuo(21)))
        self.ui.pushButton_22.clicked.connect((lambda : self.hundunhai_tansuo(22)))
        self.ui.pushButton_23.clicked.connect((lambda : self.hundunhai_tansuo(23)))
        self.ui.pushButton_24.clicked.connect((lambda : self.hundunhai_tansuo(24)))
        self.ui.pushButton_25.clicked.connect((lambda : self.hundunhai_tansuo(25)))
        self.ui.pushButton_26.clicked.connect((lambda : self.hundunhai_tansuo(26)))
        self.ui.pushButton_27.clicked.connect((lambda : self.hundunhai_tansuo(27)))
        self.ui.pushButton_28.clicked.connect((lambda : self.hundunhai_tansuo(28)))
        self.ui.pushButton_29.clicked.connect((lambda : self.hundunhai_tansuo(29)))
        self.ui.pushButton_30.clicked.connect((lambda : self.hundunhai_tansuo(30)))
        self.ui.pushButton_31.clicked.connect((lambda : self.hundunhai_tansuo(31)))
        self.ui.pushButton_32.clicked.connect((lambda : self.hundunhai_tansuo(32)))
        self.ui.pushButton_33.clicked.connect((lambda : self.hundunhai_tansuo(33)))
        self.ui.pushButton_34.clicked.connect((lambda : self.hundunhai_tansuo(34)))
        self.ui.pushButton_35.clicked.connect((lambda : self.hundunhai_tansuo(35)))
        self.ui.pushButton_36.clicked.connect((lambda : self.hundunhai_tansuo(36)))
        self.ui.pushButton_37.clicked.connect((lambda : self.hundunhai_tansuo(37)))
        self.ui.pushButton_38.clicked.connect((lambda : self.hundunhai_tansuo(38)))
        self.ui.pushButton_39.clicked.connect((lambda : self.hundunhai_tansuo(39)))
        self.ui.pushButton_40.clicked.connect((lambda : self.hundunhai_tansuo(40)))
        self.ui.pushButton_41.clicked.connect((lambda : self.hundunhai_tansuo(41)))
        self.ui.pushButton_42.clicked.connect((lambda : self.hundunhai_tansuo(42)))
        self.ui.pushButton_43.clicked.connect((lambda : self.hundunhai_tansuo(43)))
        self.ui.pushButton_44.clicked.connect((lambda : self.hundunhai_tansuo(44)))
        self.ui.pushButton_45.clicked.connect((lambda : self.hundunhai_tansuo(45)))
        self.ui.pushButton_46.clicked.connect((lambda : self.hundunhai_tansuo(46)))
        self.ui.pushButton_47.clicked.connect((lambda : self.hundunhai_tansuo(47)))
        self.ui.pushButton_48.clicked.connect((lambda : self.hundunhai_tansuo(48)))
        self.ui.pushButton_49.clicked.connect((lambda : self.hundunhai_tansuo(49)))
        self.ui.pushButton_50.clicked.connect((lambda : self.hundunhai_tansuo(50)))
        self.ui.pushButton_51.clicked.connect((lambda : self.hundunhai_tansuo(51)))
        self.ui.pushButton_52.clicked.connect((lambda : self.hundunhai_tansuo(52)))
        self.ui.pushButton_53.clicked.connect((lambda : self.hundunhai_tansuo(53)))
        self.ui.pushButton_54.clicked.connect((lambda : self.hundunhai_tansuo(54)))
        self.ui.pushButton_55.clicked.connect((lambda : self.hundunhai_tansuo(55)))
        self.ui.pushButton_56.clicked.connect((lambda : self.hundunhai_tansuo(56)))
        self.ui.pushButton_57.clicked.connect((lambda : self.hundunhai_tansuo(57)))
        self.ui.pushButton_58.clicked.connect((lambda : self.hundunhai_tansuo(58)))
        self.ui.pushButton_59.clicked.connect((lambda : self.hundunhai_tansuo(59)))
        self.ui.pushButton_60.clicked.connect((lambda : self.hundunhai_tansuo(60)))
        self.ui.pushButton_61.clicked.connect((lambda : self.hundunhai_tansuo(61)))
        self.ui.pushButton_62.clicked.connect((lambda : self.hundunhai_tansuo(62)))
        self.ui.pushButton_63.clicked.connect((lambda : self.hundunhai_tansuo(63)))
        self.ui.pushButton_64.clicked.connect((lambda : self.hundunhai_tansuo(64)))
        self.ui.pushButton_65.clicked.connect((lambda : self.hundunhai_tansuo(65)))
        self.ui.pushButton_66.clicked.connect((lambda : self.hundunhai_tansuo(66)))
        self.ui.pushButton_67.clicked.connect((lambda : self.hundunhai_tansuo(67)))
        self.ui.pushButton_68.clicked.connect((lambda : self.hundunhai_tansuo(68)))
        self.ui.pushButton_69.clicked.connect((lambda : self.hundunhai_tansuo(69)))
        self.ui.pushButton_70.clicked.connect((lambda : self.hundunhai_tansuo(70)))
        self.ui.pushButton_71.clicked.connect((lambda : self.hundunhai_tansuo(71)))
        self.ui.pushButton_72.clicked.connect((lambda : self.hundunhai_tansuo(72)))
        self.ui.pushButton_73.clicked.connect((lambda : self.hundunhai_tansuo(73)))
        self.ui.pushButton_74.clicked.connect((lambda : self.hundunhai_tansuo(74)))
        self.ui.pushButton_75.clicked.connect((lambda : self.hundunhai_tansuo(75)))
        self.ui.pushButton_76.clicked.connect((lambda : self.hundunhai_tansuo(76)))
        self.ui.pushButton_77.clicked.connect((lambda : self.hundunhai_tansuo(77)))
        self.ui.pushButton_78.clicked.connect((lambda : self.hundunhai_tansuo(78)))
        self.ui.pushButton_79.clicked.connect((lambda : self.hundunhai_tansuo(79)))
        self.ui.pushButton_80.clicked.connect((lambda : self.hundunhai_tansuo(80)))
        self.ui.pushButton_81.clicked.connect((lambda : self.hundunhai_tansuo(81)))
        self.ui.pushButton_82.clicked.connect((lambda : self.hundunhai_tansuo(82)))
        self.ui.pushButton_83.clicked.connect((lambda : self.hundunhai_tansuo(83)))
        self.ui.pushButton_84.clicked.connect((lambda : self.hundunhai_tansuo(84)))
        self.ui.pushButton_85.clicked.connect((lambda : self.hundunhai_tansuo(85)))
        self.ui.pushButton_86.clicked.connect((lambda : self.hundunhai_tansuo(86)))
        self.ui.pushButton_87.clicked.connect((lambda : self.hundunhai_tansuo(87)))
        self.ui.pushButton_88.clicked.connect((lambda : self.hundunhai_tansuo(88)))
        self.ui.pushButton_89.clicked.connect((lambda : self.hundunhai_tansuo(89)))
        self.ui.pushButton_90.clicked.connect((lambda : self.hundunhai_tansuo(90)))
        self.ui.pushButton_91.clicked.connect((lambda : self.hundunhai_tansuo(91)))
        self.ui.pushButton_92.clicked.connect((lambda : self.hundunhai_tansuo(92)))
        self.ui.pushButton_93.clicked.connect((lambda : self.hundunhai_tansuo(93)))
        self.ui.pushButton_94.clicked.connect((lambda : self.hundunhai_tansuo(94)))
        self.ui.pushButton_95.clicked.connect((lambda : self.hundunhai_tansuo(95)))
        self.ui.pushButton_96.clicked.connect((lambda : self.hundunhai_tansuo(96)))
        self.ui.pushButton_97.clicked.connect((lambda : self.hundunhai_tansuo(97)))
        self.ui.pushButton_98.clicked.connect((lambda : self.hundunhai_tansuo(98)))
        self.ui.pushButton_99.clicked.connect((lambda : self.hundunhai_tansuo(99)))
        self.ui.pushButton_100.clicked.connect((lambda : self.hundunhai_tansuo(100)))
        self.ui.pushButton_101.clicked.connect((lambda : self.hundunhai_tansuo(101)))
        self.ui.pushButton_102.clicked.connect((lambda : self.hundunhai_tansuo(102)))
        self.ui.pushButton_103.clicked.connect((lambda : self.hundunhai_tansuo(103)))
        self.ui.pushButton_104.clicked.connect((lambda : self.hundunhai_tansuo(104)))
        self.ui.pushButton_105.clicked.connect((lambda : self.hundunhai_tansuo(105)))
        self.ui.pushButton_106.clicked.connect((lambda : self.hundunhai_tansuo(106)))
        self.ui.pushButton_107.clicked.connect((lambda : self.hundunhai_tansuo(107)))
        self.ui.pushButton_108.clicked.connect((lambda : self.hundunhai_tansuo(108)))
        self.ui.pushButton_109.clicked.connect((lambda : self.hundunhai_tansuo(109)))
        self.ui.pushButton_110.clicked.connect((lambda : self.hundunhai_tansuo(110)))
        self.ui.pushButton_111.clicked.connect((lambda : self.hundunhai_tansuo(111)))
        self.ui.pushButton_112.clicked.connect((lambda : self.hundunhai_tansuo(112)))
        self.ui.pushButton_113.clicked.connect((lambda : self.hundunhai_tansuo(113)))
        self.ui.pushButton_114.clicked.connect((lambda : self.hundunhai_tansuo(114)))
        self.ui.pushButton_115.clicked.connect((lambda : self.hundunhai_tansuo(115)))
        self.ui.pushButton_116.clicked.connect((lambda : self.hundunhai_tansuo(116)))
        self.ui.pushButton_117.clicked.connect((lambda : self.hundunhai_tansuo(117)))
        self.ui.pushButton_118.clicked.connect((lambda : self.hundunhai_tansuo(118)))
        self.ui.pushButton_119.clicked.connect((lambda : self.hundunhai_tansuo(119)))
        self.ui.pushButton_120.clicked.connect((lambda : self.hundunhai_tansuo(120)))
        self.ui.pushButton_121.clicked.connect((lambda : self.hundunhai_tansuo(121)))
        self.ui.pushButton_122.clicked.connect((lambda : self.hundunhai_tansuo(122)))
        self.ui.pushButton_123.clicked.connect((lambda : self.hundunhai_tansuo(123)))
        self.ui.pushButton_124.clicked.connect((lambda : self.hundunhai_tansuo(124)))
        self.ui.pushButton_125.clicked.connect((lambda : self.hundunhai_tansuo(125)))
        self.ui.pushButton_126.clicked.connect((lambda : self.hundunhai_tansuo(126)))
        self.ui.pushButton_127.clicked.connect((lambda : self.hundunhai_tansuo(127)))
        self.ui.pushButton_128.clicked.connect((lambda : self.hundunhai_tansuo(128)))
        self.ui.pushButton_129.clicked.connect((lambda : self.hundunhai_tansuo(129)))
        self.ui.pushButton_130.clicked.connect((lambda : self.hundunhai_tansuo(130)))
        self.ui.pushButton_131.clicked.connect((lambda : self.hundunhai_tansuo(131)))
        self.ui.pushButton_132.clicked.connect((lambda : self.hundunhai_tansuo(132)))
        self.ui.pushButton_133.clicked.connect((lambda : self.hundunhai_tansuo(133)))
        self.ui.pushButton_134.clicked.connect((lambda : self.hundunhai_tansuo(134)))
        self.ui.pushButton_135.clicked.connect((lambda : self.hundunhai_tansuo(135)))
        self.ui.pushButton_136.clicked.connect((lambda : self.hundunhai_tansuo(136)))
        self.ui.pushButton_137.clicked.connect((lambda : self.hundunhai_tansuo(137)))
        self.ui.pushButton_138.clicked.connect((lambda : self.hundunhai_tansuo(138)))
        self.ui.pushButton_139.clicked.connect((lambda : self.hundunhai_tansuo(139)))
        self.ui.pushButton_140.clicked.connect((lambda : self.hundunhai_tansuo(140)))
        self.ui.pushButton_141.clicked.connect((lambda : self.hundunhai_tansuo(141)))
        self.ui.pushButton_142.clicked.connect((lambda : self.hundunhai_tansuo(142)))
        self.ui.pushButton_143.clicked.connect((lambda : self.hundunhai_tansuo(143)))
        self.ui.pushButton_144.clicked.connect((lambda : self.hundunhai_tansuo(144)))
        self.ui.pushButton_145.clicked.connect((lambda : self.hundunhai_tansuo(145)))
        self.ui.pushButton_146.clicked.connect((lambda : self.hundunhai_tansuo(146)))
        self.ui.pushButton_147.clicked.connect((lambda : self.hundunhai_tansuo(147)))
        self.ui.pushButton_148.clicked.connect((lambda : self.hundunhai_tansuo(148)))
        self.ui.pushButton_149.clicked.connect((lambda : self.hundunhai_tansuo(149)))
        self.ui.pushButton_150.clicked.connect((lambda : self.hundunhai_tansuo(150)))
        self.ui.pushButton_151.clicked.connect((lambda : self.hundunhai_tansuo(151)))
        self.ui.pushButton_152.clicked.connect((lambda : self.hundunhai_tansuo(152)))
        self.ui.pushButton_153.clicked.connect((lambda : self.hundunhai_tansuo(153)))
        self.ui.pushButton_154.clicked.connect((lambda : self.hundunhai_tansuo(154)))
        self.ui.pushButton_155.clicked.connect((lambda : self.hundunhai_tansuo(155)))
        self.ui.pushButton_156.clicked.connect((lambda : self.hundunhai_tansuo(156)))
        self.ui.pushButton_157.clicked.connect((lambda : self.hundunhai_tansuo(157)))
        self.ui.pushButton_158.clicked.connect((lambda : self.hundunhai_tansuo(158)))
        self.ui.pushButton_159.clicked.connect((lambda : self.hundunhai_tansuo(159)))
        self.ui.pushButton_160.clicked.connect((lambda : self.hundunhai_tansuo(160)))
        self.ui.pushButton_161.clicked.connect((lambda : self.hundunhai_tansuo(161)))
        self.ui.pushButton_162.clicked.connect((lambda : self.hundunhai_tansuo(162)))
        self.ui.pushButton_163.clicked.connect((lambda : self.hundunhai_tansuo(163)))
        self.ui.pushButton_164.clicked.connect((lambda : self.hundunhai_tansuo(164)))
        self.ui.pushButton_165.clicked.connect((lambda : self.hundunhai_tansuo(165)))
        self.ui.pushButton_166.clicked.connect((lambda : self.hundunhai_tansuo(166)))
        self.ui.pushButton_167.clicked.connect((lambda : self.hundunhai_tansuo(167)))
        self.ui.pushButton_168.clicked.connect((lambda : self.hundunhai_tansuo(168)))
        self.ui.pushButton_169.clicked.connect((lambda : self.hundunhai_tansuo(169)))
        self.ui.pushButton_170.clicked.connect((lambda : self.hundunhai_tansuo(170)))
        self.ui.pushButton_171.clicked.connect((lambda : self.hundunhai_tansuo(171)))
        self.ui.pushButton_172.clicked.connect((lambda : self.hundunhai_tansuo(172)))
        self.ui.pushButton_173.clicked.connect((lambda : self.hundunhai_tansuo(173)))
        self.ui.pushButton_174.clicked.connect((lambda : self.hundunhai_tansuo(174)))
        self.ui.pushButton_175.clicked.connect((lambda : self.hundunhai_tansuo(175)))
        self.ui.pushButton_176.clicked.connect((lambda : self.hundunhai_tansuo(176)))
        self.ui.pushButton_177.clicked.connect((lambda : self.hundunhai_tansuo(177)))
        self.ui.pushButton_178.clicked.connect((lambda : self.hundunhai_tansuo(178)))
        self.ui.pushButton_179.clicked.connect((lambda : self.hundunhai_tansuo(179)))
        self.ui.pushButton_180.clicked.connect((lambda : self.hundunhai_tansuo(180)))
        self.ui.pushButton_181.clicked.connect((lambda : self.hundunhai_tansuo(181)))
        self.ui.pushButton_182.clicked.connect((lambda : self.hundunhai_tansuo(182)))
        self.ui.pushButton_183.clicked.connect((lambda : self.hundunhai_tansuo(183)))
        self.ui.pushButton_184.clicked.connect((lambda : self.hundunhai_tansuo(184)))
        self.ui.pushButton_185.clicked.connect((lambda : self.hundunhai_tansuo(185)))
        self.ui.pushButton_186.clicked.connect((lambda : self.hundunhai_tansuo(186)))
        self.ui.pushButton_187.clicked.connect((lambda : self.hundunhai_tansuo(187)))
        self.ui.pushButton_188.clicked.connect((lambda : self.hundunhai_tansuo(188)))
        self.ui.pushButton_189.clicked.connect((lambda : self.hundunhai_tansuo(189)))
        self.ui.pushButton_190.clicked.connect((lambda : self.hundunhai_tansuo(190)))
        self.ui.pushButton_191.clicked.connect((lambda : self.hundunhai_tansuo(191)))
        self.ui.pushButton_192.clicked.connect((lambda : self.hundunhai_tansuo(192)))
        self.ui.pushButton_193.clicked.connect((lambda : self.hundunhai_tansuo(193)))
        self.ui.pushButton_194.clicked.connect((lambda : self.hundunhai_tansuo(194)))
        self.ui.pushButton_195.clicked.connect((lambda : self.hundunhai_tansuo(195)))
        self.ui.pushButton_196.clicked.connect((lambda : self.hundunhai_tansuo(196)))
        self.ui.pushButton_197.clicked.connect((lambda : self.hundunhai_tansuo(197)))
        self.ui.pushButton_198.clicked.connect((lambda : self.hundunhai_tansuo(198)))
        self.ui.pushButton_199.clicked.connect((lambda : self.hundunhai_tansuo(199)))
        self.ui.pushButton_200.clicked.connect((lambda : self.hundunhai_tansuo(200)))
        self.ui.pushButton_201.clicked.connect((lambda : self.hundunhai_tansuo(201)))
        self.ui.pushButton_202.clicked.connect((lambda : self.hundunhai_tansuo(202)))
        self.ui.pushButton_203.clicked.connect((lambda : self.hundunhai_tansuo(203)))
        self.ui.pushButton_204.clicked.connect((lambda : self.hundunhai_tansuo(204)))
        self.ui.pushButton_205.clicked.connect((lambda : self.hundunhai_tansuo(205)))
        self.ui.pushButton_206.clicked.connect((lambda : self.hundunhai_tansuo(206)))
        self.ui.pushButton_207.clicked.connect((lambda : self.hundunhai_tansuo(207)))
        self.ui.pushButton_208.clicked.connect((lambda : self.hundunhai_tansuo(208)))
        self.ui.pushButton_209.clicked.connect((lambda : self.hundunhai_tansuo(209)))
        self.ui.pushButton_210.clicked.connect((lambda : self.hundunhai_tansuo(210)))
        self.ui.pushButton_211.clicked.connect((lambda : self.hundunhai_tansuo(211)))
        self.ui.pushButton_212.clicked.connect((lambda : self.hundunhai_tansuo(212)))
        self.ui.pushButton_213.clicked.connect((lambda : self.hundunhai_tansuo(213)))
        self.ui.pushButton_214.clicked.connect((lambda : self.hundunhai_tansuo(214)))
        self.ui.pushButton_215.clicked.connect((lambda : self.hundunhai_tansuo(215)))
        self.ui.pushButton_216.clicked.connect((lambda : self.hundunhai_tansuo(216)))
        self.ui.pushButton_217.clicked.connect((lambda : self.hundunhai_tansuo(217)))
        self.ui.pushButton_218.clicked.connect((lambda : self.hundunhai_tansuo(218)))
        self.ui.pushButton_219.clicked.connect((lambda : self.hundunhai_tansuo(219)))
        self.ui.pushButton_220.clicked.connect((lambda : self.hundunhai_tansuo(220)))
        self.ui.pushButton_221.clicked.connect((lambda : self.hundunhai_tansuo(221)))
        self.ui.pushButton_222.clicked.connect((lambda : self.hundunhai_tansuo(222)))
        self.ui.pushButton_223.clicked.connect((lambda : self.hundunhai_tansuo(223)))
        self.ui.pushButton_224.clicked.connect((lambda : self.hundunhai_tansuo(224)))
        self.ui.pushButton_225.clicked.connect((lambda : self.hundunhai_tansuo(225)))
        self.ui.pushButton_226.clicked.connect((lambda : self.hundunhai_tansuo(226)))
        self.ui.pushButton_227.clicked.connect((lambda : self.hundunhai_tansuo(227)))
        self.ui.pushButton_228.clicked.connect((lambda : self.hundunhai_tansuo(228)))
        self.ui.pushButton_229.clicked.connect((lambda : self.hundunhai_tansuo(229)))
        self.ui.pushButton_230.clicked.connect((lambda : self.hundunhai_tansuo(230)))
        self.ui.pushButton_231.clicked.connect((lambda : self.hundunhai_tansuo(231)))
        self.ui.pushButton_232.clicked.connect((lambda : self.hundunhai_tansuo(232)))
        self.ui.pushButton_233.clicked.connect((lambda : self.hundunhai_tansuo(233)))
        self.ui.pushButton_234.clicked.connect((lambda : self.hundunhai_tansuo(234)))
        self.ui.pushButton_235.clicked.connect((lambda : self.hundunhai_tansuo(235)))
        self.ui.pushButton_236.clicked.connect((lambda : self.hundunhai_tansuo(236)))
        self.ui.pushButton_237.clicked.connect((lambda : self.hundunhai_tansuo(237)))
        self.ui.pushButton_238.clicked.connect((lambda : self.hundunhai_tansuo(238)))
        self.ui.pushButton_239.clicked.connect((lambda : self.hundunhai_tansuo(239)))
        self.ui.pushButton_240.clicked.connect((lambda : self.hundunhai_tansuo(240)))
        self.ui.pushButton_241.clicked.connect((lambda : self.hundunhai_tansuo(241)))
        self.ui.pushButton_242.clicked.connect((lambda : self.hundunhai_tansuo(242)))
        self.ui.pushButton_243.clicked.connect((lambda : self.hundunhai_tansuo(243)))
        self.ui.pushButton_244.clicked.connect((lambda : self.hundunhai_tansuo(244)))
        self.ui.pushButton_245.clicked.connect((lambda : self.hundunhai_tansuo(245)))
        self.ui.pushButton_246.clicked.connect((lambda : self.hundunhai_tansuo(246)))
        self.ui.pushButton_247.clicked.connect((lambda : self.hundunhai_tansuo(247)))
        self.ui.pushButton_248.clicked.connect((lambda : self.hundunhai_tansuo(248)))
        self.ui.pushButton_249.clicked.connect((lambda : self.hundunhai_tansuo(249)))
        self.ui.pushButton_250.clicked.connect((lambda : self.hundunhai_tansuo(250)))
        self.ui.pushButton_251.clicked.connect((lambda : self.hundunhai_tansuo(251)))
        self.ui.pushButton_252.clicked.connect((lambda : self.hundunhai_tansuo(252)))
        self.ui.pushButton_253.clicked.connect((lambda : self.hundunhai_tansuo(253)))
        self.ui.pushButton_254.clicked.connect((lambda : self.hundunhai_tansuo(254)))
        self.ui.pushButton_255.clicked.connect((lambda : self.hundunhai_tansuo(255)))
        self.ui.pushButton_256.clicked.connect((lambda : self.hundunhai_tansuo(256)))
        self.ui.pushButton_257.clicked.connect((lambda : self.hundunhai_tansuo(257)))
        self.ui.pushButton_258.clicked.connect((lambda : self.hundunhai_tansuo(258)))
        self.ui.pushButton_259.clicked.connect((lambda : self.hundunhai_tansuo(259)))
        self.ui.pushButton_260.clicked.connect((lambda : self.hundunhai_tansuo(260)))
        self.ui.pushButton_261.clicked.connect((lambda : self.hundunhai_tansuo(261)))
        self.ui.pushButton_262.clicked.connect((lambda : self.hundunhai_tansuo(262)))
        self.ui.pushButton_263.clicked.connect((lambda : self.hundunhai_tansuo(263)))
        self.ui.pushButton_264.clicked.connect((lambda : self.hundunhai_tansuo(264)))
        self.ui.pushButton_265.clicked.connect((lambda : self.hundunhai_tansuo(265)))
        self.ui.pushButton_266.clicked.connect((lambda : self.hundunhai_tansuo(266)))
        self.ui.pushButton_267.clicked.connect((lambda : self.hundunhai_tansuo(267)))
        self.ui.pushButton_268.clicked.connect((lambda : self.hundunhai_tansuo(268)))
        self.ui.pushButton_269.clicked.connect((lambda : self.hundunhai_tansuo(269)))
        self.ui.pushButton_270.clicked.connect((lambda : self.hundunhai_tansuo(270)))
        self.ui.pushButton_271.clicked.connect((lambda : self.hundunhai_tansuo(271)))
        self.ui.pushButton_272.clicked.connect((lambda : self.hundunhai_tansuo(272)))
        self.ui.pushButton_273.clicked.connect((lambda : self.hundunhai_tansuo(273)))
        self.ui.pushButton_274.clicked.connect((lambda : self.hundunhai_tansuo(274)))
        self.ui.pushButton_275.clicked.connect((lambda : self.hundunhai_tansuo(275)))
        self.ui.pushButton_276.clicked.connect((lambda : self.hundunhai_tansuo(276)))
        self.ui.pushButton_277.clicked.connect((lambda : self.hundunhai_tansuo(277)))
        self.ui.pushButton_278.clicked.connect((lambda : self.hundunhai_tansuo(278)))
        self.ui.pushButton_279.clicked.connect((lambda : self.hundunhai_tansuo(279)))
        self.ui.pushButton_280.clicked.connect((lambda : self.hundunhai_tansuo(280)))
        self.ui.pushButton_281.clicked.connect((lambda : self.hundunhai_tansuo(281)))
        self.ui.pushButton_282.clicked.connect((lambda : self.hundunhai_tansuo(282)))
        self.ui.pushButton_283.clicked.connect((lambda : self.hundunhai_tansuo(283)))
        self.ui.pushButton_284.clicked.connect((lambda : self.hundunhai_tansuo(284)))
        self.ui.pushButton_285.clicked.connect((lambda : self.hundunhai_tansuo(285)))
        self.ui.pushButton_286.clicked.connect((lambda : self.hundunhai_tansuo(286)))
        self.ui.pushButton_287.clicked.connect((lambda : self.hundunhai_tansuo(287)))
        self.ui.pushButton_288.clicked.connect((lambda : self.hundunhai_tansuo(288)))
        self.ui.pushButton_289.clicked.connect((lambda : self.hundunhai_tansuo(289)))
        self.ui.pushButton_290.clicked.connect((lambda : self.hundunhai_tansuo(290)))
        self.ui.pushButton_291.clicked.connect((lambda : self.hundunhai_tansuo(291)))
        self.ui.pushButton_292.clicked.connect((lambda : self.hundunhai_tansuo(292)))
        self.ui.pushButton_293.clicked.connect((lambda : self.hundunhai_tansuo(293)))
        self.ui.pushButton_294.clicked.connect((lambda : self.hundunhai_tansuo(294)))
        self.ui.pushButton_295.clicked.connect((lambda : self.hundunhai_tansuo(295)))
        self.ui.pushButton_296.clicked.connect((lambda : self.hundunhai_tansuo(296)))
        self.ui.pushButton_297.clicked.connect((lambda : self.hundunhai_tansuo(297)))
        self.ui.pushButton_298.clicked.connect((lambda : self.hundunhai_tansuo(298)))
        self.ui.pushButton_299.clicked.connect((lambda : self.hundunhai_tansuo(299)))
        self.ui.pushButton_300.clicked.connect((lambda : self.hundunhai_tansuo(300)))
        self.ui.pushButton_301.clicked.connect((lambda : self.hundunhai_tansuo(301)))
        self.ui.pushButton_302.clicked.connect((lambda : self.hundunhai_tansuo(302)))
        self.ui.pushButton_303.clicked.connect((lambda : self.hundunhai_tansuo(303)))
        self.ui.pushButton_304.clicked.connect((lambda : self.hundunhai_tansuo(304)))
        self.ui.pushButton_305.clicked.connect((lambda : self.hundunhai_tansuo(305)))
        self.ui.pushButton_306.clicked.connect((lambda : self.hundunhai_tansuo(306)))
        self.ui.pushButton_307.clicked.connect((lambda : self.hundunhai_tansuo(307)))
        self.ui.pushButton_308.clicked.connect((lambda : self.hundunhai_tansuo(308)))
        self.ui.pushButton_309.clicked.connect((lambda : self.hundunhai_tansuo(309)))
        self.ui.pushButton_310.clicked.connect((lambda : self.hundunhai_tansuo(310)))
        self.ui.pushButton_311.clicked.connect((lambda : self.hundunhai_tansuo(311)))
        self.ui.pushButton_312.clicked.connect((lambda : self.hundunhai_tansuo(312)))
        self.ui.pushButton_313.clicked.connect((lambda : self.hundunhai_tansuo(313)))
        self.ui.pushButton_314.clicked.connect((lambda : self.hundunhai_tansuo(314)))
        self.ui.pushButton_315.clicked.connect((lambda : self.hundunhai_tansuo(315)))
        self.ui.pushButton_316.clicked.connect((lambda : self.hundunhai_tansuo(316)))
        self.ui.pushButton_317.clicked.connect((lambda : self.hundunhai_tansuo(317)))
        self.ui.pushButton_318.clicked.connect((lambda : self.hundunhai_tansuo(318)))
        self.ui.pushButton_319.clicked.connect((lambda : self.hundunhai_tansuo(319)))
        self.ui.pushButton_320.clicked.connect((lambda : self.hundunhai_tansuo(320)))
        self.ui.pushButton_321.clicked.connect((lambda : self.hundunhai_tansuo(321)))
        self.ui.pushButton_322.clicked.connect((lambda : self.hundunhai_tansuo(322)))
        self.ui.pushButton_323.clicked.connect((lambda : self.hundunhai_tansuo(323)))
        self.ui.pushButton_324.clicked.connect((lambda : self.hundunhai_tansuo(324)))
        self.ui.pushButton_325.clicked.connect((lambda : self.hundunhai_tansuo(325)))
        self.ui.pushButton_326.clicked.connect((lambda : self.hundunhai_tansuo(326)))
        self.ui.pushButton_327.clicked.connect((lambda : self.hundunhai_tansuo(327)))
        self.ui.pushButton_328.clicked.connect((lambda : self.hundunhai_tansuo(328)))
        self.ui.pushButton_329.clicked.connect((lambda : self.hundunhai_tansuo(329)))
        self.ui.pushButton_330.clicked.connect((lambda : self.hundunhai_tansuo(330)))
        self.ui.pushButton_331.clicked.connect((lambda : self.hundunhai_tansuo(331)))
        self.ui.pushButton_332.clicked.connect((lambda : self.hundunhai_tansuo(332)))
        self.ui.pushButton_333.clicked.connect((lambda : self.hundunhai_tansuo(333)))
        self.ui.pushButton_334.clicked.connect((lambda : self.hundunhai_tansuo(334)))
        self.ui.pushButton_335.clicked.connect((lambda : self.hundunhai_tansuo(335)))
        self.ui.pushButton_336.clicked.connect((lambda : self.hundunhai_tansuo(336)))
        self.ui.pushButton_337.clicked.connect((lambda : self.hundunhai_tansuo(337)))
        self.ui.pushButton_338.clicked.connect((lambda : self.hundunhai_tansuo(338)))
        self.ui.pushButton_339.clicked.connect((lambda : self.hundunhai_tansuo(339)))
        self.ui.pushButton_340.clicked.connect((lambda : self.hundunhai_tansuo(340)))
        self.ui.pushButton_341.clicked.connect((lambda : self.hundunhai_tansuo(341)))
        self.ui.pushButton_342.clicked.connect((lambda : self.hundunhai_tansuo(342)))
        self.ui.pushButton_343.clicked.connect((lambda : self.hundunhai_tansuo(343)))
        self.ui.pushButton_344.clicked.connect((lambda : self.hundunhai_tansuo(344)))
        self.ui.pushButton_345.clicked.connect((lambda : self.hundunhai_tansuo(345)))
        self.ui.pushButton_346.clicked.connect((lambda : self.hundunhai_tansuo(346)))
        self.ui.pushButton_347.clicked.connect((lambda : self.hundunhai_tansuo(347)))
        self.ui.pushButton_348.clicked.connect((lambda : self.hundunhai_tansuo(348)))
        self.ui.pushButton_349.clicked.connect((lambda : self.hundunhai_tansuo(349)))
        self.ui.pushButton_350.clicked.connect((lambda : self.hundunhai_tansuo(350)))
        self.ui.pushButton_351.clicked.connect((lambda : self.hundunhai_tansuo(351)))
        self.ui.pushButton_352.clicked.connect((lambda : self.hundunhai_tansuo(352)))
        self.ui.pushButton_353.clicked.connect((lambda : self.hundunhai_tansuo(353)))
        self.ui.pushButton_354.clicked.connect((lambda : self.hundunhai_tansuo(354)))
        self.ui.pushButton_355.clicked.connect((lambda : self.hundunhai_tansuo(355)))
        self.ui.pushButton_356.clicked.connect((lambda : self.hundunhai_tansuo(356)))
        self.ui.pushButton_357.clicked.connect((lambda : self.hundunhai_tansuo(357)))
        self.ui.pushButton_358.clicked.connect((lambda : self.hundunhai_tansuo(358)))
        self.ui.pushButton_359.clicked.connect((lambda : self.hundunhai_tansuo(359)))
        self.ui.pushButton_360.clicked.connect((lambda : self.hundunhai_tansuo(360)))
        self.ui.pushButton_361.clicked.connect((lambda : self.hundunhai_tansuo(361)))
        self.ui.pushButton_362.clicked.connect((lambda : self.hundunhai_tansuo(362)))
        self.ui.pushButton_363.clicked.connect((lambda : self.hundunhai_tansuo(363)))
        self.ui.pushButton_364.clicked.connect((lambda : self.hundunhai_tansuo(364)))
        self.ui.pushButton_365.clicked.connect((lambda : self.hundunhai_tansuo(365)))
        self.ui.pushButton_366.clicked.connect((lambda : self.hundunhai_tansuo(366)))
        self.ui.pushButton_367.clicked.connect((lambda : self.hundunhai_tansuo(367)))
        self.ui.pushButton_368.clicked.connect((lambda : self.hundunhai_tansuo(368)))
        self.ui.pushButton_369.clicked.connect((lambda : self.hundunhai_tansuo(369)))
        self.ui.pushButton_370.clicked.connect((lambda : self.hundunhai_tansuo(370)))
        self.ui.pushButton_371.clicked.connect((lambda : self.hundunhai_tansuo(371)))
        self.ui.pushButton_372.clicked.connect((lambda : self.hundunhai_tansuo(372)))
        self.ui.pushButton_373.clicked.connect((lambda : self.hundunhai_tansuo(373)))
        self.ui.pushButton_374.clicked.connect((lambda : self.hundunhai_tansuo(374)))
        self.ui.pushButton_375.clicked.connect((lambda : self.hundunhai_tansuo(375)))
        self.ui.pushButton_376.clicked.connect((lambda : self.hundunhai_tansuo(376)))
        self.ui.pushButton_377.clicked.connect((lambda : self.hundunhai_tansuo(377)))
        self.ui.pushButton_378.clicked.connect((lambda : self.hundunhai_tansuo(378)))
        self.ui.pushButton_duihuan_tisicaoren.clicked.connect((lambda : self.lunhuibaoku_duihuan(8)))
        self.ui.pushButton_duihuan_tianfudai.clicked.connect((lambda : self.lunhuibaoku_duihuan(9)))
        self.ui.pushButton_duihuan_longfengbi.clicked.connect((lambda : self.lunhuibaoku_duihuan(11)))
        self.ui.pushButton_query_shenjie_yuanli_shop.clicked.connect((lambda : self.query_shenjie_shop(1)))
        self.ui.pushButton_query_shenjie_shangling_shop.clicked.connect((lambda : self.query_shenjie_shop(2)))
        self.ui.comboBox_query_daogong.activated.connect(self.daogong_change)
        self.ui.pushButton_tiaozhan_dianzhu_1.clicked.connect((lambda : self.gongji_dianzhu(9)))
        self.ui.pushButton_tiaozhan_dianzhu_2.clicked.connect((lambda : self.gongji_dianzhu(10)))
        self.ui.pushButton_tiaozhan_dianzhu_3.clicked.connect((lambda : self.gongji_dianzhu(11)))
        self.ui.pushButton_tiaozhan_dianzhu_4.clicked.connect((lambda : self.gongji_dianzhu(12)))
        self.ui.pushButton_tiaozhan_dianzhu_5.clicked.connect((lambda : self.gongji_dianzhu(13)))
        self.ui.pushButton_tiaozhan_dianzhu_6.clicked.connect((lambda : self.gongji_dianzhu(14)))
        self.ui.pushButton_tiaozhan_dianzhu_7.clicked.connect((lambda : self.gongji_dianzhu(15)))
        self.ui.pushButton_2_stop_tiaozhan.clicked.connect(self.huashen_2_stop_tiaozhan)
        self.ui.pushButton_2_xianjie.clicked.connect((lambda : self.huashen_2_tiaozhan(1)))
        self.ui.pushButton_2_guijie.clicked.connect((lambda : self.huashen_2_tiaozhan(2)))
        self.ui.pushButton_2_mojie.clicked.connect((lambda : self.huashen_2_tiaozhan(3)))
        self.ui.pushButton_2_shenjie.clicked.connect((lambda : self.huashen_2_tiaozhan(4)))
        self.ui.pushButton_2_fudixiaoshijie.clicked.connect((lambda : self.huashen_2_tiaozhan(5)))
        self.ui.pushButton_2_zongmenyizhi.clicked.connect((lambda : self.huashen_2_tiaozhan(6)))
        self.ui.pushButton_peiyangjindaotong.clicked.connect((lambda : self.peiyangdaotong_one(1)))
        self.ui.pushButton_peiyangmudaotong.clicked.connect((lambda : self.peiyangdaotong_one(2)))
        self.ui.pushButton_peiyangshuidaotong.clicked.connect((lambda : self.peiyangdaotong_one(3)))
        self.ui.pushButton_peiyanghuodaotong.clicked.connect((lambda : self.peiyangdaotong_one(4)))
        self.ui.pushButton_peiyangtudaotong.clicked.connect((lambda : self.peiyangdaotong_one(5)))
        self.ui.pushButton_yijianpeiyangdaotong.clicked.connect(self.yijianpeiyangdaotong)
        self.ui.pushButton_shengqianli_1.clicked.connect((lambda : self.shengdaotongqianli(1)))
        self.ui.pushButton_shengqianli_2.clicked.connect((lambda : self.shengdaotongqianli(2)))
        self.ui.pushButton_shengqianli_3.clicked.connect((lambda : self.shengdaotongqianli(3)))
        self.ui.pushButton_shengqianli_4.clicked.connect((lambda : self.shengdaotongqianli(4)))
        self.ui.pushButton_shengqianli_5.clicked.connect((lambda : self.shengdaotongqianli(5)))
        self.ui.pushButton_rendao_fudai_on.clicked.connect((lambda : self.change_fudai(1, 0)))
        self.ui.pushButton_rendao_fudai_off.clicked.connect((lambda : self.change_fudai(0, 0)))
        self.ui.pushButton_egui_fudai_on.clicked.connect((lambda : self.change_fudai(1, 1)))
        self.ui.pushButton_egui_fudai_off.clicked.connect((lambda : self.change_fudai(0, 1)))
        self.ui.pushButton_rendao_tisi_on.clicked.connect((lambda : self.change_tisi(1, 0)))
        self.ui.pushButton_rendao_tisi_off.clicked.connect((lambda : self.change_tisi(0, 0)))
        self.ui.pushButton_egui_tisi_on.clicked.connect((lambda : self.change_tisi(1, 1)))
        self.ui.pushButton_egui_tisi_off.clicked.connect((lambda : self.change_tisi(0, 1)))
        self.ui.pushButton_rendao_longfengbi_on.clicked.connect((lambda : self.change_longfengbi(1, 0)))
        self.ui.pushButton_rendao_longfengbi_off.clicked.connect((lambda : self.change_longfengbi(0, 0)))
        self.ui.pushButton_egui_longfengbi_on.clicked.connect((lambda : self.change_longfengbi(1, 1)))
        self.ui.pushButton_egui_longfengbi_off.clicked.connect((lambda : self.change_longfengbi(0, 1)))
        self.ui.pushButton_dengjipaihang_on.clicked.connect((lambda : self.xiuwei_change_show(1)))
        self.ui.pushButton_dengjipaihang_off.clicked.connect((lambda : self.xiuwei_change_show(0)))
        self.ui.pushButton_refresh_level_rank.clicked.connect(self.refresh_level_rank)
        self.ui.comboBox_level_rank_filter.activated.connect(self.level_rank_filter_change)
        self.ui.pushButton_shuxingpaihang_on.clicked.connect((lambda : self.shuxing_change_show(1)))
        self.ui.pushButton_shuxingpaihang_off.clicked.connect((lambda : self.shuxing_change_show(0)))
        self.ui.pushButton_refresh_shuxing_rank.clicked.connect(self.refresh_shuxing_rank)
        self.ui.comboBox_shuxing_rank_filter.activated.connect(self.shuxing_rank_filter_change)
        self.ui.pushButton_chongwupaihang_on.clicked.connect((lambda : self.chongwu_change_show(1)))
        self.ui.pushButton_chongwupaihang_off.clicked.connect((lambda : self.chongwu_change_show(0)))
        self.ui.pushButton_refresh_chongwu_rank.clicked.connect(self.refresh_chongwu_rank)
        self.ui.pushButton_refresh_daotong_rank.clicked.connect(self.refresh_daotong_rank)
        self.ui.pushButton_tongnianfen_pk.clicked.connect(self.tongnianfen_pk)
        self.ui.pushButton_tongnianfen_help.clicked.connect(self.tongnianfen_help)
        self.ui.pushButton_2_xiulian_help.clicked.connect(self.pushButton_2_xiulian_help)
        self.ui.pushButton_xiuxianlicheng_help.clicked.connect(self.xiuxianlicheng_help)
        self.ui.pushButton_shuxingpaihang_help.clicked.connect(self.shuxingpaihang_help)
        self.ui.pushButton_chongwupaihang_help.clicked.connect(self.chongwupaihang_help)
        self.ui.pushButton_lunhuidian_help.clicked.connect(self.lunhuidian_help)
        self.ui.pushButton_daotu_help.clicked.connect(self.daotu_help)
        self.ui.pushButton_xumiding_help.clicked.connect(self.xumiding_help)
        self.ui.pushButton_daozhu_help.clicked.connect(self.daozhu_help)
        self.ui.pushButton_dongfushuoming_help.clicked.connect(self.dongfushuoming_help)
        self.ui.pushButton_hundunhai_shoulie_help.clicked.connect(self.hundunhai_shoulie_help)
        self.ui.pushButton_kamanshouyi_help.clicked.connect(self.kamanshouyi_help)
        self.ui.pushButton_liandan_help.clicked.connect(self.liandan_help)
        self.ui.pushButton_daotongpeiyang_help.clicked.connect(self.daotongpeiyang_help)
        self.haoganrenwu_comboBox_list = [
         self.ui.comboBox_haoganrenwu_1, self.ui.comboBox_haoganrenwu_2, self.ui.comboBox_haoganrenwu_3, self.ui.comboBox_haoganrenwu_4, self.ui.comboBox_haoganrenwu_5, self.ui.comboBox_haoganrenwu_6, self.ui.comboBox_haoganrenwu_7, self.ui.comboBox_haoganrenwu_8, self.ui.comboBox_haoganrenwu_9, self.ui.comboBox_haoganrenwu_10, self.ui.comboBox_haoganrenwu_11, self.ui.comboBox_haoganrenwu_12, self.ui.comboBox_haoganrenwu_13, self.ui.comboBox_haoganrenwu_14, self.ui.comboBox_haoganrenwu_15, self.ui.comboBox_haoganrenwu_16, self.ui.comboBox_haoganrenwu_17, self.ui.comboBox_haoganrenwu_18, self.ui.comboBox_haoganrenwu_19, self.ui.comboBox_haoganrenwu_20, self.ui.comboBox_haoganrenwu_21, self.ui.comboBox_haoganrenwu_22, self.ui.comboBox_haoganrenwu_23, self.ui.comboBox_haoganrenwu_24, self.ui.comboBox_haoganrenwu_25, self.ui.comboBox_haoganrenwu_26, self.ui.comboBox_haoganrenwu_27, self.ui.comboBox_haoganrenwu_28, self.ui.comboBox_haoganrenwu_29, self.ui.comboBox_haoganrenwu_30, self.ui.comboBox_haoganrenwu_31, self.ui.comboBox_haoganrenwu_32, self.ui.comboBox_haoganrenwu_33, self.ui.comboBox_haoganrenwu_34, self.ui.comboBox_haoganrenwu_35, self.ui.comboBox_haoganrenwu_36, self.ui.comboBox_haoganrenwu_37, self.ui.comboBox_haoganrenwu_38, self.ui.comboBox_haoganrenwu_39, self.ui.comboBox_haoganrenwu_40, self.ui.comboBox_haoganrenwu_41, self.ui.comboBox_haoganrenwu_42, self.ui.comboBox_haoganrenwu_43, self.ui.comboBox_haoganrenwu_44, self.ui.comboBox_haoganrenwu_45, self.ui.comboBox_haoganrenwu_46, self.ui.comboBox_haoganrenwu_47, self.ui.comboBox_haoganrenwu_48, self.ui.comboBox_haoganrenwu_49, self.ui.comboBox_haoganrenwu_50, self.ui.comboBox_haoganrenwu_51, self.ui.comboBox_haoganrenwu_52, self.ui.comboBox_haoganrenwu_53, self.ui.comboBox_haoganrenwu_54]
        for haoganrenwu_comboBox in self.haoganrenwu_comboBox_list:
            haoganrenwu_comboBox.activated.connect(self.haoganrenwu_change)

        self.ui.comboBox_yellowtide_haiyan1.activated.connect(self.yellowtide_haiyan1_change)
        self.ui.pushButton_yellowtide_bianyuan1.clicked.connect(self.yellowtide_bianyuan1)
        self.ui.pushButton_yellowtide_hexin1.clicked.connect(self.yellowtide_hexin1)
        self.ui.pushButton_yellowtide_set_lingyan1.clicked.connect(self.yellowtide_set_lingyan1)
        self.ui.pushButton_yellowtide_broadcast_mylingyan1.clicked.connect(self.yellowtide_broadcast_mylingyan1)
        self.ui.pushButton_yellowtide_get_broadcast.clicked.connect(self.yellowtide_get_broadcast)
        self.ui.pushButton_liji_tiaozhan_jiezhu.clicked.connect(self.liji_tiaozhan_jiezhu)
        self.ui.pushButton_liji_tiaozhan_dadi.clicked.connect(self.liji_tiaozhan_dadi)
        self.ui.pushButton_liji_tiaozhan_daozhu.clicked.connect(self.liji_tiaozhan_daozhu)
        self.ui.pushButton_use_dadi_longyu.clicked.connect(self.use_dadi_longyu)
        self.ui.pushButton_use_daozhu_longyu.clicked.connect(self.use_daozhu_longyu)
        self.ui.comboBox_lingmaileixing.activated.connect(self.lingmaileixing_change)
        self.ui.comboBox_fudi_name.activated.connect(self.fudi_name_change)
        self.ui.comboBox_shentongleixing.activated.connect(self.shentongchaxun_change)
        self.ui.comboBox_shentongxingji.activated.connect(self.shentongchaxun_change)
        self.ui.comboBox_jinengleixing.activated.connect(self.jinengchaxun_change)
        self.ui.comboBox_jinengxingji.activated.connect(self.jinengchaxun_change)
        self.ui.comboBox_tianmixingji.activated.connect(self.tianmichaxun_change)
        self.ui.comboBox_liantijue_weizhi.activated.connect(self.liantichaxun_change)
        self.ui.comboBox_pingtaileixing.activated.connect(self.pingtaileixing_change)
        self.ui.comboBox_guajileixing.activated.connect(self.guajileixing_change)
        self.ui.comboBox_guajifangan.activated.connect(self.guajifangan_change)
        self.ui.comboBox_ditujibie_shua.activated.connect(self.ditujibie_shua_change)
        self.ui.comboBox_ditujibie_tou.activated.connect(self.ditujibie_tou_change)
        self.ui.comboBox_shuatucishu.activated.connect(self.shuatucishu_change)
        self.ui.comboBox_danyaoleixing.activated.connect((lambda : self.danyaoleixing_change(1)))
        self.ui.comboBox_danyaoleixing2.activated.connect((lambda : self.danyaoleixing_change(2)))
        self.ui.comboBox_danyaoleixing3.activated.connect((lambda : self.danyaoleixing_change(3)))
        self.ui.comboBox_danyaojibie.activated.connect((lambda : self.danyaojibie_change(1)))
        self.ui.comboBox_danyaojibie2.activated.connect((lambda : self.danyaojibie_change(2)))
        self.ui.comboBox_danyaojibie3.activated.connect((lambda : self.danyaojibie_change(3)))
        self.ui.comboBox_danyaoleixing4.activated.connect((lambda : self.danyaoleixing_change(4)))
        self.ui.comboBox_danyaoleixing5.activated.connect((lambda : self.danyaoleixing_change(5)))
        self.ui.comboBox_danyaoleixing6.activated.connect((lambda : self.danyaoleixing_change(6)))
        self.ui.comboBox_danyaojibie4.activated.connect((lambda : self.danyaojibie_change(4)))
        self.ui.comboBox_danyaojibie5.activated.connect((lambda : self.danyaojibie_change(5)))
        self.ui.comboBox_danyaojibie6.activated.connect((lambda : self.danyaojibie_change(6)))
        self.ui.comboBox_lianqileixing.activated.connect(self.lianqileixing_change)
        self.ui.comboBox_query_xingjun.activated.connect(self.query_xingjun_change)
        self.ui.comboBox_query_tianshen.activated.connect(self.query_tianshen_change)
        self.ui.checkBox_zidongchonglian.clicked.connect(self.zidongchonglian_change)
        self.ui.checkBox_chonglianshuatu.clicked.connect(self.chonglianshuatu_change)
        self.ui.checkBox_diertianshangxian.clicked.connect(self.diertianshangxian_change)
        self.ui.checkBox_open_auto_login.clicked.connect(self.open_auto_login_change)
        self.ui.checkBox_baoliuyifu.clicked.connect(self.baoliuyifu_change)
        self.ui.checkBox_youxianfugui.clicked.connect(self.youxianfugui_change)
        self.ui.checkBox_duihuantisicaoren.clicked.connect(self.duihuantisicaoren_change)
        self.ui.checkBox_duihuantianfudai.clicked.connect(self.duihuantianfudai_change)
        self.ui.checkBox_duihuanlongfengbi.clicked.connect(self.duihuanlongfengbi_change)
        self.ui.checkBox_zidongshilian.clicked.connect(self.zidongshilian_change)
        self.ui.checkBox_hdh_phcl.clicked.connect(self.hdh_phcl_change)
        self.ui.checkBox_yanyu_zidongtansuo.clicked.connect(self.yanyu_zidongtansuo_change)
        self.ui.checkBox_dier_shengshentong.clicked.connect(self.dier_shengshentong_change)
        self.ui.checkBox_duihuan_xiantian_daowen.clicked.connect(self.duihuan_xiantian_daowen_change)
        self.ui.checkBox_tuiyan_hundun_daotu.clicked.connect(self.tuiyan_hundun_daotu_change)
        self.ui.checkBox_auto_yanghundan.clicked.connect(self.auto_yanghundan_change)
        self.ui.checkBox_auto_lianqi.clicked.connect(self.auto_lianqi_change)
        self.ui.checkBox_auto_huntianxiandan.clicked.connect(self.auto_huntianxiandan_change)
        self.ui.checkBox_auto_xueshaxiandan.clicked.connect(self.auto_xueshaxiandan_change)
        self.ui.checkBox_lianxutoutu.clicked.connect(self.lianxutoutu_change)
        self.ui.checkBox_zhidayao.clicked.connect(self.zhidayao_change)
        self.ui.checkBox_zhidagui.clicked.connect(self.zhidagui_change)
        self.ui.checkBox_xuefutu.clicked.connect(self.xuefutu_change)
        self.ui.comboBox_xuefutucengshu.activated.connect(self.comboBox_xuefutucengshu_change)
        self.ui.comboBox_xuefutucishu.activated.connect(self.comboBox_xuefutucishu_change)
        self.ui.checkBox_zidongshengdizi.clicked.connect(self.zidongshengdizi_change)
        self.ui.comboBox_menpaidizijibie.activated.connect(self.comboBox_menpaidizijibie_change)
        self.ui.checkBox_zidongmenpailingwu.clicked.connect(self.zidongmenpailingwu_change)
        self.ui.comboBox_menpailingwuleixing.activated.connect(self.comboBox_menpailingwuleixing_change)
        self.ui.checkBox_zidongzongmenjindi.clicked.connect(self.zidongzongmenjindi_change)
        self.ui.comboBox_zongmenjindi.activated.connect(self.comboBox_zongmenjindi_change)
        self.ui.checkBox_zidonggongde.clicked.connect(self.zidonggongde_change)
        self.ui.comboBox_gongderenwu.activated.connect(self.comboBox_gongderenwu_change)
        self.ui.checkBox_zidongfudan.clicked.connect(self.zidongfudan_change)
        self.ui.comboBox_fudanleixing.activated.connect(self.comboBox_fudanleixing_change)
        self.ui.checkBox_zidongzhongtian.clicked.connect(self.zidongzhongtian_change)
        self.ui.comboBox_zhongzi.activated.connect(self.comboBox_zhongzi_change)
        self.ui.checkBox_zidongtongguantiaozhan.clicked.connect(self.zidongtongguantiaozhan_change)
        self.ui.comboBox_tongguantiaozhan.activated.connect(self.comboBox_tongguantiaozhan_change)
        self.ui.checkBox_zidongganwutiandao.clicked.connect(self.zidongganwutiandao_change)
        self.ui.comboBox_ganwutiandao.activated.connect(self.comboBox_ganwutiandao_change)
        self.ui.checkBox_zidongmaicha.clicked.connect(self.zidongmaicha_change)
        self.ui.comboBox_zidongmaicha.activated.connect(self.comboBox_zidongmaicha_change)
        self.ui.checkBox_zongmenkuangmai.clicked.connect(self.zongmenkuangmai_change)
        self.ui.comboBox_zongmenkuangmai.activated.connect(self.comboBox_zongmenkuangmai_change)
        self.ui.checkBox_zidongshenmu.clicked.connect(self.zidongshenmu_change)
        self.ui.comboBox_zidongshenmu.activated.connect(self.comboBox_zidongshenmu_change)
        self.ui.checkBox_zidonglunhuifahui.clicked.connect(self.zidonglunhuifahui_change)
        self.ui.comboBox_lunhuifahuidaguai.activated.connect(self.comboBox_lunhuifahuidaguai_change)
        self.ui.checkBox_gongdeche.clicked.connect(self.gongdeche_change)
        self.ui.comboBox_gongdeche.activated.connect(self.comboBox_gongdeche_change)
        self.ui.checkBox_daozhu_zhanweizhi.clicked.connect(self.daozhu_zhanweizhi_change)
        self.ui.checkBox_dadi_zhanweizhi.clicked.connect(self.dadi_zhanweizhi_change)
        self.ui.checkBox_jiezhu_zhanweizhi.clicked.connect(self.jiezhu_zhanweizhi_change)
        self.ui.checkBox_tianshen_5ci.clicked.connect(self.tianshen_5ci_change)
        self.ui.checkBox_lingmai_5ci.clicked.connect(self.lingmai_5ci_change)
        self.ui.checkBox_aotu_longyu.clicked.connect(self.aotu_longyu_change)
        self.ui.checkBox_zidongtianxiang.clicked.connect(self.zidongtianxiang_change)
        self.ui.comboBox_tianxiangleixing.activated.connect(self.comboBox_tianxiangleixing_change)
        self.ui.comboBox_baoku_duihuan_cao.activated.connect(self.comboBox_baoku_duihuan_cao_change)
        self.ui.comboBox_baoku_duihuan_kuang.activated.connect(self.comboBox_baoku_duihuan_kuang_change)
        self.ui.comboBox_hundunhai_cur_tansuo.activated.connect(self.comboBox_hundunhai_cur_tansuo_change)
        self.ui.comboBox_hundunhai_next_tansuo.activated.connect(self.comboBox_hundunhai_next_tansuo_change)
        self.ui.comboBox_yuanhaimijing.activated.connect(self.comboBox_yuanhaimijing_change)
        self.ui.comboBox_yuanhaimijing_cishu.activated.connect(self.comboBox_yuanhaimijing_cishu_change)
        self.ui.comboBox_haishoutansuo.activated.connect(self.comboBox_haishoutansuo_change)
        self.ui.comboBox_yunyangxiantian.activated.connect(self.comboBox_yunyangxiantian_change)
        self.ui.comboBox_foguoganwu.activated.connect(self.comboBox_foguoganwu_change)
        self.ui.comboBox_shuidaotong_work.activated.connect(self.comboBox_shuidaotong_work_change)
        self.ui.comboBox_2_chuqiaoditu.activated.connect(self.comboBox_2_chuqiaoditu_change)
        self.ui.comboBox_2_shengjimoshi.activated.connect(self.comboBox_2_shengjimoshi_change)
        self.ui.comboBox_2_xiu_mode.activated.connect(self.comboBox_2_xiu_mode_change)
        self.ui.comboBox_shengdaotu_level.activated.connect(self.comboBox_shengdaotu_level_change)
        self.ui.comboBox_liandan_stop_type.activated.connect(self.comboBox_liandan_stop_type_change)
        self.ui.comboBox_change_twt_fahui.activated.connect(self.comboBox_change_twt_fahui_change)
        self.ui.comboBox_tourujingxue.activated.connect(self.comboBox_tourujingxue_change)
        self.ui.comboBox_auto_lingyan_mode.activated.connect(self.comboBox_auto_lingyan_mode_change)
        self.ui.comboBox_auto_yellowtide.activated.connect(self.comboBox_auto_yellowtide_change)
        self.ui.comboBox_show_yellowtide.activated.connect(self.comboBox_show_yellowtide_change)
        self.ui.comboBox_renjiandao_fudai.activated.connect(self.comboBox_renjiandao_fudai_change)
        self.ui.comboBox_eguidao_fudai.activated.connect(self.comboBox_eguidao_fudai_change)
        self.ui.comboBox_maixuanhuangzhu.activated.connect(self.comboBox_maixuanhuangzhu_change)
        self.ui.comboBox_shilianzhidi.activated.connect(self.comboBox_shilianzhidi_change)
        self.ui.comboBox_shiliancengshu.activated.connect(self.comboBox_shiliancengshu_change)
        self.ui.comboBox_shiliangoumai.activated.connect(self.comboBox_shiliangoumai_change)
        self.ui.comboBox_ronglian1.activated.connect(self.comboBox_ronglian1_change)
        self.ui.comboBox_ronglian2.activated.connect(self.comboBox_ronglian2_change)
        self.ui.comboBox_xumiding.activated.connect(self.comboBox_xumiding_change)
        self.ui.comboBox_hunyuanwudao.activated.connect(self.comboBox_hunyuanwudao_change)
        self.ui.comboBox_benming1_befor.activated.connect(self.comboBox_benming1_befor_change)
        self.ui.comboBox_benming1_after.activated.connect(self.comboBox_benming1_after_change)
        self.ui.comboBox_benming2_befor.activated.connect(self.comboBox_benming2_befor_change)
        self.ui.comboBox_benming2_after.activated.connect(self.comboBox_benming2_after_change)
        self.ui.comboBox_shoulie_didian1.activated.connect(self.comboBox_shoulie_didian1_change)
        self.ui.comboBox_shoulie_didian2.activated.connect(self.comboBox_shoulie_didian2_change)
        self.ui.comboBox_next_shoulie_didian.activated.connect(self.comboBox_next_shoulie_didian_change)
        self.ui.comboBox_daotongpeiyang_moshi.activated.connect(self.comboBox_daotongpeiyang_moshi_change)
        self.ui.comboBox_daotongpeiyang_dengji.activated.connect(self.comboBox_daotongpeiyang_dengji_change)
        self.ui.comboBox_daotongpeiyang_zizhi.activated.connect(self.comboBox_daotongpeiyang_zizhi_change)
        self.ui.comboBox_faxiangleixing.activated.connect(self.comboBox_faxiangleixing_change)
        self.ui.comboBox_faxiangtaozhuang.activated.connect(self.comboBox_faxiangtaozhuang_change)
        self.ui.comboBox_charge_value.activated.connect(self.comboBox_charge_value_change)
        self.ui.pushButton_refresh_guanwei_apply.clicked.connect(self.refresh_guanwei_apply)
        self.ui.pushButton_shenguan_guanwei_cizhi.clicked.connect(self.shenguan_guanwei_cizhi)
        self.ui.pushButton_guanwei_citui.clicked.connect(self.guanwei_citui)
        self.ui.comboBox_guanwei_query.activated.connect(self.guanwei_query)
        self.ui.pushButton_guanwei_apply.clicked.connect(self.guanwei_apply)
        self.ui.pushButton_refresh_dadi_guanwei_apply.clicked.connect(self.refresh_dadi_guanwei_apply)
        self.ui.pushButton_shenguan_dadi_guanwei_cizhi.clicked.connect(self.shenguan_dadi_guanwei_cizhi)
        self.ui.pushButton_dadi_guanwei_citui.clicked.connect(self.dadi_guanwei_citui)
        self.ui.comboBox_dadi_guanwei_query.activated.connect(self.dadi_guanwei_query)
        self.ui.pushButton_dadi_guanwei_apply.clicked.connect(self.dadi_guanwei_apply)
        self.ui.pushButton_refresh_daozhu_guanwei_apply.clicked.connect(self.refresh_daozhu_guanwei_apply)
        self.ui.pushButton_shenguan_daozhu_guanwei_cizhi.clicked.connect(self.shenguan_daozhu_guanwei_cizhi)
        self.ui.pushButton_daozhu_guanwei_citui.clicked.connect(self.daozhu_guanwei_citui)
        self.ui.comboBox_daozhu_guanwei_query.activated.connect(self.daozhu_guanwei_query)
        self.ui.pushButton_daozhu_guanwei_apply.clicked.connect(self.daozhu_guanwei_apply)
        self.ui.pushButton_longyu_dadi.clicked.connect((lambda : self.change_longyu(1)))
        self.ui.pushButton_longyu_daozhu.clicked.connect((lambda : self.change_longyu(2)))
        self.ui.pushButton_longyu_lingqu.clicked.connect(self.longyu_lingqu)
        self.ui.pushButton_longyu_lingqu_2.clicked.connect(self.longyu_lingqu)
        self.ui.pushButton_guanwei_no.clicked.connect((lambda : self.guanwei_shenpi(0)))
        self.ui.pushButton_guanwei_yes.clicked.connect((lambda : self.guanwei_shenpi(1)))
        self.ui.pushButton_dadi_guanwei_no.clicked.connect((lambda : self.dadi_guanwei_shenpi(0)))
        self.ui.pushButton_dadi_guanwei_yes.clicked.connect((lambda : self.dadi_guanwei_shenpi(1)))
        self.ui.pushButton_daozhu_guanwei_no.clicked.connect((lambda : self.daozhu_guanwei_shenpi(0)))
        self.ui.pushButton_daozhu_guanwei_yes.clicked.connect((lambda : self.daozhu_guanwei_shenpi(1)))
        self.ui.checkBox_yuyue59xingjun.clicked.connect(self.yuyue59xingjun_change)
        self.ui.checkBox_yuyue59lingmai.clicked.connect(self.yuyue59lingmai_change)
        self.ui.checkBox_yuyue59tianshen.clicked.connect(self.yuyue59tianshen_change)
        self.ui.checkBox_yuyue59dianzhu.clicked.connect(self.yuyue59dianzhu_change)
        self.ui.checkBox_zidongtiaozhandadi.clicked.connect(self.zidongtiaozhandadi_change)
        self.ui.comboBox_tiaozhandadi.activated.connect(self.comboBox_tiaozhandadi_change)
        self.ui.comboBox_tiaozhan_daozhu.activated.connect(self.tiaozhan_daozhu_change)
        self.ui.comboBox_shenmozhanchang.activated.connect(self.shenmozhanchang_change)
        self.ui.checkBox_liandan2.clicked.connect(self.liandan2_change)
        self.ui.checkBox_liandan3.clicked.connect(self.liandan3_change)
        self.ui.comboBox_query_fenjie.activated.connect(self.query_fenjie_change)
        self.ui.comboBox_query_map.activated.connect(self.query_map_change)
        self.ui.comboBox_auto_filter.activated.connect(self.auto_filter_change)
        self.rf_ini()
        self.query_fenjie_change(False)
        self.ui.comboBox_guanwei_query.clear()
        self.ui.comboBox_guanwei_query.addItem(u'请选择地图')
        for ti in range(1, 34):
            self.ui.comboBox_guanwei_query.addItem(u'天-%d' % ti)

        self.ui.comboBox_guanwei_query.addItem(u'---------')
        for ti in range(1, 20):
            self.ui.comboBox_guanwei_query.addItem(u'鬼-%d' % ti)

        self.ui.comboBox_guanwei_query.addItem(u'---------')
        for ti in range(1, 16):
            self.ui.comboBox_guanwei_query.addItem(u'魔-%d' % ti)

        self.ui.comboBox_dadi_guanwei_query.clear()
        self.ui.comboBox_dadi_guanwei_query.addItem(u'请选择地图')
        for shentian in range(81):
            x = shentian / 9 + 1
            y = shentian % 9 + 1
            self.ui.comboBox_dadi_guanwei_query.addItem(u'%d-%d' % (x, y))

        self.ui.comboBox_daozhu_guanwei_query.clear()
        daozhu_name = [u'请选择地图', u'50|乙木', u'100|辰火', u'150|兑泽', u'200|坤地', u'250|巽风', u'300|艮山', 
         u'350|震雷', u'400|寅木', u'450|离火', u'500|乾阳', u'550|乾水', u'600|离木', 
         u'650|泽风', u'700|坤火', u'750|坎水', u'800|风雷', u'850|辰土', u'900|乾天', 
         u'1050|灵风', u'1100|匡御', u'1150|空生', u'1200|真所', u'1250|玄图', 
         u'1300|灵文', u'1350|精极', u'1400|神表', u'1450|华阳', u'1500|明灵', 
         u'1550|灵奥', u'1600|百咏', u'1650|天长', u'1700|大有', u'1750|十方', 
         u'1800|郁秀', u'1850|神极', u'1900|承天', u'2050|至阳', u'2100|天府', 
         u'2150|紫宫', u'2200|上星', u'2250|五灵', u'2300|神门', u'2350|天冲', 
         u'2400|天鼎', u'2450|中极', u'2500|天光', u'2550|天武', u'2600|紫云', 
         u'2650|七玄', u'2700|天华', u'2750|云庭', u'2800|灵业', u'2850|天机', 
         u'2900|真皇']
        for daozhu_index in range(len(daozhu_name)):
            self.ui.comboBox_daozhu_guanwei_query.addItem(daozhu_name[daozhu_index])

        for log_index in [1, 25]:
            self.logprint(u'-----------------修真辅助v8.5更新内容--------------------', log_index)
            self.logprint(u'1、增加混沌海第三片海的功能', log_index)
            self.logprint(u'2、增加佛国感悟指定某个地方功能，在辅助妖国狩猎旁边可设置', log_index)
            self.logprint(u'3、增加大帝和道主申官批官功能', log_index)
            self.logprint(u'4、大帝和道主挑战设置旁边，增加龙玉领取和使用的功能', log_index)
            self.logprint(u'5、修复混沌海须弥鼎自动炼须弥石可能无效的BUG', log_index)
            self.logprint(u'------------------------------------------------------------', log_index)

        self.help_tongyong()
        self.print_daotongpeiyang_info()
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        try:
            print u'当前程序路径：', dirname
            filelist = os.listdir(dirname + '\\maps\\')
            self.key_list = []
            for file in filelist:
                map_id = int(file.split('.')[0])
                self.key_list.append(map_id)

            self.shoushua_list = os.listdir(dirname + '\\shoushua_maps\\')
            if self.ui.checkBox_open_auto_login.checkState() == 2:
                self.loginGame()
        except:
            QtGui.QMessageBox.about(self, u'辅助出错', u'请检查有没有maps文件夹和maps文件夹里有无中文名文件')

        return

    def eventFilter(self, obj, event):
        if obj in self.hundunhai_button_list:
            if event.type() == QEvent.Enter:
                self.button_enter_fun(obj)
            elif event.type() == QEvent.Leave:
                self.button_leave_fun()
        return QtGui.QMainWindow.eventFilter(self, obj, event)

    def closeEvent(self, event):
        print u'程序关闭'
        self.stopLiandan()
        self.stopGuaji()
        game.flag_tuichu = True
        QCoreApplication.quit()
        sys.exit(0)
        return

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print u'隐藏程序'
            self.hide()
        return

    def makesure(self, body):
        reply = QMessageBox.question(self, self.tr(u'提醒'), self.tr(body), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

        return

    def set_game_flag(self):
        global zidongchonglian
        if self.ui.checkBox_diertianshangxian.checkState() == 2:
            game.kamanshouyi = True
        else:
            game.kamanshouyi = False
        if self.ui.checkBox_zidonglunhuifahui.checkState() == 2:
            game.flag_lunhuifahui = True
        else:
            game.flag_lunhuifahui = False
        if self.ui.checkBox_zidongchonglian.checkState() == 2:
            zidongchonglian = True
            self.ui.checkBox_diertianshangxian.setVisible(True)
            self.ui.lineEdit_after_hour.setVisible(True)
            self.ui.label_0dianshangxian.setVisible(True)
        else:
            zidongchonglian = False
            self.ui.checkBox_diertianshangxian.setVisible(False)
            self.ui.lineEdit_after_hour.setVisible(False)
            self.ui.label_0dianshangxian.setVisible(False)
        if self.ui.checkBox_zidongfudan.checkState() == 2:
            game.flag_zidongfudan = True
        else:
            game.flag_zidongfudan = False
        if self.ui.checkBox_zidongzhongtian.checkState() == 2:
            game.flag_zidongzhongtian = True
        else:
            game.flag_zidongzhongtian = False
        if self.ui.checkBox_zhidayao.checkState() == 2:
            game.flag_zhidayao = True
            self.ui.checkBox_zhidagui.setCheckState(0)
            game.flag_zhidagui = False
        else:
            game.flag_zhidayao = False
        if self.ui.checkBox_zhidagui.checkState() == 2:
            game.flag_zhidagui = True
            self.ui.checkBox_zhidayao.setCheckState(0)
            game.flag_zhidayao = False
        else:
            game.flag_zhidagui = False
        if self.ui.checkBox_gongdeche.checkState() == 2:
            game.flag_gongdeche = True
        else:
            game.flag_gongdeche = False
        if self.ui.checkBox_yuyue59xingjun.checkState() == 2:
            game.flag_yuyue59xingjun = True
        else:
            game.flag_yuyue59xingjun = False
            self.set_xingjun_button(True)
        if self.ui.checkBox_yuyue59lingmai.checkState() == 2:
            game.flag_yuyue59lingmai = True
        else:
            game.flag_yuyue59lingmai = False
            self.set_lingmai_button(True)
        if self.ui.checkBox_yuyue59tianshen.checkState() == 2:
            game.flag_yuyue59tianshen = True
        else:
            game.flag_yuyue59tianshen = False
            self.set_tianshen_button(True)
        if self.ui.checkBox_yuyue59dianzhu.checkState() == 2:
            game.flag_yuyue59dianzhu = True
        else:
            game.flag_yuyue59dianzhu = False
            self.set_dianzhu_button(True)
        if self.ui.checkBox_lianxutoutu.checkState() == 2:
            game.flag_lianxutoutu = True
        else:
            game.flag_lianxutoutu = False
        if self.ui.checkBox_xuefutu.checkState() == 2:
            game.flag_xuefutu = True
        else:
            game.flag_xuefutu = False
        if self.ui.checkBox_baoliuyifu.checkState() == 2:
            game.flag_baoliuyifu = True
        else:
            game.flag_baoliuyifu = False
        if self.ui.checkBox_duihuantisicaoren.checkState() == 2:
            game.flag_duihuantisicaoren = True
        else:
            game.flag_duihuantisicaoren = False
        if self.ui.checkBox_duihuantianfudai.checkState() == 2:
            game.flag_duihuantianfudai = True
        else:
            game.flag_duihuantianfudai = False
        if self.ui.checkBox_duihuanlongfengbi.checkState() == 2:
            game.flag_duihuanlongfengbi = True
        else:
            game.flag_duihuanlongfengbi = False
        if self.ui.checkBox_zidongshilian.checkState() == 2:
            game.flag_zidongshilian = True
        else:
            game.flag_zidongshilian = False
        if self.ui.checkBox_hdh_phcl.checkState() == 2:
            game.flag_hdh_phcl = True
        else:
            game.flag_hdh_phcl = False
        if self.ui.checkBox_youxianfugui.checkState() == 2:
            game.flag_youxianfugui = True
        else:
            game.flag_youxianfugui = False
        if self.ui.checkBox_yanyu_zidongtansuo.checkState() == 2:
            game.flag_yanyu_zidongtansuo = True
            self.ui.comboBox_hundunhai_cur_tansuo.setEnabled(False)
            self.ui.comboBox_hundunhai_next_tansuo.setEnabled(False)
        else:
            game.flag_yanyu_zidongtansuo = False
            self.ui.comboBox_hundunhai_cur_tansuo.setEnabled(True)
            self.ui.comboBox_hundunhai_next_tansuo.setEnabled(True)
        if self.ui.checkBox_dier_shengshentong.checkState() == 2:
            game.flag_dier_shengshentong = True
            self.ui.comboBox_dier_shentong_1.setVisible(True)
            self.ui.comboBox_dier_shentong_2.setVisible(True)
            self.ui.comboBox_dier_shentong_3.setVisible(True)
        else:
            game.flag_dier_shengshentong = False
            self.ui.comboBox_dier_shentong_1.setVisible(False)
            self.ui.comboBox_dier_shentong_2.setVisible(False)
            self.ui.comboBox_dier_shentong_3.setVisible(False)
        if self.ui.checkBox_duihuan_xiantian_daowen.checkState() == 2:
            game.flag_duihuan_xiantian_daowen = True
        else:
            game.flag_duihuan_xiantian_daowen = False
        if self.ui.checkBox_tuiyan_hundun_daotu.checkState() == 2:
            game.flag_tuiyan_hundun_daotu = True
        else:
            game.flag_tuiyan_hundun_daotu = False
        if self.ui.checkBox_auto_yanghundan.checkState() == 2:
            game.flag_auto_yanghundan = True
        else:
            game.flag_auto_yanghundan = False
        if self.ui.checkBox_auto_lianqi.checkState() == 2:
            game.flag_auto_lianqi = True
        else:
            game.flag_auto_lianqi = False
        if self.ui.checkBox_auto_huntianxiandan.checkState() == 2:
            game.flag_auto_huntianxiandan = True
        else:
            game.flag_auto_huntianxiandan = False
        if self.ui.checkBox_auto_xueshaxiandan.checkState() == 2:
            game.flag_auto_xueshaxiandan = True
        else:
            game.flag_auto_xueshaxiandan = False
        if self.ui.checkBox_zidongtiaozhandadi.checkState() == 2:
            game.flag_zidongtiaozhandadi = True
        else:
            game.flag_zidongtiaozhandadi = False
        if self.ui.checkBox_zidonggongde.checkState() == 2:
            game.flag_zidonggongde = True
        else:
            game.flag_zidonggongde = False
        if self.ui.checkBox_zidongshengdizi.checkState() == 2:
            game.flag_zidongshengdizi = True
        else:
            game.flag_zidongshengdizi = False
        if self.ui.checkBox_zidongmenpailingwu.checkState() == 2:
            game.flag_zidongmenpailingwu = True
        else:
            game.flag_zidongmenpailingwu = False
        if self.ui.checkBox_zidongzongmenjindi.checkState() == 2:
            game.flag_zidongzongmenjindi = True
        else:
            game.flag_zidongzongmenjindi = False
        if self.ui.checkBox_zidongtongguantiaozhan.checkState() == 2:
            game.flag_zidongtongguantiaozhan = True
        else:
            game.flag_zidongtongguantiaozhan = False
        if self.ui.checkBox_zidongganwutiandao.checkState() == 2:
            game.flag_zidongganwutiandao = True
        else:
            game.flag_zidongganwutiandao = False
        if self.ui.checkBox_zidongmaicha.checkState() == 2:
            game.flag_zidongmaicha = True
        else:
            game.flag_zidongmaicha = False
        if self.ui.checkBox_zongmenkuangmai.checkState() == 2:
            game.flag_zongmenkuangmai = True
        else:
            game.flag_zongmenkuangmai = False
        if self.ui.checkBox_zidongshenmu.checkState() == 2:
            game.flag_zidongshenmu = True
        else:
            game.flag_zidongshenmu = False
        if self.ui.checkBox_zidongtianxiang.checkState() == 2:
            game.flag_zidongtianxiang = True
        else:
            game.flag_zidongtianxiang = False
        if self.ui.checkBox_daozhu_zhanweizhi.checkState() == 2:
            game.flag_daozhu_zhanweizhi = True
        else:
            game.flag_daozhu_zhanweizhi = False
        if self.ui.checkBox_dadi_zhanweizhi.checkState() == 2:
            game.flag_dadi_zhanweizhi = True
        else:
            game.flag_dadi_zhanweizhi = False
        if self.ui.checkBox_jiezhu_zhanweizhi.checkState() == 2:
            game.flag_jiezhu_zhanweizhi = True
        else:
            game.flag_jiezhu_zhanweizhi = False
        if self.ui.checkBox_tianshen_5ci.checkState() == 2:
            game.flag_tianshen_5ci = True
        else:
            game.flag_tianshen_5ci = False
        if self.ui.checkBox_lingmai_5ci.checkState() == 2:
            game.flag_lingmai_5ci = True
        else:
            game.flag_lingmai_5ci = False
        if self.ui.checkBox_aotu_longyu.checkState() == 2:
            game.flag_aotu_longyu = True
        else:
            game.flag_aotu_longyu = False
        return

    def addmijing(self):
        text = self.ui.comboBox_mijing.currentText()
        add_flag = True
        for i in range(self.ui.listWidget_mijing.count()):
            if text == self.ui.listWidget_mijing.item(i).text():
                add_flag = False

        if add_flag:
            self.ui.listWidget_mijing.addItem(text)
            self.set_mijing_list()
        else:
            QtGui.QMessageBox.information(self, u'错误', u'请不要重复添加!')
        return

    def delmijing(self):
        if self.ui.listWidget_mijing.currentRow() != -1:
            item_deleted = self.ui.listWidget_mijing.takeItem(self.ui.listWidget_mijing.currentRow())
            item_deleted = None
            self.set_mijing_list()
        return

    def set_mijing_list(self):
        game.mijing_list = []
        mijing_conf = ''
        for i in range(self.ui.listWidget_mijing.count()):
            index = self.ui.comboBox_mijing.findText(self.ui.listWidget_mijing.item(i).text())
            game.mijing_list.append(index)
            mijing_conf += str(index) + ','

        cfg_set('guaji', 'mijing', mijing_conf[:-1])
        return

    def get_fangan_filename(self):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        index = self.ui.comboBox_guajifangan.currentIndex()
        return dirname + '\\zidingyi\\fangan%d.txt' % (index + 1)

    def add_file_line(self, text):
        filename = self.get_fangan_filename()
        lines = rf_lines(filename)
        lines.append(text)
        wf_lines(filename, lines)
        return

    def del_file_line(self, row):
        filename = self.get_fangan_filename()
        lines = rf_lines(filename)
        del lines[row]
        wf_lines(filename, lines)
        return

    def modify_file_line(self, row, text):
        filename = self.get_fangan_filename()
        lines = rf_lines(filename)
        lines[row] = text
        wf_lines(filename, lines)
        return

    def get_one_shuatu_text(self):
        leixing = self.ui.comboBox_guajileixing.currentIndex()
        index = self.ui.comboBox_ditujibie_shua.currentIndex()
        currentText = self.ui.comboBox_ditujibie_shua.currentText().split('-')
        if leixing == 0:
            map_name = str(self.chuqiao_list[index])
        else:
            map_name = currentText[0] + '-' + currentText[1]
        cishu_index = self.ui.comboBox_shuatucishu.currentIndex()
        cishu = int(self.ui.lineEdit_shuatucishu.text())
        text = '%d,%s,%d,%d' % (leixing, map_name, cishu_index, cishu)
        return text

    def addmap(self):
        text = self.get_one_shuatu_text()
        if text != '':
            self.add_file_line(text)
            self.update_shuatu_list()
        return

    def modifymap(self):
        text = self.get_one_shuatu_text()
        row = self.ui.listWidget_shuatu.currentRow()
        if row != -1:
            self.modify_file_line(row, text)
            self.update_shuatu_list()
        return

    def delmap(self):
        row = self.ui.listWidget_shuatu.currentRow()
        if row != -1:
            self.del_file_line(row)
            self.update_shuatu_list()
        return

    def get_value_by_text(self, text):
        temp = text.split(',')
        leixing = int(temp[0])
        map_id = temp[1]
        cishu_index = int(temp[2])
        cishu = int(temp[3])
        return (leixing, map_id, cishu_index, cishu)

    def listWidget_shuatu_clicked(self):
        row = self.ui.listWidget_shuatu.currentRow()
        filename = self.get_fangan_filename()
        lines = rf_lines(filename)
        text = lines[row]
        leixing, map_id, cishu_index, cishu = self.get_value_by_text(text)
        self.ui.comboBox_guajileixing.setCurrentIndex(leixing)
        self.guajileixing_change()
        if leixing == 0:
            index = self.chuqiao_list.index(int(map_id))
        else:
            index = int(map_id.split('-')[0])
        self.ui.comboBox_ditujibie_shua.setCurrentIndex(index)
        self.ui.comboBox_shuatucishu.setCurrentIndex(cishu_index)
        self.ui.lineEdit_shuatucishu.setText(str(cishu))
        self.shuatucishu_change()
        return

    def get_shoushua_map_name(self, map_id):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        filelist = os.listdir(dirname + '\\shoushua_maps\\')
        for file in filelist:
            file = file.replace('.txt', '')
            if file.find(map_id) > -1:
                return file.decode('GBK')

        return

    def update_shuatu_list(self):
        filename = self.get_fangan_filename()
        lines = rf_lines(filename)
        leixing_name = [
         u'出窍', u'手刷']
        self.ui.listWidget_shuatu.clear()
        for i in range(len(lines)):
            line = lines[i]
            leixing, map_id, cishu_index, cishu = self.get_value_by_text(line)
            cishu_name = [u'前一半', u'%d次' % cishu, u'保留最大轮数', u'卡满收益', u'后一半', u'全部']
            if leixing == 0:
                map_name = op.cailiao_map_name[int(map_id)]
            elif leixing == 1:
                map_name = self.get_shoushua_map_name(map_id)
            text = u'%s#%s#%s' % (leixing_name[leixing], map_name, cishu_name[cishu_index])
            self.ui.listWidget_shuatu.addItem(text)
            if self.step_status.has_key(i):
                if self.step_status[i] == 2:
                    self.ui.listWidget_shuatu.item(i).setTextColor(QColor('green'))
                elif self.step_status[i] == 1:
                    self.ui.listWidget_shuatu.item(i).setTextColor(QColor('blue'))
                else:
                    self.ui.listWidget_shuatu.item(i).setTextColor(QColor('red'))
            else:
                self.ui.listWidget_shuatu.item(i).setTextColor(QColor('red'))
            if cishu_index > 2:
                break

        return

    def settings_clicked(self, onoff):
        row = self.ui.listWidget_auto_info.currentRow()
        currentText = self.ui.listWidget_auto_info.item(row).text()
        index = int(currentText.split('#')[0].replace(' ', ''))
        cfg_set('auto', str(index), onoff)
        self.auto_filter_change()
        return

    def settings_on_clicked(self):
        self.settings_clicked('1')
        return

    def settings_off_clicked(self):
        self.settings_clicked('0')
        return

    def listWidget_auto_info_clicked(self):
        tips = {5: u'开启升聚灵阵，开启智能洞府，会智能升级，哪个上限不够升哪个；不开启智能洞府，为卡上限模式，不会升级草铁等级。先把草铁仆役加满最短时间挂满草铁，然后挂木头。', 6: u'开启升洗髓池，开启智能洞府，会智能升级，哪个上限不够升哪个；不开启智能洞府，为卡上限模式，不会升级草铁等级。先把草铁仆役加满最短时间挂满草铁，然后挂木头。', 7: u'开启智能洞府，关闭升聚灵阵、升洗髓池、升炼体池，即为肉木模式。', 8: u'刚开区进去，送肉，木头加满也消耗不掉。此模式会按照刚好消耗肉的方式升级木头的。也就是说本来可以升肉了，但是肉满了，于是先升木头消耗肉。', 11: u'自动门派修炼如果掌门有次数会一起开启。', 21: u'14点之后打的目的是等着别人换位置了，当天可以打一次，多点进度。如果凌晨打可能对方还没换位置，自己打了，比别人进度慢一天。', 22: u'背包空位大于12的时候，才会自动洗劫，防止丢失物品。如果背包位置紧张，还需要手动洗劫。', 63: u'此路线为直线，仅供佛系玩家使用', 24: u'辅助只会在收到邮件的时候领取一次，如果背包太小领取不了，那就自己想办法清理背包或者把背包弄大点。', 26: u'此功能只升级等级，不会点下面的技能，技能升级需要自己手动点。', 27: u'此功能凌晨购买没问题，中午刷新后有时候会不买，不放心的一定自己上号去看一下。', 28: u'此功能凌晨购买没问题，中午刷新后有时候会不买，不放心的一定自己上号去看一下。', 30: u'有玩家在偷仙界、鬼界、魔界、神界之门前，攒够刚好的声望进去，然后把声望换门派用掉，然后再去偷，因此需要攒着不吃声望。', 31: u'为了领悟7、8、9品丹方，刻意不吃炼丹心得，卡炼丹等级。前期可以在门派里学习熟练度升级炼丹等级，那么可以攒下心得，等门派无法提升炼丹等级了，再吃心得可以比别人级别高一些。', 36: u'手动会绕路走，按怪物从弱到强的方式打，无需担心。', 37: u'手动会绕路走，按怪物从弱到强的方式打，无需担心。', 38: u'手动会绕路走，按怪物从弱到强的方式打，无需担心。', 32: u'前期可以在门派里学习熟练度升级炼器等级，那么可以攒下心得，等门派无法提升炼器等级了，再吃心得可以比别人级别高一些。', 41: u'福地小世界一天只能进一次，开启这个不用再手动偷了。', 51: u'宗主、副宗主免费，其他成员需要花费上灵，慎选。', 52: u'血浮屠只有最高级才能够灵石兑换声望高于1:1，前期血浮屠还不如每天2次5000灵石换5000声望，建议开区就开启。', 60: u'此功能未检测是否已经学会，退出再进相同门派后，开启的话可能会再兑换一次，自己要注意及时关闭。', 61: u'专治手抖。', 62: u'洗劫三层不要看防御，要看攻击。怪4500万血，50回合打死，理论上攻击起码得50万以上再说', 63: u'此路线为直线，仅供佛系玩家使用', 64: u'此路线为直线，仅供佛系玩家使用', 70: u'这个是免费的那个修炼', 79: u'自动打能打得过的灵脉，如果没灵脉，就打矿脉', 88: u'氪金买了青云诀的就开启这个增加加成', 89: u'大神强渡专用', 91: u'国家多了之后，每天消耗灵石巨大，慎选', 93: u'有人要攒着等入了宗门再用', 96: u'炼体池总共10级，升满了请关闭此选项。', 100: u'我也不懂为啥要晚点，总之懂的就开，不懂的就关掉。', 103: u'识别吃天元丹情况，没吃满的从低到高挨个炼', 104: u'识别吃地元丹情况，没吃满的从低到高挨个炼', 107: u'请在宠物界面设置战斗宠物。', 110: u'前期不要选。', 111: u'开启会在法会开启的时候买对应的信物，本身有这个信物的可以等用掉了再开启，不然会一直有信物占背包。', 112: u'开启会在法会开启的时候买对应的信物，本身有这个信物的可以等用掉了再开启，不然会一直有信物占背包。', 113: u'开启会在法会开启的时候买对应的信物，本身有这个信物的可以等用掉了再开启，不然会一直有信物占背包。', 114: u'开启会在法会开启的时候买对应的信物，本身有这个信物的可以等用掉了再开启，不然会一直有信物占背包。', 115: u'开启会在法会开启的时候买对应的信物，本身有这个信物的可以等用掉了再开启，不然会一直有信物占背包。', 117: u'为方便换材料，12点之后再自动打。另外征服度到达250就不会再打了。', 118: u'如果后期只想合成本命换白妖丹，118、119、127三个可以一起开启。', 119: u'只兑换第一本命，不包含辅助本命。', 121: u'这个功能是为了第二天手动先培养再派遣。', 122: u'接车用。'}
        row = self.ui.listWidget_auto_info.currentRow()
        currentText = self.ui.listWidget_auto_info.item(row).text()
        index = int(currentText.split('#')[0].replace(' ', ''))
        if index == 86:
            self.logprint(tips[index], 51)
        elif index in tips.keys():
            self.logprint(tips[index], 3)
        if cfg_get('auto', str(index)) == '1':
            self.ui.pushButton_settings_on.setEnabled(False)
            self.ui.pushButton_settings_off.setEnabled(True)
        else:
            self.ui.pushButton_settings_on.setEnabled(True)
            self.ui.pushButton_settings_off.setEnabled(False)
        return

    def update_auto_list(self):
        del game.settings_on[:]
        count = self.ui.listWidget_auto_info.count()
        for i in range(count):
            currentText = self.ui.listWidget_auto_info.item(i).text()
            index = int(currentText.split('#')[0].replace(' ', ''))
            if cfg_get('auto', str(index)) == '1':
                game.settings_on.append(index)
                self.ui.listWidget_auto_info.item(i).setText(currentText.replace(' ', ''))
                self.ui.listWidget_auto_info.item(i).setTextColor(QColor('green'))
            else:
                self.ui.listWidget_auto_info.item(i).setText(u'    ' + currentText.replace(' ', ''))
                self.ui.listWidget_auto_info.item(i).setTextColor(QColor('red'))

        print game.settings_on
        self.ui.pushButton_settings_on.setEnabled(False)
        self.ui.pushButton_settings_off.setEnabled(False)
        return

    def filter_auto_by_list(self, show_list):
        count = self.ui.listWidget_auto_info.count()
        for index in range(count):
            if index not in show_list:
                self.ui.listWidget_auto_info.item(index).setTextColor(QColor('white'))

        return

    def auto_filter_change(self):
        show_list_list = [[], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 44, 88, 96, 97, 109, 116, 
          121],
         [
          11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 55, 
          56, 57, 58, 59, 60, 65, 110, 111, 112, 113, 114, 
          115],
         [
          29, 30, 31, 32, 33, 44, 45, 46, 73, 93, 101, 
          105, 119],
         [
          34, 35, 36, 37, 38, 39, 47, 48, 49, 50, 63, 
          64, 87],
         [
          15, 20, 36, 37, 38, 48, 49, 50, 63, 64, 65, 
          66, 67, 68, 69, 74, 75, 76, 80, 81, 82, 83, 84, 
          85, 98, 99],
         [
          27, 28, 52, 53, 54, 60, 71, 86, 94, 98, 111, 
          112, 113, 114, 115, 118],
         [
          71, 72, 73, 80, 81, 82, 90, 91, 92, 98, 99, 
          100, 101],
         [
          47, 48, 49, 50, 51, 72, 87, 92, 95, 99],
         [
          21, 100, 105, 108, 121, 122, 125]]
        index = self.ui.comboBox_auto_filter.currentIndex()
        self.update_auto_list()
        if index > 0:
            self.filter_auto_by_list(show_list_list[index])
        return

    def read_skill_order(self):
        leixing_order = cfg_get('guaji', 'skill_order')
        game.leixing_order = leixing_order.split(',')
        self.update_skill_list()
        return

    def skill_order_up(self):
        row = self.ui.listWidget_skillorder.currentRow()
        if row >= 1:
            temp = game.leixing_order[row - 1]
            game.leixing_order[row - 1] = game.leixing_order[row]
            game.leixing_order[row] = temp
            cfg_set('guaji', 'skill_order', (',').join(game.leixing_order))
            self.update_skill_list()
        return

    def skill_order_down(self):
        row = self.ui.listWidget_skillorder.currentRow()
        count = self.ui.listWidget_skillorder.count()
        if row < count - 1 and row >= 0:
            temp = game.leixing_order[row + 1]
            game.leixing_order[row + 1] = game.leixing_order[row]
            game.leixing_order[row] = temp
            cfg_set('guaji', 'skill_order', (',').join(game.leixing_order))
            self.update_skill_list()
        return

    def skill_order_delete(self):
        row = self.ui.listWidget_skillorder.currentRow()
        if row >= 0:
            del game.leixing_order[row]
            cfg_set('guaji', 'skill_order', (',').join(game.leixing_order))
            self.update_skill_list()
        return

    def skill_order_reset(self):
        if 61 in game.settings_on:
            if self.makesure(u'是否要重置技能升级顺序？'):
                game.leixing_order = [
                 '2', '1', '5', '4', '13', 
                 '10', '3', '12']
                cfg_set('guaji', 'skill_order', (',').join(game.leixing_order))
                self.update_skill_list()
        else:
            game.leixing_order = [
             '2', '1', '5', '4', '13', '10', '3', 
             '12']
            cfg_set('guaji', 'skill_order', (',').join(game.leixing_order))
            self.update_skill_list()
        return

    def skill_order_clicked(self):
        self.ui.pushButton_skill_order_up.setEnabled(True)
        self.ui.pushButton_skill_order_down.setEnabled(True)
        self.ui.pushButton_skill_order_delete.setEnabled(True)
        return

    def update_skill_list(self):
        leixing_name = {2: u'灵气', 1: u'修为', 5: u'防御', 4: u'攻击', 13: u'生命', 10: u'闪避', 3: u'速度', 12: u'雷抗'}
        text = self.ui.listWidget_skillorder.clear()
        self.ui.listWidget_skillorder.setStyleSheet('QListWidget{border:1px solid gray; color:black; }QListWidget::item:selected{background:blue; }')
        list_font = QFont()
        list_font.setPointSize(15)
        list_font.setBold(False)
        list_font.setWeight(50)
        self.ui.listWidget_skillorder.setFont(list_font)
        print game.leixing_order
        for leixing in game.leixing_order:
            text = self.ui.listWidget_skillorder.addItem(leixing_name[int(leixing)])

        self.ui.pushButton_skill_order_up.setEnabled(False)
        self.ui.pushButton_skill_order_down.setEnabled(False)
        self.ui.pushButton_skill_order_delete.setEnabled(False)
        return

    def get_shijian_name(self, place, shijian):
        didian_name = [u'', u'赤霄天', u'碧霄天', u'青霄天', u'玄霄天', u'玉霄天', u'琅霄天', u'紫霄天', u'火霄天', 
         u'神霄天']
        shijian_name = [u'', u'仙防', u'魔防', u'鬼防', u'释防', u'妖防', u'仙攻', u'魔攻', u'鬼攻', u'释攻', 
         u'妖攻', u'太易之石-深入探索', u'太易之石-浅尝辄止', u'太初之石-深入探索', u'太初之石-浅尝辄止', 
         u'太始之石-深入探索', u'太始之石-浅尝辄止', u'太极之石-深入探索', u'太极之石-浅尝辄止', u'太素之石-深入探索', 
         u'太素之石-浅尝辄止']
        return u'%s-%s' % (didian_name[place], shijian_name[shijian])

    def add_shenmo_shijian(self):
        place = self.ui.comboBox_shenmozhanchang_didian.currentIndex()
        shijian = self.ui.comboBox_shenmozhanchang_shijian.currentIndex()
        save_code = '%d-%d' % (place, shijian)
        save_code_all = cfg_get('shenjie', 'shenmo_shijian')
        if len(save_code_all) > 1:
            save_code_list = save_code_all.split(',')
            if save_code in save_code_list:
                QtGui.QMessageBox.information(self, u'错误', u'请不要重复添加!')
                return
            save_code_all += ',' + save_code
        else:
            save_code_all = save_code
        cfg_set('shenjie', 'shenmo_shijian', save_code_all)
        self.update_shenmo_shijian_list()
        return

    def remove_shenmo_shijian(self):
        index = self.ui.listWidget_shenmozhanchang_shijian.currentRow()
        if index != -1:
            save_code_all = cfg_get('shenjie', 'shenmo_shijian')
            if len(save_code_all) > 0:
                save_code_list = save_code_all.split(',')
                del save_code_list[index]
                cfg_set('shenjie', 'shenmo_shijian', (',').join(save_code_list))
                self.update_shenmo_shijian_list()
        return

    def update_shenmo_shijian_list(self):
        game.shenmozhanchang_shijian_list = []
        self.ui.listWidget_shenmozhanchang_shijian.clear()
        save_code_all = cfg_get('shenjie', 'shenmo_shijian')
        if len(save_code_all) > 2:
            save_code_list = save_code_all.split(',')
            for save_code in save_code_list:
                place = int(save_code.split('-')[0])
                shijian = int(save_code.split('-')[1])
                game.shenmozhanchang_shijian_list.append([place, shijian])
                text = self.get_shijian_name(place, shijian)
                self.ui.listWidget_shenmozhanchang_shijian.addItem(text)

        return

    def update_pet_info(self):
        self.ui.listWidget_chongwu.clear()
        state_text = [u'    ', u'    ', u'-骑乘中', u'-出战中']
        move_type_name = [u'', u'陆行', u'飞行', u'御海']
        can_ride_text = [u'不可骑乘', u'可骑乘']
        for key in game.pet_dict.keys():
            move_type, level, speed, name, can_ride, state = game.pet_dict[key]
            text = u'%d|[%d级]%s%s\n            [%s:%d]  [%s]' % (key, level, name, state_text[state], move_type_name[move_type], speed, can_ride_text[can_ride])
            self.ui.listWidget_chongwu.addItem(text)

        return

    def get_chongwu_index(self):
        row = self.ui.listWidget_chongwu.currentRow()
        if row >= 0:
            currentText = self.ui.listWidget_chongwu.item(row).text()
            index = int(currentText.split('|')[0])
            print 'index =', index
            return index
        else:
            return -1

        return

    def chongwu_action(self, action):
        global game_obj
        index = self.get_chongwu_index()
        if index >= 0:
            game_obj.chongwu_action(action, index)
        else:
            QtGui.QMessageBox.information(self, u'错误', u'没有选中宠物!')
        return

    def chongwu_chuzhan(self):
        self.chongwu_action(2)
        return

    def chongwu_qicheng(self):
        self.chongwu_action(1)
        return

    def chongwu_xiuxi(self):
        self.chongwu_action(0)
        return

    def update_chongwu_lable(self, type, index):
        lable_list = [self.ui.label_zhandou_chongwu, self.ui.label_luxing_chongwu, self.ui.label_feixing_chongwu, self.ui.label_yuhai_chongwu]
        pet_type_name = [u'战斗', u'陆行', u'飞行', u'御海']
        if index == 0:
            lable_list[type].setText(u'%s宠物:未设置' % pet_type_name[type])
        else:
            not_found = True
            for key in game.pet_dict.keys():
                if index == key:
                    not_found = False
                    move_type, level, speed, name, can_ride, state = game.pet_dict[key]
                    if type == 0:
                        lable_list[type].setText(u'%s宠物:%d|[等级:%d]%s' % (pet_type_name[type], key, level, name))
                    else:
                        lable_list[type].setText(u'%s宠物:%d|[速度:%d]%s' % (pet_type_name[type], key, speed, name))
                    return

            if not_found:
                lable_list[type].setText(u'%s宠物:设置的宠物未找到' % pet_type_name[type])
        return

    def set_zhandouchongwu(self):
        index = self.get_chongwu_index()
        game.index_zhandouchongwu = index
        cfg_set('chongwu', 'zhandou', str(index))
        self.update_chongwu_lable(0, index)
        return

    def set_luxingchongwu(self):
        index = self.get_chongwu_index()
        game.index_luxingchongwu = index
        cfg_set('chongwu', 'luxing', str(index))
        self.update_chongwu_lable(1, index)
        return

    def set_feixingchongwu(self):
        index = self.get_chongwu_index()
        game.index_feixingchongwu = index
        cfg_set('chongwu', 'feixing', str(index))
        self.update_chongwu_lable(2, index)
        return

    def set_yuhaichongwu(self):
        index = self.get_chongwu_index()
        game.index_yuhaichongwu = index
        cfg_set('chongwu', 'yuhai', str(index))
        self.update_chongwu_lable(3, index)
        return

    def quxiao_zhandouchongwu(self):
        game.index_zhandouchongwu = 0
        cfg_set('chongwu', 'zhandou', '0')
        self.update_chongwu_lable(0, 0)
        return

    def quxiao_luxingchongwu(self):
        game.index_luxingchongwu = 0
        cfg_set('chongwu', 'luxing', '0')
        self.update_chongwu_lable(1, 0)
        return

    def quxiao_feixingchongwu(self):
        game.index_feixingchongwu = 0
        cfg_set('chongwu', 'feixing', '0')
        self.update_chongwu_lable(2, 0)
        return

    def quxiao_yuhaichongwu(self):
        game.index_yuhaichongwu = 0
        cfg_set('chongwu', 'yuhai', '0')
        self.update_chongwu_lable(3, 0)
        return

    def zidongchonglian_change(self):
        cfg_set('guaji', 'zidongchonglian', str(self.ui.checkBox_zidongchonglian.checkState()))
        self.set_game_flag()
        return

    def diertianshangxian_change(self):
        cfg_set('login', 'diertianshangxian', str(self.ui.checkBox_diertianshangxian.checkState()))
        self.set_game_flag()
        return

    def zhidayao_change(self):
        cfg_set('guaji', 'zhidayao', str(self.ui.checkBox_zhidayao.checkState()))
        if self.ui.checkBox_zhidayao.checkState() == 2:
            self.ui.checkBox_zhidagui.setCheckState(0)
        self.set_game_flag()
        return

    def zhidagui_change(self):
        cfg_set('guaji', 'zhidagui', str(self.ui.checkBox_zhidagui.checkState()))
        if self.ui.checkBox_zhidagui.checkState() == 2:
            self.ui.checkBox_zhidayao.setCheckState(0)
        self.set_game_flag()
        return

    def xuefutu_change(self):
        cfg_set('fuben', 'xuefutu', str(self.ui.checkBox_xuefutu.checkState()))
        self.set_game_flag()
        return

    def comboBox_xuefutucengshu_change(self):
        index = self.ui.comboBox_xuefutucengshu.currentIndex()
        game.index_xuefutucengshu = index
        cfg_set('fuben', 'xuefutucengshu', str(index))
        return

    def comboBox_xuefutucishu_change(self):
        index = self.ui.comboBox_xuefutucishu.currentIndex()
        game.index_xuefutucishu = index
        cfg_set('fuben', 'xuefutucishu', str(index))
        return

    def chonglianshuatu_change(self):
        cfg_set('guaji', 'chonglianshuatu', str(self.ui.checkBox_chonglianshuatu.checkState()))
        return

    def yuyue59xingjun_change(self):
        cfg_set('guaji', 'yuyue59xingjun', str(self.ui.checkBox_yuyue59xingjun.checkState()))
        self.set_game_flag()
        return

    def yuyue59lingmai_change(self):
        cfg_set('guaji', 'yuyue59lingmai', str(self.ui.checkBox_yuyue59lingmai.checkState()))
        self.set_game_flag()
        return

    def yuyue59tianshen_change(self):
        cfg_set('guaji', 'yuyue59tianshen', str(self.ui.checkBox_yuyue59tianshen.checkState()))
        self.set_game_flag()
        return

    def yuyue59dianzhu_change(self):
        cfg_set('guaji', 'yuyue59dianzhu', str(self.ui.checkBox_yuyue59dianzhu.checkState()))
        self.set_game_flag()
        return

    def lianxutoutu_change(self):
        cfg_set('guaji', 'lianxutoutu', str(self.ui.checkBox_lianxutoutu.checkState()))
        self.set_game_flag()
        return

    def shenmozhanchang_change(self):
        index = self.ui.comboBox_shenmozhanchang.currentIndex()
        game.index_shenmozhanchang = index
        cfg_set('guaji', 'index_shenmozhanchang', str(index))
        return

    def zidongtiaozhandadi_change(self):
        state = self.ui.checkBox_zidongtiaozhandadi.checkState()
        cfg_set('guaji', 'zidongtiaozhandadi', str(state))
        self.set_game_flag()
        return

    def comboBox_tiaozhandadi_change(self):
        index = self.ui.comboBox_tiaozhandadi.currentIndex()
        game.index_tiaozhandadi = index
        cfg_set('guaji', 'index_tiaozhandadi', str(index))
        if index > 80:
            index = index - 80
        if game_obj.shengming > 10:
            self.ui.comboBox_query_fenjie.setCurrentIndex(13)
            self.query_fenjie_change(False)
            self.ui.comboBox_query_map.setCurrentIndex(index)
            self.query_map_change()
        return

    def liji_tiaozhan_dadi(self):
        index = self.ui.comboBox_tiaozhandadi.currentIndex()
        map_id = 1114 + index
        if index >= 81:
            map_id = 1115 + index - 81
        x_xingtian = (map_id - 1114) / 9 + 1
        y = (map_id - 1114) % 9 + 1
        if self.makesure(u'是否要挑战%d-%d?' % (x_xingtian, y)):
            game_obj.liji_tiaozhan_dadi(x_xingtian, map_id)
        return

    def tiaozhan_daozhu_change(self, is_query_daochang=True):
        index = self.ui.comboBox_tiaozhan_daozhu.currentIndex()
        game.index_tiaozhandaozhu = index
        cfg_set('guaji', 'index_tiaozhandaozhu', str(index))
        self.ui.textBrowser_query.clear()
        daozhu_id_list = [0, 5, 16, 19, 37, 40, 44, 50, 61, 63, 73, 80, 85, 88, 90, 100, 
         107, 115, 126, 139, 144, 151, 155, 167, 170, 172, 187, 
         190, 202, 213, 218, 223, 225, 228, 235, 240, 252, 257, 
         268, 272, 285, 289, 302, 305, 309, 316, 325, 328, 339, 
         342, 345, 359, 361, 366, 378]
        daozhu_id = daozhu_id_list[index]
        if daozhu_id not in game_obj.hundunhai_yitansuo_list:
            self.logprint(u'未探索', 192)
        if index > 0:
            self.ui.comboBox_query_fenjie.setCurrentIndex(14)
            self.query_fenjie_change(False)
            self.ui.comboBox_query_map.setCurrentIndex(index - 1)
            self.query_map_change()
            if is_query_daochang:
                game_obj.query_daochang(index)
        return

    def liji_tiaozhan_daozhu(self):
        index = self.ui.comboBox_tiaozhan_daozhu.currentIndex()
        text = self.ui.comboBox_tiaozhan_daozhu.currentText()
        if index > 0:
            if self.makesure(u'是否要挑战[%s]' % text):
                game_obj.liji_tiaozhan_daozhu(index)
        return

    def use_dadi_longyu(self):
        game_obj.use_item(10089, 1)
        return

    def use_daozhu_longyu(self):
        game_obj.use_item(10090, 1)
        return

    def baoliuyifu_change(self):
        cfg_set('guaji', 'baoliuyifu', str(self.ui.checkBox_baoliuyifu.checkState()))
        self.set_game_flag()
        return

    def youxianfugui_change(self):
        cfg_set('guaji', 'youxianfugui', str(self.ui.checkBox_youxianfugui.checkState()))
        self.set_game_flag()
        return

    def duihuantisicaoren_change(self):
        cfg_set('guaji', 'duihuantisicaoren', str(self.ui.checkBox_duihuantisicaoren.checkState()))
        self.set_game_flag()
        return

    def duihuantianfudai_change(self):
        cfg_set('guaji', 'duihuantianfudai', str(self.ui.checkBox_duihuantianfudai.checkState()))
        self.set_game_flag()
        return

    def duihuanlongfengbi_change(self):
        cfg_set('guaji', 'duihuanlongfengbi', str(self.ui.checkBox_duihuanlongfengbi.checkState()))
        self.set_game_flag()
        return

    def zidongshilian_change(self):
        cfg_set('guaji', 'zidongshilian', str(self.ui.checkBox_zidongshilian.checkState()))
        self.set_game_flag()
        return

    def hdh_phcl_change(self):
        cfg_set('guaji', 'hdh_phcl', str(self.ui.checkBox_hdh_phcl.checkState()))
        self.set_game_flag()
        return

    def yanyu_zidongtansuo_change(self):
        cfg_set('guaji', 'yanyu_zidongtansuo', str(self.ui.checkBox_yanyu_zidongtansuo.checkState()))
        self.set_game_flag()
        return

    def duihuan_xiantian_daowen_change(self):
        cfg_set('guaji', 'duihuan_xiantian_daowen', str(self.ui.checkBox_duihuan_xiantian_daowen.checkState()))
        self.set_game_flag()
        return

    def tuiyan_hundun_daotu_change(self):
        cfg_set('guaji', 'tuiyan_hundun_daotu', str(self.ui.checkBox_tuiyan_hundun_daotu.checkState()))
        self.set_game_flag()
        return

    def dier_shengshentong_change(self):
        cfg_set('guaji', 'dier_shengshentong', str(self.ui.checkBox_dier_shengshentong.checkState()))
        self.set_game_flag()
        game_obj.chakan_2_xiu()
        return

    def auto_yanghundan_change(self):
        cfg_set('guaji', 'auto_yanghundan', str(self.ui.checkBox_auto_yanghundan.checkState()))
        self.set_game_flag()
        return

    def auto_lianqi_change(self):
        cfg_set('guaji', 'auto_lianqi', str(self.ui.checkBox_auto_lianqi.checkState()))
        self.set_game_flag()
        return

    def auto_huntianxiandan_change(self):
        cfg_set('guaji', 'auto_huntianxiandan', str(self.ui.checkBox_auto_huntianxiandan.checkState()))
        self.set_game_flag()
        return

    def auto_xueshaxiandan_change(self):
        cfg_set('guaji', 'auto_xueshaxiandan', str(self.ui.checkBox_auto_xueshaxiandan.checkState()))
        self.set_game_flag()
        return

    def open_auto_login_change(self):
        cfg_set('guaji', 'open_auto_login', str(self.ui.checkBox_open_auto_login.checkState()))
        return

    def gongdeche_change(self):
        cfg_set('guaji', 'gongdeche', str(self.ui.checkBox_gongdeche.checkState()))
        self.set_game_flag()
        return

    def comboBox_gongdeche_change(self):
        index = self.ui.comboBox_gongdeche.currentIndex()
        game.index_gongdeche = index
        cfg_set('guaji', 'index_gongdeche', str(index))
        fenjie_index = 0
        map_index = 0
        if 0 <= index <= 31:
            fenjie_index = 5
            map_index = index + 1
        elif 32 <= index <= 64:
            fenjie_index = 5
            map_index = index - 32
        elif 66 <= index <= 84:
            fenjie_index = 6
            map_index = index - 66
        elif 86 <= index <= 100:
            fenjie_index = 7
            map_index = index - 86
        elif 101 <= index <= 118:
            fenjie_index = 6
            map_index = index - 100
        elif 119 <= index <= 132:
            fenjie_index = 7
            map_index = index - 118
        else:
            fenjie_index = 7
            map_index = 14
        if game_obj.shengming > 10 and fenjie_index > 0:
            self.ui.comboBox_query_fenjie.setCurrentIndex(fenjie_index)
            self.query_fenjie_change(False)
            self.ui.comboBox_query_map.setCurrentIndex(map_index)
            self.query_map_change()
        return

    def liji_tiaozhan_jiezhu(self):
        index = self.ui.comboBox_gongdeche.currentIndex()
        map_id = 0
        if 0 <= index <= 31:
            map_id = 1027 + index
        elif 32 <= index <= 64:
            map_id = 1026 + index - 32
        elif 66 <= index <= 84:
            map_id = 1060 + index - 66
        elif 86 <= index <= 100:
            map_id = 1080 + index - 86
        elif 101 <= index <= 118:
            map_id = 1061 + index - 101
        elif 119 <= index <= 132:
            map_id = 1081 + index - 119
        else:
            map_id = 0
        if map_id >= 1026:
            if self.makesure(u'确定要挑战[%s]吗？' % op.map_name[map_id]):
                game_obj.liji_tiaozhan_jiezhu(map_id)
        else:
            QtGui.QMessageBox.information(self, u'错误', u'未知错误，联系作者！')
        return

    def zidongtongguantiaozhan_change(self):
        state = self.ui.checkBox_zidongtongguantiaozhan.checkState()
        cfg_set('guaji', 'zidongtongguantiaozhan', str(state))
        self.set_game_flag()
        return

    def comboBox_tongguantiaozhan_change(self):
        index = self.ui.comboBox_tongguantiaozhan.currentIndex()
        game.index_tongguantiaozhan = index
        cfg_set('guaji', 'tongguantiaozhan', str(index))
        return

    def zidongganwutiandao_change(self):
        state = self.ui.checkBox_zidongganwutiandao.checkState()
        cfg_set('guaji', 'zidongganwutiandao', str(state))
        self.set_game_flag()
        return

    def comboBox_ganwutiandao_change(self):
        index = self.ui.comboBox_ganwutiandao.currentIndex()
        game.index_ganwutiandao = index
        cfg_set('guaji', 'ganwutiandao', str(index))
        return

    def zidongmaicha_change(self):
        state = self.ui.checkBox_zidongmaicha.checkState()
        cfg_set('guaji', 'zidongmaicha', str(state))
        self.set_game_flag()
        return

    def comboBox_zidongmaicha_change(self):
        index = self.ui.comboBox_zidongmaicha.currentIndex()
        game.index_zidongmaicha = index
        cfg_set('guaji', 'indexmaicha', str(index))
        return

    def zongmenkuangmai_change(self):
        state = self.ui.checkBox_zongmenkuangmai.checkState()
        cfg_set('guaji', 'zongmenkuangmai', str(state))
        self.set_game_flag()
        return

    def comboBox_zongmenkuangmai_change(self):
        index = self.ui.comboBox_zongmenkuangmai.currentIndex()
        game.index_zongmenkuangmai = index
        cfg_set('guaji', 'index_zongmenkuangmai', str(index))
        return

    def zidongshenmu_change(self):
        state = self.ui.checkBox_zidongshenmu.checkState()
        cfg_set('guaji', 'zidongshenmu', str(state))
        self.set_game_flag()
        return

    def comboBox_zidongshenmu_change(self):
        index = self.ui.comboBox_zidongshenmu.currentIndex()
        game.index_zidongshenmu = index
        cfg_set('guaji', 'index_shenmu', str(index))
        return

    def zidongzongmenjindi_change(self):
        state = self.ui.checkBox_zidongzongmenjindi.checkState()
        cfg_set('guaji', 'zidongzongmenjindi', str(state))
        self.set_game_flag()
        return

    def comboBox_zongmenjindi_change(self):
        index = self.ui.comboBox_zongmenjindi.currentIndex()
        game.index_zongmenjindi = index
        cfg_set('guaji', 'zongmenjindi', str(index))
        if index == 0:
            self.logprint(u'7星门派给[清灵草]', 3)
            self.logprint(u'8星门派给[太玄果+清灵草]', 3)
            self.logprint(u'9星门派给[太玄果+清灵草+醉龙草]', 3)
            self.logprint(u'10-11星给[太玄果+清灵草+醉龙草+活气果]', 3)
        elif index == 1:
            self.logprint(u'6星门派给[蓝晶石]', 3)
            self.logprint(u'7星门派给[蓝晶石+月冥石]', 3)
            self.logprint(u'8星门派给[蓝晶石+月冥石+青精石]', 3)
            self.logprint(u'9星门派给[蓝晶石+月冥石+青精石+黑曜石]', 3)
            self.logprint(u'10-11星给[蓝晶石+月冥石+青精石+黑曜石+万年铁精]', 3)
        else:
            self.logprint(u'6星门派给[5转金丹+劣质妖丹]', 3)
            self.logprint(u'7-8星门派给[6转金丹+劣质妖丹]', 3)
            self.logprint(u'9-10星门派给[劣质妖丹+白妖丹]', 3)
            self.logprint(u'11星门派给[劣质妖丹+白妖丹+绿妖丹]', 3)
        return

    def zidonglunhuifahui_change(self):
        cfg_set('guaji', 'zidonglunhuifahui', str(self.ui.checkBox_zidonglunhuifahui.checkState()))
        self.set_game_flag()
        return

    def comboBox_lunhuifahuidaguai_change(self):
        index = self.ui.comboBox_lunhuifahuidaguai.currentIndex()
        game.index_lunhuifahuidaguai = index
        cfg_set('guaji', 'lunhuifahuidaguai', str(index))
        return

    def zidonggongde_change(self):
        state = self.ui.checkBox_zidonggongde.checkState()
        cfg_set('guaji', 'zidonggongde', str(state))
        self.set_game_flag()
        return

    def comboBox_gongderenwu_change(self):
        index = self.ui.comboBox_gongderenwu.currentIndex()
        game.index_gongderenwu = index
        cfg_set('guaji', 'gongderenwu', str(index))
        return

    def zidongshengdizi_change(self):
        state = self.ui.checkBox_zidongshengdizi.checkState()
        cfg_set('guaji', 'zidongshengdizi', str(state))
        self.set_game_flag()
        return

    def comboBox_menpaidizijibie_change(self):
        index = self.ui.comboBox_menpaidizijibie.currentIndex()
        game.index_menpaidizijibie = index
        cfg_set('guaji', 'menpaidizijibie', str(index))
        return

    def zidongmenpailingwu_change(self):
        state = self.ui.checkBox_zidongmenpailingwu.checkState()
        cfg_set('guaji', 'zidongmenpailingwu', str(state))
        self.set_game_flag()
        return

    def comboBox_menpailingwuleixing_change(self):
        index = self.ui.comboBox_menpailingwuleixing.currentIndex()
        game.index_menpailingwuleixing = index
        cfg_set('guaji', 'menpailingwuleixing', str(index))
        return

    def zidongfudan_change(self):
        cfg_set('guaji', 'zidongfudan', str(self.ui.checkBox_zidongfudan.checkState()))
        self.set_game_flag()
        return

    def comboBox_fudanleixing_change(self):
        index = self.ui.comboBox_fudanleixing.currentIndex()
        game.index_fudanleixing = index
        cfg_set('guaji', 'fudanleixing', str(index))
        return

    def zidongzhongtian_change(self):
        cfg_set('guaji', 'zidongzhongtian', str(self.ui.checkBox_zidongzhongtian.checkState()))
        self.set_game_flag()
        return

    def comboBox_zhongzi_change(self):
        index = self.ui.comboBox_zhongzi.currentIndex()
        game.index_zhongzi = index
        cfg_set('guaji', 'zhongzi', str(index))
        return

    def daozhu_zhanweizhi_change(self):
        cfg_set('guaji', 'daozhu_zhanweizhi', str(self.ui.checkBox_daozhu_zhanweizhi.checkState()))
        self.set_game_flag()
        return

    def dadi_zhanweizhi_change(self):
        cfg_set('guaji', 'dadi_zhanweizhi', str(self.ui.checkBox_dadi_zhanweizhi.checkState()))
        self.set_game_flag()
        return

    def jiezhu_zhanweizhi_change(self):
        cfg_set('guaji', 'jiezhu_zhanweizhi', str(self.ui.checkBox_jiezhu_zhanweizhi.checkState()))
        self.set_game_flag()
        return

    def tianshen_5ci_change(self):
        cfg_set('guaji', 'tianshen_5ci', str(self.ui.checkBox_tianshen_5ci.checkState()))
        self.set_game_flag()
        return

    def lingmai_5ci_change(self):
        cfg_set('guaji', 'lingmai_5ci', str(self.ui.checkBox_lingmai_5ci.checkState()))
        self.set_game_flag()
        return

    def aotu_longyu_change(self):
        cfg_set('guaji', 'aotu_longyu', str(self.ui.checkBox_aotu_longyu.checkState()))
        self.set_game_flag()
        return

    def zidongtianxiang_change(self):
        cfg_set('guaji', 'zidongtianxiang', str(self.ui.checkBox_zidongtianxiang.checkState()))
        self.set_game_flag()
        return

    def comboBox_baoku_duihuan_cao_change(self):
        index = self.ui.comboBox_baoku_duihuan_cao.currentIndex()
        game.index_baoku_duihuan_cao = index
        cfg_set('guaji', 'index_baoku_duihuan_cao', str(index))
        return

    def comboBox_baoku_duihuan_kuang_change(self):
        index = self.ui.comboBox_baoku_duihuan_kuang.currentIndex()
        game.index_baoku_duihuan_kuang = index
        cfg_set('guaji', 'index__baoku_duihuan_kuang', str(index))
        return

    def comboBox_tianxiangleixing_change(self):
        index = self.ui.comboBox_tianxiangleixing.currentIndex()
        game.index_tianxiangleixing = index
        cfg_set('guaji', 'tianxiangleixing', str(index))
        return

    def comboBox_yunyangxiantian_change(self):
        index = self.ui.comboBox_yunyangxiantian.currentIndex()
        game.index_yunyangxiantian = index
        cfg_set('guaji', 'index_yunyangxiantian', str(index))
        return

    def comboBox_foguoganwu_change(self):
        index = self.ui.comboBox_foguoganwu.currentIndex()
        game.index_foguoganwu = index
        cfg_set('guaji', 'index_foguoganwu', str(index))
        return

    def comboBox_shuidaotong_work_change(self):
        index = self.ui.comboBox_shuidaotong_work.currentIndex()
        game.index_shuidaotong_work = index
        cfg_set('guaji', 'index_shuidaotong_work', str(index))
        return

    def comboBox_change_twt_fahui_change(self):
        index = self.ui.comboBox_change_twt_fahui.currentIndex()
        game.index_change_twt_fahui = index
        cfg_set('guaji', 'index_change_twt_fahui', str(index))
        game_obj.query_twt_fahui()
        return

    def comboBox_2_chuqiaoditu_change(self):
        index = self.ui.comboBox_2_chuqiaoditu.currentIndex()
        game.index_2_chuqiaoditu = index
        cfg_set('guaji', 'index_2_chuqiaoditu', str(index))
        return

    def comboBox_liandan_stop_type_change(self):
        index = self.ui.comboBox_liandan_stop_type.currentIndex()
        game.index_liandan_stop_type = index
        cfg_set('guaji', 'index_liandan_stop_type', str(index))
        return

    def comboBox_2_shengjimoshi_change(self):
        index = self.ui.comboBox_2_shengjimoshi.currentIndex()
        game.index_2_shengjimoshi = index
        cfg_set('guaji', 'index_2_shengjimoshi', str(index))
        return

    def comboBox_2_xiu_mode_change(self):
        index = self.ui.comboBox_2_xiu_mode.currentIndex()
        game.index_2_xiu_mode = index
        cfg_set('guaji', 'index_2_xiu_mode', str(index))
        game_obj.chakan_2_xiu()
        return

    def comboBox_shengdaotu_level_change(self):
        index = self.ui.comboBox_shengdaotu_level.currentIndex()
        game.index_shengdaotu_level = index
        cfg_set('guaji', 'index_shengdaotu_level', str(index))
        game_obj.show_daotu()
        return

    def comboBox_tourujingxue_change(self):
        index = self.ui.comboBox_tourujingxue.currentIndex()
        game.index_tourujingxue = index
        cfg_set('guaji', 'index_tourujingxue', str(index))
        return

    def comboBox_show_yellowtide_change(self):
        index = self.ui.comboBox_show_yellowtide.currentIndex()
        game.index_show_yellowtide = index
        cfg_set('guaji', 'index_show_yellowtide', str(index))
        game_obj.refresh_yellowtide()
        return

    def comboBox_auto_lingyan_mode_change(self):
        index = self.ui.comboBox_auto_lingyan_mode.currentIndex()
        game.index_auto_lingyan_mode = index
        cfg_set('guaji', 'index_auto_lingyan_mode', str(index))
        return

    def comboBox_auto_yellowtide_change(self):
        index = self.ui.comboBox_auto_yellowtide.currentIndex()
        game.index_auto_yellowtide = index
        cfg_set('guaji', 'index_auto_yellowtide', str(index))
        if index == 0:
            self.ui.comboBox_auto_lingyan_mode.setEnabled(False)
        else:
            self.ui.comboBox_auto_lingyan_mode.setEnabled(True)
        return

    def change_fudai(self, onoff, type):
        game_obj.change_fudai(onoff, type, False)
        return

    def change_tisi(self, onoff, type):
        game_obj.change_tisi(onoff, type, False)
        return

    def change_longfengbi(self, onoff, type):
        game_obj.change_longfengbi(onoff, type, False)
        return

    def comboBox_renjiandao_fudai_change(self):
        onoff_text = [
         u'关', u'开']
        use_tisicaoren = [u'未用', u'已用']
        index = self.ui.comboBox_renjiandao_fudai.currentIndex()
        game.index_renjiandao_fudai = index
        cfg_set('guaji', 'index_renjiandao_fudai', str(index))
        game_obj.start_check_need_change_fudai()
        if index == 0:
            self.logprint(u'关闭人间道使用福袋', 51)
            self.ui.pushButton_rendao_fudai_on.setEnabled(True)
            self.ui.pushButton_rendao_fudai_off.setEnabled(True)
        else:
            self.ui.pushButton_rendao_fudai_on.setEnabled(False)
            self.ui.pushButton_rendao_fudai_off.setEnabled(False)
            self.logprint(u'\n人间道到了[%d]次，替死草人[%s]，福袋为[%s]，设置的选项为[%d]' % (game_obj.rendao_cur_cishu, use_tisicaoren[game_obj.rendao_use_tisicaoren], onoff_text[game_obj.rendao_settings['tianfudai']], index + 5), 51, False)
        return

    def comboBox_eguidao_fudai_change(self):
        onoff_text = [u'关', u'开']
        use_tisicaoren = [u'未用', u'已用']
        index = self.ui.comboBox_eguidao_fudai.currentIndex()
        game.index_eguidao_fudai = index
        cfg_set('guaji', 'index_eguidao_fudai', str(index))
        game_obj.start_check_need_change_fudai()
        if index == 0:
            self.ui.pushButton_egui_fudai_on.setEnabled(True)
            self.ui.pushButton_egui_fudai_off.setEnabled(True)
            self.logprint(u'关闭恶鬼道使用福袋', 51)
        else:
            self.ui.pushButton_egui_fudai_on.setEnabled(False)
            self.ui.pushButton_egui_fudai_off.setEnabled(False)
            self.logprint(u'\n恶鬼道到了[%d]次，替死草人[%s]，福袋为[%s]，设置的选项为[%d]' % (game_obj.egui_cur_cishu, use_tisicaoren[game_obj.egui_use_tisicaoren], onoff_text[game_obj.egui_settings['tianfudai']], index + 5), 51, False)
        return

    def comboBox_shilianzhidi_change(self):
        index = self.ui.comboBox_shilianzhidi.currentIndex()
        cfg_set('guaji', 'index_shilianzhidi', str(index))
        return

    def comboBox_shiliancengshu_change(self):
        index = self.ui.comboBox_shiliancengshu.currentIndex()
        cfg_set('guaji', 'index_shiliancengshu', str(index))
        return

    def comboBox_shiliangoumai_change(self):
        index = self.ui.comboBox_shiliangoumai.currentIndex()
        cfg_set('guaji', 'index_shiliangoumai', str(index))
        return

    def comboBox_maixuanhuangzhu_change(self):
        index = self.ui.comboBox_maixuanhuangzhu.currentIndex()
        game.index_maixuanhuangzhu = index
        cfg_set('guaji', 'index_maixuanhuangzhu', str(index))
        return

    def comboBox_ronglian1_change(self):
        index = self.ui.comboBox_ronglian1.currentIndex()
        game.index_ronglian1 = index
        cfg_set('guaji', 'index_ronglian1', str(index))
        return

    def comboBox_ronglian2_change(self):
        index = self.ui.comboBox_ronglian2.currentIndex()
        game.index_ronglian2 = index
        cfg_set('guaji', 'index_ronglian2', str(index))
        return

    def comboBox_xumiding_change(self):
        index = self.ui.comboBox_xumiding.currentIndex()
        game.index_xumiding = index
        cfg_set('guaji', 'index_xumiding', str(index))
        return

    def comboBox_hunyuanwudao_change(self):
        index = self.ui.comboBox_hunyuanwudao.currentIndex()
        game.index_hunyuanwudao = index
        cfg_set('guaji', 'index_hunyuanwudao', str(index))
        return

    def comboBox_hundunhai_cur_tansuo_change(self):
        index = self.ui.comboBox_hundunhai_cur_tansuo.currentIndex()
        game.index_cur_tansuo = index
        cfg_set('guaji', 'index_cur_tansuo', str(index))
        return

    def comboBox_hundunhai_next_tansuo_change(self):
        index = self.ui.comboBox_hundunhai_next_tansuo.currentIndex()
        game.index_next_tansuo = index
        cfg_set('guaji', 'index_next_tansuo', str(index))
        return

    def comboBox_yuanhaimijing_change(self):
        index = self.ui.comboBox_yuanhaimijing.currentIndex()
        game.index_yuanhaimijing = index
        cfg_set('guaji', 'index_yuanhaimijing', str(index))
        return

    def comboBox_yuanhaimijing_cishu_change(self):
        index = self.ui.comboBox_yuanhaimijing_cishu.currentIndex()
        game.yuanhaimijing_cishu = index
        cfg_set('guaji', 'yuanhaimijing_cishu', str(index))
        return

    def comboBox_haishoutansuo_change(self):
        index = self.ui.comboBox_haishoutansuo.currentIndex()
        game.index_haishoutansuo = index
        cfg_set('guaji', 'index_haishoutansuo', str(index))
        return

    def comboBox_benming1_befor_change(self):
        index = self.ui.comboBox_benming1_befor.currentIndex()
        game.index_benming1_befor = index
        cfg_set('guaji', 'index_benming1_befor', str(index))
        return

    def comboBox_benming1_after_change(self):
        index = self.ui.comboBox_benming1_after.currentIndex()
        game.index_benming1_after = index
        cfg_set('guaji', 'index_benming1_after', str(index))
        return

    def comboBox_benming2_befor_change(self):
        index = self.ui.comboBox_benming2_befor.currentIndex()
        game.index_benming2_befor = index
        cfg_set('guaji', 'index_benming2_befor', str(index))
        return

    def comboBox_benming2_after_change(self):
        index = self.ui.comboBox_benming2_after.currentIndex()
        game.index_benming2_after = index
        cfg_set('guaji', 'index_benming2_after', str(index))
        return

    def comboBox_daotongpeiyang_moshi_change(self):
        index = self.ui.comboBox_daotongpeiyang_moshi.currentIndex()
        game.index_daotongpeiyang_moshi = index
        cfg_set('guaji', 'daotongpeiyang_moshi', str(index))
        self.refresh_daotongpeiyang()
        return

    def comboBox_daotongpeiyang_dengji_change(self):
        index = self.ui.comboBox_daotongpeiyang_dengji.currentIndex()
        game.index_daotongpeiyang_dengji = index
        cfg_set('guaji', 'daotongpeiyang_dengji', str(index))
        self.refresh_daotongpeiyang()
        return

    def comboBox_daotongpeiyang_zizhi_change(self):
        index = self.ui.comboBox_daotongpeiyang_zizhi.currentIndex()
        game.index_daotongpeiyang_zizhi = index
        cfg_set('guaji', 'daotongpeiyang_zizhi', str(index))
        self.refresh_daotongpeiyang()
        return

    def update_daotong_info(self, infos, comboBox):
        for info in infos:
            text = info[1]
            comboBox.addItem(text)

        return

    def refresh_daotongpeiyang(self):
        game_obj.target_jindaotong = 0
        game_obj.target_mudaotong = 0
        game_obj.target_shuidaotong = 0
        game_obj.target_huodaotong = 0
        game_obj.target_tudaotong = 0
        self.ui.comboBox_jindaotong_list.clear()
        self.ui.comboBox_mudaotong_list.clear()
        self.ui.comboBox_shuidaotong_list.clear()
        self.ui.comboBox_huodaotong_list.clear()
        self.ui.comboBox_tudaotong_list.clear()
        dengji_list = [12, 22, 32, 42, 52, 62, 72, 82, 92, 102, 112, 122, 132, 142, 
         143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 
         154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 
         165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 
         176, 177, 178, 179, 180, 181, 181, 181, 181]
        index_moshi = self.ui.comboBox_daotongpeiyang_moshi.currentIndex()
        index_dengji = self.ui.comboBox_daotongpeiyang_dengji.currentIndex()
        target_dengji = dengji_list[index_dengji]
        index_zizhi = self.ui.comboBox_daotongpeiyang_zizhi.currentIndex() + 1
        jindaotong_list = []
        mudaotong_list = []
        shuidaotong_list = []
        huodaotong_list = []
        tudaotong_list = []
        sex_name = [
         u'男', u'女']
        for daotonginfo in game_obj.daotonginfos:
            tail = u''
            max_dengji = daotonginfo.max_linggen_level
            zizhi = daotonginfo.zizhi
            qianli = daotonginfo.qianli
            if max_dengji < target_dengji:
                continue
            if zizhi < index_zizhi:
                continue
            if daotonginfo.water > 1:
                tail = u'-水道童'
            if daotonginfo.water > 1 and daotonginfo.sex != game_obj.sex:
                if index_moshi <= 1 or index_moshi == 2 and daotonginfo.wood + daotonginfo.mud == 2:
                    if daotonginfo.water < target_dengji:
                        text = u'%.3d|%s 资质:%d 潜力:%d 水灵根:%s %s' % (daotonginfo.id, daotonginfo.name, zizhi, qianli, op.linggen_name[daotonginfo.water], sex_name[daotonginfo.sex]) + tail
                        shuidaotong_list.append([daotonginfo.water + zizhi, text, daotonginfo.id])
                    continue
            if daotonginfo.gold > 1 and daotonginfo.gold < target_dengji:
                text = u'%.3d|%s 资质:%d 潜力:%d 金灵根:%s %s' % (daotonginfo.id, daotonginfo.name, zizhi, qianli, op.linggen_name[daotonginfo.gold], sex_name[daotonginfo.sex]) + tail
                jindaotong_list.append([daotonginfo.gold + zizhi, text, daotonginfo.id])
            elif daotonginfo.wood > 1 and daotonginfo.wood < target_dengji:
                text = u'%.3d|%s 资质:%d 潜力:%d 木灵根:%s %s' % (daotonginfo.id, daotonginfo.name, zizhi, qianli, op.linggen_name[daotonginfo.wood], sex_name[daotonginfo.sex]) + tail
                mudaotong_list.append([daotonginfo.wood + zizhi, text, daotonginfo.id])
            elif daotonginfo.fire > 1 and daotonginfo.fire < target_dengji:
                text = u'%.3d|%s 资质:%d 潜力:%d 火灵根:%s %s' % (daotonginfo.id, daotonginfo.name, zizhi, qianli, op.linggen_name[daotonginfo.fire], sex_name[daotonginfo.sex]) + tail
                huodaotong_list.append([daotonginfo.fire + zizhi, text, daotonginfo.id])
            elif daotonginfo.mud > 1 and daotonginfo.mud < target_dengji:
                text = u'%.3d|%s 资质:%d 潜力:%d 土灵根:%s %s' % (daotonginfo.id, daotonginfo.name, zizhi, qianli, op.linggen_name[daotonginfo.mud], sex_name[daotonginfo.sex]) + tail
                tudaotong_list.append([daotonginfo.mud + zizhi, text, daotonginfo.id])

        jindaotong_list.sort(reverse=True)
        mudaotong_list.sort(reverse=True)
        shuidaotong_list.sort(reverse=True)
        huodaotong_list.sort(reverse=True)
        tudaotong_list.sort(reverse=True)
        self.update_daotong_info(jindaotong_list, self.ui.comboBox_jindaotong_list)
        self.update_daotong_info(mudaotong_list, self.ui.comboBox_mudaotong_list)
        self.update_daotong_info(shuidaotong_list, self.ui.comboBox_shuidaotong_list)
        self.update_daotong_info(huodaotong_list, self.ui.comboBox_huodaotong_list)
        self.update_daotong_info(tudaotong_list, self.ui.comboBox_tudaotong_list)
        if len(jindaotong_list) > 0:
            game_obj.target_jindaotong = jindaotong_list[0][2]
        if len(mudaotong_list) > 0:
            game_obj.target_mudaotong = mudaotong_list[0][2]
        if len(shuidaotong_list) > 0:
            game_obj.target_shuidaotong = shuidaotong_list[0][2]
        if len(huodaotong_list) > 0:
            game_obj.target_huodaotong = huodaotong_list[0][2]
        if len(tudaotong_list) > 0:
            game_obj.target_tudaotong = tudaotong_list[0][2]
        id_list = [
         game_obj.target_jindaotong, game_obj.target_mudaotong, game_obj.target_shuidaotong, game_obj.target_huodaotong, game_obj.target_tudaotong]
        print id_list
        return

    def shengdaotongqianli(self, type):
        comboBox_list = [
         self.ui.comboBox_jindaotong_list, self.ui.comboBox_jindaotong_list, self.ui.comboBox_mudaotong_list, self.ui.comboBox_shuidaotong_list, self.ui.comboBox_huodaotong_list, self.ui.comboBox_tudaotong_list]
        text = comboBox_list[type].currentText()
        if len(text) > 3:
            id = int(text.split('|')[0])
            game_obj.shengdaotongqianli(id, type)
        return

    def peiyangdaotong_one(self, type):
        comboBox_list = [self.ui.comboBox_jindaotong_list, self.ui.comboBox_jindaotong_list, self.ui.comboBox_mudaotong_list, self.ui.comboBox_shuidaotong_list, self.ui.comboBox_huodaotong_list, self.ui.comboBox_tudaotong_list]
        text = comboBox_list[type].currentText()
        if len(text) > 3:
            id = int(text.split('|')[0])
            game_obj.peiyang_daotong(id, type)
        return

    def yijianpeiyangdaotong(self):
        game_obj.start_auto_peiyang_daotong()
        return

    def xiuwei_change_show(self, is_show):
        if is_show == 1:
            self.ui.pushButton_dengjipaihang_on.setEnabled(False)
        else:
            self.ui.pushButton_dengjipaihang_off.setEnabled(False)
        game_obj.change_show(1, is_show)
        QtGui.QMessageBox.about(self, u'提示', u'需要点击刷新排名按钮才会更新结果')
        self.ui.pushButton_refresh_level_rank.setEnabled(True)
        return

    def shuxing_change_show(self, is_show):
        if is_show == 1:
            self.ui.pushButton_shuxingpaihang_on.setEnabled(False)
        else:
            self.ui.pushButton_shuxingpaihang_off.setEnabled(False)
        game_obj.change_show(2, is_show)
        QtGui.QMessageBox.about(self, u'提示', u'需要点击刷新排名按钮才会更新结果')
        self.ui.pushButton_refresh_shuxing_rank.setEnabled(True)
        return

    def chongwu_change_show(self, is_show):
        if is_show == 1:
            self.ui.pushButton_chongwupaihang_on.setEnabled(False)
        else:
            self.ui.pushButton_chongwupaihang_off.setEnabled(False)
        game_obj.change_show(3, is_show)
        QtGui.QMessageBox.about(self, u'提示', u'需要点击刷新排名按钮才会更新结果')
        self.ui.pushButton_refresh_chongwu_rank.setEnabled(True)
        return

    def tongnianfen_pk(self):
        index = self.ui.comboBox_nianfen_delta.currentIndex()
        game_obj.tongnianfen_pk(index)
        self.ui.pushButton_tongnianfen_pk.setEnabled(False)
        return

    def refresh_level_rank(self):
        game_obj.get_level_rank()
        self.ui.pushButton_refresh_level_rank.setEnabled(False)
        self.ui.comboBox_level_rank_filter.setEnabled(True)
        return

    def level_rank_filter_change(self):
        for i in range(1001, 1021):
            self.logprint(u'', i)

        index_dict = {15: 1, 18: 2, 21: 3, 24: 4, 27: 5, 29: 6, 31: 7, 34: 8, 37: 9, 40: 10, 42: 11, 72: 12, 74: 13, 76: 14, 78: 15, 80: 16, 82: 17, 84: 18, 86: 19, 88: 20, 90: 21, 92: 22, 94: 23, 96: 24, 98: 25, 100: 26, 102: 27}
        index = self.ui.comboBox_level_rank_filter.currentIndex()
        if index > 0:
            for key1, value1 in game_obj.level_rank_obj.items():
                if int(key1) == index:
                    obj = game_obj.level_rank_obj[key1]
                    for key2, value2 in obj.items():
                        self.logprint(value2, 1000 + index_dict[int(key2)])

        return

    def refresh_shuxing_rank(self):
        game_obj.get_shuxing_rank()
        self.ui.pushButton_refresh_shuxing_rank.setEnabled(False)
        self.ui.comboBox_shuxing_rank_filter.setEnabled(True)
        return

    def shuxing_rank_filter_change(self):
        for i in range(1101, 1119):
            self.logprint(u'', i)

        index = self.ui.comboBox_shuxing_rank_filter.currentIndex()
        if index > 0:
            for key1, value1 in game_obj.shuxing_rank_obj.items():
                if int(key1) == index:
                    obj = game_obj.shuxing_rank_obj[key1]
                    for key2, value2 in obj.items():
                        self.logprint(value2, 1100 + int(key2))

        return

    def refresh_chongwu_rank(self):
        game_obj.get_chongwu_rank()
        self.ui.pushButton_refresh_chongwu_rank.setEnabled(False)
        return

    def refresh_daotong_rank(self):
        game_obj.get_daotong_rank()
        self.ui.pushButton_refresh_daotong_rank.setEnabled(False)
        return

    def comboBox_shoulie_didian1_change(self):
        index = self.ui.comboBox_shoulie_didian1.currentIndex()
        game.index_shoulie_didian1 = index
        cfg_set('guaji', 'shoulie_didian1', str(index))
        return

    def comboBox_shoulie_didian2_change(self):
        index = self.ui.comboBox_shoulie_didian2.currentIndex()
        game.index_shoulie_didian2 = index
        cfg_set('guaji', 'shoulie_didian2', str(index))
        return

    def comboBox_next_shoulie_didian_change(self):
        index = self.ui.comboBox_next_shoulie_didian.currentIndex()
        game.index_next_shoulie_didian = index
        cfg_set('guaji', 'next_shoulie_didian', str(index))
        return

    def comboBox_faxiangleixing_change(self):
        index = self.ui.comboBox_faxiangleixing.currentIndex()
        game.index_faxiangleixing = index
        cfg_set('guaji', 'faxiangleixing', str(index))
        return

    def comboBox_faxiangtaozhuang_change(self):
        index = self.ui.comboBox_faxiangtaozhuang.currentIndex()
        game.index_faxiangtaozhuang = index
        cfg_set('guaji', 'faxiangtaozhuang', str(index))
        return

    def comboBox_charge_value_change(self):
        index = self.ui.comboBox_charge_value.currentIndex()
        game.index_charge_value = index
        cfg_set('guaji', 'index_charge_value', str(index))
        if game_obj != None:
            game_obj.set_charge_value()
        if index == 0:
            self.logprint(u'没选择充值额度，默认按2万氪的进度来防止翻车', 1)
        elif game_obj != None:
            self.logprint(u'当前选择的充值额度:%d' % game_obj.chongzhi, 1)
        return

    def query_shenjie_shop(self, type):
        query_id_list = []
        self.ui.textBrowser_yuanli_shop.clear()
        xinwu6_id_list = [0, 3056, 3057, 3058, 3059, 3060, 3061, 3089, 3090, 3091, 3092, 
         3093, 3094, 3095, 3096, 3097, 3098, 3099, 3100, 3101, 
         3102]
        xinwu7_id_list = [0, 3062, 3063, 3064, 3065, 3066, 3067, 3068, 3069, 3070, 3071, 
         3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3111, 
         3112, 3113]
        xinwu8_id_list = [0, 3072, 3073, 3074, 3075, 3076, 3077, 3078, 3079, 3080, 3114, 
         3115, 3116, 3117, 3118, 3119, 3120, 3121]
        xinwu9_id_list = [0, 3081, 3082, 3083, 3084, 3085, 3086, 3087, 3088]
        danfang_id_list = [13049, 13050, 13051, 13052, 13053, 13054, 13055, 13056, 13057, 13058, 
         13059, 13060, 13061, 13062, 13063, 13064, 13065, 13066, 
         10072, 10073, 10074, 10075, 10076, 10077, 0, 0, 0, 8419, 
         8420, 8421, 8422, 8423, 8424, 8425, 8426, 8427, 8428, 
         8429, 8430, 8431, 8432, 8433, 8434, 8435, 8436, 8437, 
         8438, 8439, 8440, 8441, 8442, 8443, 8444, 8445, 8446, 
         8447, 8448, 8449, 8450, 8451, 8452, 8453, 8454, 8455, 
         8456, 8457, 8458, 8459, 8460, 8461, 8462, 8463, 8464, 
         8465, 8466, 8467, 8468, 8469, 8470, 8471, 8472, 8473, 
         8474, 8475, 8476, 8477, 8478, 8479, 8480, 8481, 8482, 
         8483, 8484, 8485, 8486, 8487, 8488, 8489, 8490, 8491, 
         8492, 8493, 8494, 8495, 8496, 8497, 8498, 8499, 8500, 
         8501, 8502, 8503, 8504, 8505, 8506, 8507, 8508]
        gongfang_shentong_id_list = [9072, 9073, 9074, 9075, 9076, 9077, 9078, 9079, 9080, 9081, 9082, 
         9083, 9084, 9085, 9086, 9087, 9088, 9089, 9090, 9091, 
         9092, 9093, 9094, 9095, 9096, 9097, 9098, 9099, 9100, 
         9101, 9102, 9103, 9104, 9105, 9106, 9107, 9108, 9109, 
         9110, 9111, 9112, 9113, 9114, 9115, 9116, 9117, 9118, 
         9119, 9120, 9121, 9122, 9123, 9124, 9125, 9126, 9127, 
         9128, 9129, 9130, 9131, 9132, 9133, 9134, 9135, 9136, 
         9137, 9138, 9139, 9140, 9141, 9142, 9143]
        zhenshang_shentong_id_list = [9288, 9289, 9540, 9290, 9291, 9541, 9292, 9293, 9542, 9294, 9295, 
         9543, 9296, 9297, 9544, 9298, 9299, 9545, 9300, 9301, 
         9546, 9302, 9303, 9547, 9304, 9305, 9548, 9378, 9379, 
         9585, 9380, 9381, 9586, 9382, 9383, 9587, 9384, 9385, 
         9588, 9386, 9387, 9589, 9388, 9389, 9590, 9390, 9391, 
         9591, 9392, 9393, 9592, 9394, 9395, 9593, 9270, 9271, 
         9531, 9272, 9273, 9532, 9274, 9275, 9533, 9276, 9277, 
         9534, 9278, 9279, 9535, 9280, 9281, 9536, 9282, 9283, 
         9537, 9284, 9285, 9538, 9286, 9287, 9539, 9360, 9361, 
         9576, 9362, 9363, 9577, 9364, 9365, 9578, 9366, 9367, 
         9579, 9368, 9369, 9580, 9370, 9371, 9581, 9372, 9373, 
         9582, 9374, 9375, 9583, 9376, 9377, 9584, 9306, 9307, 
         9549, 9308, 9309, 9550, 9310, 9311, 9551, 9312, 9313, 
         9552, 9314, 9315, 9553, 9316, 9317, 9554, 9318, 9319, 
         9555, 9320, 9321, 9556, 9322, 9323, 9557, 9396, 9397, 
         9594, 9398, 9399, 9595, 9400, 9401, 9596, 9402, 9403, 
         9597, 9404, 9405, 9598, 9406, 9407, 9599, 9408, 9409, 
         9600, 9410, 9411, 9601, 9412, 9413, 9602, 9252, 9253, 
         9522, 9254, 9255, 9523, 9256, 9257, 9524, 9258, 9259, 
         9525, 9260, 9261, 9526, 9262, 9263, 9527, 9264, 9265, 
         9528, 9266, 9267, 9529, 9268, 9269, 9530, 9342, 9343, 
         9567, 9344, 9345, 9568, 9346, 9347, 9569, 9348, 9349, 
         9570, 9350, 9351, 9571, 9352, 9353, 9572, 9354, 9355, 
         9573, 9356, 9357, 9574, 9358, 9359, 9575, 9324, 9325, 
         9558, 9326, 9327, 9559, 9328, 9329, 9560, 9330, 9331, 
         9561, 9332, 9333, 9562, 9334, 9335, 9563, 9336, 9337, 
         9564, 9338, 9339, 9565, 9340, 9341, 9566, 9414, 9415, 
         9603, 9416, 9417, 9604, 9418, 9419, 9605, 9420, 9421, 
         9606, 9422, 9423, 9607, 9424, 9425, 9608, 9426, 9427, 
         9609, 9428, 9429, 9610, 9430, 9431, 9611]
        qita_id_list = [0, 13048, 13086, 3311, 10078, 10079, 10080, 10081, 10082, 10083]
        xinwu6_id = xinwu6_id_list[self.ui.comboBox_shop_menpai6.currentIndex()]
        xinwu7_id = xinwu7_id_list[self.ui.comboBox_shop_menpai7.currentIndex()]
        xinwu8_id = xinwu8_id_list[self.ui.comboBox_shop_menpai8.currentIndex()]
        xinwu9_id = xinwu9_id_list[self.ui.comboBox_shop_menpai9.currentIndex()]
        query_id_list.append(xinwu6_id)
        query_id_list.append(xinwu7_id)
        query_id_list.append(xinwu8_id)
        query_id_list.append(xinwu9_id)
        danfang_leixing_index = self.ui.comboBox_shop_danfangleixing.currentIndex()
        danfang_pinji_index = self.ui.comboBox_shop_danfang_pinji.currentIndex()
        if danfang_leixing_index > 0 and danfang_pinji_index > 0:
            danfang_id = danfang_id_list[(danfang_leixing_index - 1) * 9 + danfang_pinji_index - 1]
            query_id_list.append(danfang_id)
        shentong_leixing_index = self.ui.comboBox_shop_shentong_leixing.currentIndex()
        shentong_pinji_index = self.ui.comboBox_shop_shentong_pinji.currentIndex()
        if shentong_leixing_index > 0 and shentong_pinji_index > 0:
            if shentong_leixing_index >= 3:
                pos = (shentong_leixing_index - 3) * 27 + (shentong_pinji_index - 1) * 3
                query_id_list.append(zhenshang_shentong_id_list[pos])
                query_id_list.append(zhenshang_shentong_id_list[pos + 1])
                query_id_list.append(zhenshang_shentong_id_list[pos + 2])
            else:
                pos = (shentong_leixing_index - 1) * 36 + (shentong_pinji_index - 1) * 4
                query_id_list.append(gongfang_shentong_id_list[pos])
                query_id_list.append(gongfang_shentong_id_list[pos + 1])
                query_id_list.append(gongfang_shentong_id_list[pos + 2])
                query_id_list.append(gongfang_shentong_id_list[pos + 3])
        qita_index = self.ui.comboBox_shop_qita.currentIndex()
        query_id_list.append(qita_id_list[qita_index])
        print query_id_list
        for query_id in query_id_list:
            if query_id == 0:
                continue
            self.query_shenjie_shop_oneid(query_id, type)

        return

    def query_shenjie_shop_oneid(self, query_id, type):
        price_name = [
         u'', u'愿力', u'上灵']
        self.ui.textBrowser_yuanli_shop.append(u'开始搜索[%s]...' % op.item_name[query_id])
        for shop_key in game.shenjie_shop_info.keys():
            if type == 1:
                if shop_key < 82:
                    continue
                xingji = (shop_key - 82) / 9 + 1
            elif shop_key >= 82:
                continue
            xingji = (shop_key - 1) / 9 + 1
            for item_info in game.shenjie_shop_info[shop_key]:
                item_id = item_info[0]
                item_price = item_info[1]
                if query_id == item_id:
                    self.ui.textBrowser_yuanli_shop.append(u'在[%d星天-%s]发现[%s]，价格[%d]%s！\n' % (xingji, op.shenjie_shop_name[shop_key], op.item_name[item_id], item_price, price_name[type]))
                    return

        self.ui.textBrowser_yuanli_shop.append(u'未找到！\n')
        return

    def sendverifynum(self):
        print 'sendverifynum'
        index = self.ui.comboBox_pingtaileixing.currentIndex() + 1
        phonenum = trans_utf8(self.ui.lineEdit_phonenum.text())
        if phonenum == '0' or phonenum == '':
            self.logprint(u'#########请输入手机号!#########', 1)
            return
        cfg_set('login', 'phonenum', phonenum)
        if self.last_accountId != '0' and self.last_accountId != '':
            self.ui.lineEdit_verifynum.setText(u'无需验证码')
        elif index == 3:
            self.logprint(u'九游用户请按照如下步骤，通过游戏界面获取手机验证码', 1)
            self.logprint(u'1、手机打开想不想修真游戏，在登录时点击切换账号', 1)
            self.logprint(u'2、点击九游APP快速登录，然后选择其他账号', 1)
            self.logprint(u'3、在手机登录标签页，输入手机号，点击获取验证码', 1)
            self.logprint(u'4、点击汉字完成认证', 1)
            self.logprint(u'5、将手机上收到的验证码，填写到辅助中，点登录', 1)
        elif index in (4, 6):
            a, b, d = game.get_server_info(flag_login=index, phonenum=phonenum)
            self.logprint(u'如果手机收不到验证码，请按照如下步骤，通过游戏界面获取验证码', 1)
            self.logprint(u'1、手机打开想不想修真游戏，在登录后点击切换账号', 1)
            self.logprint(u'2、选择手机号方式登录，输入两遍手机号后，点击获取验证码', 1)
            self.logprint(u'3、将手机上收到的验证码，填写到辅助中，点登录', 1)
        self.ui.lineEdit_verifynum.setEnabled(True)
        self.ui.pushButton_login.setVisible(True)
        return

    def loginGame(self):
        self.pingtaileixing = self.ui.comboBox_pingtaileixing.currentIndex()
        if self.pingtaileixing in (0, 4, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18,
                                   19, 20, 21, 22, 23, 24, 25, 28):
            self.ui.label_tip_2.setVisible(True)
        self.server_id = int(trans_utf8(self.ui.comboBox_server_id.currentText()).split(':')[0])
        print 'now server_id:', self.server_id
        for server_info in self.server_info_list:
            if server_info[0] == self.server_id:
                self.server_ip = server_info[2]
                self.server_port = server_info[3]
                break

        username = trans_utf8(self.ui.lineEdit_username.text())
        password = trans_utf8(self.ui.lineEdit_password.text())
        phonenum = trans_utf8(self.ui.lineEdit_phonenum.text())
        cfg_set('login', 'pingtaileixing', str(self.pingtaileixing))
        cfg_set('login', 'server_id', str(self.server_id))
        cfg_set('login', 'username', username)
        cfg_set('login', 'password', password)
        cfg_set('login', 'phonenum', phonenum)
        self.gamethread = GameThread(self)
        self.gamethread.signal.connect(self.logprint)
        self.gamethread.start()
        return

    def login_success(self):
        self.ui.comboBox_pingtaileixing.setEnabled(False)
        self.ui.comboBox_server_id.setEnabled(False)
        self.ui.lineEdit_username.setEnabled(False)
        self.ui.lineEdit_password.setEnabled(False)
        self.ui.lineEdit_phonenum.setEnabled(False)
        self.ui.lineEdit_verifynum.setEnabled(False)
        self.ui.pushButton_login.setEnabled(False)
        self.ui.pushButton_sendverifynum.setVisible(False)
        return

    def fuzhichongzhiid(self):
        openid = trans_utf8(self.ui.lineEdit_chongzhiID.text())
        clipboard = QApplication.clipboard()
        clipboard.setText(openid)
        return

    def save_openid(self):
        openid = trans_utf8(self.ui.lineEdit_username.text())
        openid = openid.strip()
        cfg_set('login', 'accountId', openid, 'config.ini')
        self.ui.pushButton_login.setEnabled(True)
        self.ui.pushButton_save_openid.setVisible(False)
        self.ui.label_username.setVisible(False)
        self.ui.lineEdit_username.setVisible(False)
        self.ui.label_tip_2.setVisible(True)
        self.last_accountId = openid
        return

    def guajifangan_change(self):
        self.update_shuatu_list()
        return

    def guajileixing_change(self):
        index = self.ui.comboBox_guajileixing.currentIndex()
        self.ui.comboBox_ditujibie_tou.clear()
        self.chuqiao_list = []
        self.ui.comboBox_ditujibie_shua.clear()
        self.toutu_list = []
        for map_id in self.key_list:
            if map_id not in game.maps_list:
                try:
                    self.toutu_list.append(map_id)
                    self.ui.comboBox_ditujibie_tou.addItem(op.cailiao_map_name[map_id])
                except:
                    pass

        if game.dangqian_map_id in self.toutu_list:
            self.ui.comboBox_ditujibie_tou.setCurrentIndex(self.toutu_list.index(game.dangqian_map_id))
        if index == 0:
            for map_id in game.maps_list:
                if map_id < 2000 or map_id > 4000:
                    if map_id in self.key_list:
                        try:
                            if map_id not in (1025, 1059, 1079):
                                self.chuqiao_list.append(map_id)
                                self.ui.comboBox_ditujibie_shua.addItem(op.cailiao_map_name[map_id])
                        except:
                            pass

        elif index == 1:
            for line in self.shoushua_list:
                map_id = int(line.split('-')[1])
                if map_id in game.maps_list:
                    try:
                        self.ui.comboBox_ditujibie_shua.addItem(line.decode('GBK'))
                    except:
                        pass

        return

    def ditujibie_change(self, map_id, boss_list):
        print map_id, op.map_name[map_id], op.map_name[map_id][:2]
        shuxing_names = [u'仙攻', u'魔攻', u'妖攻', u'鬼攻', u'释攻']
        map = op.cailiao_map_name[map_id]
        content = map[:map.find(u' ')]
        if boss_list.has_key(content):
            text = u'本地图Boss如下:\n'
            for npc in boss_list[content].keys():
                value = boss_list[content][npc]
                zong_shanghai = max(value[0] - game_obj.fangyu, 1)
                if len(value) > 2:
                    shuxing_shanghai = max(value[2] - game_obj.shuxing_fangyu[value[3]], 1)
                    zong_shanghai += shuxing_shanghai
                count = game_obj.shengming / zong_shanghai
                if count > 50:
                    count = 50
                if len(value) > 2:
                    text += u'%s: 攻击:%d 生命:%d %s:%d 抗[%d]刀\n' % (npc, value[0], value[1], shuxing_names[value[3]], value[2], count)
                else:
                    text += u'%s: 攻击:%d 生命:%d 抗[%d]刀\n' % (npc, value[0], value[1], count)

            self.logprint(text, 1)
        return

    def ditujibie_shua_change(self):
        leixing_index = self.ui.comboBox_guajileixing.currentIndex()
        if leixing_index == 1:
            currentText = self.ui.comboBox_ditujibie_shua.currentText()
            map_id = int(currentText.split('-')[1])
            self.ditujibie_change(map_id, op.map_mo_boss)
        return

    def ditujibie_tou_change(self):
        ditu_index = self.ui.comboBox_ditujibie_tou.currentIndex()
        map_id = self.toutu_list[ditu_index]
        if map_id >= 3000 and map_id < 4000:
            self.ui.comboBox_toutucishu.setEnabled(False)
        else:
            self.ditujibie_change(map_id, op.map_boss)
            self.ui.comboBox_toutucishu.setEnabled(True)
        return

    def shuatucishu_change(self):
        cishu_index = self.ui.comboBox_shuatucishu.currentIndex()
        if cishu_index == 1:
            self.ui.lineEdit_shuatucishu.setVisible(True)
        else:
            self.ui.lineEdit_shuatucishu.setVisible(False)
        return

    def set_guaji_items_status(self, status):
        self.ui.pushButton_starttoutu.setEnabled(status)
        self.ui.pushButton_stoptoutu.setEnabled(status)
        self.ui.pushButton_addmap.setEnabled(status)
        self.ui.pushButton_modifymap.setEnabled(status)
        self.ui.pushButton_delmap.setEnabled(status)
        self.ui.pushButton_longgu.setEnabled(status)
        self.ui.pushButton_fengchi.setEnabled(status)
        self.ui.pushButton_xiaolingshan.setEnabled(status)
        self.ui.pushButton_kunlunmijing.setEnabled(status)
        self.ui.pushButton_xianshoudao.setEnabled(status)
        self.ui.pushButton_wangshengchi.setEnabled(status)
        self.ui.pushButton_modian.setEnabled(status)
        self.ui.comboBox_ditujibie_tou.setEnabled(status)
        self.ui.comboBox_toutucishu.setEnabled(status)
        self.ui.comboBox_guajifangan.setEnabled(status)
        self.ui.comboBox_guajileixing.setEnabled(status)
        self.ui.comboBox_ditujibie_shua.setEnabled(status)
        self.ui.comboBox_shuatucishu.setEnabled(status)
        self.ui.lineEdit_shuatucishu.setEnabled(status)
        return

    def startGuaji(self):
        global chonglianjiange
        if game.flag_guaji == False:
            game.after_hour = int(self.ui.lineEdit_after_hour.text())
            cfg_set('login', 'after_hour', str(game.after_hour))
            chonglianjiange = int(self.ui.lineEdit_chonglianjiange.text())
            cfg_set('login', 'chonglianjiange', str(chonglianjiange))
            self.ui.pushButton_startguaji.setEnabled(False)
            self.ui.pushButton_stopguaji.setEnabled(True)
            self.set_guaji_items_status(False)
            game.flag_guaji = True
            if game.flag_chonglian == True:
                index = int(cfg_get('fuben', 'guajifangan'))
            else:
                index = self.ui.comboBox_guajifangan.currentIndex()
                cfg_set('fuben', 'guajifangan', str(index))
            game_obj.start_guaji(index)
        return

    def stopGuaji(self):
        game.flag_guaji = False
        if game.is_stop_over:
            self.ui.pushButton_startguaji.setEnabled(True)
            self.ui.pushButton_stopguaji.setEnabled(False)
            self.set_guaji_items_status(True)
        else:
            self.logprint(u'正在停止，请稍等...', 1)
        return

    def starttoutu(self):
        self.ui.pushButton_starttoutu.setEnabled(False)
        self.ui.pushButton_stoptoutu.setEnabled(True)
        self.ui.comboBox_ditujibie_tou.setEnabled(False)
        self.ui.comboBox_toutucishu.setEnabled(False)
        map_index = self.ui.comboBox_ditujibie_tou.currentIndex()
        map_id = self.toutu_list[map_index]
        cishu_index = self.ui.comboBox_toutucishu.currentIndex()
        cishu_list = [1, 5, 10, 50, 100, 500]
        game.flag_toutu = True
        game_obj.start_toutu(map_id, cishu_list[cishu_index])
        return

    def stoptoutu(self):
        game.flag_toutu = False
        self.ui.pushButton_starttoutu.setEnabled(True)
        self.ui.pushButton_stoptoutu.setEnabled(False)
        self.ui.comboBox_ditujibie_tou.setEnabled(True)
        self.ui.comboBox_toutucishu.setEnabled(True)
        return

    def active_map(self, map_id):
        self.ui.pushButton_startguaji.setEnabled(False)
        self.ui.pushButton_longgu.setEnabled(False)
        self.ui.pushButton_fengchi.setEnabled(False)
        self.ui.pushButton_xiaolingshan.setEnabled(False)
        self.ui.pushButton_kunlunmijing.setEnabled(False)
        self.ui.pushButton_xianshoudao.setEnabled(False)
        self.ui.pushButton_wangshengchi.setEnabled(False)
        self.ui.pushButton_modian.setEnabled(False)
        self.ui.pushButton_stopguaji.setEnabled(True)
        game_obj.start_active_map(map_id)
        return

    def longgu(self):
        self.active_map(2011)
        return

    def fengchi(self):
        self.active_map(2012)
        return

    def xiaolingshan(self):
        self.active_map(2001)
        return

    def kunlunmijing(self):
        self.active_map(2006)
        return

    def xianshoudao(self):
        self.active_map(2003)
        return

    def wangshengchi(self):
        self.active_map(2004)
        return

    def modian(self):
        self.active_map(2005)
        return

    def lijichonglian(self):
        global lijichonglian
        lijichonglian = True
        return

    def yijianshoudaotong(self):
        self.ui.pushButton_yijianshoudaotong.setEnabled(False)
        self.ui.pushButton_yijianshoudaotong2.setEnabled(False)
        self.ui.pushButton_yijianshoudaotong3.setEnabled(False)
        type_list = [7, 6, 3, 2]
        game_obj.print_daotong = True
        game_obj.start_shoudaotong(type_list, True)
        return

    def yijianshoudaotong2(self):
        self.ui.pushButton_yijianshoudaotong.setEnabled(False)
        self.ui.pushButton_yijianshoudaotong2.setEnabled(False)
        self.ui.pushButton_yijianshoudaotong3.setEnabled(False)
        type_list = [7, 6, 5, 4, 3]
        game_obj.print_daotong = True
        game_obj.start_shoudaotong(type_list, True)
        return

    def yijianshoudaotong3(self):
        self.ui.pushButton_yijianshoudaotong.setEnabled(False)
        self.ui.pushButton_yijianshoudaotong2.setEnabled(False)
        self.ui.pushButton_yijianshoudaotong3.setEnabled(False)
        type_list = [7, 6, 5, 4, 3, 2]
        game_obj.print_daotong = True
        game_obj.start_shoudaotong(type_list, True)
        return

    def qingkongrizhi(self):
        self.logprint(u'', 21)
        return

    def chakanzishenshuxing(self):
        game_obj.chakanzishenshuxing()
        return

    def tiaozhanwangxianlou(self, count):
        if self.makesure(u'是否要挑战望仙楼%d次?' % count):
            game_obj.tiaozhanwangxianlou(count)
        return

    def tuiyan_daotu(self):
        if self.makesure(u'是否要推衍混沌道图？'):
            if game_obj.tuiyan_daotu() == False:
                QtGui.QMessageBox.information(self, u'错误', u'当前无可推衍道图!')
        return

    def lunhuibaoku_duihuan(self, index):
        game_obj.lunhuibaoku_duihuan(index)
        return

    def shengji_zifu(self):
        game_obj.shengji_zifu()
        return

    def dajieyin(self):
        if 61 in game.settings_on:
            if self.makesure(u'是否要挑战接引？'):
                game_obj.dajieyin()
        else:
            game_obj.dajieyin()
        return

    def maiwangxianlouxinwu(self):
        game_obj.maiwangxianlouxinwu()
        return

    def jieyinhuangongde(self):
        if 61 in game.settings_on:
            if self.makesure(u'是否要接引符昆仑宝库换150功德？'):
                game_obj.jieyinhuangongde()
        else:
            game_obj.jieyinhuangongde()
        return

    def songli_longgu(self):
        name = trans_utf8(self.ui.lineEdit_songli_longgu.text())
        if len(name) > 0:
            print repr(name)
            game.longgu_target_name = base64.b64encode(name)
            cfg_set('guaji', 'longgu_target_name', game.longgu_target_name)
        else:
            game.longgu_target_name = ''
            cfg_set('guaji', 'longgu_target_name', '0')
        return

    def songli_fengchi(self):
        name = trans_utf8(self.ui.lineEdit_songli_fengchi.text())
        if len(name) > 0:
            print repr(name)
            game.fengchi_target_name = base64.b64encode(name)
            cfg_set('guaji', 'fengchi_target_name', game.fengchi_target_name)
        else:
            game.fengchi_target_name = ''
            cfg_set('guaji', 'fengchi_target_name', '0')
        return

    def songli_dijun(self):
        name = trans_utf8(self.ui.lineEdit_songli_dijun.text())
        if len(name) > 0:
            print repr(name)
            game.dijun_target_name = base64.b64encode(name)
            cfg_set('guaji', 'dijun_target_name', game.dijun_target_name)
        else:
            game.dijun_target_name = ''
            cfg_set('guaji', 'dijun_target_name', '0')
        return

    def iosling200wan(self):
        game_obj.gettwobaiwan()
        return

    def xidaotong6w(self):
        game_obj.start_xidaotong6w(1)
        return

    def xidaotong6w_30ci(self):
        game_obj.start_xidaotong6w(30)
        return

    def start_xuefutu(self):
        if 61 in game.settings_on:
            if self.makesure(u'是否要开始血浮屠？'):
                game_obj.start_xuefutu()
        else:
            game_obj.start_xuefutu()
        return

    def xidaotong20(self):
        game_obj.start_xidaotong(20)
        return

    def xidaotongutil(self):
        if 61 in game.settings_on:
            if self.makesure(u'是否要洗1000道童直到出为止？'):
                game_obj.start_xidaotong(999)
        else:
            game_obj.start_xidaotong(999)
        return

    def chakandanfang(self):
        game_obj.print_danfang()
        return

    def chakanqifang(self):
        game_obj.print_qifang()
        return

    def chakanchidan(self):
        game_obj.chakanchidan()
        return

    def xijie(self, shop_id):
        game_obj.start_xijie(shop_id)
        return

    def kanjineng(self):
        game_obj.kanjineng()
        return

    def jinmenpai(self):
        game_obj.jinmenpai()
        return

    def tuimenpai(self):
        if self.makesure(u'是否要退出门派？') == False:
            return
        game_obj.tuimenpai()
        return

    def maijineng(self):
        if self.makesure(u'是否要花声望买技能点？') == False:
            return
        game_obj.maijineng()
        return

    def xijiezhenbaoge1(self):
        self.xijie(1)
        return

    def xijiexianshufang1(self):
        self.xijie(4)
        return

    def xijiezhenbaoge2(self):
        self.xijie(2)
        return

    def xijiexianshufang2(self):
        self.xijie(5)
        return

    def set_liandan_able(self, able):
        self.ui.comboBox_danyaoleixing.setEnabled(able)
        self.ui.comboBox_danyaojibie.setEnabled(able)
        self.ui.comboBox_danlujibie.setEnabled(able)
        self.ui.spinBox_lianzhicishu.setEnabled(able)
        self.ui.comboBox_danyaoleixing2.setEnabled(able)
        self.ui.comboBox_danyaojibie2.setEnabled(able)
        self.ui.comboBox_danlujibie2.setEnabled(able)
        self.ui.spinBox_lianzhicishu2.setEnabled(able)
        self.ui.comboBox_danyaoleixing3.setEnabled(able)
        self.ui.comboBox_danyaojibie3.setEnabled(able)
        self.ui.comboBox_danlujibie3.setEnabled(able)
        self.ui.spinBox_lianzhicishu3.setEnabled(able)
        self.ui.comboBox_danyaoleixing4.setEnabled(able)
        self.ui.comboBox_danyaojibie4.setEnabled(able)
        self.ui.comboBox_danlujibie4.setEnabled(able)
        self.ui.spinBox_lianzhicishu4.setEnabled(able)
        self.ui.comboBox_danyaoleixing5.setEnabled(able)
        self.ui.comboBox_danyaojibie5.setEnabled(able)
        self.ui.comboBox_danlujibie5.setEnabled(able)
        self.ui.spinBox_lianzhicishu5.setEnabled(able)
        self.ui.comboBox_danyaoleixing6.setEnabled(able)
        self.ui.comboBox_danyaojibie6.setEnabled(able)
        self.ui.comboBox_danlujibie6.setEnabled(able)
        self.ui.spinBox_lianzhicishu6.setEnabled(able)
        return

    def liandan2_change(self):
        cfg_set('liandan', 'liandan2', str(self.ui.checkBox_liandan2.checkState()))
        if self.ui.checkBox_liandan2.checkState() == 2:
            self.ui.comboBox_danyaoleixing2.setEnabled(True)
            self.ui.comboBox_danyaojibie2.setEnabled(True)
            self.ui.comboBox_danlujibie2.setEnabled(True)
            self.ui.spinBox_lianzhicishu2.setEnabled(True)
        else:
            self.ui.comboBox_danyaoleixing2.setEnabled(False)
            self.ui.comboBox_danyaojibie2.setEnabled(False)
            self.ui.comboBox_danlujibie2.setEnabled(False)
            self.ui.spinBox_lianzhicishu2.setEnabled(False)
        return

    def liandan3_change(self):
        cfg_set('liandan', 'liandan3', str(self.ui.checkBox_liandan3.checkState()))
        if self.ui.checkBox_liandan3.checkState() == 2:
            self.ui.comboBox_danyaoleixing3.setEnabled(True)
            self.ui.comboBox_danyaojibie3.setEnabled(True)
            self.ui.comboBox_danlujibie3.setEnabled(True)
            self.ui.spinBox_lianzhicishu3.setEnabled(True)
        else:
            self.ui.comboBox_danyaoleixing3.setEnabled(False)
            self.ui.comboBox_danyaojibie3.setEnabled(False)
            self.ui.comboBox_danlujibie3.setEnabled(False)
            self.ui.spinBox_lianzhicishu3.setEnabled(False)
        return

    def save_liandan_cfg(self, leixing, danyao, danlu, cishu, index):
        danyaoleixing = leixing.currentIndex()
        danyaojibie = danyao.currentIndex()
        danlujibie = danlu.currentIndex()
        lianzhicishu = cishu.value()
        if index == 1:
            cfg_set('liandan', 'danyaoleixing', str(danyaoleixing))
            cfg_set('liandan', 'danyaojibie', str(danyaojibie))
            cfg_set('liandan', 'danlujibie', str(danlujibie))
            cfg_set('liandan', 'lianzhicishu', str(lianzhicishu))
        else:
            cfg_set('liandan', 'danyaoleixing%d' % index, str(danyaoleixing))
            cfg_set('liandan', 'danyaojibie%d' % index, str(danyaojibie))
            cfg_set('liandan', 'danlujibie%d' % index, str(danlujibie))
            cfg_set('liandan', 'lianzhicishu%d' % index, str(lianzhicishu))
        danyao_id = op.danyao_id_list[danyaojibie][danyaoleixing]
        return [danlujibie + 1, danyao_id, lianzhicishu]

    def startLiandan(self):
        all_liandan_list = []
        game.flag_liandan = True
        if game.flag_auto_huntianxiandan == True:
            all_liandan_list.append([9, 133, 1])
            all_liandan_list.append([9, 115, 1])
        if game.flag_auto_xueshaxiandan == True:
            all_liandan_list.append([9, 127, 1])
            all_liandan_list.append([9, 118, 1])
        if game.flag_auto_yanghundan == True:
            all_liandan_list.append([4, 104, 10])
        liandan1 = self.save_liandan_cfg(self.ui.comboBox_danyaoleixing, self.ui.comboBox_danyaojibie, self.ui.comboBox_danlujibie, self.ui.spinBox_lianzhicishu, 1)
        all_liandan_list.append(liandan1)
        liandan4 = self.save_liandan_cfg(self.ui.comboBox_danyaoleixing4, self.ui.comboBox_danyaojibie4, self.ui.comboBox_danlujibie4, self.ui.spinBox_lianzhicishu4, 4)
        liandan5 = self.save_liandan_cfg(self.ui.comboBox_danyaoleixing5, self.ui.comboBox_danyaojibie5, self.ui.comboBox_danlujibie5, self.ui.spinBox_lianzhicishu5, 5)
        liandan6 = self.save_liandan_cfg(self.ui.comboBox_danyaoleixing6, self.ui.comboBox_danyaojibie6, self.ui.comboBox_danlujibie6, self.ui.spinBox_lianzhicishu6, 6)
        if self.ui.checkBox_liandan2.checkState() == 2:
            liandan2 = self.save_liandan_cfg(self.ui.comboBox_danyaoleixing2, self.ui.comboBox_danyaojibie2, self.ui.comboBox_danlujibie2, self.ui.spinBox_lianzhicishu2, 2)
            all_liandan_list.append(liandan2)
        if self.ui.checkBox_liandan3.checkState() == 2:
            liandan3 = self.save_liandan_cfg(self.ui.comboBox_danyaoleixing3, self.ui.comboBox_danyaojibie3, self.ui.comboBox_danlujibie3, self.ui.spinBox_lianzhicishu3, 3)
            all_liandan_list.append(liandan3)
        self.ui.pushButton_startliandan.setEnabled(False)
        self.ui.pushButton_stopliandan.setEnabled(True)
        self.set_liandan_able(False)
        print u'炼丹设置', all_liandan_list
        game_obj.start_liandan(all_liandan_list)
        game_obj.start_daotong_liandan([liandan4, liandan5, liandan6])
        return

    def stopLiandan(self):
        self.ui.pushButton_startliandan.setEnabled(True)
        self.ui.pushButton_stopliandan.setEnabled(False)
        game.flag_liandan = False
        self.set_liandan_able(True)
        return

    def change_longyu(self, nWLXRewordIndex):
        if self.makesure(u'必须要领取龙玉后才能切换，确定吗？') == False:
            return
        game_obj.change_longyu(nWLXRewordIndex)
        return

    def longyu_lingqu(self):
        if self.makesure(u'确定要领取龙玉吗？') == False:
            return
        game_obj.lingqu_longyu()
        return

    def refresh_guanwei_apply(self):
        game_obj.refresh_guanwei_apply()
        return

    def refresh_dadi_guanwei_apply(self):
        game_obj.refresh_dadi_guanwei_apply()
        return

    def refresh_daozhu_guanwei_apply(self):
        game_obj.refresh_daozhu_guanwei_apply()
        return

    def shenguan_guanwei_cizhi(self):
        if self.makesure(u'确定要辞职吗？') == False:
            return
        game_obj.shenguan_guanwei_cizhi()
        return

    def shenguan_dadi_guanwei_cizhi(self):
        if self.makesure(u'确定要辞职吗？') == False:
            return
        game_obj.shenguan_dadi_guanwei_cizhi()
        return

    def shenguan_daozhu_guanwei_cizhi(self):
        if self.makesure(u'确定要辞职吗？') == False:
            return
        game_obj.shenguan_daozhu_guanwei_cizhi()
        return

    def guanwei_citui(self):
        index = self.ui.comboBox_guanwei_list.currentIndex()
        text = self.ui.comboBox_guanwei_list.currentText()
        if self.makesure(u'确定要辞退%s吗？' % text) == False:
            return
        game_obj.guanwei_citui(index + 1)
        return

    def dadi_guanwei_citui(self):
        index = self.ui.comboBox_dadi_guanwei_list.currentIndex()
        text = self.ui.comboBox_dadi_guanwei_list.currentText()
        if self.makesure(u'确定要辞退%s吗？' % text) == False:
            return
        game_obj.dadi_guanwei_citui(index + 1)
        return

    def daozhu_guanwei_citui(self):
        index = self.ui.comboBox_daozhu_guanwei_list.currentIndex()
        text = self.ui.comboBox_daozhu_guanwei_list.currentText()
        if self.makesure(u'确定要辞退%s吗？' % text) == False:
            return
        game_obj.daozhu_guanwei_citui(index + 1)
        return

    def guanwei_shenpi(self, yesorno):
        index = self.ui.comboBox_guanwei_apply_list.currentIndex()
        if index > 0:
            type = [
             u'拒绝', u'通过']
            text = self.ui.comboBox_guanwei_apply_list.currentText()
            temp = text.split(u'|')
            if self.makesure(u'确定要%s[%s]的申请吗？' % (type[yesorno], temp[1])) == False:
                return
            game_obj.guanwei_shenpi(yesorno, int(temp[0]), int(temp[2]), trans_utf8(temp[1]))
        return

    def dadi_guanwei_shenpi(self, yesorno):
        index = self.ui.comboBox_dadi_guanwei_apply_list.currentIndex()
        if index > 0:
            type = [
             u'拒绝', u'通过']
            text = self.ui.comboBox_dadi_guanwei_apply_list.currentText()
            temp = text.split(u'|')
            if self.makesure(u'确定要%s[%s]的申请吗？' % (type[yesorno], temp[1])) == False:
                return
            game_obj.dadi_guanwei_shenpi(yesorno, int(temp[0]), int(temp[2]), trans_utf8(temp[1]))
        return

    def daozhu_guanwei_shenpi(self, yesorno):
        index = self.ui.comboBox_daozhu_guanwei_apply_list.currentIndex()
        if index > 0:
            type = [
             u'拒绝', u'通过']
            text = self.ui.comboBox_daozhu_guanwei_apply_list.currentText()
            temp = text.split(u'|')
            if self.makesure(u'确定要%s[%s]的申请吗？' % (type[yesorno], temp[1])) == False:
                return
            game_obj.daozhu_guanwei_shenpi(yesorno, int(temp[0]), int(temp[2]), trans_utf8(temp[1]))
        return

    def guanwei_query(self):
        index = self.ui.comboBox_guanwei_query.currentIndex()
        game_obj.guanwei_query(1025 + index)
        return

    def dadi_guanwei_query(self):
        index = self.ui.comboBox_dadi_guanwei_query.currentIndex()
        game_obj.dadi_guanwei_query(1113 + index)
        return

    def daozhu_guanwei_query(self):
        index = self.ui.comboBox_daozhu_guanwei_query.currentIndex()
        game_obj.daozhu_guanwei_query(index)
        return

    def guanwei_apply(self):
        index = self.ui.comboBox_guanwei_query.currentIndex()
        map_id = 1025 + index
        officerlevel = self.ui.comboBox_shenguan_guanwei_list.currentIndex() + 1
        game_obj.guanwei_apply(map_id, officerlevel)
        return

    def dadi_guanwei_apply(self):
        index = self.ui.comboBox_dadi_guanwei_query.currentIndex()
        map_id = 1113 + index
        officerlevel = self.ui.comboBox_shenguan_dadi_guanwei_list.currentIndex() + 1
        game_obj.dadi_guanwei_apply(map_id, officerlevel)
        return

    def daozhu_guanwei_apply(self):
        index = self.ui.comboBox_daozhu_guanwei_query.currentIndex()
        officerlevel = self.ui.comboBox_shenguan_daozhu_guanwei_list.currentIndex() + 1
        game_obj.daozhu_guanwei_apply(index, officerlevel)
        return

    def gongdeduihuanlingli(self):
        game_obj.shilian_duihuan(1)
        return

    def shanglingduihuanlingli(self):
        game_obj.shilian_duihuan(2)
        return

    def huashen_2_stop_tiaozhan(self):
        self.logprint(u'1', 1702)
        return

    def huashen_2_tiaozhan(self, type):
        count_list = [
         0, 1, 5, 10, 20, 50, 100]
        index = self.ui.comboBox_2_tiaozhancishu.currentIndex()
        count = count_list[index]
        self.logprint(u'0', 1702)
        self.logprint(u'', 20401)
        game_obj.start_huashen_2_tiaozhan(type, count)
        return

    def startshilian(self):
        target_place = self.ui.comboBox_shilianzhidi.currentIndex()
        if target_place == 0:
            self.logprint(u'请选择对应的试炼之地', 32)
        elif game.flag_zidongshilian == False:
            if self.makesure(u'是否要开始试炼？') == False:
                return
        game.flag_shilian = True
        start_10_index = self.ui.comboBox_shiliancengshu.currentIndex()
        lingliduihuan_index = self.ui.comboBox_shiliangoumai.currentIndex()
        self.ui.pushButton_startshilian.setEnabled(False)
        self.ui.pushButton_stopshilian.setEnabled(True)
        game_obj.start_shilian(target_place, start_10_index, lingliduihuan_index)
        return

    def stopshilian(self):
        game.flag_shilian = False
        self.ui.pushButton_startshilian.setEnabled(True)
        self.ui.pushButton_stopshilian.setEnabled(False)
        return

    def hundunhai_shoulie_place_change(self):
        id_index1 = self.ui.comboBox_hundunhai_shoulie_place_1.currentIndex()
        id_index2 = self.ui.comboBox_hundunhai_shoulie_place_2.currentIndex()
        id_index3 = self.ui.comboBox_hundunhai_shoulie_place_3.currentIndex()
        game.index_hundunhai_shoulie_place1 = id_index1
        game.index_hundunhai_shoulie_place2 = id_index2
        game.index_hundunhai_shoulie_place3 = id_index3
        cfg_set('hundunhai', 'shoulie_place_index', '%d,%d,%d' % (id_index1, id_index2, id_index3))
        if game_obj != None:
            game_obj.update_daowen_info()
        return

    def yellowtide_haiyan1_change(self):
        self.ui.comboBox_yellowtide_lingyan_weizhi1.clear()
        self.ui.comboBox_yellowtide_lingyan_weizhi1.addItem(u'请选择灵眼位置')
        sea_id = self.ui.comboBox_show_yellowtide.currentIndex() + 1
        index = self.ui.comboBox_yellowtide_haiyan1.currentIndex()
        text = self.ui.comboBox_yellowtide_haiyan1.currentText()
        self.ui.pushButton_yellowtide_bianyuan1.setEnabled(False)
        self.ui.pushButton_yellowtide_hexin1.setEnabled(False)
        self.ui.pushButton_yellowtide_set_lingyan1.setEnabled(False)
        if index > 0:
            place_id = int(text.split('|')[0])
            game_obj.query_yellowtide_haiyan_info(sea_id, place_id)
            if game_obj.yellowtide_open:
                self.ui.pushButton_yellowtide_bianyuan1.setEnabled(True)
                self.ui.pushButton_yellowtide_hexin1.setEnabled(True)
                if game_obj.yellowtide_kelingyan:
                    self.ui.pushButton_yellowtide_set_lingyan1.setEnabled(True)
        return

    def yellowtide_bianyuan1(self):
        sea_id = self.ui.comboBox_show_yellowtide.currentIndex() + 1
        text = self.ui.comboBox_yellowtide_haiyan1.currentText()
        index = self.ui.comboBox_yellowtide_haiyan1.currentIndex()
        if index > 0:
            place_id = int(text.split('|')[0])
            game_obj.set_yellowtide_bianyuan(sea_id, place_id)
        return

    def yellowtide_hexin1(self):
        sea_id = self.ui.comboBox_show_yellowtide.currentIndex() + 1
        text = self.ui.comboBox_yellowtide_haiyan1.currentText()
        index = self.ui.comboBox_yellowtide_haiyan1.currentIndex()
        if index > 0:
            place_id = int(text.split('|')[0])
            game_obj.set_yellowtide_hexin(sea_id, place_id)
        return

    def yellowtide_set_lingyan1(self):
        text = self.ui.comboBox_yellowtide_lingyan_weizhi1.currentText()
        index = self.ui.comboBox_yellowtide_lingyan_weizhi1.currentIndex()
        if index > 0:
            lingyan_id = int(text.split('|')[0])
            game_obj.set_yellowtide_lingyan(text, lingyan_id)
        return

    def yellowtide_broadcast_mylingyan1(self):
        sea_id = self.ui.comboBox_show_yellowtide.currentIndex() + 1
        if game_obj.yellowtide_kelingyan:
            game_obj.send_yellowtide_lingyan(sea_id)
            self.ui.pushButton_yellowtide_broadcast_mylingyan1.setEnabled(False)
        else:
            self.logprint(u'当前灵眼位置已经结束战斗，通告无意义。', 40)
        return

    def yellowtide_shoudong(self):
        self.logprint(u'----------------------------测试手动---------------------------', 40, False)
        game_obj.auto_set_yellowtide()
        return

    def yellowtide_get_broadcast(self):
        self.logprint(u'----------------------------当前通告---------------------------', 40, False)
        game_obj.get_myserver_info()
        self.ui.pushButton_yellowtide_get_broadcast.setEnabled(False)
        self.ui.pushButton_yellowtide_set_lingyan1.setEnabled(True)
        return

    def startLianqi(self):
        game.flag_lianqi = True
        lianqileixing = self.ui.comboBox_lianqileixing.currentIndex()
        qilujibie = self.ui.comboBox_qilujibie.currentIndex()
        lianqicishu = self.ui.spinBox_lianqicishu.value()
        cfg_set('lianqi', 'lianqileixing', str(lianqileixing))
        cfg_set('lianqi', 'qilujibie', str(qilujibie))
        cfg_set('lianqi', 'lianqicishu', str(lianqicishu))
        self.ui.pushButton_startlianqi.setEnabled(False)
        self.ui.pushButton_stoplianqi.setEnabled(True)
        game_obj.start_lianqi(qilujibie, lianqileixing, lianqicishu)
        return

    def stopLianqi(self):
        self.ui.pushButton_startlianqi.setEnabled(True)
        self.ui.pushButton_stoplianqi.setEnabled(False)
        game.flag_lianqi = False
        return

    def initGameParam(self):
        try:
            if not os.path.exists('settings.ini'):
                pingtaileixing_old = cfg_get('login', 'pingtaileixing', 'config.ini')
                if int(pingtaileixing_old) != '0':
                    cfg_set('login', 'pingtaileixing', str(pingtaileixing_old))
                server_id_old = cfg_get('login', 'server_id', 'config.ini')
                if int(server_id_old) != '0':
                    cfg_set('login', 'server_id', str(server_id_old))
                username_old = cfg_get('login', 'username', 'config.ini')
                if username_old != '0':
                    cfg_set('login', 'username', username_old)
                password_old = cfg_get('login', 'password', 'config.ini')
                if password_old != '0':
                    cfg_set('login', 'password', password_old)
                phonenum_old = cfg_get('login', 'phonenum', 'config.ini')
                if phonenum_old != '0':
                    cfg_set('login', 'phonenum', phonenum_old)
        except:
            pass

        return

    def update_serverid_info(self, index):
        self.ui.comboBox_server_id.clear()
        self.server_info_list = game.get_sdk_all_server_info(index)
        self.server_id_list = []
        if not self.server_info_list[0]:
            self.logprint(self.server_info_list[1], 90)
            self.ui.label_chongzhi.setText(u'到期提供此ID：')
            return
        self.ui.label_chongzhi.setText(u'充值提供此ID：')
        for server_info in self.server_info_list:
            self.ui.comboBox_server_id.addItem('%d:%s' % (server_info[0], server_info[1]))
            self.server_id_list.append(server_info[0])

        server_id_index = 0
        if self.server_id in self.server_id_list and self.last_pingtaileixing == self.ui.comboBox_pingtaileixing.currentIndex():
            server_id_index = self.server_id_list.index(self.server_id)
        else:
            print 'not found server_id! set 0'
        self.ui.comboBox_server_id.setCurrentIndex(server_id_index)
        return

    def pingtaileixing_change(self):
        index = self.ui.comboBox_pingtaileixing.currentIndex() + 1
        if index in (1, 5, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                     23, 24, 25, 26, 29):
            self.ui.lineEdit_password.setVisible(False)
            self.ui.lineEdit_phonenum.setVisible(False)
            self.ui.lineEdit_verifynum.setVisible(False)
            self.ui.label_password.setVisible(False)
            self.ui.label_tip.setVisible(False)
            openid = cfg_get('login', 'accountId', 'config.ini')
            if openid == '0' or openid == '':
                self.ui.label_username.setText(u'请输入修真登录助手提取的ID:')
                self.ui.lineEdit_username.setVisible(True)
                self.ui.pushButton_login.setEnabled(False)
                self.ui.pushButton_save_openid.setVisible(True)
            else:
                self.ui.pushButton_login.setEnabled(True)
                self.ui.label_username.setVisible(False)
                self.ui.lineEdit_username.setVisible(False)
                self.ui.pushButton_save_openid.setVisible(False)
                self.ui.label_tip_2.setVisible(True)
            self.ui.pushButton_sendverifynum.setVisible(False)
        else:
            self.ui.pushButton_save_openid.setVisible(False)
            self.ui.pushButton_login.setEnabled(True)
            self.ui.lineEdit_phonenum.setVisible(True)
            self.ui.label_tip_2.setVisible(False)
        if index == 13:
            self.ui.lineEdit_username.setVisible(False)
            self.ui.lineEdit_password.setVisible(False)
            self.ui.lineEdit_phonenum.setVisible(False)
            self.ui.lineEdit_verifynum.setVisible(False)
            self.ui.pushButton_login.setVisible(True)
            self.ui.label_username.setVisible(False)
            self.ui.label_password.setVisible(False)
            self.ui.label_tip.setVisible(True)
            self.ui.pushButton_sendverifynum.setVisible(False)
        if index in (2, 27, 28):
            self.ui.lineEdit_username.setVisible(True)
            self.ui.lineEdit_password.setVisible(True)
            self.ui.lineEdit_phonenum.setVisible(False)
            self.ui.label_tip_2.setVisible(False)
            self.ui.lineEdit_verifynum.setVisible(False)
            self.ui.pushButton_login.setVisible(True)
            self.ui.label_username.setVisible(True)
            self.ui.label_password.setVisible(True)
            self.ui.label_username.setText(u'用户名：')
            self.ui.label_password.setText(u'密码：')
            self.ui.label_tip.setVisible(False)
            self.ui.pushButton_sendverifynum.setVisible(False)
        elif index == 3 or index == 4 or index == 6:
            self.ui.lineEdit_username.setVisible(False)
            self.ui.lineEdit_password.setVisible(False)
            self.ui.lineEdit_phonenum.setVisible(True)
            self.ui.lineEdit_verifynum.setVisible(True)
            self.ui.label_username.setVisible(True)
            self.ui.label_password.setVisible(True)
            self.ui.label_username.setText(u'手机号：')
            self.ui.label_password.setText(u'验证码：')
            self.ui.label_tip.setVisible(False)
            self.ui.pushButton_sendverifynum.setVisible(True)
        self.update_serverid_info(index)
        return

    def print_danyaoinfo(self, danyao_id, who=1):
        info = op.dan_makeinfo[danyao_id]
        self.logprint(u'----------------------------------------------------------------', 2, False)
        text = u'\n  需要药材:'
        for i in [1, 3, 5]:
            if info[i] > 0:
                text += u' %s*%d' % (op.item_name[info[i]], info[i + 1])

        if info[0] > 0:
            text += u' 一炉最大成丹[%d]个' % info[0]
        else:
            text += u' 一炉最大成丹[未知]个'
        self.logprint(text, 2, False)
        spinBox_list = [self.ui.spinBox_lianzhicishu, self.ui.spinBox_lianzhicishu, self.ui.spinBox_lianzhicishu2, self.ui.spinBox_lianzhicishu3, self.ui.spinBox_lianzhicishu4, self.ui.spinBox_lianzhicishu5, self.ui.spinBox_lianzhicishu6]
        if game_obj != None:
            count = game_obj.print_yaocao_count(danyao_id)
            spinBox_list[who].setValue(count)
        return

    def danyaoleixing_change(self, who):
        comboBox_danyaoleixing = self.comboBox_danyaoleixing_list[who]
        comboBox_danyaojibie = self.comboBox_danyaojibie_list[who]
        danyaoleixing = comboBox_danyaoleixing.currentIndex()
        comboBox_danyaojibie.setEnabled(False)
        if danyaoleixing == 9:
            comboBox_danyaojibie.setCurrentIndex(3)
        elif danyaoleixing == 10:
            comboBox_danyaojibie.setCurrentIndex(1)
        elif danyaoleixing == 22:
            comboBox_danyaojibie.setCurrentIndex(2)
        elif danyaoleixing == 33:
            comboBox_danyaojibie.setCurrentIndex(4)
        elif danyaoleixing == 34:
            comboBox_danyaojibie.setCurrentIndex(3)
        elif danyaoleixing == 35:
            comboBox_danyaojibie.setCurrentIndex(6)
        else:
            comboBox_danyaojibie.setEnabled(True)
        danyaojibie = comboBox_danyaojibie.currentIndex()
        danyao_id = op.danyao_id_list[danyaojibie][danyaoleixing]
        self.danyaojibie_change(who)
        return

    def danyaojibie_change(self, who):
        comboBox_danyaoleixing = self.comboBox_danyaoleixing_list[who]
        comboBox_danyaojibie = self.comboBox_danyaojibie_list[who]
        comboBox_danlujibie = self.comboBox_danlujibie_list[who]
        comboBox_danlujibie.setEnabled(True)
        danyaoleixing = comboBox_danyaoleixing.currentIndex()
        danyaojibie = comboBox_danyaojibie.currentIndex()
        if danyaoleixing == 11:
            comboBox_danlujibie.setCurrentIndex(danyaojibie / 3)
        elif danyaoleixing == 21:
            comboBox_danlujibie.setCurrentIndex(danyaojibie / 3 + 3)
        elif danyaoleixing > 11 and danyaoleixing < 21:
            comboBox_danlujibie.setCurrentIndex(8)
        else:
            comboBox_danlujibie.setCurrentIndex(danyaojibie)
        danyao_id = op.danyao_id_list[danyaojibie][danyaoleixing]
        self.print_danyaoinfo(danyao_id, who)
        return

    def lianqileixing_change(self):
        index = self.ui.comboBox_lianqileixing.currentIndex()
        if index < 9:
            self.ui.comboBox_qilujibie.setCurrentIndex(8 - index)
        elif index >= 9 and index <= 12:
            self.ui.comboBox_qilujibie.setCurrentIndex(8 - (index - 9))
        else:
            self.ui.comboBox_qilujibie.setCurrentIndex(0)
        return

    def daogong_change(self):
        index = self.ui.comboBox_query_daogong.currentIndex()
        game_obj.query_daogong(index + 1)
        return

    def xumiding_help(self):
        QtGui.QMessageBox.information(self, u'建议', u'1、同类型须弥石，须弥鼎炼制的材料差异不大。但是普通炼器那一、四、七仙品须弥石图纸炼制的话，花费核心材料较少。并且黑曜石、万年铁精等材料可以通过魔核兑换，因此可以根据实际情况选择普通炼器图纸方式炼制一、四、七仙品须弥石。\n\n2、须弥仙石图纸在鬼1枉死地狱功德司购买')
        return

    def daotu_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、选了自动升道图后，所需的材料会自动兑换，无脑挂着。\n\n2、道图前面的数字为等级，后面的数字为道纹数量。\n\n3、勾选“自动换先天道纹”，会在好感或征服度够了之后自动换5个道纹合成道图，建议勾选。\n\n4、自动推衍混沌道图会消耗玄黄推衍道图，混沌海前期慎重勾选。\n\n5、可以不勾选自动推衍混沌道图，看到混沌道图列表里有5个道纹了，根据玄黄之气手动推衍。')
        return

    def lunhuidian_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、为了节省福袋特意开发本功能，可以设定从第几次开始勾选使用福袋。经测试，业力收入和使用福袋的个数有关系，因此后半截使用福袋没有全程使用的收益高。\n\n2、开了替死草人的情况下，如果在设定次数之前意外死亡，替死草人可以挽救一下；如果在设定之后还没死，会在替死草人发挥作用后，再开启福袋，最大程度节省福袋。所以不用设置的很大，如果运气好活的久，也会在替死草人之后使用福袋。\n\n3、当有福袋为开的时候，低于12个会自动兑换福袋。如果不想兑换，请点击关按钮。\n\n4、由于后期卡满收益间隔太久，辅助会动态计算卡满收益时间，估算期间是否会达到设定的值，如果达到会在下线前勾选使用福袋。\n\n5、增加刷百世帝王福袋设置，可以选择第几次关福袋，做到既早死又有福袋收益。')
        return

    def xiuxianlicheng_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、点击刷新排名后，可选择查看对应氪度的排名。\n\n2、凑个热闹和退隐江湖分别表示自己参与/不参与排行，点击后别人刷新时就不会出现自己，自己这边的显示需要自己手动刷新排名才会更新。\n\n3、为避免频繁点击刷新，最长每隔15分钟，会重置“刷新排名”按钮，可再次刷新。')
        return

    def pushButton_2_xiulian_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、如果自动添加的不是秘籍，请去第3个标签【自动功能】的【技能】界面调整优先升级的顺序，然后游戏里上号取消掉心法。')
        return

    def shuxingpaihang_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、点击刷新排名后，可选择查看对应氪度的排名。\n\n2、凑个热闹和退隐江湖分别表示自己参与/不参与排行，点击后别人刷新时就不会出现自己，自己这边的显示需要自己手动刷新排名才会更新。\n\n3、为避免频繁点击刷新，最长每隔15分钟，会重置“刷新排名”按钮，可再次刷新。')
        return

    def chongwupaihang_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、海宠要资质5星及以上，非龙凤宠物需要40级或者资质6星及以上才会参与排名。\n\n2、凑个热闹和退隐江湖分别表示自己参与/不参与排行，点击后别人刷新时就不会出现自己，自己这边的显示需要自己手动刷新排名才会更新。\n\n3、为避免频繁点击刷新，最长每隔15分钟，会重置“刷新排名”按钮，可再次刷新。')
        return

    def tongnianfen_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'1、选择相差年份之后，点击游历四方， 会在所有兔子用户中筛选氪度区间一致的道友进行比拼。\n\n2、如果没找到对应的道友，请放宽年份限制再次查询。\n\n3、为避免频繁点击刷新，最长每隔15分钟，会重置“游历四方”按钮，可再次刷新。')
        return

    def daozhu_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'辅助不会卡点抢，想抢的自己卡时间游戏里狂点吧。')
        return

    def dongfushuoming_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'洞府升级模式说明：\n\n1、只开7#智能洞府，没开升级建筑，为肉木模式，肉木互怼。前期可以开启8#[新区前期用]肉木模式卡肉升木，防止肉满了溢出。\n\n2、开启7#智能洞府，开启 5#升聚灵阵 或 6#洗髓池，普通升级模式，哪个建筑不够升哪个建筑。\n\n3、关闭7#智能洞府，开启 5#升聚灵阵 或 6#洗髓池，卡上限升级模式，优先生产满草铁，之后再生产木头。\n\n4、全都关了，那就是纯手动模式。\n\n5、开启了自动卡满收益，下线前会调整洞府，防止停产或者溢出。')
        return

    def hundunhai_shoulie_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'狩猎刷图逻辑比较复杂，详细逻辑如下：\n\n1、为了防止符文满了浪费轮数，辅助是1轮1轮的刷。\n2、设置了2-3个，辅助会检测道纹数量，1满了刷2，2满了刷3。\n3、设置了2-3个，道纹都满了的情况下，辅助会1轮1轮挨个刷。\n4、只设置了1个，道纹满了会自动停止，直到过了中午12点，会刷掉剩下的轮数防止浪费。\n\n提示1：只刷1个图但是道纹满了，又想早点刷，那就3个都设置成1个图就可以了。\n提示2：刷2个图，但是想2:1的比例刷，那就把2个设置成A图，1个设置成B图。')
        return

    def kamanshouyi_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'鬼佬有个隐藏福利：\n出窍后离线，第二天登录此次出窍结算为满收益。\n\n\n主要注意几点：\n1、当天未出窍完的次数，算作第二天次数。\n2、为追求最大收益，可以吃定魂丹增加最大出窍次数。\n\n\n具体辅助操作：\n1、辅助刷图添加最后面2个添加次数选择：“保留最大轮数”选项。后面添加“卡收益”（卡收益选择那个图就是出窍那个图）\n2、辅助勾选几点之后自动卡收益到时间会自动下线（辅助为24小时制），辅助会第二天自动登录辅助。\n3、比如辅助设置21点卡收益，而你需要21点30分才能刷完，辅助会等你刷完在卡收益，不会到了时间就掉线。\n4、自行计算最大出窍完成刷图需要的时间。至少在距0点前出窍结束。\n\n\n弊端：\n1、星君、灵脉、天神 ，混沌，低保可能都没有。（被打了辅助下线状态保护不了你哦）')
        return

    def liandan_help(self):
        QtGui.QMessageBox.information(self, u'说明', u'炼丹说明：\n主界面的炼丹，3个设置会轮流炼丹，如果3个都没材料则等待10分钟继续。\n洞府炼丹室的3个可以同时进行，如果某个吃丹满了就会停止，没材料不会停止。\n\n\n后期建议：\n1、洞府炼丹室那设置成养魂丹、养神丹、魔劫丹等低级丹药。\n2、主界面那设置高级丹药如仙丹等，有材料就会炼。')
        return

    def daotongpeiyang_help(self):
        self.print_daotongpeiyang_info()
        QtGui.QMessageBox.information(self, u'道童培养说明', u'1、上方左边资质下拉框可设置高于x星才培养\n2、上方右边等级下拉框可设置培养到的目标等级，已达到或者超过该等级的道童，则不显示在下方。\n\n3、左边的下拉是设置自动培养模式的，选择关闭则不自动培养\n4、万一辅助出问题没自动培养，可以点击一键手动培养\n\n5、5个道童列表的下拉，自动按顺序培养到目标等级。\n6、每个培养按钮，点一次培养一次，可选择某一个道童手动培养。')
        return

    def print_daotongpeiyang_info(self):
        self.logprint(u'-----------------------------', 45)
        self.logprint(u'潜力1星最高培养到:极品一阶', 45)
        self.logprint(u'潜力2星最高培养到:凡仙一阶', 45)
        self.logprint(u'潜力3星最高培养到:地仙一阶', 45)
        self.logprint(u'潜力4星最高培养到:大罗一阶', 45)
        self.logprint(u'潜力5星最高培养到:仙君十阶', 45)
        self.logprint(u'-----------------------------', 45)
        self.logprint(u'资质4星消耗材料增加20%', 45)
        self.logprint(u'资质3星消耗材料增加50%', 45)
        self.logprint(u'资质2星消耗材料增加80%', 45)
        self.logprint(u'资质1星消耗材料增加100%', 45)
        self.logprint(u'-----------------------------', 45)
        return

    def gongji_dianzhu(self, weizhi):
        if 61 in game.settings_on:
            if self.makesure(u'是否要挑战该位置？') == False:
                return
        index = self.ui.comboBox_query_daogong.currentIndex()
        game_obj.tiaozhan_dianzhu(index + 1, weizhi)
        if game.flag_yuyue59dianzhu:
            self.set_dianzhu_button(False, weizhi)
        return

    def set_dianzhu_button(self, status, weizhi=0, text=u'预约中...'):
        button_list = [
         self.ui.pushButton_tiaozhan_dianzhu_1, self.ui.pushButton_tiaozhan_dianzhu_2, self.ui.pushButton_tiaozhan_dianzhu_3, self.ui.pushButton_tiaozhan_dianzhu_4, self.ui.pushButton_tiaozhan_dianzhu_5, self.ui.pushButton_tiaozhan_dianzhu_6, self.ui.pushButton_tiaozhan_dianzhu_7]
        for i in range(len(button_list)):
            button_list[i].setEnabled(status)
            button_list[i].setVisible(status)
            button_list[i].setText(u'%d-挑战' % (i + 1))

        if weizhi >= 9:
            button_list[weizhi - 9].setEnabled(status)
            button_list[weizhi - 9].setVisible(True)
            button_list[weizhi - 9].setText(text)
        return

    def query_tianshen_change(self):
        map_id = self.ui.comboBox_query_tianshen.currentIndex() + 1114
        game_obj.query_tianshen(map_id)
        return

    def set_tianshen_button(self, status, index=0, text=u'预约中...'):
        button_list = [
         self.ui.pushButton_gongji_tianshen11, self.ui.pushButton_gongji_tianshen12, self.ui.pushButton_gongji_tianshen13, self.ui.pushButton_gongji_tianshen14, self.ui.pushButton_gongji_tianshen15, self.ui.pushButton_gongji_tianshen16, self.ui.pushButton_gongji_tianshen17, self.ui.pushButton_gongji_tianshen18, self.ui.pushButton_gongji_tianshen19, self.ui.pushButton_gongji_tianshen20]
        for i in range(len(button_list)):
            button_list[i].setEnabled(status)
            button_list[i].setVisible(status)
            button_list[i].setText(u'%d-挑战' % (i + 1))

        if index > 10:
            button_list[index - 11].setEnabled(status)
            button_list[index - 11].setVisible(True)
            button_list[index - 11].setText(text)
        return

    def gongji_tianshen(self, index):
        if 61 in game.settings_on:
            if self.makesure(u'是否要挑战该位置？') == False:
                return
        map_id = self.ui.comboBox_query_tianshen.currentIndex() + 1114
        game_obj.gongji_tianshen(map_id, index)
        if game.flag_yuyue59tianshen:
            self.set_tianshen_button(False, index)
        return

    def gongji_tianshen_11(self):
        self.gongji_tianshen(11)
        return

    def gongji_tianshen_12(self):
        self.gongji_tianshen(12)
        return

    def gongji_tianshen_13(self):
        self.gongji_tianshen(13)
        return

    def gongji_tianshen_14(self):
        self.gongji_tianshen(14)
        return

    def gongji_tianshen_15(self):
        self.gongji_tianshen(15)
        return

    def gongji_tianshen_16(self):
        self.gongji_tianshen(16)
        return

    def gongji_tianshen_17(self):
        self.gongji_tianshen(17)
        return

    def gongji_tianshen_18(self):
        self.gongji_tianshen(18)
        return

    def gongji_tianshen_19(self):
        self.gongji_tianshen(19)
        return

    def gongji_tianshen_20(self):
        self.gongji_tianshen(20)
        return

    def query_xingjun_change(self):
        map_id = self.ui.comboBox_query_xingjun.currentIndex() + 1026
        game_obj.query_xingjun(map_id)
        return

    def set_xingjun_button(self, status, index=0, text=u'预约中...'):
        button_list = [
         self.ui.pushButton_gongji_xingjun_11, self.ui.pushButton_gongji_xingjun_12, self.ui.pushButton_gongji_xingjun_13, self.ui.pushButton_gongji_xingjun_14, self.ui.pushButton_gongji_xingjun_15, self.ui.pushButton_gongji_xingjun_16, self.ui.pushButton_gongji_xingjun_17, self.ui.pushButton_gongji_xingjun_18, self.ui.pushButton_gongji_xingjun_19, self.ui.pushButton_gongji_xingjun_20, self.ui.pushButton_gongji_xingjun_21, self.ui.pushButton_gongji_xingjun_22, self.ui.pushButton_gongji_xingjun_23]
        for i in range(len(button_list)):
            button_list[i].setEnabled(status)
            button_list[i].setVisible(status)
            button_list[i].setText(u'%d-挑战' % (i + 1))

        if index > 10:
            button_list[index - 11].setEnabled(status)
            button_list[index - 11].setVisible(True)
            button_list[index - 11].setText(text)
        return

    def gongji_xingjun(self, index):
        if 61 in game.settings_on:
            if self.makesure(u'是否要挑战该位置？') == False:
                return
        map_id = self.ui.comboBox_query_xingjun.currentIndex() + 1026
        game_obj.gongji_xingjun(map_id, index)
        if game.flag_yuyue59xingjun:
            self.set_xingjun_button(False, index)
        return

    def gongji_xingjun_11(self):
        self.gongji_xingjun(11)
        return

    def gongji_xingjun_12(self):
        self.gongji_xingjun(12)
        return

    def gongji_xingjun_13(self):
        self.gongji_xingjun(13)
        return

    def gongji_xingjun_14(self):
        self.gongji_xingjun(14)
        return

    def gongji_xingjun_15(self):
        self.gongji_xingjun(15)
        return

    def gongji_xingjun_16(self):
        self.gongji_xingjun(16)
        return

    def gongji_xingjun_17(self):
        self.gongji_xingjun(17)
        return

    def gongji_xingjun_18(self):
        self.gongji_xingjun(18)
        return

    def gongji_xingjun_19(self):
        self.gongji_xingjun(19)
        return

    def gongji_xingjun_20(self):
        self.gongji_xingjun(20)
        return

    def gongji_xingjun_21(self):
        self.gongji_xingjun(21)
        return

    def gongji_xingjun_22(self):
        self.gongji_xingjun(22)
        return

    def gongji_xingjun_23(self):
        self.gongji_xingjun(23)
        return

    def set_lingmai_button(self, status, index=0, text=u'预约中...'):
        button_list = [
         self.ui.pushButton_gongji_lingmai1, self.ui.pushButton_gongji_lingmai2, self.ui.pushButton_gongji_lingmai3, self.ui.pushButton_gongji_lingmai4, self.ui.pushButton_gongji_lingmai5, self.ui.pushButton_gongji_lingmai6]
        for i in range(len(button_list)):
            button_list[i].setEnabled(status)
            button_list[i].setVisible(status)
            button_list[i].setText(u'%d-挑战' % (i + 1))

        if index > 0:
            button_list[index - 1].setEnabled(status)
            button_list[index - 1].setVisible(True)
            button_list[index - 1].setText(text)
        return

    def gongji_lingmai(self, index):
        if 61 in game.settings_on:
            if self.makesure(u'是否要挑战该位置？') == False:
                return
        fudi_name = self.ui.comboBox_fudi_name.currentText()
        if len(fudi_name.split('-')) > 1:
            space_id = int(fudi_name.split('-')[2])
            game_obj.gongji_lingmai(space_id, index)
            if game.flag_yuyue59lingmai:
                self.set_lingmai_button(False, index)
        else:
            self.logprint(u'没有破阵完的灵脉', 27)
        return

    def gongji_lingmai6(self):
        self.gongji_lingmai(6)
        return

    def gongji_lingmai5(self):
        self.gongji_lingmai(5)
        return

    def gongji_lingmai4(self):
        self.gongji_lingmai(4)
        return

    def gongji_lingmai3(self):
        self.gongji_lingmai(3)
        return

    def gongji_lingmai2(self):
        self.gongji_lingmai(2)
        return

    def gongji_lingmai1(self):
        self.gongji_lingmai(1)
        return

    def lingmaileixing_change(self):
        index = self.ui.comboBox_lingmaileixing.currentIndex()
        self.ui.comboBox_fudi_name.clear()
        for i in game_obj.pozhen_list:
            if i % 5 == index:
                item = u'%d星-%s-%d' % ((i - 1) / 10 + 1, op.fudi_name[i], i)
                self.ui.comboBox_fudi_name.addItem(item)

        self.fudi_name_change()
        return

    def show_help(self, index):
        help_text = [self.ui.textBrowser_help_tongyong, self.ui.textBrowser_help_shuatutoutu, self.ui.textBrowser_help_liandanlianqi, self.ui.textBrowser_help_dongfu, self.ui.textBrowser_help_daotong, self.ui.textBrowser_help_tongguantiaozhan, self.ui.textBrowser_help_gongdeche, self.ui.textBrowser_help_xingjunlingmai, self.ui.textBrowser_help_zhongtianfudan, self.ui.textBrowser_help_jiezhujiangli, self.ui.textBrowser_help_chongwujineng, self.ui.textBrowser_help_ditudiaoluo]
        for i in range(len(help_text)):
            if index == i:
                help_text[i].setVisible(True)
            else:
                help_text[i].setVisible(False)

        return

    def help_tongyong(self):
        self.show_help(0)
        return

    def help_shuatutoutu(self):
        self.show_help(1)
        return

    def help_liandanlianqi(self):
        self.show_help(2)
        return

    def help_dongfu(self):
        self.show_help(3)
        return

    def help_daotong(self):
        self.show_help(4)
        return

    def help_tongguantiaozhan(self):
        self.show_help(5)
        return

    def help_gongdeche(self):
        self.show_help(6)
        return

    def help_xingjunlingmai(self):
        self.show_help(7)
        return

    def help_zhongtianfudan(self):
        self.show_help(8)
        return

    def help_jiezhujiangli(self):
        self.show_help(9)
        return

    def help_chongwujineng(self):
        self.show_help(10)
        return

    def help_ditudiaoluo(self):
        self.show_help(11)
        return

    def dier_shentong_change(self):
        index_1 = self.ui.comboBox_dier_shentong_1.currentIndex()
        index_2 = self.ui.comboBox_dier_shentong_2.currentIndex()
        index_3 = self.ui.comboBox_dier_shentong_3.currentIndex()
        save_str = '%d,%d,%d' % (index_1, index_2, index_3)
        cfg_set('guaji', 'dier_shentong_order', save_str)
        type_list = [5, 4, 13, 1, 10, 15, 20, 17, 22, 16, 21, 18, 23, 19, 24]
        game.dier_shentong_order = [type_list[index_1], type_list[index_2], type_list[index_3]]
        return

    def shentongchaxun_change(self):
        text = self.ui.comboBox_shentongleixing.currentText()
        index_leixing = self.ui.comboBox_shentongleixing.currentIndex()
        index_xingji = self.ui.comboBox_shentongxingji.currentIndex()
        type_list = [5, 4, 13, 1, 10, 15, 20, 17, 22, 16, 21, 18, 23, 19, 24]
        type = type_list[index_leixing]
        if game_obj != None:
            game_obj.print_weixueshentong(text, type, index_xingji + 1)
        return

    def jinengchaxun_change(self):
        index_leixing = self.ui.comboBox_jinengleixing.currentIndex()
        index_xingji = self.ui.comboBox_jinengxingji.currentIndex()
        type_list = [5, 4, 10, 3, 12, 1]
        type = type_list[index_leixing]
        xingji = index_xingji + 1
        game_obj.print_jineng_info(type, xingji)
        return

    def tianmichaxun_change(self):
        index_xingji = self.ui.comboBox_tianmixingji.currentIndex()
        game_obj.print_tianmi_info(index_xingji + 1)
        return

    def liantichaxun_change(self):
        index_xingji = self.ui.comboBox_liantijue_weizhi.currentIndex()
        game_obj.print_lianti_info(index_xingji)
        return

    def fudi_name_change(self):
        fudi_name = self.ui.comboBox_fudi_name.currentText()
        if len(fudi_name.split('-')) > 1:
            space_id = int(fudi_name.split('-')[2])
            if game_obj.shengming > 10:
                self.ui.comboBox_query_fenjie.setCurrentIndex(12)
                self.query_fenjie_change(False)
                self.ui.comboBox_query_map.setCurrentIndex(space_id - 1)
                self.query_map_change()
            game_obj.query_lingmai_info(space_id)
        else:
            self.logprint(u'没有破阵完的灵脉', 27)
        return

    def query_fenjie_change(self, map_change=True):
        self.query_fenjie = self.ui.comboBox_query_fenjie.currentIndex()
        self.ui.comboBox_query_map.clear()
        self.ui.textBrowser_query.clear()
        self.ui.comboBox_query_map.addItems(op.query_1_list[self.query_fenjie])
        if map_change:
            self.query_map_change()
        if self.query_fenjie >= 8 and self.query_fenjie <= 10:
            self.ui.pushButton_kaishitiaozhan.setVisible(True)
            self.ui.pushButton_tingzhitiaozhan.setVisible(True)
        else:
            self.ui.pushButton_kaishitiaozhan.setVisible(False)
            self.ui.pushButton_tingzhitiaozhan.setVisible(False)
        return

    def query_map_change(self):
        self.ui.textBrowser_query.clear()
        self.query_map = self.ui.comboBox_query_map.currentIndex()
        shuxing_gongji = 0
        shuxing_shanghai = 0
        daozhu_shuxing_type = [[5, 5, 4, 4], [4, 4, 3, 3], [4, 4, 3, 3], [3, 3, 2, 2], [3, 3, 2, 2], [2, 2, 1, 1], [2, 2, 1, 1], [5, 5, 4, 4], [1, 1, 5, 5], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1], [1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4], [4, 4, 5, 5], [5, 5, 1, 1]]
        if self.query_fenjie == 8:
            if self.query_map % 2 == 1:
                self.logprint(u'当前关卡不需要挑战，去给老和尚奉上功德吧!', 17)
                self.ui.pushButton_kaishitiaozhan.setVisible(False)
                self.ui.pushButton_tingzhitiaozhan.setVisible(False)
                return
            else:
                self.ui.pushButton_kaishitiaozhan.setVisible(True)
                self.ui.pushButton_tingzhitiaozhan.setVisible(True)
        array1 = range(len(op.query_2_list[self.query_fenjie]))
        if self.query_fenjie in [11, 12]:
            array1 = array1[::-1]
        for i in array1:
            npc = op.query_2_list[self.query_fenjie][i]
            value = op.query_3_list[self.query_fenjie][self.query_map][i]
            gongji = value[0]
            shengming = value[1]
            if value[0] < 10000:
                shuxing_gongji = 2.0 + 0.1 * self.query_map
                gongji = value[0] * 10000
                shengming *= 10000
                shuxing_names = [[u'仙攻', u'鬼攻'], [u'魔攻', u'释攻'], [u'妖攻', u'仙攻'], [u'鬼攻', u'魔攻'], [u'释攻', u'妖攻']]
                text = u'%s: 攻击:%.1f万 生命:%.1f万 %s:%.1f万' % (npc, value[0], value[1], shuxing_names[self.query_map % 5][i % 2], shuxing_gongji)
            elif self.query_fenjie == 13:
                zhenshang = [
                 10000, 12000, 14000, 16000, 
                 18000, 20000, 22000, 24000, 26000, 29000, 
                 32000, 35000, 35000, 38000, 41000, 44000, 
                 47000, 50000, 54000, 58000, 50000, 52000, 
                 54000, 56000, 58000, 60000, 62000, 65000, 
                 68000, 71000, 74000, 77000, 80000, 83000, 
                 86000, 89000, 92000, 95000, 98000, 101000, 
                 104000, 107000, 110000, 113000, 116000, 119000, 
                 121000, 124000, 127000, 130000, 133000, 136000, 
                 139000, 142000, 146000, 150000, 154000, 158000, 
                 162000, 166000, 170000, 174000, 178000, 182000, 
                 186000, 190000, 194000, 198000, 202000, 206000, 
                 210000, 214000, 218000, 222000, 226000, 230000, 
                 234000, 238000, 242000, 246000, 250000]
                shuxing_gongji = zhenshang[self.query_map]
                shuxing_names = [[u'鬼攻', u'仙攻'], [u'魔攻', u'鬼攻'], [u'释攻', u'魔攻'], [u'妖攻', u'释攻'], [u'仙攻', u'妖攻']]
                text = u'%s: 攻击:%.1f万 生命:%.1f万 %s:%.1f万' % (npc, gongji / 10000.0, shengming / 10000.0, shuxing_names[self.query_map % 5][i % 2], shuxing_gongji / 10000.0)
            elif self.query_fenjie == 14:
                zhenshang = [
                 [
                  26000, 26000, 26000, 30000], [36000, 36000, 36000, 40000], [46000, 46000, 46000, 50000], [56000, 56000, 56000, 60000], [66000, 66000, 66000, 70000], [76000, 76000, 76000, 80000], [86000, 86000, 86000, 90000], [96000, 96000, 96000, 100000], [106000, 106000, 106000, 116000], [121000, 121000, 121000, 133000], [126000, 126000, 126000, 138000], [131000, 131000, 131000, 143000], [136000, 136000, 136000, 148000], [141000, 141000, 141000, 153000], [146000, 146000, 146000, 158000], [151000, 151000, 151000, 163000], [156000, 156000, 156000, 168000], [161000, 161000, 161000, 173000], [166000, 166000, 166000, 178000], [171000, 171000, 171000, 183000], [176000, 176000, 176000, 188000], [181000, 181000, 181000, 193000], [186000, 186000, 186000, 198000], [191000, 191000, 191000, 203000], [196000, 196000, 196000, 208000], [201000, 201000, 201000, 213000], [206000, 206000, 206000, 218000], [211000, 211000, 211000, 223000], [216000, 216000, 216000, 228000], [221000, 221000, 221000, 233000], [226000, 226000, 226000, 238000], [231000, 231000, 231000, 243000], [236000, 236000, 236000, 248000], [241000, 241000, 241000, 253000], [246000, 246000, 246000, 258000], [251000, 251000, 251000, 263000], [256000, 256000, 256000, 26800], [261000, 261000, 261000, 27300], [266000, 266000, 266000, 27800], [271000, 271000, 271000, 28300], [276000, 276000, 276000, 28800], [281000, 281000, 281000, 29300], [286000, 286000, 286000, 29800], [291000, 291000, 291000, 30300], [296000, 296000, 296000, 30800], [301000, 301000, 301000, 31300], [306000, 306000, 306000, 31800], [311000, 311000, 311000, 32300], [316000, 316000, 316000, 32800], [321000, 321000, 321000, 33300], [326000, 326000, 326000, 33800], [331000, 331000, 331000, 34300], [336000, 336000, 336000, 34800], [341000, 341000, 341000, 353000]]
                shuxing_gongji = zhenshang[self.query_map][i]
                shuxing_names = [u'', u'仙攻', u'鬼攻', u'魔攻', u'释攻', u'妖攻']
                text = u'%s: 攻击:%.1f万 生命:%.1f万 %s:%.1f万' % (npc, gongji / 10000.0, shengming / 10000.0, shuxing_names[daozhu_shuxing_type[self.query_map][i]], shuxing_gongji / 10000.0)
            else:
                text = u'%s: 攻击:%.1f万 生命:%.1f万' % (npc, gongji / 10000.0, shengming / 10000.0)
            if game_obj != None:
                shuxing_fangyu = 0
                if self.query_fenjie == 11:
                    if i % 2 == 0:
                        shuxing_fangyu = game_obj.shuxing_fangyu[self.query_map % 5]
                    else:
                        shuxing_fangyu = game_obj.shuxing_fangyu[(self.query_map + 3) % 5]
                elif self.query_fenjie == 13:
                    temp_shuxing_fangyu = [
                     0, 0, 0, 0, 0]
                    temp_shuxing_fangyu[0] = game_obj.shuxing_fangyu[3]
                    temp_shuxing_fangyu[1] = game_obj.shuxing_fangyu[1]
                    temp_shuxing_fangyu[2] = game_obj.shuxing_fangyu[4]
                    temp_shuxing_fangyu[3] = game_obj.shuxing_fangyu[2]
                    temp_shuxing_fangyu[4] = game_obj.shuxing_fangyu[0]
                    if i % 2 == 0:
                        shuxing_fangyu = temp_shuxing_fangyu[self.query_map % 5]
                    else:
                        shuxing_fangyu = temp_shuxing_fangyu[(self.query_map + 4) % 5]
                elif self.query_fenjie == 14:
                    temp_shuxing_fangyu = [
                     0, 0, 0, 0, 0, 
                     0]
                    temp_shuxing_fangyu[1] = game_obj.shuxing_fangyu[0]
                    temp_shuxing_fangyu[2] = game_obj.shuxing_fangyu[3]
                    temp_shuxing_fangyu[3] = game_obj.shuxing_fangyu[1]
                    temp_shuxing_fangyu[4] = game_obj.shuxing_fangyu[4]
                    temp_shuxing_fangyu[5] = game_obj.shuxing_fangyu[2]
                    shuxing_fangyu = temp_shuxing_fangyu[daozhu_shuxing_type[self.query_map][i]]
                shuxing_shanghai = max(shuxing_gongji - shuxing_fangyu, 1)
                putong_shanghai = max(gongji - game_obj.fangyu, 1)
                zongshanghai = int(putong_shanghai + shuxing_shanghai)
                count = game_obj.shengming / zongshanghai
                if count > 50:
                    count = 50
                text += u' 抗[%d]刀' % count
            self.logprint(text, 17)

        if self.query_fenjie in [5, 6, 7]:
            map_start = [
             0, 0, 0, 0, 0, 1026, 1060, 1080]
            if game_obj != None:
                map_id = map_start[self.query_fenjie] + self.query_map
                game_obj.chaxunjiezhuinfo(map_id)
                time.sleep(0.2)
                self.logprint(u'\n' + game_obj.jiezhuinfo, 17)
        if self.query_fenjie == 13:
            game_obj.dadi_info = u''
            game_obj.reqsuperworldinfo(1114 + self.query_map)
            time.sleep(1)
            self.logprint(u'\n' + game_obj.dadi_info, 17)
            self.logprint(u'\n大帝奖励：', 17)
            self.logprint(op.dadi_jiangli[self.query_map], 17)
        return

    def startTiaozhan(self):
        game.flag_zidongtiaozhanfoyaohai = True
        self.ui.pushButton_tingzhitiaozhan.setEnabled(True)
        self.ui.pushButton_kaishitiaozhan.setEnabled(False)
        index_fenjie = self.ui.comboBox_query_fenjie.currentIndex()
        index_query_map = self.ui.comboBox_query_map.currentIndex()
        game_obj.start_tiaozhan(index_fenjie, index_query_map)
        return

    def stopTiaozhan(self):
        game.flag_zidongtiaozhanfoyaohai = False
        self.ui.pushButton_tingzhitiaozhan.setEnabled(False)
        self.ui.pushButton_kaishitiaozhan.setEnabled(True)
        return

    def study_xinfa(self):
        if self.makesure(u'学心法有可能会忘记当前门派攻诀，是否继续？'):
            game_obj.study_skill('xinfa')
        return

    def set_haoganrenwu_list(self):
        config_str = cfg_get('hundunhai', 'haoganrenwu')
        temp_list = config_str.split(',')
        for i in range(len(self.haoganrenwu_comboBox_list)):
            if i < len(temp_list):
                game.haoganrenwu_list[i] = int(temp_list[i])
                self.haoganrenwu_comboBox_list[i].setCurrentIndex(int(temp_list[i]))

        print 'haoganrenwu_list =', game.haoganrenwu_list
        return

    def haoganrenwu_change(self):
        for i in range(len(self.haoganrenwu_comboBox_list)):
            game.haoganrenwu_list[i] = self.haoganrenwu_comboBox_list[i].currentIndex()

        print 'haoganrenwu_list =', game.haoganrenwu_list
        temp = ''
        for a in game.haoganrenwu_list:
            temp += str(a) + ','

        cfg_set('hundunhai', 'haoganrenwu', temp[:-1])
        return

    def hundunhai_button_modify(self, id, text, color):
        button = self.hundunhai_button_list[id]
        button.setText(text)
        if color == 0:
            button.setStyleSheet('QPushButton{background-color:#BEBFC3}')
        elif color == 1:
            button.setStyleSheet('QPushButton{background-color:lightgreen}')
        elif color == 2:
            button.setStyleSheet('QPushButton{background-color:lightblue}')
        else:
            button.setStyleSheet('QPushButton{background-color:gray}')
        return

    def hundunhai_button_pop(self, id_list):
        font = QtGui.QFont()
        font.setBold(True)
        font2 = QtGui.QFont()
        font2.setBold(False)
        for id in range(1, 379):
            if id in id_list:
                self.hundunhai_button_list[id].setFont(font)
            else:
                self.hundunhai_button_list[id].setFont(font2)

        return

    def button_enter_fun(self, obj):
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setOverline(True)
        font.setPointSize(11)
        for id in range(1, 379):
            self.hundunhai_button_list[id].setEnabled(False)

        for id in range(1, 379):
            if obj == self.hundunhai_button_list[id]:
                for one_taozhuang in op.daowen_taozhuang:
                    if id in one_taozhuang:
                        for yy in one_taozhuang:
                            self.hundunhai_button_list[yy].setEnabled(True)
                            self.hundunhai_button_list[yy].setFont(font)

                self.hundunhai_button_list[id].setEnabled(True)
                near_place_id_list = op.near_place_id_list_dict[id]
                for near_place_id in near_place_id_list:
                    self.hundunhai_button_list[near_place_id].setEnabled(True)

                return

        return

    def button_leave_fun(self):
        font2 = QtGui.QFont()
        font2.setUnderline(False)
        font2.setOverline(False)
        font2.setPointSize(9)
        for id in range(1, 379):
            self.hundunhai_button_list[id].setEnabled(True)
            self.hundunhai_button_list[id].setFont(font2)

        fun_list = [
         self.show_all, self.show_hundunshoulie, self.show_hundunshengling_fight, self.show_hundunshengling_exchange, self.show_jiezhu, self.show_pk, self.show_npc]
        fun_list[self.last_status]()
        return

    def show_all(self):
        self.last_status = 0
        self.hundunhai_button_pop([])
        return

    def show_hundunshoulie(self):
        self.last_status = 1
        self.hundunhai_button_pop([3, 4, 6, 13, 17, 18, 24, 29, 30, 32, 35, 36, 43, 47, 48, 54, 
         55, 60, 71, 72, 76, 78, 83, 84, 86, 91, 96, 102, 103, 
         113, 114, 117, 118, 121, 124, 125, 129, 130, 135, 138, 
         142, 146, 147, 150, 158, 161, 162, 163, 168, 174, 178, 
         179, 180, 185, 189, 197, 198, 201, 203, 209, 212, 215, 
         216, 219, 220, 230, 231, 233, 234, 245, 248, 251, 255, 
         256, 258, 260, 263, 273, 274, 276, 278, 279, 280, 284, 
         286, 291, 303, 308, 310, 313, 314, 317, 321, 327, 329, 
         332, 333, 336, 340, 343, 355, 357, 358, 362, 368, 370, 
         373, 376])
        return

    def show_hundunshengling_fight(self):
        self.last_status = 2
        self.hundunhai_button_pop([9, 12, 14, 21, 33, 41, 52, 56, 58, 65, 69, 87, 93, 104, 106, 
         109, 111, 123, 137, 141, 148, 153, 156, 173, 175, 176, 
         183, 188, 194, 196, 200, 222, 226, 229, 239, 250, 259, 
         265, 269, 271, 282, 287, 295, 298, 301, 318, 320, 331, 
         335, 346, 356, 363, 369, 375])
        return

    def show_hundunshengling_exchange(self):
        self.last_status = 3
        self.hundunhai_button_pop([1, 7, 11, 26, 28, 31, 42, 45, 62, 64, 67, 77, 82, 95, 98, 101, 
         108, 119, 127, 134, 136, 140, 157, 160, 164, 181, 184, 
         193, 199, 204, 214, 221, 236, 241, 244, 247, 253, 262, 
         266, 283, 290, 304, 306, 311, 319, 330, 338, 341, 344, 
         349, 351, 354, 365, 372])
        return

    def show_jiezhu(self):
        self.last_status = 4
        self.hundunhai_button_pop([5, 16, 19, 37, 40, 44, 50, 61, 63, 73, 80, 85, 88, 90, 100, 
         107, 115, 126, 139, 144, 151, 155, 167, 170, 172, 187, 
         190, 202, 213, 218, 223, 225, 228, 235, 240, 252, 257, 
         268, 272, 285, 289, 302, 305, 309, 316, 325, 328, 339, 
         342, 345, 359, 361, 366, 378])
        return

    def show_pk(self):
        self.last_status = 5
        self.hundunhai_button_pop([10, 15, 22, 34, 38, 46, 49, 53, 57, 68, 74, 79, 81, 94, 105, 
         110, 116, 122, 131, 133, 143, 149, 154, 165, 177, 182, 
         191, 195, 205, 207, 210, 217, 232, 238, 243, 246, 254, 
         261, 275, 281, 294, 297, 300, 307, 312, 322, 326, 334, 
         337, 348, 353, 360, 374, 377])
        return

    def show_npc(self):
        self.last_status = 6
        self.hundunhai_button_pop([2, 8, 20, 23, 25, 27, 39, 51, 59, 66, 70, 75, 89, 92, 97, 99, 
         112, 120, 128, 132, 145, 152, 159, 166, 169, 171, 186, 
         192, 206, 208, 211, 224, 227, 237, 242, 249, 264, 267, 
         270, 277, 288, 292, 293, 296, 299, 315, 323, 324, 347, 
         350, 352, 364, 367, 371])
        return

    def hundunhai_tansuo(self, place_index):
        print u'点击的id', place_index
        if place_index in game_obj.hundunhai_ketansuo_list:
            tips_text = u'是否探索当前地点？'
            if game_obj.hundunhai_tansuo_info.has_key(place_index):
                tips_text = game_obj.hundunhai_tansuo_info[place_index] + tips_text
            if self.makesure(tips_text):
                game_obj.hundunhai_tansuo(place_index)
        elif place_index in game_obj.hundunhai_yitansuo_list and place_index in [3, 4, 6, 13, 17, 18, 24, 29, 30, 32, 35, 36, 43, 47, 48, 54, 
         55, 60, 71, 72, 76, 78, 83, 84, 86, 91, 96, 102, 103, 
         113, 114, 117, 118, 121, 124, 125, 129, 130, 135, 138, 
         142, 146, 147, 150, 158, 161, 162, 163, 168, 174, 178, 
         179, 180, 185, 189, 197, 198, 201, 203, 209, 212, 215, 
         216, 219, 220, 230, 231, 233, 234, 245, 248, 251, 255, 
         256, 258, 260, 263, 273, 274, 276, 278, 279, 280, 284, 
         286, 291, 303, 308, 310, 313, 314, 317, 321, 327, 329, 
         332, 333, 336, 340, 343, 355, 357, 358, 362, 368, 370, 
         373, 376]:
            if self.makesure(u'是否挑战此狩猎地点？'):
                game_obj.hundunhai_shoulie_tongguan(place_index)
        return

    def study_gongjue(self):
        game_obj.study_skill('gongjue')
        return

    def rf_ini(self):
        print 'rf_ini'
        self.last_accountId = cfg_get('login', 'accountId', 'config.ini')
        self.last_access_token = cfg_get('login', 'access_token', 'config.ini')
        self.pingtaileixing = int(cfg_get('login', 'pingtaileixing'))
        self.ui.lineEdit_chonglianjiange.setText(cfg_get('login', 'chonglianjiange'))
        self.ui.lineEdit_after_hour.setText(cfg_get('login', 'after_hour'))
        game.after_hour = int(cfg_get('login', 'after_hour'))
        self.last_pingtaileixing = self.pingtaileixing
        self.ui.comboBox_pingtaileixing.setCurrentIndex(self.pingtaileixing)
        self.server_id = int(cfg_get('login', 'server_id'))
        self.imei = '865166021737195'
        if self.imei == '0' or self.imei == '':
            self.imei = sdk.rand_imei()
            cfg_set('login', 'imei', str(self.imei))
        self.pingtaileixing_change()
        self.last_username = cfg_get('login', 'username')
        self.last_phonenum = cfg_get('login', 'phonenum')
        self.last_password = cfg_get('login', 'password')
        self.ui.lineEdit_username.setText(self.last_username)
        self.ui.lineEdit_password.setText(self.last_password)
        self.ui.lineEdit_phonenum.setText(self.last_phonenum)
        self.ui.checkBox_zidongchonglian.setCheckState(int(cfg_get('guaji', 'zidongchonglian')))
        self.ui.checkBox_chonglianshuatu.setCheckState(int(cfg_get('guaji', 'chonglianshuatu')))
        self.ui.checkBox_diertianshangxian.setCheckState(int(cfg_get('login', 'diertianshangxian')))
        self.ui.checkBox_open_auto_login.setCheckState(int(cfg_get('guaji', 'open_auto_login')))
        if int(cfg_get('guaji', 'open_auto_login')) == 2:
            game.flag_chonglian = True
        self.ui.checkBox_duihuantisicaoren.setCheckState(int(cfg_get('guaji', 'duihuantisicaoren')))
        self.ui.checkBox_duihuantianfudai.setCheckState(int(cfg_get('guaji', 'duihuantianfudai')))
        self.ui.checkBox_duihuanlongfengbi.setCheckState(int(cfg_get('guaji', 'duihuanlongfengbi')))
        self.ui.checkBox_zidongshilian.setCheckState(int(cfg_get('guaji', 'zidongshilian')))
        self.ui.checkBox_hdh_phcl.setCheckState(int(cfg_get('guaji', 'hdh_phcl')))
        self.ui.checkBox_youxianfugui.setCheckState(int(cfg_get('guaji', 'youxianfugui')))
        self.ui.checkBox_baoliuyifu.setCheckState(int(cfg_get('guaji', 'baoliuyifu')))
        self.ui.checkBox_yanyu_zidongtansuo.setCheckState(int(cfg_get('guaji', 'yanyu_zidongtansuo')))
        self.ui.checkBox_dier_shengshentong.setCheckState(int(cfg_get('guaji', 'dier_shengshentong')))
        self.ui.checkBox_duihuan_xiantian_daowen.setCheckState(int(cfg_get('guaji', 'duihuan_xiantian_daowen')))
        self.ui.checkBox_tuiyan_hundun_daotu.setCheckState(int(cfg_get('guaji', 'tuiyan_hundun_daotu')))
        self.ui.checkBox_auto_yanghundan.setCheckState(int(cfg_get('guaji', 'auto_yanghundan')))
        self.ui.checkBox_auto_lianqi.setCheckState(int(cfg_get('guaji', 'auto_lianqi')))
        self.ui.checkBox_auto_huntianxiandan.setCheckState(int(cfg_get('guaji', 'auto_huntianxiandan')))
        self.ui.checkBox_auto_xueshaxiandan.setCheckState(int(cfg_get('guaji', 'auto_xueshaxiandan')))
        self.ui.checkBox_lianxutoutu.setCheckState(int(cfg_get('guaji', 'lianxutoutu')))
        self.ui.checkBox_zhidayao.setCheckState(int(cfg_get('guaji', 'zhidayao')))
        self.ui.checkBox_zhidagui.setCheckState(int(cfg_get('guaji', 'zhidagui')))
        self.ui.checkBox_xuefutu.setCheckState(int(cfg_get('fuben', 'xuefutu')))
        self.ui.comboBox_xuefutucengshu.setCurrentIndex(int(cfg_get('fuben', 'xuefutucengshu')))
        game.index_xuefutucengshu = int(cfg_get('fuben', 'xuefutucengshu'))
        self.ui.comboBox_xuefutucishu.setCurrentIndex(int(cfg_get('fuben', 'xuefutucishu')))
        game.index_xuefutucishu = int(cfg_get('fuben', 'xuefutucishu'))
        try:
            game.longgu_target_name = cfg_get('guaji', 'longgu_target_name')
            if len(game.longgu_target_name) >= 4:
                name = base64.b64decode(game.longgu_target_name)
                print u'readcfg:', name.decode('utf8')
                self.ui.lineEdit_songli_longgu.setText(name.decode('utf8'))
            game.fengchi_target_name = cfg_get('guaji', 'fengchi_target_name')
            if len(game.fengchi_target_name) >= 4:
                name = base64.b64decode(game.fengchi_target_name)
                print u'readcfg:', name.decode('utf8')
                self.ui.lineEdit_songli_fengchi.setText(name.decode('utf8'))
            game.dijun_target_name = cfg_get('guaji', 'dijun_target_name')
            if len(game.dijun_target_name) >= 4:
                name = base64.b64decode(game.dijun_target_name)
                print u'readcfg:', name.decode('utf8')
                self.ui.lineEdit_songli_dijun.setText(name.decode('utf8'))
        except:
            pass

        self.ui.checkBox_zidonglunhuifahui.setCheckState(int(cfg_get('guaji', 'zidonglunhuifahui')))
        game.index_lunhuifahuidaguai = int(cfg_get('guaji', 'lunhuifahuidaguai'))
        self.ui.comboBox_lunhuifahuidaguai.setCurrentIndex(game.index_lunhuifahuidaguai)
        self.ui.checkBox_zidonggongde.setCheckState(int(cfg_get('guaji', 'zidonggongde')))
        game.index_gongderenwu = int(cfg_get('guaji', 'gongderenwu'))
        self.ui.comboBox_gongderenwu.setCurrentIndex(game.index_gongderenwu)
        self.ui.checkBox_zidongshengdizi.setCheckState(int(cfg_get('guaji', 'zidongshengdizi')))
        game.index_menpaidizijibie = int(cfg_get('guaji', 'menpaidizijibie'))
        self.ui.comboBox_menpaidizijibie.setCurrentIndex(game.index_menpaidizijibie)
        self.ui.checkBox_zidongmenpailingwu.setCheckState(int(cfg_get('guaji', 'zidongmenpailingwu')))
        game.index_menpailingwuleixing = int(cfg_get('guaji', 'menpailingwuleixing'))
        self.ui.comboBox_menpailingwuleixing.setCurrentIndex(game.index_menpailingwuleixing)
        self.ui.checkBox_zidongzongmenjindi.setCheckState(int(cfg_get('guaji', 'zidongzongmenjindi')))
        game.index_zongmenjindi = int(cfg_get('guaji', 'zongmenjindi'))
        self.ui.comboBox_zongmenjindi.setCurrentIndex(game.index_zongmenjindi)
        self.ui.checkBox_zidongtongguantiaozhan.setCheckState(int(cfg_get('guaji', 'zidongtongguantiaozhan')))
        game.index_tongguantiaozhan = int(cfg_get('guaji', 'tongguantiaozhan'))
        self.ui.comboBox_tongguantiaozhan.setCurrentIndex(game.index_tongguantiaozhan)
        self.ui.checkBox_zidongganwutiandao.setCheckState(int(cfg_get('guaji', 'zidongganwutiandao')))
        game.index_ganwutiandao = int(cfg_get('guaji', 'ganwutiandao'))
        self.ui.comboBox_ganwutiandao.setCurrentIndex(game.index_ganwutiandao)
        self.ui.checkBox_zidongmaicha.setCheckState(int(cfg_get('guaji', 'zidongmaicha')))
        game.index_zidongmaicha = int(cfg_get('guaji', 'indexmaicha'))
        self.ui.comboBox_zidongmaicha.setCurrentIndex(game.index_zidongmaicha)
        self.ui.checkBox_gongdeche.setCheckState(int(cfg_get('guaji', 'gongdeche')))
        game.index_gongdeche = int(cfg_get('guaji', 'index_gongdeche'))
        self.ui.comboBox_gongdeche.setCurrentIndex(game.index_gongdeche)
        self.ui.checkBox_zidongfudan.setCheckState(int(cfg_get('guaji', 'zidongfudan')))
        game.index_fudanleixing = int(cfg_get('guaji', 'fudanleixing'))
        self.ui.comboBox_fudanleixing.setCurrentIndex(game.index_fudanleixing)
        self.ui.checkBox_zidongzhongtian.setCheckState(int(cfg_get('guaji', 'zidongzhongtian')))
        game.index_zhongzi = int(cfg_get('guaji', 'zhongzi'))
        self.ui.comboBox_zhongzi.setCurrentIndex(game.index_zhongzi)
        self.ui.checkBox_zongmenkuangmai.setCheckState(int(cfg_get('guaji', 'zongmenkuangmai')))
        game.index_zongmenkuangmai = int(cfg_get('guaji', 'index_zongmenkuangmai'))
        self.ui.comboBox_zongmenkuangmai.setCurrentIndex(game.index_zongmenkuangmai)
        self.ui.checkBox_zidongshenmu.setCheckState(int(cfg_get('guaji', 'zidongshenmu')))
        game.index_zidongshenmu = int(cfg_get('guaji', 'index_shenmu'))
        self.ui.comboBox_zidongshenmu.setCurrentIndex(game.index_zidongshenmu)
        self.ui.checkBox_zidongtianxiang.setCheckState(int(cfg_get('guaji', 'zidongtianxiang')))
        self.ui.checkBox_daozhu_zhanweizhi.setCheckState(int(cfg_get('guaji', 'daozhu_zhanweizhi')))
        self.ui.checkBox_dadi_zhanweizhi.setCheckState(int(cfg_get('guaji', 'dadi_zhanweizhi')))
        self.ui.checkBox_jiezhu_zhanweizhi.setCheckState(int(cfg_get('guaji', 'jiezhu_zhanweizhi')))
        self.ui.checkBox_tianshen_5ci.setCheckState(int(cfg_get('guaji', 'tianshen_5ci')))
        self.ui.checkBox_lingmai_5ci.setCheckState(int(cfg_get('guaji', 'lingmai_5ci')))
        self.ui.checkBox_aotu_longyu.setCheckState(int(cfg_get('guaji', 'aotu_longyu')))
        game.index_tianxiangleixing = int(cfg_get('guaji', 'tianxiangleixing'))
        self.ui.comboBox_tianxiangleixing.setCurrentIndex(game.index_tianxiangleixing)
        game.index_shenmozhanchang = int(cfg_get('guaji', 'index_shenmozhanchang'))
        self.ui.comboBox_shenmozhanchang.setCurrentIndex(game.index_shenmozhanchang)
        game.index_baoku_duihuan_cao = int(cfg_get('guaji', 'index_baoku_duihuan_cao'))
        self.ui.comboBox_baoku_duihuan_cao.setCurrentIndex(game.index_baoku_duihuan_cao)
        game.index_baoku_duihuan_kuang = int(cfg_get('guaji', 'index_baoku_duihuan_kuang'))
        self.ui.comboBox_baoku_duihuan_kuang.setCurrentIndex(game.index_baoku_duihuan_kuang)
        game.index_shoulie_didian1 = int(cfg_get('guaji', 'shoulie_didian1'))
        self.ui.comboBox_shoulie_didian1.setCurrentIndex(game.index_shoulie_didian1)
        game.index_shoulie_didian2 = int(cfg_get('guaji', 'shoulie_didian2'))
        self.ui.comboBox_shoulie_didian2.setCurrentIndex(game.index_shoulie_didian2)
        game.index_next_shoulie_didian = int(cfg_get('guaji', 'next_shoulie_didian'))
        self.ui.comboBox_next_shoulie_didian.setCurrentIndex(game.index_next_shoulie_didian)
        game.index_daotongpeiyang_moshi = int(cfg_get('guaji', 'daotongpeiyang_moshi'))
        self.ui.comboBox_daotongpeiyang_moshi.setCurrentIndex(game.index_daotongpeiyang_moshi)
        game.index_daotongpeiyang_dengji = int(cfg_get('guaji', 'daotongpeiyang_dengji'))
        self.ui.comboBox_daotongpeiyang_dengji.setCurrentIndex(game.index_daotongpeiyang_dengji)
        game.index_daotongpeiyang_zizhi = int(cfg_get('guaji', 'daotongpeiyang_zizhi'))
        self.ui.comboBox_daotongpeiyang_zizhi.setCurrentIndex(game.index_daotongpeiyang_zizhi)
        game.index_faxiangleixing = int(cfg_get('guaji', 'faxiangleixing'))
        self.ui.comboBox_faxiangleixing.setCurrentIndex(game.index_faxiangleixing)
        game.index_faxiangtaozhuang = int(cfg_get('guaji', 'faxiangtaozhuang'))
        self.ui.comboBox_faxiangtaozhuang.setCurrentIndex(game.index_faxiangtaozhuang)
        game.index_charge_value = int(cfg_get('guaji', 'index_charge_value'))
        self.ui.comboBox_charge_value.setCurrentIndex(game.index_charge_value)
        self.ui.checkBox_zidongtiaozhandadi.setCheckState(int(cfg_get('guaji', 'zidongtiaozhandadi')))
        game.index_tiaozhandadi = int(cfg_get('guaji', 'index_tiaozhandadi'))
        self.ui.comboBox_tiaozhandadi.setCurrentIndex(game.index_tiaozhandadi)
        game.index_tiaozhandaozhu = int(cfg_get('guaji', 'index_tiaozhandaozhu'))
        self.ui.comboBox_tiaozhan_daozhu.setCurrentIndex(game.index_tiaozhandaozhu)
        self.ui.checkBox_yuyue59xingjun.setCheckState(int(cfg_get('guaji', 'yuyue59xingjun')))
        self.ui.checkBox_yuyue59lingmai.setCheckState(int(cfg_get('guaji', 'yuyue59lingmai')))
        self.ui.checkBox_yuyue59tianshen.setCheckState(int(cfg_get('guaji', 'yuyue59tianshen')))
        self.ui.checkBox_yuyue59dianzhu.setCheckState(int(cfg_get('guaji', 'yuyue59dianzhu')))
        game.index_cur_tansuo = int(cfg_get('guaji', 'index_cur_tansuo'))
        self.ui.comboBox_hundunhai_cur_tansuo.setCurrentIndex(game.index_cur_tansuo)
        game.index_next_tansuo = int(cfg_get('guaji', 'index_next_tansuo'))
        self.ui.comboBox_hundunhai_next_tansuo.setCurrentIndex(game.index_next_tansuo)
        game.index_yuanhaimijing = int(cfg_get('guaji', 'index_yuanhaimijing'))
        self.ui.comboBox_yuanhaimijing.setCurrentIndex(game.index_yuanhaimijing)
        game.yuanhaimijing_cishu = int(cfg_get('guaji', 'yuanhaimijing_cishu'))
        self.ui.comboBox_yuanhaimijing_cishu.setCurrentIndex(game.yuanhaimijing_cishu)
        game.index_haishoutansuo = int(cfg_get('guaji', 'index_haishoutansuo'))
        self.ui.comboBox_haishoutansuo.setCurrentIndex(game.index_haishoutansuo)
        game.index_maixuanhuangzhu = int(cfg_get('guaji', 'index_maixuanhuangzhu'))
        self.ui.comboBox_maixuanhuangzhu.setCurrentIndex(game.index_maixuanhuangzhu)
        self.ui.comboBox_shilianzhidi.setCurrentIndex(int(cfg_get('guaji', 'index_shilianzhidi')))
        self.ui.comboBox_shiliancengshu.setCurrentIndex(int(cfg_get('guaji', 'index_shiliancengshu')))
        self.ui.comboBox_shiliangoumai.setCurrentIndex(int(cfg_get('guaji', 'index_shiliangoumai')))
        game.index_ronglian1 = int(cfg_get('guaji', 'index_ronglian1'))
        self.ui.comboBox_ronglian1.setCurrentIndex(game.index_ronglian1)
        game.index_ronglian2 = int(cfg_get('guaji', 'index_ronglian2'))
        self.ui.comboBox_ronglian2.setCurrentIndex(game.index_ronglian2)
        game.index_xumiding = int(cfg_get('guaji', 'index_xumiding'))
        self.ui.comboBox_xumiding.setCurrentIndex(game.index_xumiding)
        game.index_hunyuanwudao = int(cfg_get('guaji', 'index_hunyuanwudao'))
        self.ui.comboBox_hunyuanwudao.setCurrentIndex(game.index_hunyuanwudao)
        game.index_yunyangxiantian = int(cfg_get('guaji', 'index_yunyangxiantian'))
        self.ui.comboBox_yunyangxiantian.setCurrentIndex(game.index_yunyangxiantian)
        game.index_foguoganwu = int(cfg_get('guaji', 'index_foguoganwu'))
        self.ui.comboBox_foguoganwu.setCurrentIndex(game.index_foguoganwu)
        game.index_shuidaotong_work = int(cfg_get('guaji', 'index_shuidaotong_work'))
        self.ui.comboBox_shuidaotong_work.setCurrentIndex(game.index_shuidaotong_work)
        game.index_2_chuqiaoditu = int(cfg_get('guaji', 'index_2_chuqiaoditu'))
        self.ui.comboBox_2_chuqiaoditu.setCurrentIndex(game.index_2_chuqiaoditu)
        game.index_2_shengjimoshi = int(cfg_get('guaji', 'index_2_shengjimoshi'))
        self.ui.comboBox_2_shengjimoshi.setCurrentIndex(game.index_2_shengjimoshi)
        game.index_2_xiu_mode = int(cfg_get('guaji', 'index_2_xiu_mode'))
        self.ui.comboBox_2_xiu_mode.setCurrentIndex(game.index_2_xiu_mode)
        game.index_shengdaotu_level = int(cfg_get('guaji', 'index_shengdaotu_level'))
        self.ui.comboBox_shengdaotu_level.setCurrentIndex(game.index_shengdaotu_level)
        game.index_liandan_stop_type = int(cfg_get('guaji', 'index_liandan_stop_type'))
        self.ui.comboBox_liandan_stop_type.setCurrentIndex(game.index_liandan_stop_type)
        game.index_change_twt_fahui = int(cfg_get('guaji', 'index_change_twt_fahui'))
        self.ui.comboBox_change_twt_fahui.setCurrentIndex(game.index_change_twt_fahui)
        game.index_tourujingxue = int(cfg_get('guaji', 'index_tourujingxue'))
        self.ui.comboBox_tourujingxue.setCurrentIndex(game.index_tourujingxue)
        game.index_auto_lingyan_mode = int(cfg_get('guaji', 'index_auto_lingyan_mode'))
        self.ui.comboBox_auto_lingyan_mode.setCurrentIndex(game.index_auto_lingyan_mode)
        game.index_auto_yellowtide = int(cfg_get('guaji', 'index_auto_yellowtide'))
        self.ui.comboBox_auto_yellowtide.setCurrentIndex(game.index_auto_yellowtide)
        game.index_show_yellowtide = int(cfg_get('guaji', 'index_show_yellowtide'))
        self.ui.comboBox_show_yellowtide.setCurrentIndex(game.index_show_yellowtide)
        game.index_renjiandao_fudai = int(cfg_get('guaji', 'index_renjiandao_fudai'))
        self.ui.comboBox_renjiandao_fudai.setCurrentIndex(game.index_renjiandao_fudai)
        game.index_eguidao_fudai = int(cfg_get('guaji', 'index_eguidao_fudai'))
        self.ui.comboBox_eguidao_fudai.setCurrentIndex(game.index_eguidao_fudai)
        game.index_benming1_befor = int(cfg_get('guaji', 'index_benming1_befor'))
        self.ui.comboBox_benming1_befor.setCurrentIndex(game.index_benming1_befor)
        game.index_benming1_after = int(cfg_get('guaji', 'index_benming1_after'))
        self.ui.comboBox_benming1_after.setCurrentIndex(game.index_benming1_after)
        game.index_benming2_befor = int(cfg_get('guaji', 'index_benming2_befor'))
        self.ui.comboBox_benming2_befor.setCurrentIndex(game.index_benming2_befor)
        game.index_benming2_after = int(cfg_get('guaji', 'index_benming2_after'))
        self.ui.comboBox_benming2_after.setCurrentIndex(game.index_benming2_after)
        self.set_game_flag()
        mijing_list = cfg_get('guaji', 'mijing').split(',')
        for mijing in mijing_list:
            try:
                self.ui.listWidget_mijing.addItem(self.ui.comboBox_mijing.itemText(int(mijing)))
            except:
                pass

        self.set_mijing_list()
        self.update_auto_list()
        self.update_shenmo_shijian_list()
        self.read_skill_order()
        self.ui.comboBox_danyaoleixing.setCurrentIndex(int(cfg_get('liandan', 'danyaoleixing')))
        self.danyaoleixing_change(1)
        self.ui.comboBox_danyaojibie.setCurrentIndex(int(cfg_get('liandan', 'danyaojibie')))
        self.danyaojibie_change(1)
        self.ui.comboBox_danlujibie.setCurrentIndex(int(cfg_get('liandan', 'danlujibie')))
        self.ui.spinBox_lianzhicishu.setValue(int(cfg_get('liandan', 'lianzhicishu')))
        self.ui.comboBox_danyaoleixing2.setCurrentIndex(int(cfg_get('liandan', 'danyaoleixing2')))
        self.danyaoleixing_change(2)
        self.ui.comboBox_danyaojibie2.setCurrentIndex(int(cfg_get('liandan', 'danyaojibie2')))
        self.danyaojibie_change(2)
        self.ui.comboBox_danlujibie2.setCurrentIndex(int(cfg_get('liandan', 'danlujibie2')))
        self.ui.spinBox_lianzhicishu2.setValue(int(cfg_get('liandan', 'lianzhicishu2')))
        self.ui.comboBox_danyaoleixing3.setCurrentIndex(int(cfg_get('liandan', 'danyaoleixing3')))
        self.danyaoleixing_change(3)
        self.ui.comboBox_danyaojibie3.setCurrentIndex(int(cfg_get('liandan', 'danyaojibie3')))
        self.danyaojibie_change(3)
        self.ui.comboBox_danlujibie3.setCurrentIndex(int(cfg_get('liandan', 'danlujibie3')))
        self.ui.spinBox_lianzhicishu3.setValue(int(cfg_get('liandan', 'lianzhicishu3')))
        self.ui.comboBox_danyaoleixing4.setCurrentIndex(int(cfg_get('liandan', 'danyaoleixing4')))
        self.danyaoleixing_change(4)
        self.ui.comboBox_danyaojibie4.setCurrentIndex(int(cfg_get('liandan', 'danyaojibie4')))
        self.danyaojibie_change(4)
        self.ui.comboBox_danlujibie4.setCurrentIndex(int(cfg_get('liandan', 'danlujibie4')))
        self.ui.spinBox_lianzhicishu4.setValue(int(cfg_get('liandan', 'lianzhicishu4')))
        self.ui.comboBox_danyaoleixing5.setCurrentIndex(int(cfg_get('liandan', 'danyaoleixing5')))
        self.danyaoleixing_change(5)
        self.ui.comboBox_danyaojibie5.setCurrentIndex(int(cfg_get('liandan', 'danyaojibie5')))
        self.danyaojibie_change(5)
        self.ui.comboBox_danlujibie5.setCurrentIndex(int(cfg_get('liandan', 'danlujibie5')))
        self.ui.spinBox_lianzhicishu5.setValue(int(cfg_get('liandan', 'lianzhicishu5')))
        self.ui.comboBox_danyaoleixing6.setCurrentIndex(int(cfg_get('liandan', 'danyaoleixing6')))
        self.danyaoleixing_change(6)
        self.ui.comboBox_danyaojibie6.setCurrentIndex(int(cfg_get('liandan', 'danyaojibie6')))
        self.danyaojibie_change(6)
        self.ui.comboBox_danlujibie6.setCurrentIndex(int(cfg_get('liandan', 'danlujibie6')))
        self.ui.spinBox_lianzhicishu6.setValue(int(cfg_get('liandan', 'lianzhicishu6')))
        self.ui.checkBox_liandan2.setCheckState(int(cfg_get('liandan', 'liandan2')))
        self.liandan2_change()
        self.ui.checkBox_liandan3.setCheckState(int(cfg_get('liandan', 'liandan3')))
        self.liandan3_change()
        self.set_haoganrenwu_list()
        shoulie_place_index = cfg_get('hundunhai', 'shoulie_place_index')
        if len(shoulie_place_index) > 2:
            place_index_list = shoulie_place_index.split(',')
            self.ui.comboBox_hundunhai_shoulie_place_1.setCurrentIndex(int(place_index_list[0]))
            self.ui.comboBox_hundunhai_shoulie_place_2.setCurrentIndex(int(place_index_list[1]))
            self.ui.comboBox_hundunhai_shoulie_place_3.setCurrentIndex(int(place_index_list[2]))
            self.hundunhai_shoulie_place_change()
        dier_shentong_order = cfg_get('guaji', 'dier_shentong_order')
        if len(dier_shentong_order) > 2:
            type_index_list = dier_shentong_order.split(',')
            self.ui.comboBox_dier_shentong_1.setCurrentIndex(int(type_index_list[0]))
            self.ui.comboBox_dier_shentong_2.setCurrentIndex(int(type_index_list[1]))
            self.ui.comboBox_dier_shentong_3.setCurrentIndex(int(type_index_list[2]))
            self.dier_shentong_change()
        self.ui.comboBox_lianqileixing.setCurrentIndex(int(cfg_get('lianqi', 'lianqileixing')))
        self.lianqileixing_change()
        self.ui.comboBox_qilujibie.setCurrentIndex(int(cfg_get('lianqi', 'qilujibie')))
        self.ui.spinBox_lianqicishu.setValue(int(cfg_get('lianqi', 'lianqicishu')))
        return

    def wf_ini(self):
        print 'wf_ini'
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.write(open('config.ini', 'w'))
        return

    def read_guaji_cfg(self):
        try:
            self.guajileixing_change()
        except:
            traceback.print_exc()

        self.shuatucishu_change()
        fangan = int(cfg_get('fuben', 'guajifangan'))
        self.ui.comboBox_guajifangan.setCurrentIndex(fangan)
        self.update_shuatu_list()
        return

    def str2int(self, text):
        return int(text)

    def setbutton(self):
        self.ui.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.ui.lineEdit_password.setText(self.ui.lineEdit_password.text())
        self.ui.lineEdit_verifynum.setEchoMode(QLineEdit.Password)
        self.ui.lineEdit_verifynum.setText(self.ui.lineEdit_verifynum.text())
        self.ui.lineEdit_phonenum.setEnabled(False)
        self.ui.lineEdit_verifynum.setEnabled(False)
        return

    def logprint(self, str, int, print_time=True):
        global chonglianjiange
        label_dict = {101: (self.ui.label_jueseming), 102: (self.ui.label_level), 103: (self.ui.label_xiuwei), 104: (self.ui.label_lingshi), 105: (self.ui.label_shengwang), 106: (self.ui.label_lingqi), 107: (self.ui.label_fubenlunshu), 108: (self.ui.label_shiwu), 109: (self.ui.label_mucai), 110: (self.ui.label_lingcao), 111: (self.ui.label_xuantie), 112: (self.ui.label_julingzhen_level), 113: (self.ui.label_xisuichi_level), 114: (self.ui.label_menpaigongxian), 115: (self.ui.label_beibaorongliang), 116: (self.ui.label_servertime), 117: (self.ui.label_2), 118: (self.ui.label_dangqianxingjun), 119: (self.ui.label_dangqianlingmai), 120: (self.ui.label_taiyizhiqi), 121: (self.ui.label_taichuzhiqi), 122: (self.ui.label_taishizhiqi), 123: (self.ui.label_taijizhiqi), 124: (self.ui.label_taisuzhiqi), 125: (self.ui.label_yuanli), 126: (self.ui.label_shenshi), 127: (self.ui.label_dangqiantianshen), 128: (self.ui.label_dangqianmap), 129: (self.ui.label_dangqianmenpai), 130: (self.ui.label_dangqianfudimap), 131: (self.ui.label_shuatujindu), 132: (self.ui.label_shanglunyongshi), 133: (self.ui.label_skillcount), 134: (self.ui.label_shenmozhanchangshengyucishu), 135: (self.ui.label_haishoutansuo), 136: (self.ui.label_shiliansuozaidi), 137: (self.ui.label_shilianlingli), 138: (self.ui.label_shilianjifen), 139: (self.ui.label_shilianshitou), 140: (self.ui.label_shilianquyu), 141: (self.ui.label_shilianjibaishu), 142: (self.ui.label_shiliangongdeduihuan), 143: (self.ui.label_shilianshanglingduihuan), 144: (self.ui.label_foguo_jindu), 145: (self.ui.label_yaoguo_jindu), 146: (self.ui.label_haiguo_jindu), 147: (self.ui.label_zhandou_chongwu), 148: (self.ui.label_luxing_chongwu), 149: (self.ui.label_feixing_chongwu), 150: (self.ui.label_yuhai_chongwu), 151: (self.ui.label_lianti_body_level), 152: (self.ui.label_lianti_qixue), 153: (self.ui.label_hongmengyuanye), 154: (self.ui.label_xinyangzhili), 155: (self.ui.label_fabao1), 156: (self.ui.label_fabao2), 157: (self.ui.label_lianti_shengyuqixue), 158: (self.ui.label_tianwaitianfahuishengwang), 159: (self.ui.label_dangqianlunhuifahui), 160: (self.ui.label_gongde), 161: (self.ui.label_jinlingyuan), 162: (self.ui.label_mulingyuan), 163: (self.ui.label_shuilingyuan), 164: (self.ui.label_huolingyuan), 165: (self.ui.label_tulingyuan), 166: (self.ui.label_lingye), 167: (self.ui.label_daotong_count), 168: (self.ui.label_puyi_count), 169: (self.ui.label_yuanshendengji), 170: (self.ui.label_yijindan), 171: (self.ui.label_yaoguoshoulie_didian), 172: (self.ui.label_yaoguo_jingxue1), 173: (self.ui.label_yaoguo_jingxue2), 174: (self.ui.label_liantijue_bei), 175: (self.ui.label_liantijue_nan), 176: (self.ui.label_liantijue_xi), 177: (self.ui.label_liantijue_dong), 178: (self.ui.label_yellowtide_starttime), 179: (self.ui.label_yellowtide_explorertime), 180: (self.ui.label_yellowtide_endtime), 181: (self.ui.label_yellowtide_status), 182: (self.ui.label_yellowtide_lingyan_weizhi1), 183: (self.ui.label_yellowtide_tansuo_weizhi1), 184: (self.ui.label_yuanshenzhili), 185: (self.ui.label_renjiandao), 186: (self.ui.label_eguidao), 187: (self.ui.label_fudai), 188: (self.ui.label_tisicaoren), 189: (self.ui.label_xianmoti), 190: (self.ui.label_kongxingzhou), 191: (self.ui.label_nanhailianmeng), 192: (self.ui.label_daozhu_jindu), 193: (self.ui.label_longfengbi), 194: (self.ui.label_shenguan_jiezhu), 195: (self.ui.label_dangqianxingjun_2), 196: (self.ui.label_shenguan_myjiezhu), 197: (self.ui.label_fabao3), 198: (self.ui.label_fabao3_info)}
        label_dict2 = {3001: (self.ui.label_foguo_ganwu1), 3002: (self.ui.label_foguo_ganwu2), 3003: (self.ui.label_foguo_ganwu3), 3004: (self.ui.label_foguo_ganwu4), 3005: (self.ui.label_foguo_ganwu5), 3006: (self.ui.label_foguo_ganwu6), 3007: (self.ui.label_foguo_ganwu7), 3008: (self.ui.label_foguo_ganwu8), 3009: (self.ui.label_foguo_ganwu9), 3010: (self.ui.label_foguo_ganwu10), 3011: (self.ui.label_dadi_longyu_shuliang), 3012: (self.ui.label_daozhu_longyu_shuliang), 3013: (self.ui.label_shenguan_dadi), 3014: (self.ui.label_dangqiantianshen_2), 3015: (self.ui.label_shenguan_mydadi), 3016: (self.ui.label_shenguan_daozhu), 3017: (self.ui.label_hundunhai_guanwei_2), 3018: (self.ui.label_shenguan_mydaozhu)}
        text_dict = {211: (self.ui.lineEdit_xingjun_11), 212: (self.ui.lineEdit_xingjun_12), 213: (self.ui.lineEdit_xingjun_13), 214: (self.ui.lineEdit_xingjun_14), 215: (self.ui.lineEdit_xingjun_15), 216: (self.ui.lineEdit_xingjun_16), 217: (self.ui.lineEdit_xingjun_17), 218: (self.ui.lineEdit_xingjun_18), 219: (self.ui.lineEdit_xingjun_19), 220: (self.ui.lineEdit_xingjun_20), 221: (self.ui.lineEdit_xingjun_21), 222: (self.ui.lineEdit_xingjun_22), 223: (self.ui.lineEdit_xingjun_23)}
        lingmai_text_dict = {306: (self.ui.lineEdit_lingmai6), 305: (self.ui.lineEdit_lingmai5), 304: (self.ui.lineEdit_lingmai4), 303: (self.ui.lineEdit_lingmai3), 302: (self.ui.lineEdit_lingmai2), 301: (self.ui.lineEdit_lingmai1)}
        tianshen_text_dict = {411: (self.ui.lineEdit_tianshen11), 412: (self.ui.lineEdit_tianshen12), 413: (self.ui.lineEdit_tianshen13), 414: (self.ui.lineEdit_tianshen14), 415: (self.ui.lineEdit_tianshen15), 416: (self.ui.lineEdit_tianshen16), 417: (self.ui.lineEdit_tianshen17), 418: (self.ui.lineEdit_tianshen18), 419: (self.ui.lineEdit_tianshen19), 420: (self.ui.lineEdit_tianshen20)}
        shilian_text_dict = {501: (self.ui.lineEdit_shilian_weizhi1), 502: (self.ui.lineEdit_shilian_weizhi2), 503: (self.ui.lineEdit_shilian_weizhi3), 504: (self.ui.lineEdit_shilian_weizhi4), 505: (self.ui.lineEdit_shilian_weizhi5)}
        hundunhai_lable_dict = {601: (self.ui.label_hundunzhili), 602: (self.ui.label_hundunhai_tansuo_shengyu_count), 603: (self.ui.label_hundunhai_tansuo_shengyu_goumai), 604: (self.ui.label_xuanhuangzhiqi), 605: (self.ui.label_xuanhuangzhu_count), 606: (self.ui.label_jiuxuanwudao_xinde), 607: (self.ui.label_hundunhuoyuan), 608: (self.ui.label_hundunshuijing), 609: (self.ui.label_hundunmusui), 610: (self.ui.label_hundunjinjing), 611: (self.ui.label_hunduntuyuan), 612: (self.ui.label_hundunhai_guanwei), 613: (self.ui.label_shoulie_cishu), 614: (self.ui.label_daowenshuliang), 615: (self.ui.label_xuanhuangzhiqi2)}
        dianzhu_text_dict = {701: (self.ui.lineEdit_dianzhu_1), 702: (self.ui.lineEdit_dianzhu_2), 703: (self.ui.lineEdit_dianzhu_3), 704: (self.ui.lineEdit_dianzhu_4), 705: (self.ui.lineEdit_dianzhu_5), 706: (self.ui.lineEdit_dianzhu_6), 707: (self.ui.lineEdit_dianzhu_7)}
        haoganrenwu_lable_dict = {8001: (self.ui.label_haoganrenwu_1), 8007: (self.ui.label_haoganrenwu_2), 8011: (self.ui.label_haoganrenwu_3), 8026: (self.ui.label_haoganrenwu_4), 8028: (self.ui.label_haoganrenwu_5), 8031: (self.ui.label_haoganrenwu_6), 8042: (self.ui.label_haoganrenwu_7), 8045: (self.ui.label_haoganrenwu_8), 8062: (self.ui.label_haoganrenwu_9), 8064: (self.ui.label_haoganrenwu_10), 8067: (self.ui.label_haoganrenwu_11), 8077: (self.ui.label_haoganrenwu_12), 8082: (self.ui.label_haoganrenwu_13), 8095: (self.ui.label_haoganrenwu_14), 8098: (self.ui.label_haoganrenwu_15), 8101: (self.ui.label_haoganrenwu_16), 8108: (self.ui.label_haoganrenwu_17), 8119: (self.ui.label_haoganrenwu_18), 8127: (self.ui.label_haoganrenwu_19), 8134: (self.ui.label_haoganrenwu_20), 8140: (self.ui.label_haoganrenwu_21), 8136: (self.ui.label_haoganrenwu_22), 8157: (self.ui.label_haoganrenwu_23), 8160: (self.ui.label_haoganrenwu_24), 8164: (self.ui.label_haoganrenwu_25), 8184: (self.ui.label_haoganrenwu_26), 8181: (self.ui.label_haoganrenwu_27), 8193: (self.ui.label_haoganrenwu_28), 8204: (self.ui.label_haoganrenwu_29), 8199: (self.ui.label_haoganrenwu_30), 8214: (self.ui.label_haoganrenwu_31), 8221: (self.ui.label_haoganrenwu_32), 8236: (self.ui.label_haoganrenwu_33), 8241: (self.ui.label_haoganrenwu_34), 8247: (self.ui.label_haoganrenwu_35), 8244: (self.ui.label_haoganrenwu_36)}
        textBrowser_dict = {46: (self.ui.textBrowser_myjingjie_years), 47: (self.ui.textBrowser_roushen_years), 1001: (self.ui.textBrowser_zuikuaifenshen), 1002: (self.ui.textBrowser_zuikuaiheti), 1003: (self.ui.textBrowser_zuikuaidongxu), 1004: (self.ui.textBrowser_zuikuaidacheng), 1005: (self.ui.textBrowser_zuikuaidongzhen), 1006: (self.ui.textBrowser_zuikuaisanxian), 1007: (self.ui.textBrowser_zuikuaiyouxian), 1008: (self.ui.textBrowser_zuikuaidixian1), 1009: (self.ui.textBrowser_zuikuaitianxian), 1010: (self.ui.textBrowser_zuikuaijinxian), 1011: (self.ui.textBrowser_zuikuaidaluojinxian), 1012: (self.ui.textBrowser_zuikuaixuanxian), 1013: (self.ui.textBrowser_zuikuaixianjun), 1014: (self.ui.textBrowser_zuikuaixianzun), 1015: (self.ui.textBrowser_zuikuaizhundixian), 1016: (self.ui.textBrowser_zuikuaidixian2), 1017: (self.ui.textBrowser_zuikuaizhunsheng), 1018: (self.ui.textBrowser_zuikuaishengren), 1019: (self.ui.textBrowser_zuikuaiyizhuanshengren), 1020: (self.ui.textBrowser_zuikuaierzhuanshengren), 1101: (self.ui.textBrowser_zhenfangzonghe), 1102: (self.ui.textBrowser_zuidalunshu), 1103: (self.ui.textBrowser_hundunzhili), 1104: (self.ui.textBrowser_dongxudachengfangyu), 1105: (self.ui.textBrowser_dongzhenqifangyu), 1106: (self.ui.textBrowser_sanxianyouxianfangyu), 1107: (self.ui.textBrowser_dixian1fangyu), 1108: (self.ui.textBrowser_tianxianqifangyu), 1109: (self.ui.textBrowser_jinxiandaluofangyu), 1110: (self.ui.textBrowser_xuanxianqifangyu), 1111: (self.ui.textBrowser_xianjunqifangyu), 1112: (self.ui.textBrowser_xianzunqifangyu), 1113: (self.ui.textBrowser_zhundixianqifangyu), 1114: (self.ui.textBrowser_dixian2fangyu), 1115: (self.ui.textBrowser_zhunshengqifangyu), 1116: (self.ui.textBrowser_shengrenqifangyu), 1117: (self.ui.textBrowser_yizhuanshengrenfangyu), 1118: (self.ui.textBrowser_erzhuanshengrenfangyu), 1201: (self.ui.textBrowser_xianchongzizhi), 1202: (self.ui.textBrowser_guichongzizhi), 1203: (self.ui.textBrowser_mochongzizhi), 1204: (self.ui.textBrowser_haichongzizhi), 1205: (self.ui.textBrowser_longfenggongji2), 1206: (self.ui.textBrowser_longfenggongji3), 1207: (self.ui.textBrowser_longfenggongji4), 1208: (self.ui.textBrowser_longfenggongji5), 1209: (self.ui.textBrowser_longfenggongji6), 1210: (self.ui.textBrowser_longfenggongji7), 1211: (self.ui.textBrowser_longfenggongji8), 1212: (self.ui.textBrowser_longfenggongji9), 1301: (self.ui.textBrowser_three_daotong_zuiduo), 1302: (self.ui.textBrowser_one_daotong_zuiduo), 1303: (self.ui.textBrowser_chouman_daotong_zuishao), 1304: (self.ui.textBrowser_chouman_daotong_zuiduo), 1305: (self.ui.textBrowser_shuidaotong51), 1306: (self.ui.textBrowser_shuidaotong61), 1307: (self.ui.textBrowser_shuidaotong71), 1308: (self.ui.textBrowser_shuidaotong101), 1309: (self.ui.textBrowser_shuidaotong130)}
        label_paihang_dict = {2001: (self.ui.label_zuikuaifenshen), 2002: (self.ui.label_zuikuaiheti), 2003: (self.ui.label_zuikuaidongxu), 2004: (self.ui.label_zuikuaidacheng), 2005: (self.ui.label_zuikuaidongzhen), 2006: (self.ui.label_zuikuaisanxian), 2007: (self.ui.label_zuikuaiyouxian), 2008: (self.ui.label_zuikuaidixian1), 2009: (self.ui.label_zuikuaitianxian), 2010: (self.ui.label_zuikuaijinxian), 2011: (self.ui.label_zuikuaidaluojinxian), 2012: (self.ui.label_zuikuaixuanxian), 2013: (self.ui.label_zuikuaixianjun), 2014: (self.ui.label_zuikuaixianzun), 2015: (self.ui.label_zuikuaizhundixian), 2016: (self.ui.label_zuikuaidixian2), 2017: (self.ui.label_zuikuaizhunsheng), 2018: (self.ui.label_zuikuaishengren), 2019: (self.ui.label_zuikuaiyizhuanshengren), 2020: (self.ui.label_zuikuaierzhuanshengren), 2301: (self.ui.label_three_daotong_zuiduo), 2302: (self.ui.label_one_daotong_zuiduo), 2303: (self.ui.label_chouman_daotong_zuishao), 2304: (self.ui.label_chouman_daotong_zuiduo), 2305: (self.ui.label_shuidaotong51), 2306: (self.ui.label_shuidaotong61), 2307: (self.ui.label_shuidaotong71), 2308: (self.ui.label_shuidaotong101), 2309: (self.ui.label_shuidaotong130)}
        label_2_huashen_dict = {20001: (self.ui.label_2_level), 20002: (self.ui.label_2_roushen), 20003: (self.ui.label_2_xiuwei), 20004: (self.ui.label_2_lunshu), 20005: (self.ui.label_2_xianjie), 20006: (self.ui.label_2_guijie), 20007: (self.ui.label_2_mojie), 20008: (self.ui.label_2_shenjie), 20009: (self.ui.label_2_fudixiaoshijie), 20010: (self.ui.label_2_zongmenyizhi), 20011: (self.ui.label_hundun_fabao_name), 20012: (self.ui.label_hundun_fabao_lv), 20013: (self.ui.label_xumiding_jindu)}
        button_2_huashen_dict = {20301: (self.ui.pushButton_2_xianjie), 20302: (self.ui.pushButton_2_guijie), 20303: (self.ui.pushButton_2_mojie), 20304: (self.ui.pushButton_2_shenjie), 20305: (self.ui.pushButton_2_fudixiaoshijie), 20306: (self.ui.pushButton_2_zongmenyizhi)}
        now = time.strftime('\n[%Y-%m-%d %H:%M:%S] ', time.localtime(time.time()))
        if int > 100 and int < 200:
            label_dict[int].setText(str)
        if int > 2000 and int < 3000:
            label_paihang_dict[int].setText(str)
        if int > 3000 and int < 4000:
            label_dict2[int].setText(str)
        if int > 20000 and int < 20300:
            label_2_huashen_dict[int].setText(str)
        if int > 20300 and int < 20400:
            if self.str2int(str) == 0:
                button_2_huashen_dict[int].setEnabled(False)
            else:
                button_2_huashen_dict[int].setEnabled(True)
        if int == 200:
            self.setWindowTitle(u'[' + str + u']' + u'想不想修真—兔子辅助v8.5--一千天的陪伴，数万年的服务')
        if int > 200 and int < 300:
            text_dict[int].setText(str)
        if int > 300 and int < 400:
            lingmai_text_dict[int].setText(str)
        if int > 400 and int < 500:
            tianshen_text_dict[int].setText(str)
        if int > 500 and int < 600:
            shilian_text_dict[int].setText(str)
        if int > 600 and int < 700:
            hundunhai_lable_dict[int].setText(str)
        if int > 700 and int < 720:
            dianzhu_text_dict[int].setText(str)
        if int > 8000 and int < 9000:
            haoganrenwu_lable_dict[int].setText(str)
        if int > 1000 and int < 1600:
            textBrowser_dict[int].clear()
            textBrowser_dict[int].append(str)
        if int == 20401:
            if len(str) < 2:
                self.ui.textBrowser_2_tiaozhan_info.clear()
            else:
                self.ui.textBrowser_2_tiaozhan_info.append(str)
        if int == 20402:
            if len(str) < 2:
                self.ui.textBrowser_xiantian_daotu.clear()
            else:
                self.ui.textBrowser_xiantian_daotu.append(str)
        if int == 20403:
            if len(str) < 2:
                self.ui.textBrowser_hundun_daotu.clear()
            else:
                self.ui.textBrowser_hundun_daotu.append(str)
        if int == 0:
            self.webdialog.ui.qwebview.load(QUrl(str))
            self.webdialog.show()
        if int == 1:
            self.ui.textBrowser_fuben.append(now + str)
        if int == 2:
            if print_time:
                self.ui.textBrowser_liandan.append(now[1:] + str)
            else:
                self.ui.textBrowser_liandan.append(str)
        if int == 3:
            self.ui.textBrowser_xitongxinxi.append(now + str)
        if int == 4:
            self.read_guaji_cfg()
        if int == 5:
            self.ui.textBrowser_xuexijineng.append(str)
        if int == 6:
            parts = str.split(u'|')
            id = self.str2int(parts[0])
            text = parts[1]
            color = self.str2int(parts[2])
            self.hundunhai_button_modify(id, text, color)
        if int == 7:
            QtGui.QMessageBox.information(self, u'【提醒】', u'【注意】：灵石不够最大轮数，卡满收益要注意。')
        if int == 8:
            type = self.str2int(str)
            if type == 0:
                today = self.str2int(time.strftime('%Y%m%d', time.localtime()))
                yuanhai_date = self.str2int(cfg_get('guaji', 'yuanhaimijing_date'))
                if today == yuanhai_date:
                    game.today_is_yuanhai = True
                else:
                    game.today_is_yuanhai = False
            else:
                today = time.strftime('%Y%m%d', time.localtime())
                cfg_set('guaji', 'yuanhaimijing_date', today)
        if int == 9:
            if len(str) < 2:
                self.ui.textBrowser_2_chidan.clear()
            else:
                self.ui.textBrowser_2_chidan.append(str)
        if int == 10:
            if len(str) < 2:
                self.ui.textBrowser_2_jineng.clear()
            else:
                self.ui.textBrowser_2_jineng.append(str)
        if int == 11:
            self.stoptoutu()
        if int == 12:
            self.ui.comboBox_query_xingjun.setCurrentIndex(self.str2int(str) - 1026)
        if int == 13:
            self.stopLiandan()
        if int == 14:
            self.stopGuaji()
        if int == 15:
            self.ui.label_leasttime.setText(u'辅助剩余时间：' + str)
        if int == 16:
            self.ui.lineEdit_chongzhiID.setText(str)
        if int == 17:
            if str == u'11':
                self.tiaozhan_daozhu_change(False)
            else:
                self.ui.textBrowser_query.append(str)
        if int == 18:
            self.stopLianqi()
        if int == 19:
            self.ui.pushButton_yijianshoudaotong.setEnabled(True)
            self.ui.pushButton_yijianshoudaotong2.setEnabled(True)
            self.ui.pushButton_yijianshoudaotong3.setEnabled(True)
        if int == 20:
            self.ui.pushButton_lijichonglian.setEnabled(True)
            self.ui.pushButton_lijichonglian.setVisible(True)
        if int == 21:
            self.ui.textBrowser_fuben.setPlainText('')
            self.ui.textBrowser_liandan.setPlainText('')
            self.ui.textBrowser_xitongxinxi.setPlainText('')
            self.ui.textBrowser_daotongpeiyang_info.setPlainText('')
            self.ui.textBrowser_lunhuidian_xinxi.setPlainText('')
            self.print_daotongpeiyang_info()
        if int == 22:
            self.ui.label_shengjixuyao.setText(str)
        if int == 23:
            self.ui.label_haichaduoshao.setText(str)
        if int == 24:
            print str
            fenjie = self.str2int(str) / 100
            map = self.str2int(str) % 100
            print fenjie, map
            self.ui.comboBox_query_fenjie.setCurrentIndex(fenjie)
            self.query_fenjie_change(False)
            self.ui.comboBox_query_map.setCurrentIndex(map)
            self.query_map_change()
        if int == 25:
            self.ui.textBrowser_zhongyaoxinxi_2.append(now + str)
        if int == 26:
            self.ui.pushButton_lijichonglian.setEnabled(False)
            self.ui.pushButton_lijichonglian.setVisible(False)
        if int == 27:
            self.ui.textBrowser_lingmaiinfo.append(now + '\n' + str)
        if int == 28:
            index = self.str2int(str.split(u'|')[0])
            text = str.split(u'|')[1]
            self.ui.comboBox_ganwutiandao.setItemText(index, text)
        if int == 29:
            index = self.str2int(str.split(u'|')[0])
            status = self.str2int(str.split(u'|')[1])
            self.step_status[index] = status
            self.update_shuatu_list()
        if int == 30:
            if self.str2int(str) == 1:
                self.ui.pushButton_study_xinfa.setEnabled(False)
            else:
                self.ui.pushButton_study_xinfa.setEnabled(True)
        if int == 31:
            if self.str2int(str) == 1:
                self.ui.pushButton_study_gongjue.setEnabled(False)
            else:
                self.ui.pushButton_study_gongjue.setEnabled(True)
        if int == 32:
            self.ui.textBrowser_shilian_log_dongzuo.append(str)
        if int == 33:
            self.ui.textBrowser_shilian_log_tongji.append(str)
        if int == 34:
            self.ui.textBrowser_xiaoshijie.clear()
        if int == 35:
            self.ui.textBrowser_xiaoshijie.append(str)
        if int == 36:
            if self.str2int(str) == 0:
                self.ui.label_tuzi_tips_yueka.setVisible(False)
            else:
                self.ui.label_tuzi_tips_yueka.setVisible(True)
        if int == 37:
            if self.str2int(str) == 0:
                self.ui.label_tuzi_tips_putong.setVisible(False)
            else:
                self.ui.label_tuzi_tips_putong.setVisible(True)
        if int == 38:
            if self.str2int(str) == 0:
                self.ui.label_tuzi_tips_shoushua.setVisible(False)
            else:
                self.ui.label_tuzi_tips_shoushua.setVisible(True)
        if int == 39:
            pass
        if int == 40:
            if print_time:
                self.ui.textBrowser_xuanhuangchaoxi.append(now + str)
            else:
                self.ui.textBrowser_xuanhuangchaoxi.append(str)
        if int == 41:
            if len(str) < 2:
                self.ui.textBrowser_jueseshuxing.clear()
            elif print_time:
                self.ui.textBrowser_jueseshuxing.append(now + str)
            else:
                self.ui.textBrowser_jueseshuxing.append(str)
        if int == 42:
            if len(str) < 2:
                self.ui.textBrowser_yuanli_shop.clear()
            else:
                self.ui.textBrowser_yuanli_shop.append(now + str)
        if int == 43:
            self.ui.textBrowser_zhongyaoxinxi.append(now + str)
        if int == 44:
            self.refresh_daotongpeiyang()
        if int == 45:
            self.ui.textBrowser_daotongpeiyang_info.append(now + str)
        if int >= 46 and int <= 50:
            if len(str) < 2:
                textBrowser_dict[int].clear()
            else:
                textBrowser_dict[int].append(str)
        if int == 51:
            if print_time:
                self.ui.textBrowser_lunhuidian_xinxi.append(now + str)
            else:
                self.ui.textBrowser_lunhuidian_xinxi.append(str)
        if int == 52:
            self.comboBox_renjiandao_fudai_change()
            self.comboBox_eguidao_fudai_change()
        if int == 53:
            if print_time:
                self.ui.textBrowser_hundunhai_info.append(now + str)
            else:
                self.ui.textBrowser_hundunhai_info.append(str)
        if int == 54:
            chonglianjiange = 2
        if int == 55:
            self.ui.comboBox_hundunhai_cur_tansuo.clear()
            self.ui.comboBox_hundunhai_next_tansuo.clear()
            self.ui.comboBox_hundunhai_cur_tansuo.addItem(u'选择当前探索位置')
            self.ui.comboBox_hundunhai_next_tansuo.addItem(u'下一个探索位置')
            id_list = [0, 1, 3, 2, 13, 14, 6, 7, 22, 12, 4, 15, 8, 11, 9, 20, 
             24, 10, 17, 23, 21, 26, 18, 25, 5, 29, 31, 
             33, 35, 27, 30, 28, 32, 34, 16, 36, 42, 38, 
             39, 41, 19, 43, 47, 40, 45, 49, 51, 52, 46, 
             48, 44, 53, 60, 54, 56, 62, 37, 58, 59, 55, 
             69, 66, 50, 57, 71, 64, 70, 68, 65, 78, 61, 
             74, 67, 72, 76, 79, 77, 63, 87, 83, 75, 89, 
             81, 86, 80, 82, 96, 92, 84, 94, 97, 73, 95, 
             98, 91, 105, 101, 93, 85, 99, 103, 106, 104, 
             114, 110, 88, 102, 116, 108, 112, 113, 109, 123, 
             90, 119, 111, 125, 117, 121, 124, 107, 118, 122, 
             120, 100, 115, 126, 129, 127, 128, 133, 132, 
             131, 134, 130, 135, 140, 139, 148, 141, 138, 
             137, 142, 136, 143, 144, 147, 149, 157, 150, 
             146, 145, 151, 152, 156, 158, 166, 159, 155, 
             154, 160, 153, 161, 165, 167, 168, 175, 164, 
             163, 169, 162, 170, 174, 176, 177, 184, 173, 
             178, 171, 172, 179, 183, 185, 186, 182, 187, 
             189, 181, 180, 188, 193, 190, 195, 194, 192, 
             191, 196, 197, 201, 202, 204, 200, 203, 199, 
             205, 211, 198, 206, 213, 210, 209, 208, 212, 
             218, 214, 207, 220, 215, 219, 222, 223, 217, 
             221, 216, 224, 229, 225, 231, 227, 226, 232, 
             230, 233, 228, 238, 240, 237, 236, 241, 234, 
             239, 242, 247, 246, 249, 235, 245, 244, 250, 
             243, 251, 248, 252, 255, 253, 254, 259, 258, 
             260, 256, 261, 266, 257, 265, 274, 267, 264, 
             262, 269, 268, 275, 263, 273, 283, 276, 272, 
             277, 270, 278, 271, 284, 282, 292, 285, 281, 
             286, 279, 287, 280, 289, 293, 291, 294, 301, 
             290, 295, 288, 296, 305, 303, 300, 310, 299, 
             304, 297, 302, 298, 311, 312, 309, 315, 308, 
             313, 306, 314, 307, 316, 321, 320, 318, 319, 
             322, 323, 328, 317, 330, 329, 326, 331, 327, 
             337, 324, 325, 332, 335, 338, 339, 340, 333, 
             336, 346, 341, 334, 342, 348, 344, 349, 347, 
             350, 355, 343, 345, 357, 353, 358, 356, 354, 
             359, 364, 352, 351, 362, 367, 366, 365, 368, 
             363, 373, 360, 375, 361, 371, 376, 377, 374, 
             369, 372, 370, 378]
            for xid in range(1, len(self.tansuo_name)):
                item_text = self.tansuo_name[xid]
                place_id = id_list[xid]
                if place_id in game_obj.hundunhai_yitansuo_list:
                    self.ui.comboBox_hundunhai_cur_tansuo.addItem(u'[已探索]' + item_text)
                    self.ui.comboBox_hundunhai_next_tansuo.addItem(u'[已探索]' + item_text)
                elif place_id in game_obj.hundunhai_ketansuo_list:
                    self.ui.comboBox_hundunhai_cur_tansuo.addItem(item_text)
                    self.ui.comboBox_hundunhai_next_tansuo.addItem(item_text)
                else:
                    self.ui.comboBox_hundunhai_cur_tansuo.addItem(u'  ' + item_text)
                    self.ui.comboBox_hundunhai_next_tansuo.addItem(u'  ' + item_text)

            self.ui.comboBox_hundunhai_cur_tansuo.setCurrentIndex(game.index_cur_tansuo)
            self.ui.comboBox_hundunhai_next_tansuo.setCurrentIndex(game.index_next_tansuo)
        if int == 56:
            if print_time:
                self.ui.textBrowser_hundunhai_info_2.append(now + str)
            else:
                self.ui.textBrowser_hundunhai_info_2.append(str)
        if int == 57:
            self.startLianqi()
        if int == 58:
            if len(str) == 0:
                self.ui.comboBox_shenguan_guanwei_list.clear()
            elif len(str) == 1:
                self.ui.comboBox_shenguan_guanwei_list.setCurrentIndex(9)
            else:
                self.ui.comboBox_shenguan_guanwei_list.addItem(str)
        if int == 59:
            if self.str2int(str) == 0:
                self.ui.groupBox_jiezhu_piguan.setEnabled(False)
                self.ui.groupBox_guanwei_apply.setEnabled(True)
            else:
                self.ui.groupBox_jiezhu_piguan.setEnabled(True)
                self.ui.groupBox_guanwei_apply.setEnabled(False)
        if int == 60:
            if len(str) < 2:
                self.ui.comboBox_guanwei_apply_list.clear()
                self.ui.comboBox_guanwei_apply_list.addItem(u'申请列表')
            else:
                self.ui.comboBox_guanwei_apply_list.addItem(str)
        if int == 61:
            if len(str) == 0:
                self.ui.comboBox_guanwei_list.clear()
            elif len(str) == 1:
                self.ui.comboBox_guanwei_list.setCurrentIndex(9)
            else:
                self.ui.comboBox_guanwei_list.addItem(str)
        if int == 62:
            if print_time:
                self.ui.textBrowser_hundunhai_info_3.append(now + str)
            else:
                self.ui.textBrowser_hundunhai_info_3.append(str)
        if int == 63:
            if self.str2int(str) == 0:
                self.ui.groupBox_dadi_guanwei_apply.setEnabled(True)
                self.ui.groupBox_dadi_piguan.setEnabled(False)
            else:
                self.ui.groupBox_dadi_guanwei_apply.setEnabled(False)
                self.ui.groupBox_dadi_piguan.setEnabled(True)
        if int == 64:
            if self.str2int(str) == 0:
                self.ui.groupBox_daozhu_guanwei_apply.setEnabled(True)
                self.ui.groupBox_daozhu_piguan.setEnabled(False)
            else:
                self.ui.groupBox_daozhu_guanwei_apply.setEnabled(False)
                self.ui.groupBox_daozhu_piguan.setEnabled(True)
        if int == 65:
            if len(str) == 0:
                self.ui.comboBox_shenguan_dadi_guanwei_list.clear()
            elif len(str) == 1:
                self.ui.comboBox_shenguan_dadi_guanwei_list.setCurrentIndex(9)
            else:
                self.ui.comboBox_shenguan_dadi_guanwei_list.addItem(str)
        if int == 66:
            if len(str) == 0:
                self.ui.comboBox_shenguan_daozhu_guanwei_list.clear()
            elif len(str) == 1:
                self.ui.comboBox_shenguan_daozhu_guanwei_list.setCurrentIndex(7)
            else:
                self.ui.comboBox_shenguan_daozhu_guanwei_list.addItem(str)
        if int == 67:
            if len(str) == 0:
                self.ui.comboBox_dadi_guanwei_list.clear()
            elif len(str) == 1:
                self.ui.comboBox_dadi_guanwei_list.setCurrentIndex(9)
            else:
                self.ui.comboBox_dadi_guanwei_list.addItem(str)
        if int == 68:
            if len(str) == 0:
                self.ui.comboBox_daozhu_guanwei_list.clear()
            elif len(str) == 1:
                self.ui.comboBox_daozhu_guanwei_list.setCurrentIndex(7)
            else:
                self.ui.comboBox_daozhu_guanwei_list.addItem(str)
        if int == 69:
            if len(str) < 2:
                self.ui.comboBox_dadi_guanwei_apply_list.clear()
                self.ui.comboBox_dadi_guanwei_apply_list.addItem(u'申请列表')
            else:
                self.ui.comboBox_dadi_guanwei_apply_list.addItem(str)
        if int == 70:
            if len(str) < 2:
                self.ui.comboBox_daozhu_guanwei_apply_list.clear()
                self.ui.comboBox_daozhu_guanwei_apply_list.addItem(u'申请列表')
            else:
                self.ui.comboBox_daozhu_guanwei_apply_list.addItem(str)
        if int == 71:
            self.ui.textBrowser_shenguan_info.append(now + str)
        if int == 77:
            self.ui.comboBox_yellowtide_haiyan1.clear()
            self.ui.comboBox_yellowtide_haiyan1.addItem(u'请选择海眼')
            self.ui.comboBox_yellowtide_lingyan_weizhi1.clear()
            self.ui.comboBox_yellowtide_lingyan_weizhi1.addItem(u'请选择灵眼位置')
            print str
            if len(str) > 0:
                place_id_list = str.split(u'|')
                for place_id in place_id_list:
                    id = self.str2int(place_id)
                    self.ui.comboBox_yellowtide_haiyan1.addItem(u'%s|%s' % (place_id, op.hundunhai_name_ori[id]))

        if int == 78:
            index = self.ui.comboBox_yellowtide_haiyan1.currentIndex()
            self.ui.comboBox_yellowtide_lingyan_weizhi1.clear()
            self.ui.comboBox_yellowtide_lingyan_weizhi1.addItem(u'请选择灵眼位置')
            if index > 0:
                text_list = str.split(u'@@')
                for text in text_list:
                    self.ui.comboBox_yellowtide_lingyan_weizhi1.addItem(text)

        if int == 79:
            self.ui.pushButton_refresh_level_rank.setEnabled(True)
            self.ui.pushButton_refresh_shuxing_rank.setEnabled(True)
            self.ui.pushButton_refresh_chongwu_rank.setEnabled(True)
            self.ui.pushButton_refresh_daotong_rank.setEnabled(True)
            self.ui.pushButton_dengjipaihang_on.setEnabled(True)
            self.ui.pushButton_dengjipaihang_off.setEnabled(True)
            self.ui.pushButton_shuxingpaihang_on.setEnabled(True)
            self.ui.pushButton_shuxingpaihang_off.setEnabled(True)
            self.ui.pushButton_tongnianfen_pk.setEnabled(True)
            if game_obj.yellowtide_kelingyan:
                self.ui.pushButton_yellowtide_broadcast_mylingyan1.setEnabled(True)
                self.ui.pushButton_yellowtide_get_broadcast.setEnabled(True)
        if int == 80:
            self.ui.tabWidget_all.setTabText(9, u'兔子娱乐')
            self.ui.tabWidget_6.setVisible(True)
        if int == 81:
            index = self.str2int(str.split(u'|')[0])
            text = str.split(u'|')[1]
            self.set_xingjun_button(False, index, text)
        if int == 82:
            self.set_xingjun_button(True)
        if int == 83:
            index = self.str2int(str.split(u'|')[0])
            text = str.split(u'|')[1]
            self.set_lingmai_button(False, index, text)
        if int == 84:
            self.set_lingmai_button(True)
        if int == 85:
            index = self.str2int(str.split(u'|')[0])
            text = str.split(u'|')[1]
            self.set_tianshen_button(False, index, text)
        if int == 86:
            self.set_tianshen_button(True)
        if int == 87:
            index = self.str2int(str.split(u'|')[0])
            text = str.split(u'|')[1]
            self.set_dianzhu_button(False, index, text)
        if int == 88:
            self.set_dianzhu_button(True)
        if int == 89:
            self.ui.comboBox_query_daogong.setCurrentIndex(self.str2int(str) - 1)
        if int == 90:
            self.ui.lineEdit_chongzhiID.setText(str)
            self.login_success()
        if int == 91:
            self.setbutton()
        if int == 92:
            self.startGuaji()
        if int == 93:
            self.startLiandan()
        if int == 94:
            self.ui.comboBox_lingmaileixing.setCurrentIndex(1)
            self.lingmaileixing_change()
        if int == 95:
            self.stopshilian()
        if int == 96:
            self.startshilian()
        if int == 97:
            game.after_hour = self.str2int(self.ui.lineEdit_after_hour.text())
        if int == 98:
            self.update_pet_info()
        if int == 99:
            game.index_zhandouchongwu = self.str2int(cfg_get('chongwu', 'zhandou'))
            self.update_chongwu_lable(0, game.index_zhandouchongwu)
            game.index_luxingchongwu = self.str2int(cfg_get('chongwu', 'luxing'))
            self.update_chongwu_lable(1, game.index_luxingchongwu)
            game.index_feixingchongwu = self.str2int(cfg_get('chongwu', 'feixing'))
            self.update_chongwu_lable(2, game.index_feixingchongwu)
            game.index_yuhaichongwu = self.str2int(cfg_get('chongwu', 'yuhai'))
            self.update_chongwu_lable(3, game.index_yuhaichongwu)
        if int == 1702:
            a = False
            b = True
            if self.str2int(str) == 1:
                b = False
                a = True
            game.flag_huashen_2_stop_tiaozhan = a
            button_2_huashen_list = [self.ui.pushButton_2_xianjie, self.ui.pushButton_2_guijie, self.ui.pushButton_2_mojie, self.ui.pushButton_2_shenjie, self.ui.pushButton_2_fudixiaoshijie, self.ui.pushButton_2_zongmenyizhi]
            for button in button_2_huashen_list:
                button.setEnabled(a)

            self.ui.pushButton_2_stop_tiaozhan.setEnabled(b)
        if int == 1701:
            if len(str) < 2:
                self.ui.textBrowser_tongnianfen_pkresult.clear()
            else:
                self.ui.textBrowser_tongnianfen_pkresult.append(str)
        if int == 21001:
            if len(str) < 2:
                self.ui.comboBox_2_chuqiaoditu.clear()
            elif len(str) == 2:
                self.ui.comboBox_2_chuqiaoditu.setCurrentIndex(game.index_2_chuqiaoditu)
            else:
                self.ui.comboBox_2_chuqiaoditu.addItem(str)
        return


class GameThread(QThread):
    signal = pyqtSignal(str, int, bool)

    def __init__(self, mainself, parent=None):
        super(GameThread, self).__init__(parent)
        self.mainself = mainself
        return

    def nine_game_encrypt_body(self, part1, authCode=''):
        plain_body = part1
        if len(authCode) > 2:
            plain_body += ',"authCode":"%s"' % authCode
        plain_body += '},"game":%s,"client":%s}' % (self.b['game'].encode('utf8'), self.b['client'].encode('utf8'))
        print type(plain_body), '[plain_body] =', plain_body
        if getCoding(plain_body) == 'unicode':
            plain_body = plain_body.encode('utf8')
        aes_key = self.b['aes_key'].encode('utf8')
        aes_iv = self.b['aes_iv'].encode('utf8')
        aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        padding_len = 16 - len(plain_body) % 16
        padding_body = plain_body + chr(padding_len) * padding_len
        en_data = aes.encrypt(padding_body)
        d = base64.b64encode(en_data)
        k = self.b['k'].encode('utf8')
        i = self.b['i'].encode('utf8')
        v = 5
        body = '{"i":"%s","k":"%s","d":"%s","v":%d}' % (i, k, d, v)
        return body

    def nine_game_login(self, login_type, part1, authCode=''):
        body = self.nine_game_encrypt_body(part1, authCode)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'okhttp/${project.version}', 
           'Accept-Encoding': 'gzip'}
        url = 'http://sdk.9game.cn/ng/client/%s?ver=0&df=adat&os=android' % login_type
        response = requests.post(url, headers=headers, data=body, timeout=10)
        obj = json.loads(response.text)
        temp = base64.b64decode(obj['d'].encode('utf8'))
        aes = AES.new(self.b['aes_key'].encode('utf8'), AES.MODE_CBC, self.b['aes_iv'].encode('utf8'))
        plain = aes.decrypt(temp)
        ret = plain[:0 - ord(plain[-1])]
        obj2 = json.loads(ret)
        print '[login ret]'
        print obj2
        self.signal.emit(u'登录结果:【%s】！\n' % obj2['state']['msg'], 1, True)
        if obj2['state']['code'] == 1 and obj2['state']['subCode'] == 2000000:
            sid = obj2['data']['sid'].encode('utf8')
            cfg_set('login', 'access_token', sid, 'config.ini')
            if obj2['data'].has_key('serviceTicket'):
                cfg_set('login', 'serviceticket', obj2['data']['serviceTicket'].encode('utf8'), 'config.ini')
            return sid
        if obj2['state']['subCode'] == 4005400 and authCode == '':
            self.signal.emit(u'弹出白框看不到图片，请联系兔子换云主机即可解决！', 1, True)
            auth_url = obj2['data']['authUrl'].encode('gbk')
            self.signal.emit(auth_url, 0, True)
            for i in range(300):
                if self.mainself.webdialog.auth_code != '':
                    return self.nine_game_login(login_type, part1, self.mainself.webdialog.auth_code)
                time.sleep(1)

            return False
        return False
        return

    def nine_game_loginByPassword(self, username, password):
        part1 = '{"id":' + str(int(time.time()) * 1000 + 145) + ',"service":"ngaccount.loginByPassword","data":{"name":"%s","password":"5|%s","encrypt":1,"loginType":2,"datagram":"%s"' % (username, self.b['en_password'].encode('utf8'), self.b['datagram'].encode('utf8'))
        return self.nine_game_login('ngaccount.loginByPassword', part1)

    def nine_game_loginWithServiceTicket(self):
        serviceTicket = cfg_get('login', 'serviceticket', 'config.ini')
        if len(serviceTicket) < 10:
            return False
        part1 = '{"id":' + str(int(time.time()) * 1000 + 145) + ',"service":"ngaccount.loginWithServiceTicket","data":{"clusterCode":"","serviceTicket":"%s","loginType": 2,"datagram":"%s"' % (serviceTicket, self.b['datagram'].encode('utf8'))
        return self.nine_game_login('ngaccount.loginWithServiceTicket', part1)

    def nine_game_loginWithSmsCode(self, phonenum, smscode):
        part1 = '{"id":' + str(int(time.time()) * 1000 + 145) + ',"service": "ngaccount.loginWithSmsCode","data": {"mobile": "%s","smsCode": "%s","loginType": 1,"datagram": "%s"' % (phonenum, smscode, self.b['datagram'].encode('utf8'))
        return self.nine_game_login('ngaccount.loginWithSmsCode', part1)

    def nine_game_sendSmsCode(self, phonenum):
        part1 = '{"id":' + str(int(time.time()) * 1000 + 145) + ',"service": "auth.captcha.sendSmsCodeForLogin","data": {"mobile": "%s", "datagram": "%s"' % (phonenum, self.b['datagram'].encode('utf8'))
        return self.nine_game_login('auth.captcha.sendSmsCodeForLogin', part1)

    def dangle_login(self):
        url = 'https://ngsdk.d.cn/api/user/login'
        android_header = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; vivo x5s l Build/LMY47I)', 
           'Connection': 'Keep-Alive', 
           'Accept-Encoding': 'gzip'}
        android_header['SDK_VERSION'] = '4611'
        response = requests.post(url, headers=android_header, data=rf('dangle.txt'), verify=False, timeout=10)
        return response.content

    def run(self):
        global chonglianjiange
        global game_obj
        global lijichonglian
        global xiaomi_deviceId
        xiaomi_deviceId = ''
        flag_login = self.mainself.ui.comboBox_pingtaileixing.currentIndex() + 1
        username = trans_utf8(self.mainself.ui.lineEdit_username.text())
        password = trans_utf8(self.mainself.ui.lineEdit_password.text())
        verifynum = trans_utf8(self.mainself.ui.lineEdit_verifynum.text())
        phonenum = trans_utf8(self.mainself.ui.lineEdit_phonenum.text())
        server_id = self.mainself.server_id
        server_ip = self.mainself.server_ip
        server_port = self.mainself.server_port
        imei = self.mainself.imei
        last_username = self.mainself.last_username
        last_phonenum = self.mainself.last_phonenum
        last_accountId = self.mainself.last_accountId
        last_access_token = self.mainself.last_access_token
        print '[last_accountId]', last_accountId
        print '[last_access_token]', last_access_token
        accountId = last_accountId
        access_token = last_access_token
        if len(accountId) > 2:
            self.signal.emit(accountId, 90, True)
        while True:
            try:
                if flag_login == 3 and len(access_token) < 4:
                    if len(verifynum) < 4 and len(last_accountId) < 4:
                        self.signal.emit(u'请点击获取验证码按钮查看验证码获取方法！', 1, True)
                        return
                if flag_login == 13:
                    if not os.path.exists('dangle.txt'):
                        self.signal.emit(u'当乐端首次登录需要联系美女客服，QQ：158855054！', 1, True)
                        return
                    access_token = self.dangle_login()
                a, self.b, d = game.get_server_info(flag_login, accountId, access_token, server_id, server_ip, server_port, username, password, phonenum, verifynum)
                print 'd =', repr(d), type(d)
                if d == 'wait':
                    self.signal.emit(u'登录失败，原因【操作频繁】，请5分钟后再试！', 1, True)
                    time.sleep(300)
                    continue
                elif d == 'notime':
                    self.signal.emit(a, 90, True)
                    self.signal.emit(u'登录失败，原因【辅助到期】，可加美女QQ：158855054 联系试用。', 1, True)
                    return
                elif d == 'local_error':
                    self.signal.emit(a, 1, True)
                    return
                if d == '9game_needlogin':
                    print d
                    access_token = self.nine_game_loginWithServiceTicket()
                    if access_token == False:
                        if flag_login == 2:
                            access_token = self.nine_game_loginByPassword(username, password)
                        elif flag_login == 3:
                            access_token = self.nine_game_loginWithSmsCode(phonenum, verifynum)
                        else:
                            access_token = False
                    if access_token == False:
                        self.signal.emit(u'登录失败，原因【服务器繁忙】，10分钟后再次尝试！', 1, True)
                        for i in range(600):
                            time.sleep(1)
                            if lijichonglian == True:
                                break

                        access_token = cfg_get('login', 'access_token', 'config.ini')
                        continue
                    a, self.b, d = game.get_server_info(flag_login, accountId, access_token, server_id, server_ip, server_port, username, password, phonenum, verifynum)
                elif d == 'xiaomi_need_zhushou':
                    self.signal.emit(u'小米登录失败，请使用助手登录游戏采集登录信息', 1, True)
                if d != 'success':
                    self.signal.emit(u'登录失败，原因【未知】，10分钟后再次尝试！', 1, True)
                    time.sleep(600)
                    continue
                chargeId = a
                accountId = a
                self.signal.emit(chargeId, 90, True)
                cfg_set('login', 'accountid', chargeId, 'config.ini')
                if len(xiaomi_deviceId) > 10 and flag_login == 7:
                    cfg_set('login', 'access_token', xiaomi_deviceId, 'config.ini')
                print self.b
                if flag_login == 7:
                    if self.b['xiaomi_chonglian'] == 1:
                        self.mainself.ui.label_tip_2.setText(u'已经可以告别助手了，自动重连了！！')
                        self.mainself.ui.label_tip_2.setVisible(True)
                game_obj = game.game(self.signal, chargeId)
                if game_obj.login(self.b):
                    self.signal.emit('', 91, True)
                    if game.flag_chonglian == True:
                        time.sleep(30)
                        if self.mainself.ui.checkBox_chonglianshuatu.checkState() == 2:
                            self.signal.emit('', 92, True)
                            time.sleep(3)
                        self.signal.emit('', 93, True)
                        if game.flag_auto_lianqi == True:
                            self.signal.emit('', 57, True)
                    game.flag_chonglian = False
                    lijichonglian = False
                    game_obj.start_work()
                chonglianjiange = int(self.mainself.ui.lineEdit_chonglianjiange.text())
                cfg_set('login', 'chonglianjiange', str(chonglianjiange))
                lijichonglian = False
                if zidongchonglian:
                    game.after_hour = int(self.mainself.ui.lineEdit_after_hour.text())
                    cfg_set('login', 'after_hour', str(game.after_hour))
                    a = time.localtime(time.time())
                    if game.kamanshouyi and a.tm_hour >= game.after_hour:
                        minute = random.randint(6, 58)
                        if game.all_chuqiao_count > 950 or accountId == 'xbxxz_0FDVtiIBQWCyDfG0mifWRklm2n5ODahI0nx+pxOwuAFnCgP/DQV+EtnivUlcfVMN':
                            minute = random.randint(3, 10)
                        target_hour = 0
                        if 122 in game.settings_on:
                            target_hour = 1
                        tips_text = u'<html><head/><body><p><span style=" font-size:10pt; font-weight:600; color:#ff0000;">辅助已掉线卡满收益，第二天%d点%d分上线！</span></p></body></html>' % (target_hour, minute)
                        while True:
                            self.signal.emit(tips_text, 116, True)
                            time.sleep(random.randint(1, 59))
                            a = time.localtime(time.time())
                            if a.tm_hour == target_hour:
                                if a.tm_min >= minute:
                                    break

                    else:
                        self.signal.emit(u'%d分钟后重连' % chonglianjiange, 1, True)
                        for i in range(60 * chonglianjiange):
                            time.sleep(1)
                            if lijichonglian == True:
                                break

                    game.flag_chonglian = True
                    del game_obj
                else:
                    while lijichonglian == False:
                        time.sleep(2)

            except:
                try:
                    tb = traceback.format_exc()
                    if not os.path.isdir('log'):
                        os.makedirs('log')
                    f = open(os.path.join('log', 'gui_error.log'), 'a')
                    f.write('[%s]\n%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), tb))
                    f.close()
                    tip = u'登录出现问题，10分钟后再次尝试（原因:%s，详见 log\\gui_error.log）' % tb.splitlines()[-1]
                except Exception:
                    tip = u'登录出现问题，10分钟后再次尝试'
                self.signal.emit(tip, 1, True)
                time.sleep(600)

        return


class WebDialog(QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        QWebView.__init__(self)
        self.auth_code = ''
        self.deviceId = ''
        self.ui = BrowserDialog()
        self.ui.setupUi(self)
        self.ui.lineEdit.returnPressed.connect(self.loadURL)
        self.ui.qwebview.page().currentFrame().loadFinished.connect(self.getauthcode)
        return

    def loadURL(self):
        url = self.ui.lineEdit.text()
        self.ui.qwebview.load(QUrl(url))
        self.show()
        return

    def getauthcode(self):
        url = trans_utf8(self.ui.qwebview.url().toString())
        index = url.find('auth_code=')
        if index > -1:
            self.auth_code = url[index + 10:]
            print '[auth_code]', self.auth_code
            self.close()
        return


def main():
    app = QApplication(sys.argv)
    dialog = XbxxzDialog()
    dialog.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    main()
