from tkinter import Tk, Frame
from container import Container


class Manager(Tk):
    def _init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("caja registradora 1.0")
        self.resizable(False,False)
        #COLOR AZULITO
        self.configure(bg="#C6D9E3")
        #la altura y anchura
        self.geometry(8000*400+120+20)

        self.container = Frame(self, bg="#C6D9E3")
        self.container.pack(fill="both",expand=True)

        self.frames = {
           Container: None
        }

        def load_frames(self):
            for FrameClass in self.frames.keys():
                frame = FrameClass(self.container, self)
                self.frames[FrameClass] = frame

        def show_frame(self, frame_class):
            frame = self.frames[frame_class]
            frame.tkraise()

    def main():
        app = Manager()
        app.mainloop()

    if __name__== "_main_":
        main()

       