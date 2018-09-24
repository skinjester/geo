import multiprocessing
import cv2

def cam_loop(pipe_parent):
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        if img is not None:
            pipe_parent.send(img)

def show_loop(pipe_child):
    cv2.namedWindow('syntheticaf')

    while True:
        from_queue = pipe_child.recv()
        cv2.imshow('syntheticaf', from_queue)


        key = cv2.waitKey(10) & 0xFF
        if key == 27: # ESC
            break

if __name__ == '__main__':

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    pipe_parent, pipe_child = multiprocessing.Pipe()

    cam_process = multiprocessing.Process(target=cam_loop,args=(pipe_parent, ))
    cam_process.start()

    show_process = multiprocessing.Process(target=show_loop,args=(pipe_child, ))
    show_process.start()

    cam_process.join()
    show_loop.join()
