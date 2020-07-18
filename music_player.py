import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk, GObject ,Gio
import eyed3

import pygame
import os

class HeaderBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="")
        self.set_border_width(10)
        self.set_default_size(500, 400)
        self.Active=0
        self.Check=None
        self.time=80
        self.a=0
        self.z=40
        self.text=""
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Namikaze Player"
        self.set_titlebar(header_bar)
     
        # Audio button on right
        self.audio_button = Gtk.VolumeButton()
        print(self.audio_button.get_value())
        self.audio_button.connect("value-changed",self.s_volume)
     
        header_bar.pack_end(self.audio_button)



        # Create a box and link items together
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        # Left arrow
        self.left_arrow = Gtk.Button()
        self.left_arrow.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(self.left_arrow)
        self.left_arrow.connect("clicked",self.previous)

        #pause button
        self.pause_button = Gtk.Button()
        pause_icon = Gio.ThemedIcon(name="gtk-media-pause")
        image = Gtk.Image.new_from_gicon(pause_icon, Gtk.IconSize.BUTTON)
        self.pause_button.connect("clicked",self.pausesong)
        self.pause_button.add(image)
        
        box.add(self.pause_button)
          

        self.play_button = Gtk.Button()
        play_icon = Gio.ThemedIcon(name="gtk-media-play")
        image = Gtk.Image.new_from_gicon(play_icon, Gtk.IconSize.BUTTON)
        self.play_button.add(image)
        self.play_button.connect("clicked",self.unpausesong)

        
        box.add(self.play_button)

        # Right arrow
        self.right_arrow = Gtk.Button()
        self.right_arrow.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(self.right_arrow)
        self.right_arrow.connect("clicked",self.next)
        header_bar.pack_start(box)


        #box for music files
        self.box_ = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)

        
        self.music_windows=Gtk.ScrolledWindow()
        self.music_windows.set_policy(Gtk.PolicyType.NEVER,
                               Gtk.PolicyType.AUTOMATIC)

        box_music = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.music_windows.add(box_music)
       
        self.box_.pack_start(self.music_windows,True,True,0)

        people_list_store = Gtk.ListStore(int, str,str)
        
        self.add(self.box_)

        
        music_=os.listdir("/home/shazib/Music/mp3")
        self.music_=music_
        self.w_dir="/home/shazib/Music/mp3/"

        for item in enumerate (  music_):
            item=list(item)
            try:
              timing=eyed3.load(self.w_dir+item[1]).info.time_secs
              self.pure_time="0"+str(int(timing//60))+":"+str(int(timing%60))
            except:
                self.pure_time="NA"
            item.append(self.pure_time)
            item[1]=item[1][:30]

            people_list_store.append(item)

        self.people_tree_view = Gtk.TreeView(people_list_store)

        for i, col_title in enumerate(["No..","music", "time"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)

            # Make column sortable and selectable
            column.set_sort_column_id(i)

            self.people_tree_view.append_column(column)
        selected_row = self.people_tree_view.get_selection()
        selected_row.connect("changed", self.item_selected)

        # Handle selection
        # selected_row = people_tree_view.get_selection()
        # selected_row.connect("changed", self.item_selected)
        box_music.pack_start(self.people_tree_view,True,True,0)
        self.new_box= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        self.progres=Gtk.ProgressBar()
        self.progres.set_property("width-request",200)
        self.progres.set_show_text(True)
        self.progres.set_text("NA")
        self.box_.add(self.new_box)
        self.new_box.pack_end(self.progres,True,True,0)

        self.title=Gtk.Label("nothing")
        self.title.set_property("width-request", 200)
        self.new_box.pack_start(self.title,False, True,0)
        
        self.time_call=GObject.timeout_add(1000,self.prosetter,None)
        self.s_volume()
    def prosetter(self, user_data):
        self.play_time=pygame.mixer.music.get_pos()/1000
        self.progres.set_fraction(self.play_time/self.time)
        self.show_time="0"+str(int(self.play_time//60))+":"+str(int(self.play_time%60))

        self.progres.set_text(str(self.show_time+"/"+self.pure_time))
        return True

    def playsong(self,music_,widget,**args):
        load=self.w_dir+music_[self.Active]
        music_file=eyed3.load(load)
        try:
         self.text=music_file.tag.title
        except:
            self.text=load
        
        self.title.set_markup(f"<b>{self.text}</b>")
        self.time=music_file.info.time_secs
        
        print(self.time)
         
        pygame.mixer.music.load(load)

        
        # Playing Selected Song
        pygame.mixer.music.play()
 
    def stopsong(self,widget,**args  ):
        # Displaying Status
        # self.status.set("-Stopped")
        # Stopped Song
        pygame.mixer.music.stop()
        self.progres.set_fraction(0.0)
        
       

        
    def pausesong(self,widget,**args):
    
        pygame.mixer.music.pause()
      
        

    def unpausesong(self,widget,**args):
        # Displaying Status
        # self.status.set("-Playing")
        # Playing back Song
        pygame.mixer.music.unpause()
       
    def item_selected(self, selection):
      self.stopsong(" ")
      if self.Check!=None:
        self.model, self.row = selection.get_selected()
        if self.row is not None:
          self.Active=self.model[self.row][0]
          print(self.Active)
          self.playsong(self.music_," ")
      else:
          self.Check=True
    def next(self,*args):
        self.stopsong(" ")
        self.Active+=1
        self.playsong(self.music_," ")
    def previous(self,*args):
        self.stopsong(" ")
        self.Active-=1
        # self.people_tree_view.set_cursor(,column=self.Active)
        # print(self.people_tree_view.get_cursor())
        
        self.playsong(self.music_," ")
    

    def s_volume(self,*args):
        volume_=self.audio_button.get_value()
        print(volume_)
        pygame.mixer.music.set_volume(volume_)

            


       
window = HeaderBarWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()
