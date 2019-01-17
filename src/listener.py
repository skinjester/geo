import data, cv2

# keyboard event handler
def listener():
    key = cv2.waitKey(1) & 0xFF
    log.critical('key pressed: {}'.format(key))

    if key == 85:  # PAGE UP : increase gamma
        log.warning('{}:{} {} {}'.format('B1', key, 'PAGEUP', 'GAMMA+'))
        data.Webcam.get().gamma += 0.1
        data.Webcam.get().update_gamma(data.Webcam.get().gamma)
        return

    elif key == 86:  # PAGE DOWN decrease gamma
        log.warning('{}:{} {} {}'.format('B2', key, 'PAGEDOWN', 'GAMMA-'))
        data.Webcam.get().gamma -= 0.1
        data.Webcam.get().update_gamma(data.Webcam.get().gamma)
        return

    elif key == 81:  # left-arrow key: previous program
        log.warning('x{}:{} {} {}'.format('B3', key, 'ARROWL', 'PROGRAM-'))
        data.Model.prev_program()
        data.Model.reset_feature()
        return

    elif key == 83:  # right-arrow key: next program
        log.warning('{}:{} {} {}'.format('B4', key, 'ARROWR', 'PROGRAM+'))
        data.Model.next_program()
        data.Model.reset_feature()
        return

    elif key == 122:  # z key: next network layer
        log.warning('{}:{} {} {}'.format('C3', key, 'Z', 'LAYER-'))
        data.Model.prev_layer()
        data.Model.reset_feature()
        return

    elif key == 120:  # x key: previous network layer
        log.warning('{}:{} {} {}'.format('C4', key, 'X', 'LAYER+'))
        data.Model.next_layer()
        data.Model.reset_feature()
        return

    elif key == 44:  # , key : previous featuremap
        log.warning('{}:{} {} {}'.format('D3', key, ',', 'Feature-'))
        data.Model.prev_feature()
        data.Renderer.request_wakeup()

    elif key == 46:  # . key : next featuremap
        log.warning('{}:{} {} {}'.format('D4', key, '.', 'Feature+'))
        data.Model.next_feature()
        data.Renderer.request_wakeup()

    elif key == 91:  # [
        log.warning('{}:{} {} {}'.format('E1', key, '[', 'GAMMA -'))
        data.Webcam.get().gamma -= 0.1
        data.Webcam.get().update_gamma(data.Webcam.get().gamma)
        return

    elif key == 93:  # ]
        log.warning('{}:{} {} {}'.format('E2', key, ']', 'GAMMA +'))
        data.Webcam.get().gamma += 0.1
        data.Webcam.get().update_gamma(data.Webcam.get().gamma)
        return

    elif key == 45:  # _ key (underscore) : decrease detection floor
        data.Webcam.get().motiondetector.decrease_floor()
        log.warning('{}:{} {} {} :{}'.format('E3', key, '-', 'FLOOR-', data.Webcam.get().motiondetector.floor))
        return

    elif key == 61:  # = key (equals): increase detection floor
        data.Webcam.get().motiondetector.increase_floor()
        log.warning('{}:{} {} {} :{}'.format('E4', key, '=', 'FLOOR+', data.Webcam.get().motiondetector.floor))
        return

    elif key == 112:  # p key : pause/unpause motion detection
        data.Webcam.get().motiondetector.toggle_pause()
        # data.Model.autofeature = not data.Webcam.get().motiondetector.is_paused
        log.warning('{}:{} {} {}:{}'.format('F2', key, 'P', 'PAUSE',data.Webcam.get().motiondetector.is_paused))
        if not data.Webcam.get().motiondetector.is_paused:
            data.Renderer.request_wakeup()
        else:
            data.pause_img = data.Webcam.get().read()
        return

    elif key == 96:  # `(tilde) key: toggle HUD
        data.Viewport.toggle_HUD()
        log.warning('{}:{} {} {}:{}'.format('F3', key, '`', 'TOGGLE HUD', data.Viewport.b_show_HUD))
        return

    elif key == 49:  # 1 key : toggle motion detect window
        data.Viewport.toggle_monitor()
        log.warning('{}:{} {} {}:{}'.format('F4', key, '1', 'MOTION MONITOR', data.Viewport.b_show_monitor))
        return

    elif key == 27:  # ESC: Exit
        log.warning('{}:{} {} {}'.format('**', key, 'ESC', 'SHUTDOWN'))
        data.Viewport.shutdown()
        return

    elif key == 32:  # SPACE: toggle autofeature
        data.Model.autofeature = not data.Model.autofeature
        log.warning('{}:{} {} {}:{}'.format('**', key, 'SPACE', 'AUTOFEATURE', data.Model.autofeature ))
        return

    elif key==10: # ENTER key: save picture
        log.warning('{}:{} {} {}'.format('**',key,'ENTER','SAVE IMAGE'))
        # data.Viewport.export()
        data.Renderer.request_photo()
        return

    elif key==55: # 7 key: reduce equalization clipping
        log.warning('{}:{} {} {}'.format('**',key,'7','EQUALIZE CLIP --'))
        data.Postprocess.adjust_eq_clip(False)
        return

    elif key==56: # 8 key: increase equalization clipping
        log.warning('{}:{} {} {}'.format('**',key,'8','EQUALIZE CLIP ++'))
        data.Postprocess.adjust_eq_clip(True)
        return


    elif key == 57:  # 9 key: reduce equalization gridsize
        log.warning('{}:{} {} {}'.format('**', key, '9', 'EQUALIZE GRIDSIZE --'))
        data.Postprocess.adjust_eq_grid(False)
        return

    elif key == 48:  # \ key: increase equalization grid size
        log.warning('{}:{} {} {}'.format('**', key, '0', 'EQUALIZE GRIDSIZE ++'))
        data.Postprocess.adjust_eq_grid(True)
        return

    elif key == 123:  # { key: toggle widetime
        log.warning('{}:{} {} {}'.format('**', key, '0', 'TOGGLE WIDETIME'))
        data.Model.widetime = not data.Model.widetime
        return

    elif key == 125:  # } key: toggle timeloop
        log.warning('{}:{} {} {}'.format('**', key, '0', 'TOGGLE TIMELOOP'))
        data.Model.timeloop = not data.Model.timeloop
        return


# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.WARNING)
