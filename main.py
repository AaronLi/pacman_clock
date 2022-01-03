from pygame import *
from pacman_map import PacmanMap
import datetime
from search_map_solver import ClockSolver
import threading

def render_clock(map: PacmanMap, time_to_render):
    print(threading.currentThread().getName(), "rendering clock")
    render_width, render_height = map.get_render_dimensions()
    hour = time_to_render.hour % 12
    minute = time_to_render.minute
    digits = (hour // 10, hour % 10, minute // 10, minute % 10)
    draw_surface = Surface((render_width * 4, render_height))
    solutions = []
    for digit_num, digit in enumerate(digits):
        solver = ClockSolver(map, (digit,))
        solver.solve()
        print(threading.currentThread().getName(), "solved digit", digit_num)
        board = map.draw((digit,))
        # for from_ in solver.efficient_adjacency:
        #     for dest in solver.efficient_adjacency[from_]:
        #         draw.line(board, (0, 255, 0), (from_[0] * pac_map.DRAW_SCALE, from_[1] * pac_map.DRAW_SCALE), (dest[0] * pac_map.DRAW_SCALE, dest[1] * pac_map.DRAW_SCALE), 5)
        #
        # for from_ in solver.efficient_adjacency:
        #     for dest in solver.efficient_adjacency[from_]:
        #         draw.circle(board, (255, 0, 0), (dest[0] * pac_map.DRAW_SCALE, dest[1] * pac_map.DRAW_SCALE), 5)

        for path in solver.solution:
            draw.line(board, (255, 255, 0), (path[0][0] * pac_map.DRAW_SCALE + pac_map.DRAW_SCALE//2, path[0][1] * pac_map.DRAW_SCALE+pac_map.DRAW_SCALE+ pac_map.DRAW_SCALE//2),
                      (path[1][0] * pac_map.DRAW_SCALE+ pac_map.DRAW_SCALE//2, path[1][1] * pac_map.DRAW_SCALE+pac_map.DRAW_SCALE+ pac_map.DRAW_SCALE//2), 5)

        # image.save(board, f"clock{digit_num}.png")
        draw_surface.blit(board, (draw_width * digit_num, 0))
        solutions.append(solver.solution)
    return draw_surface, solutions

pac_map = PacmanMap()

pac_map.load("maps/singledigit_small")
print(pac_map)


draw_width, draw_height = pac_map.get_render_dimensions()

running = True

clock = time.Clock()

screen_size = (draw_width*4, draw_height)
print(screen_size)
prepared_image, prepared_solutions = render_clock(pac_map, datetime.datetime.now())
prepared_time = datetime.datetime.now().replace(second=0, microsecond=0)
display_image = None
display_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
display_solutions = None
solution_index = [0, 0]
delay_time = 30
render_thread = None
screen = display.set_mode(screen_size)
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
    if datetime.datetime.now() >= display_time + datetime.timedelta(minutes=1):
        if render_thread is not None:
            render_thread.join()
        display_image = prepared_image
        display_time = prepared_time
        display_solutions = prepared_solutions
        prepared_image = None
        prepared_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
        solution_index = [0, 0]

    if display_image is not None:
        screen.blit(display_image, (0, 0))
        solution_step = display_solutions[solution_index[0]][solution_index[1]]
        if len(display_solutions[solution_index[0]]) == solution_index[1] + 1:
            if solution_index[0] + 1 < len(display_solutions):
                solution_index[0] += 1
                solution_index[1] = 0
        elif delay_time <= 0:
            solution_index[1] += 1
            start, end = display_solutions[solution_index[0]][solution_index[1]]
            #manhattan distance
            distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
            # delay time is distance/ 10 seconds long
            delay_time = int(60 * (distance / 10))
        else:
            delay_time -= 1

        #print(solution_index, display_solutions[solution_index[0]][solution_index[1]])
        draw.line(screen, (255, 0, 0), (solution_step[0][0] * pac_map.DRAW_SCALE + solution_index[0] * draw_width+ pac_map.DRAW_SCALE//2, solution_step[0][1] * pac_map.DRAW_SCALE + pac_map.DRAW_SCALE+ pac_map.DRAW_SCALE//2), (solution_step[1][0] * pac_map.DRAW_SCALE + solution_index[0] * draw_width+ pac_map.DRAW_SCALE//2, solution_step[1][1] * pac_map.DRAW_SCALE + pac_map.DRAW_SCALE+ pac_map.DRAW_SCALE//2), 5)

        display.flip()
        clock.tick(60)
        display.set_caption(f"FPS: {clock.get_fps():.2f}")
    if prepared_image is None and (render_thread is None or not render_thread.is_alive()):
        def update_prepared(map, time):
            global prepared_image, prepared_solutions
            prepared_image, prepared_solutions = render_clock(map, time)
        render_thread = threading.Thread(target=update_prepared, args=(pac_map, datetime.datetime.now() + datetime.timedelta(minutes=1)))
        render_thread.start()