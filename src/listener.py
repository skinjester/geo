import cv2

# keyboard event handler
def listener(Model, Webcam, Viewport, log, update_HUD_log):
    key = cv2.waitKey(1) & 0xFF
    log.debug('key pressed: {}'.format(key))

    if key == 85:  # PAGE UP : increase gamma
        log.warning('{}:{} {} {}'.format('B1', key, 'PAGEUP', 'GAMMA+'))
        Webcam.get().gamma += 0.1
        Webcam.get().update_gamma(Webcam.get().gamma)
        return

    elif key == 86:  # PAGE DOWN decrease gamma
        log.warning('{}:{} {} {}'.format('B2', key, 'PAGEDOWN', 'GAMMA-'))
        Webcam.get().gamma -= 0.1
        Webcam.get().update_gamma(Webcam.get().gamma)
        return

    elif key == 81:  # left-arrow key: previous program
        log.warning('x{}:{} {} {}'.format('B3', key, 'ARROWL', 'PROGRAM-'))
        Model.prev_program()
        Model.reset_feature()
        return

    elif key == 83:  # right-arrow key: next program
        log.warning('{}:{} {} {}'.format('B4', key, 'ARROWR', 'PROGRAM+'))
        Model.next_program()
        Model.reset_feature()
        return

    elif key == 122:  # z key: next network layer
        log.warning('{}:{} {} {}'.format('C3', key, 'Z', 'LAYER-'))
        Model.prev_layer()
        Model.reset_feature()
        return

    elif key == 120:  # x key: previous network layer
        log.warning('{}:{} {} {}'.format('C4', key, 'X', 'LAYER+'))
        Model.next_layer()
        Model.reset_feature()
        return

    elif key == 44:  # , key : previous featuremap
        log.warning('{}:{} {} {}'.format('D3', key, ',', 'Feature-'))
        Model.prev_feature()

    elif key == 46:  # . key : next featuremap
        log.warning('{}:{} {} {}'.format('D4', key, '.', 'Feature+'))
        Model.next_feature()

    elif key == 91:  # [
        log.warning('{}:{} {} {}'.format('E1', key, '[', 'GAMMA -'))
        Webcam.get().gamma -= 0.1
        Webcam.get().update_gamma(Webcam.get().gamma)
        return

    elif key == 93:  # ]
        log.warning('{}:{} {} {}'.format('E2', key, ']', 'GAMMA +'))
        Webcam.get().gamma += 0.1
        Webcam.get().update_gamma(Webcam.get().gamma)
        return

    elif key == 45:  # _ key (underscore) : decrease detection floor
        Webcam.get().motiondetector.decrease_floor()
        log.warning('{}:{} {} {} :{}'.format('E3', key, '-', 'FLOOR-', Webcam.get().motiondetector.floor))
        return

    elif key == 61:  # = key (equals): increase detection floor
        Webcam.get().motiondetector.increase_floor()
        log.warning('{}:{} {} {} :{}'.format('E4', key, '=', 'FLOOR+', Webcam.get().motiondetector.floor))
        return

    elif key == 112:  # p key : pause/unpause motion detection
        Webcam.get().motiondetector.toggle_pause()
        log.warning('{}:{} {} {}:{}'.format('F2', key, 'P', 'PAUSE',Webcam.get().motiondetector.is_paused))
        return

    elif key == 96:  # `(tilde) key: toggle HUD
        Viewport.toggle_HUD()
        log.warning('{}:{} {} {}:{}'.format('F3', key, '`', 'TOGGLE HUD', Viewport.b_show_HUD))
        return

    elif key == 49:  # 1 key : toggle motion detect window
        Viewport.toggle_monitor()
        log.warning('{}:{} {} {}:{}'.format('F4', key, '1', 'MOTION MONITOR', Viewport.b_show_monitor))
        return

    elif key == 27:  # ESC: Exit
        log.warning('{}:{} {} {}'.format('**', key, 'ESC', 'SHUTDOWN'))
        Viewport.shutdown()
        Webcam.get().motiondetector.export.close()  # close the motion detector data export file
        return

    elif key == 32:  # SPACE: toggle program cycle
        Model.toggle_program_cycle()
        log.warning('{}:{} {} {}:{}'.format('**', key, 'SPACE', 'PROGRAM CYCLE', Model.program_running ))
        return
