#!/usr/bin/env python
#@todo Rename function

import os
import sys
import pygtk
pygtk.require('2.0')
import gtk

class ImageMover:
    destination_bindings = {
        "e": "/home/tuflus/My Pictures/Europa",
        "f": "/home/tuflus/My Pictures/Funny",
        "c": "/home/tuflus/My Pictures/Cool",
        "g": "/home/tuflus/My Pictures/Gente",
        "s": "."
    }

    def __init__(self):
        if len(sys.argv) is 2 and os.path.isdir(sys.argv[1]):
            self.PICTURES_PATH = sys.argv[1]
        else:
            self.PICTURES_PATH = os.getcwd()

        print "Running on " + self.PICTURES_PATH

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("key_press_event", self.key_handler)

        os.chdir(self.PICTURES_PATH)
        self.files = os.listdir(".")
        
        alignment = gtk.Alignment(0.5, 0, 0, 0)
        self.image = gtk.Image()
        alignment.add(self.image)
        self.image.show()
        self.window.add(alignment)
        alignment.show()

        self.window.move(0, 0)
        self.window.resize(gtk.gdk.screen_width(), gtk.gdk.screen_height()-150)
        self.window.show()
        
        self.current_filename = self.show_next_image()

    def show_next_image(self):
        image_filename = self.files.pop()         
        while os.path.isdir(image_filename):
            image_filename = self.files.pop()
        self.window.set_title(image_filename)

        # THIS IS AWFUL AWFUL CODE
        try:
            self.pixbuf = gtk.gdk.pixbuf_new_from_file(image_filename)
        except:
            # ignore files that cant be loaded as a pixbuf
            return self.show_next_image()
        alignment_rect = self.image.get_parent().get_allocation()

        self.fit_pixbuf(alignment_rect.width, alignment_rect.height)
        self.image.set_from_pixbuf(self.pixbuf)
        
        return image_filename
    
    def key_handler(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == "Delete":
            os.remove(self.current_filename)
            print "Deleted " + self.current_filename
            self.current_filename = self.show_next_image()
        elif keyname in self.destination_bindings:
            dest = self.destination_bindings[keyname]
            print self.current_filename + " --> " + os.path.join(dest, self.current_filename)
            os.rename(self.current_filename, os.path.join(dest, self.current_filename))
            self.current_filename = self.show_next_image()

    def fit_pixbuf(self, width, height):
        aspect = self.pixbuf.get_width() / float(self.pixbuf.get_height())

        if aspect >= 1:
            if self.pixbuf.get_width() > width:
                self.pixbuf = self.pixbuf.scale_simple(width, int(width / aspect), gtk.gdk.INTERP_BILINEAR)
        else:
            if self.pixbuf.get_height() > height:
                self.pixbuf = self.pixbuf.scale_simple(int(height * aspect), height, gtk.gdk.INTERP_BILINEAR)

    def main(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()

if __name__ == "__main__":
    base = ImageMover()
    base.main()
