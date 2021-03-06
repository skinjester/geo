import data, cv2, sys, thread, time, PIL.Image, numpy as np
import hud.console as console

class Viewport(object):

    def __init__(self, window_name, monitor, fullscreen, listener):
        self.window_name = '{}-{}'.format(window_name, data.username)
        self.b_show_HUD = False
        self.b_show_monitor = False
        self.imagesavepath = '/home/gary/Desktop/magicmirror'
        self.currentview = None
        self.listener = listener
        self.force_refresh = True
        self.fullscreen = fullscreen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        if self.fullscreen:
            cv2.setWindowProperty(self.window_name, 0, 1)
        cv2.moveWindow(self.window_name, monitor[0], monitor[1])

    def show(self, image):
        if self.b_show_HUD:
            image = console.draw(image)
        self.currentview = image
        cv2.imshow(self.window_name, self.currentview)
        self.monitor()
        self.listener()

    def export(self):
        rgb=self.currentview
        data.make_sure_path_exists(self.imagesavepath)
        export_path = '{}/{}.png'.format(
            self.imagesavepath,
            time.strftime('%m-%d-%H-%M-%s')
        )
        log.critical('{} {}:{}'.format('*'*8, 'export_path', export_path))
        cv2.imwrite(export_path, rgb)

    # forces new cycle with new camera image
    def refresh(self):
        self.force_refresh = True

    def monitor(self):
        if self.b_show_monitor:
            msg = data.Webcam.get().motiondetector.monitor_msg
            image = data.Webcam.get().buffer_t
            cv2.putText(image, msg, (20, 20), data.FONT, 0.5, data.WHITE)
            cv2.imshow('delta', image)

    def toggle_HUD(self):
        self.b_show_HUD = not self.b_show_HUD

    def toggle_monitor(self):
        self.b_show_monitor = not self.b_show_monitor
        if self.b_show_monitor:
            cv2.namedWindow('delta', cv2.WINDOW_AUTOSIZE)
        else:
            cv2.destroyWindow('delta')

    def shutdown(self):
        log.critical('-------- EXITING --------')
        for camera in data.Webcam.get_camera_list():
            camera.stop()
        data.Composer.stop()
        cv2.destroyAllWindows()
        thread.interrupt_main()



# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
