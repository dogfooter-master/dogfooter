import likeyoubot_game as lybgame
import likeyoubot_darkeden_scene as lybscene
from likeyoubot_configure import LYBConstant as lybconstant
import time
import sys
import tkinter
from tkinter import ttk
from tkinter import font
import copy


class LYBDarkEden(lybgame.LYBGame):
    work_list = [
        '게임 시작',
        '로그인',
        '메인 퀘스트',
        '일일 퀘스트',
        '자동 사냥',
        '결투장',
        '토벌대',

        '알림',
        '[반복 시작]',
        '[반복 종료]',
        '[작업 대기]',
        '[작업 예약]',
        '']

    darkeden_icon_list = [
        'darkeden_icon',
    ]

    def __init__(self, game_name, game_data_name, window):
        lybgame.LYBGame.__init__(self, lybconstant.LYB_GAME_DARKEDEN, lybconstant.LYB_GAME_DATA_DARKEDEN, window)

    def process(self, window_image):
        rc = super(LYBDarkEden, self).process(window_image)
        if rc < 0:
            return rc

        return rc

    def custom_check(self, window_image, window_pixel):

        resource_name = 'skip_dehwa_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(5):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(710, 335, 790, 360)
            )
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('대화 스킵: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return 'skip'

        resource_name = 'skip_npc_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(5):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(710, 400, 790, 450)
            )
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('NPC 대화: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return 'skip'

        resource_name = 'confirm_20181129_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(3):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(360, 300, 450, 450)
            )
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('확인: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return 'skip'

        resource_name = 'confirm_20181129_1_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(3):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.8,
                custom_flag=1,
                custom_rect=(360, 300, 450, 450)
            )
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('확인: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return 'skip'

        if True:
            self.process_tutorial()


        # 패배!
        # (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
        # 					self.window_image,
        # 					'defeat_press_key_loc',
        # 					custom_below_level=(250, 250, 250),
        # 					custom_top_level=(255, 255, 255),
        # 					custom_threshold=0.7,
        # 					custom_flag=1,
        # 					custom_rect=(280, 190, 360, 230)
        # 					)
        # if loc_x != -1:
        # 	self.logger.warn('전투 패배: ' + str(match_rate))
        # 	self.mouse_click('defeat_press_key_0')

        return ''

    def get_screen_by_location(self, window_image):

        scene_name = self.scene_init_screen(window_image)
        if len(scene_name) > 0:
            return scene_name

        # scene_name = self.jeontoo_scene(window_image)
        # if len(scene_name) > 0:
        # 	return scene_name

        # scene_name = self.scene_google_play_account_select(window_image)
        # if len(scene_name) > 0:
        # 	return scene_name


        tutorial_index = self.get_option('tutorial_index')
        if tutorial_index == None:
            tutorial_index = 0

        if tutorial_index > 5:
            self.set_option('tutorial_index', 0)
            resource_name = 'tutorial_loc'
            if not resource_name in self.resource_manager.resource_dic:
                return

            resource = self.resource_manager.resource_dic[resource_name]

            for pb_name in resource:
                self.logger.debug(pb_name)
                self.mouse_click(pb_name)
                time.sleep(0.1)
        else:
            self.set_option('tutorial_index', tutorial_index + 1)

        return ''

    # def jeontoo_scene(self, window_image):
    # 	(loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
    # 						self.window_image,
    # 						'jeontoo_scene_loc',
    # 						custom_below_level=(100, 100, 100),
    # 						custom_top_level=(255, 255, 255),
    # 						custom_threshold=0.7,
    # 						custom_flag=1,
    # 						custom_rect=(5, 90, 80, 130)
    # 						)
    # 	if match_rate > 0.7:
    # 		return 'jeontoo_scene'

    # 	return ''

    def scene_init_screen(self, window_image):

        loc_x = -1
        loc_y = -1

        if self.player_type == 'nox':
            for each_icon in LYBDarkEden.darkeden_icon_list:
                (loc_x, loc_y), match_rate = self.locationOnWindowPart(
                    window_image,
                    self.resource_manager.pixel_box_dic[each_icon],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(80, 110, 700, 370)
                )
                # print('[DEBUG] nox yh icon:', (loc_x, loc_y), match_rate)
                if loc_x != -1:
                    break
        else:
            for each_icon in LYBDarkEden.darkeden_icon_list:
                (loc_x, loc_y), match_rate = self.locationOnWindowPart(
                    window_image,
                    self.resource_manager.pixel_box_dic[each_icon],
                    custom_threshold=0.8,
                    custom_flag=1,
                    custom_rect=(30, 10, 740, 370)
                )
                # print('[DEBUG] momo yh icon:', (loc_x, loc_y), match_rate)
                if loc_x != -1:
                    break

        if loc_x == -1:
            return ''

        return 'init_screen_scene'

    def scene_google_play_account_select(self, window_image):
        loc_x_list = []
        loc_y_list = []

        (loc_x, loc_y) = lybgame.LYBGame.locationOnWindow(
            window_image,
            self.resource_manager.pixel_box_dic['google_play_letter']
        )
        loc_x_list.append(loc_x)
        loc_y_list.append(loc_y)

        for i in range(6):
            (loc_x, loc_y) = lybgame.LYBGame.locationOnWindow(
                window_image,
                self.resource_manager.pixel_box_dic['google_play_letter_' + str(i)]
            )

            loc_x_list.append(loc_x)
            loc_y_list.append(loc_y)

        for each_loc in loc_x_list:
            if each_loc == -1:
                return ''
            else:
                continue

        return 'google_play_account_select_scene'

    def clear_scene(self):
        last_scene = self.scene_dic
        self.scene_dic = {}
        for scene_name, scene in last_scene.items():
            if ('google_play_account_select_scene' in scene_name or
                        'logo_screen_scene' in scene_name or
                        'connect_account_scene' in scene_name
                ):
                self.scene_dic[scene_name] = last_scene[scene_name]

    def add_scene(self, scene_name):
        self.scene_dic[scene_name] = lybscene.LYBDarkEdenScene(scene_name)
        self.scene_dic[scene_name].setLoggingQueue(self.logging_queue)
        self.scene_dic[scene_name].setGameObject(self)

    def process_tutorial(self):
        resource_name = 'control_pad_tutorial_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(10):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_rect=(130, 300, 400, 340)
            )
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('콘트롤 패드 튜토리얼: ' + str(match_rate))
                self.get_scene('main_scene').lyb_mouse_drag('pad_direction_center', 'pad_direction_1', stop_delay=2)
                return 'skip'
    
        resource_name = 'potion_tutorial_loc'
        elapsed_time = time.time() - self.get_scene('main_scene').get_checkpoint(resource_name)
        if elapsed_time > self.period_bot(10):
            (loc_x, loc_y), match_rate = self.locationResourceOnWindowPart(
                self.window_image,
                resource_name,
                custom_threshold=0.7,
                custom_flag=1,
                custom_rect=(5, 180, 150, 210),
            )
            if loc_x != -1:
                self.get_scene('main_scene').set_checkpoint(resource_name)
                self.logger.info('상점에서 회복 물약 구입' + str(match_rate))
                self.get_scene('sangjeom_scene').status = 0
                self.get_scene('main_scene').lyb_mouse_click_location(loc_x, loc_y)
                return 'skip'

class LYBDarkEdenTab(lybgame.LYBGameTab):
    def __init__(self, root_frame, configure, game_options, inner_frame_dics, width, height,
                 game_name=lybconstant.LYB_GAME_DARKEDEN):
        lybgame.LYBGameTab.__init__(self, root_frame, configure, game_options, inner_frame_dics, width, height,
                                    game_name)

    def set_work_list(self):
        lybgame.LYBGameTab.set_work_list(self)

        for each_work in LYBDarkEden.work_list:
            self.option_dic['work_list_listbox'].insert('end', each_work)
            self.configure.common_config[self.game_name]['work_list'].append(each_work)

    def set_option(self):
        # PADDING
        frame = ttk.Frame(
            master=self.master,
            relief=self.frame_relief
        )
        frame.pack(pady=5)

        self.inner_frame_dic['options'] = ttk.Frame(
            master=self.master,
            relief=self.frame_relief
        )

        self.option_dic['option_note'] = ttk.Notebook(
            master=self.inner_frame_dic['options']
        )

        self.inner_frame_dic['common_tab_frame'] = ttk.Frame(
            master=self.option_dic['option_note'],
            relief=self.frame_relief
        )

        self.inner_frame_dic['common_tab_frame'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['option_note'].add(self.inner_frame_dic['common_tab_frame'], text='일반')

        self.inner_frame_dic['work_tab_frame'] = ttk.Frame(
            master=self.option_dic['option_note'],
            relief=self.frame_relief
        )
        self.inner_frame_dic['work_tab_frame'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['option_note'].add(self.inner_frame_dic['work_tab_frame'], text='작업')

        self.inner_frame_dic['notify_tab_frame'] = ttk.Frame(
            master=self.option_dic['option_note'],
            relief=self.frame_relief
        )
        self.inner_frame_dic['notify_tab_frame'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.option_dic['option_note'].add(self.inner_frame_dic['notify_tab_frame'], text='알림')

        # ------

        # 일반 탭 좌측
        frame_l = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 일반 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['common_tab_frame'])
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 좌측
        frame_l = ttk.Frame(self.inner_frame_dic['work_tab_frame'])
        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 중간
        frame_m = ttk.Frame(self.inner_frame_dic['work_tab_frame'])
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 작업 탭 우측
        frame_r = ttk.Frame(self.inner_frame_dic['work_tab_frame'])
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # 알림 탭 좌
        frame_l = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])
        frame_l.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # 알림 탭 중
        frame_m = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])
        frame_m.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        # 알림 탭 우
        frame_r = ttk.Frame(self.inner_frame_dic['notify_tab_frame'])
        frame_r.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        # ------

        self.option_dic['option_note'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)
        self.inner_frame_dic['options'].pack(anchor=tkinter.NW, fill=tkinter.BOTH, expand=True)

        self.set_game_option()

    def callback_main_quest_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())

    def callback_main_quest_each_stringvar(self, args, option_name):
        self.set_game_config(option_name, self.option_dic[option_name].get())
