import likeyoubot_resource as lybrsc
import likeyoubot_message
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import pyautogui
import operator
import random
import likeyoubot_game as lybgame
import likeyoubot_hundredsoul as lybgamehundredsoul
from likeyoubot_configure import LYBConstant as lybconstant
import likeyoubot_scene
import time

class LYBHundredSoulScene(likeyoubot_scene.LYBScene):
    def __init__(self, scene_name):
        likeyoubot_scene.LYBScene.__init__(self, scene_name)

    def process(self, window_image, window_pixels):

        super(LYBHundredSoulScene, self).process(window_image, window_pixels)

        rc = 0
        if self.scene_name == 'init_screen_scene':
            rc = self.init_screen_scene()
        elif self.scene_name == 'main_scene':
            rc = self.main_scene()
        elif self.scene_name == 'login_scene':
            rc = self.login_scene()
        elif self.scene_name == 'notification_scene':
            rc = self.notification_scene()
        elif self.scene_name == 'dashboard_scene':
            rc = self.dashboard_scene()
        elif self.scene_name == 'immu_scene':
            rc = self.immu_scene()
        elif self.scene_name == 'config_scene':
            rc = self.config_scene()
        elif self.scene_name == 'logout_scene':
            rc = self.logout_scene()
        elif self.scene_name == 'connect_account_scene':
            rc = self.connect_account_scene()
        elif self.scene_name == 'terms_scene':
            rc = self.terms_scene()
        elif self.scene_name == 'google_play_account_select_scene':
            rc = self.google_play_account_select_scene()
        elif self.scene_name == 'google_play_account_select_1_scene':
            rc = self.google_play_account_select_1_scene()
        elif self.scene_name == 'google_play_account_select_2_scene':
            rc = self.google_play_account_select_2_scene()
        elif self.scene_name == 'gisadan_scene':
            rc = self.gisadan_scene()
        elif self.scene_name == 'seong_scene':
            rc = self.seong_scene()




            



        else:
            rc = self.else_scene()

        return rc

    def else_scene(self):

        if self.status == 0:
            self.logger.info('unknown scene: ' + self.scene_name)
            self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def seong_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'seong_scene_give_' + 'emerald' + '_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
            	self.click_resource(resource_name)
            else:
            	self.status = 10
        elif self.status == 10:
        	self.lyb_mouse_click('back', custom_threshold=0)
        	self.status = 0
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def gisadan_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 1:
        	self.lyb_mouse_click('gisadan_scene_chulseok_bosang', custom_threshold=0)
        	self.status += 1
        elif self.status == 2:
        	if self.click_resource('gisadan_scene_give_new_loc') is True:
        		self.game_object.get_scene('seong_scene').status = 0
        	self.status += 1
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def login_scene(self):
        self.game_object.current_matched_scene['name'] = ''
        self.schedule_list = self.get_game_config('schedule_list')

        if not '로그인' in self.schedule_list:
            return 0

        elapsedTime = time.time() - self.get_checkpoint('start')
        if elapsedTime > 120:
            self.status = 0

        if self.status == 0:
            self.set_checkpoint('start')
            self.status += 1
        elif self.status == 1:
            self.lyb_mouse_click(self.scene_name + '_touch', custom_threshold=0)
            self.status += 1
        elif self.status >= 2 and self.status < 6:
            self.status += 1
        elif self.status == 6:
            self.lyb_mouse_click(self.scene_name + '_touch', custom_threshold=0)
            self.status += 1
        elif self.status >= 7 and self.status < 10:
            self.status += 1
        elif self.status >= 10 and self.status < 70:
            self.logger.info('로그인 화면 랙 인식: ' + str(self.status - 10) + '/60')
            if self.status % 10 == 0:
                self.lyb_mouse_click(self.scene_name + '_touch', custom_threshold=0)
            self.status += 1
        elif self.status == 70:
            self.game_object.terminate_application()
            self.status += 1
        else:
            self.status = 0

        return self.status

    def google_play_account_select_1_scene(self):
        return self.game_object.get_scene('google_play_account_select_scene').process(self.window_image, self.window_pixels)

    def google_play_account_select_2_scene(self):
        return self.game_object.get_scene('google_play_account_select_scene').process(self.window_image, self.window_pixels)

    def google_play_account_select_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            account_index = self.get_option('account_index')
            if account_index is None:
                account_index = 0
                self.set_option('account_index', account_index)

            self.set_option('click_index', account_index)

            resource_name = 'google_play_account_select_scene_account_1_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                self.set_option('click_index', 10)
                self.status = 200
                return self.status

            resource_name = 'google_play_account_select_scene_account_2_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                if account_index > 1:
                    self.set_option('account_index', 0)
                    account_index = 0
               
                self.set_option('click_index', 20 + account_index)
                self.status = 200
                return self.status

            resource_name = 'google_play_account_select_scene_account_3_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            self.logger.debug(resource_name + ' ' + str(round(match_rate, 2)))
            if match_rate > 0.9:
                if account_index > 2:
                    self.set_option('account_index', 0)
                    account_index = 0
               
                self.set_option('click_index', account_index)
                self.status = 200
                return self.status

            self.set_option('last_status', 99999)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1

            pb_name = 'google_play_account_select_scene_add'
            (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                self.window_image,
                self.game_object.resource_manager.pixel_box_dic[pb_name],
                custom_threshold=0.6,
                custom_flag=1,
                custom_rect=(180, 400, 210, 460))
            self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
            if loc_x != -1:
                self.status = 1000
            else:
                click_index = self.get_option('click_index')
                if click_index > 3:
                    if loc_x != -1:
                        self.status = 1000
                    else:
                        self.set_option('last_status', self.status)
                        self.set_option('click_index', click_index - 1)
                        self.status = 100
                else:             
                    self.status = 200
        elif self.status == 100:
            self.lyb_mouse_drag('google_play_account_drag_bot', 'google_play_account_drag_top', delay=2)
            self.status += 1
        elif self.status == 101:
            self.status = self.get_option('last_status')
        elif self.status == 200:
            index = str(self.get_option('click_index'))
            self.logger.warn('index=' + index)
            pb_name = 'google_play_account_select_scene_list_' + index
            account_index = self.get_option('account_index')
            self.set_option('account_index', account_index + 1)
            self.lyb_mouse_click(pb_name, custom_threshold=0)
            self.status = 99999
        elif 1000 <= self.status < 1005:
            self.lyb_mouse_drag('google_play_account_select_scene_drag_top', 'google_play_account_select_scene_drag_bot')
            self.status += 1
        elif self.status == 1005:
            self.set_option('account_index', 0)
            self.status = 0
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def terms_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1

            isClicked = False
            resource_name = 'terms_scene_check_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for pb_name in resource:
                match_rate = self.game_object.rateMatchedPixelBox(self.window_pixels, pb_name)
                if match_rate > 0.9:
                    self.lyb_mouse_click(pb_name)
                    isClicked = True

            if isClicked is False:
                self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def connect_account_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        else:
            self.game_object.get_scene('terms_scene').status = 0
            self.game_object.get_scene('google_play_account_select_scene').status = 0
            self.lyb_mouse_click(self.scene_name + '_google', custom_threshold=0)
                
            self.status = 0

        return self.status

    def logout_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 100 <= self.status < 110:
            self.status += 1
            if self.click_resource('logout_scene_ok_loc') is True:
                self.game_object.get_scene('connect_account_scene').status = 0
                self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def config_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif self.status == 100:
            self.game_object.get_scene('logout_scene').status = 100
            self.status += 1
        elif 101 <= self.status < 110:
            self.status += 1
            if self.click_resource('config_scene_logout_loc') is False:
                self.lyb_mouse_click('config_scene_tab_account', custom_threshold=0)
            else:
                self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def immu_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.set_option('last_status', 99999)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            resource_name = 'immu_scene_new_loc'
            resource = self.game_object.resource_manager.resource_dic[resource_name]
            for pb_name in resource:
                (loc_x, loc_y), match_rate = self.game_object.locationOnWindowPart(
                    self.window_image,
                    self.game_object.resource_manager.pixel_box_dic[pb_name],
                    custom_threshold=0.7,
                    custom_flag=1,
                    custom_rect=(200, 80, 700, 130))
                self.logger.debug(pb_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    self.set_option('last_status', self.status)
                    self.status = 10
                    return self.status
            self.status = 99999
        elif 10 <= self.status < 20:
            self.status += 1
            resource_name = 'immu_scene_bosang_loc'
            match_rate = self.game_object.rateMatchedResource(self.window_pixels, resource_name)
            if match_rate > 0.9:
                self.lyb_mouse_click('immu_scene_bosang_0', custom_threshold=0)
                return self.status
            self.status = self.get_option('last_status')
        elif self.status == 20:
            self.status = self.get_option('last_status')
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def notification_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            if self.click_resource('notification_scene_bosang_loc') is True:
                self.game_object.get_scene('immu_scene').status = 0
                return self.status

            self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def dashboard_scene(self):

        if self.status == 0:
            self.logger.info('scene: ' + self.scene_name)
            self.status += 1
        elif 1 <= self.status < 10:
            self.status += 1
            button_loc_x, button_loc_y = self.get_location('dashboard_scene_button')
            pDic = {}
            resource_name = 'dashboard_scene_jeontoo_loc'
            for i in range(5):
                (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart(
                    self.window_image,
                    resource_name,
                    custom_threshold=0.7,
                    custom_flag=1,
                    custom_rect=(120, 130 + (i * 60) - 30, 200, 130 + (i * 60) + 30),
                    )
                if loc_x != -1:
                    pDic[(loc_x, loc_y)] = match_rate

            sorted_list = sorted(pDic.items(), key=operator.itemgetter(1), reverse=True)
            self.logger.warn(sorted_list)
            if len(sorted_list) > 0:
                loc_x, loc_y = sorted_list[0][0]
                self.lyb_mouse_click_location(button_loc_x + 50, loc_y + 10)
                self.game_object.get_scene('tamheom_scene').status = 0
            else:
                self.status = 99999
        else:
            if self.scene_name + '_close_icon' in self.game_object.resource_manager.pixel_box_dic:
                self.lyb_mouse_click(self.scene_name + '_close_icon', custom_threshold=0)
                
            self.status = 0

        return self.status

    def init_screen_scene(self):
        
        self.schedule_list = self.get_game_config('schedule_list')
        if not '게임 시작' in self.schedule_list:
            return 0


        loc_x = -1
        loc_y = -1


        if self.game_object.player_type == 'nox':
            for each_icon in lybgamehundredsoul.LYBHundredSoul.hundredsoul_icon_list:
                (loc_x, loc_y),  match_rate = self.game_object.locationOnWindowPart(
                                self.window_image,
                                self.game_object.resource_manager.pixel_box_dic[each_icon],
                                custom_threshold=0.8,
                                custom_flag=1,
                                custom_rect=(80, 110, 700, 370)
                                )
                # self.logger.debug(match_rate)
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    break
        else:
            for each_icon in lybgamehundredsoul.LYBHundredSoul.hundredsoul_icon_list:
                (loc_x, loc_y),  match_rate = self.game_object.locationOnWindowPart(
                                self.window_image,
                                self.game_object.resource_manager.pixel_box_dic[each_icon],
                                custom_threshold=0.8,
                                custom_flag=1,
                                custom_rect=(30, 10, 740, 370)
                                )
                # self.logger.debug(match_rate)
                if loc_x != -1:
                    self.lyb_mouse_click_location(loc_x, loc_y)
                    break

        return 0






















































































    #################################
    #                               #
    #                               #
    #			MAIN SCENE 			#
    #                               #
    #                               #
    #################################
    
    def main_scene(self):

        if self.game_object.current_schedule_work != self.current_work:
            self.game_object.current_schedule_work = self.current_work

        self.game_object.main_scene = self

        is_clicked = self.pre_process_main_scene()
        if is_clicked == True:
            return self.status

        self.schedule_list = self.get_game_config('schedule_list')
        if len(self.schedule_list) == 1:
            self.logger.warn('스케쥴 작업이 없어서 종료합니다.')
            return -1

        if self.status == 0:
            self.status += 1
        elif self.status >= 1 and self.status < 1000:

            self.set_schedule_status()

        elif self.status == self.get_work_status('메인 퀘스트'):

            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(600):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag') == True:
                self.set_option(self.current_work + '_end_flag', False)
                self.set_option(self.current_work + '_inner_status', None)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.process_main_quest()

        elif self.status == self.get_work_status('기사단'):

            elapsed_time = self.get_elapsed_time()
            if elapsed_time > self.period_bot(5):
                self.set_option(self.current_work + '_end_flag', True)

            if self.get_option(self.current_work + '_end_flag') == True:
                self.set_option(self.current_work + '_end_flag', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

            self.click_resource('main_scene_gisadan_loc')
            self.game_object.get_scene('gisadan_scene').status = 0

        elif self.status == self.get_work_status('알림'):

            try:
                self.game_object.telegram_send(str(self.get_game_config(lybconstant.LYB_DO_STRING_NOTIFY_MESSAGE)))
                self.status = self.last_status[self.current_work] + 1
            except:
                recovery_count = self.get_option(self.current_work + 'recovery_count')
                if recovery_count == None:
                    recovery_count = 0

                if recovery_count > 2:
                    self.status = self.last_status[self.current_work] + 1
                    self.set_option(self.current_work + 'recovery_count', 0)
                else:
                    self.logger.error(traceback.format_exc())
                    self.set_option(self.current_work + 'recovery_count', recovery_count + 1)

        elif self.status == self.get_work_status('[작업 예약]'):

            self.logger.warn('[작업 예약]')
            self.game_object.wait_for_start_reserved_work = False
            self.status = self.last_status[self.current_work] + 1

        elif self.status == self.get_work_status('[작업 대기]'):
            elapsed_time = self.get_elapsed_time()
            limit_time = int(self.get_game_config(lybconstant.LYB_DO_STRING_WAIT_FOR_NEXT))
            if elapsed_time > limit_time:
                self.set_option(self.current_work + '_end_flag', True)
            else:
                self.loggingElapsedTime('[작업 대기]', int(elapsed_time), limit_time, period=10)

            if self.get_option(self.current_work + '_end_flag') == True:
                self.set_option(self.current_work + '_end_flag', False)
                self.status = self.last_status[self.current_work] + 1
                return self.status

        elif self.status == self.get_work_status('[반복 시작]'):

            self.set_option('loop_start', self.last_status[self.current_work])
            self.status = self.last_status[self.current_work] + 1

        elif self.status == self.get_work_status('[반복 종료]'):

            loop_count = self.get_option('loop_count')
            if loop_count == None:
                loop_count = 1

            self.logger.debug('[반복 종료] ' + str(loop_count) + ' 회 수행 완료, ' +
             str(int(self.get_game_config(lybconstant.LYB_DO_STRING_COUNT_LOOP)) - loop_count) + ' 회 남음')
            if loop_count >= int(self.get_game_config(lybconstant.LYB_DO_STRING_COUNT_LOOP)):
                self.status = self.last_status[self.current_work] + 1
                self.set_option('loop_count', 1)
                self.set_option('loop_start', None)
            else:
                self.status = self.get_option('loop_start')
                # print('DEBUG LOOP STATUS = ', self.status )

                if self.status == None:
                    self.logger.debug('[반복 시작] 점을 찾지 못해서 다음 작업을 수행합니다')
                    self.status = self.last_status[self.current_work] + 1

                self.set_option('loop_count', loop_count + 1)

        else:
            self.status = self.last_status[self.current_work] + 1


        return self.status

















































































    def callback_logoff(self):
    	self.lyb_mouse_click('main_scene_config', custom_threshold=0)
    	self.game_object.get_scene('config_scene').status = 100

    def pre_process_main_scene(self):

        return False

    def process_main_quest(self):
        if self.process_notification() is True:
            return True

        if self.process_dashboard(self.current_work) is True:
            return True

        return False

    def process_notification(self):
        resource_name = 'main_scene_notification_new_loc'
        elapsed_time = time.time() - self.get_checkpoint(resource_name)
        if elapsed_time < self.period_bot(60):
            return False

        self.set_checkpoint(resource_name)

        if self.click_resource(resource_name, near=4) == True:
            self.game_object.get_scene('notification_scene').status = 0
            return True

        return False

    def process_dashboard(self, current_work):
        cs = current_work + '_inner_status'

        inner_status = self.get_option(cs)
        if inner_status is None:
            inner_status = 0

        if inner_status == 0:
            self.lyb_mouse_click('main_scene_alarm', custom_threshold=0)       
            self.game_object.get_scene('dashboard_scene').status = 0
            self.set_option(cs, inner_status + 1)
        else:
            self.set_option(cs, inner_status + 1)
            return False


        return True

    def get_work_status(self, work_name):
        if work_name in lybgamehundredsoul.LYBHundredSoul.work_list:
            return (lybgamehundredsoul.LYBHundredSoul.work_list.index(work_name) + 1) * 1000
        else:
            return 99999

    def click_resource(self, resource_name, custom_threshold=0.7, near=32):
        isMatched, rate = self.click_resource2(resource_name, custom_threshold=custom_threshold, near=near)

        return isMatched

    def click_resource2(self, resource_name, custom_threshold=0.7, near=32):
        (loc_x, loc_y), match_rate = self.game_object.locationResourceOnWindowPart2(
            self.window_image,
            resource_name,
            custom_threshold=custom_threshold,
            near=near,
            debug=True,
            custom_flag=1)
        self.logger.debug(resource_name + ' ' + str((loc_x, loc_y)) + ' ' + str(match_rate))
        if loc_x != -1:
            self.lyb_mouse_click_location(loc_x, loc_y)
            return True, match_rate

        return False, match_rate