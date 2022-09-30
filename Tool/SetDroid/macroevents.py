import time
import random
from event import Event
from policy import Policy

class Macroevents(object):

    def __init__(self,executor):
        self.app_list = ["tasks","ominiNotes"]
        self.executor = executor

    def set_macro_flag(self,app_path,event):
        app = app_path[0]
        # tasks
        app_name = app.split('/')[-2]
        rate = random.randint(1,100)
        if app_name == "tasks" and (event.action == "click" or event.action == "longclick"):
            if event.view.resourceId == "org.tasks:id/fab":
                if rate > 30: # 70% execute macroevents
                    return True
        elif app_name == "ominiNotes" and event.action == "click":
            if event.view.resourceId == "it.feio.android.omninotes:id/fab_expand_menu_button":
                if rate > 30:
                    return True
        return False
    
    def execute_preactions(self,app_path,devices,event_count):
        i = 0
        while(i < len(app_path)):
            # ./App/tasks/tasks-11.12.apk
            app = app_path[i]
            # tasks
            app_name = app.split('/')[-2]
            if app_name in self.app_list:
                # print("do pre-actions")
                # 11.12
                version = app.split('/')[-1].split('-')[-1].replace('.apk','')
                view_list = []
                action_list = []
                text_list = []
                if app_name == "tasks":
                    # add a task named "Study" with a tag "Study"
                    view_list = ["org.tasks:id/fab","org.tasks:id/appbarlayout",
                            "","org.tasks:id/search_input",
                            "org.tasks:id/tag_row","android.widget.ImageButton","android.widget.ImageButton"]
                    action_list = ["click","edit",
                        "click_with_text","edit",
                        "click","click","click"]
                    text_list = ["","Study","Add tags","my"]
                elif app_name == "ominiNotes":
                        # skip
                    view_list = ["it.feio.android.omninotes:id/next","it.feio.android.omninotes:id/next","it.feio.android.omninotes:id/next",
                    "it.feio.android.omninotes:id/next","it.feio.android.omninotes:id/next","it.feio.android.omninotes:id/done",
                        # add title and content
                        "it.feio.android.omninotes:id/fab_expand_menu_button","it.feio.android.omninotes:id/fab_note",
                        "it.feio.android.omninotes:id/detail_title","it.feio.android.omninotes:id/detail_content",
                        # add category
                        "it.feio.android.omninotes:id/menu_category","it.feio.android.omninotes:id/buttonDefaultPositive",
                        "it.feio.android.omninotes:id/category_title","it.feio.android.omninotes:id/save","android.widget.ImageButton"]
                    action_list = ["click","click","click",
                        "click","click","click",
                        "click","click",
                        "edit","edit",
                        "click","click",
                        "edit","click","click"
                        ]
                    text_list = ["","","","","","","","","new note","this is a note. #study #work","","","todo"]

                    if version <= "5.3.2" or (version >= "5.4.3" and version <="5.5.4"):
                        view_list.insert(6,"it.feio.android.omninotes:id/buttonDefaultPositive")
                        action_list.insert(6,"click")
                        text_list.insert(6,"")
                        
                if len(view_list) == 0 or len(action_list) == 0:
                    print("apk actions not defined!!!!!!!!")
                    break

                self.execute_macroevents(devices[i],view_list,action_list,text_list,event_count)
            i = i + 1


    def execute_macroevents_add(self,app_path,device,event_count):
        i = 0
        str1 = self.executor.policy.random_text()
        # str2 = self.executor.policy.random_text()
        while(i < len(app_path)):
            print("add macro!!!!!!!!!!!!!!!!!!!")
            app = app_path[0]
            app_name = app.split('/')[-2]
            version = app.split('/')[-1].split('-')[-1].replace('.apk','')
            view_list = []
            action_list = []
            text_list = []

            if app_name == "tasks":
                view_list = ["org.tasks:id/appbarlayout",
                        "","android:id/text1","android.widget.ImageButton"]
                action_list = ["edit",
                    "click_with_text","click_with_text","click"]
                text_list = [str1,"Does not repeat","Every day"]
            elif app_name == "ominiNotes":
                rate = random.randint(0,1)
                
                # 50% add a note or checklist
                # add Text note
                if rate == 0: 
                    view_list = [
                        # add title and content
                        "it.feio.android.omninotes:id/fab_note",
                        "it.feio.android.omninotes:id/detail_title","it.feio.android.omninotes:id/detail_content",
                        # add category
                        "it.feio.android.omninotes:id/menu_category","it.feio.android.omninotes:id/buttonDefaultPositive",
                        "it.feio.android.omninotes:id/category_title","it.feio.android.omninotes:id/save","android.widget.ImageButton"]
                    action_list = [
                        "click",
                        "edit","edit",
                        "click","click",
                        "edit","click","click"
                        ]
                    text_list = ["","added note","macroevents. #work","","","event"]
                # add Checklist
                else:
                    view_list = [
                        # add title and content
                        "it.feio.android.omninotes:id/fab_checklist",
                        "it.feio.android.omninotes:id/detail_title","","",
                        # add category
                        "it.feio.android.omninotes:id/menu_category","it.feio.android.omninotes:id/buttonDefaultPositive",
                        "it.feio.android.omninotes:id/category_title","it.feio.android.omninotes:id/save","android.widget.ImageButton"]
                    action_list = [
                        "click",
                        "edit","edit_with_text","edit_with_text",
                        "click","click",
                        "edit","click","click"
                        ]
                    text_list = ["","new checklist","New item$go to store","New item$homework","","","event"]

            if len(view_list) == 0 or len(action_list) == 0:
                print("apk actions not defined!!!!!!!!")
                break

            self.execute_macroevents(device[i],view_list,action_list,text_list,event_count)
            i = i + 1


    def execute_macroevents(self,device,view_list,action_list,text_list,event_count):
        i = 0
        cnt = 0
        while i < len(view_list):
            for view in device.state.all_views:
                # skip permission and pop-ups
                if view.text == "Dismiss":
                    device._click(view,"Dismiss")
                    time.sleep(1)
                    continue
                if view.resourceId == "com.android.packageinstaller:id/permission_allow_button":
                    device.click(view,None)
                    time.sleep(1)
                    continue

                # execute
                if action_list[i] == "click":
                    if view.resourceId == view_list[i] or view.className == view_list[i]:
                        # execute events
                        device.click(view,None)
                        time.sleep(1)
                        i = i + 1
                        break
                elif action_list[i] == "click_with_text":
                    if view.text == text_list[i]:
                        device._click(view,text_list[i])
                        time.sleep(1)
                        i = i + 1
                        break
                elif action_list[i] == "edit":
                    if view.resourceId == view_list[i] or view.className == view_list[i]:
                        device.click(view,None)
                        time.sleep(1)
                        device.use.send_keys(text_list[i], clear=True)
                        time.sleep(1)
                        i = i + 1
                        break
                elif action_list[i] == "edit_with_text":
                    if view.text == text_list[i].split('$')[0]:
                        device._click(view,text_list[i].split('$')[0])
                        time.sleep(1)
                        device.use.send_keys(text_list[i].split('$')[1], clear=True)
                        time.sleep(1)
                        i = i + 1
                        break

            self.executor.update_all_state(event_count)
            cnt = cnt + 1
            print("update")
            # error handle
            if cnt > len(view_list) + 2:
                print("error now exit macroevent")
                break
        print("END__________________________________________________")
        time.sleep(0.5)