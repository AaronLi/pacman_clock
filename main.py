from pygame import *
from pacman_map import PacmanMap
import datetime
from map_solver import ClockSolver

def render_clock(map: PacmanMap, time_to_render):
    render_width, render_height = map.get_render_dimensions()
    hour = time_to_render.hour % 12
    minute = time_to_render.minute
    digits = (hour // 10, hour % 10, minute // 10, minute % 10)
    draw_surface = Surface((render_width * 4, render_height))

    for digit_num, digit in enumerate(digits):
        solver = ClockSolver(map, (digit,))
        board = map.draw((digit,))
        solver.solve()
        # for from_ in solver.efficient_adjacency:
        #     for dest in solver.efficient_adjacency[from_]:
        #         draw.line(board, (0, 255, 0), (from_[0] * pac_map.DRAW_SCALE, from_[1] * pac_map.DRAW_SCALE), (dest[0] * pac_map.DRAW_SCALE, dest[1] * pac_map.DRAW_SCALE), 5)
        #
        # for from_ in solver.efficient_adjacency:
        #     for dest in solver.efficient_adjacency[from_]:
        #         draw.circle(board, (255, 0, 0), (dest[0] * pac_map.DRAW_SCALE, dest[1] * pac_map.DRAW_SCALE), 5)

        for path in solver.solution:
            draw.line(board, (255, 255, 0), (path[0][0] * pac_map.DRAW_SCALE, path[0][1] * pac_map.DRAW_SCALE+pac_map.DRAW_SCALE),
                      (path[1][0] * pac_map.DRAW_SCALE, path[1][1] * pac_map.DRAW_SCALE+pac_map.DRAW_SCALE), 5)

        # image.save(board, f"clock{digit_num}.png")
        draw_surface.blit(board, (draw_width * digit_num, 0))
    return draw_surface

pac_map = PacmanMap()

pac_map.load("maps/singledigit")
print(pac_map)


draw_width, draw_height = pac_map.get_render_dimensions()

running = True

clock = time.Clock()

screen_size = (draw_width*4, draw_height)
print(screen_size)
screen = display.set_mode(screen_size)
prepared_image = render_clock(pac_map, datetime.datetime.now())
prepared_time = datetime.datetime.now().replace(second=0, microsecond=0)
display_image = None
display_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
    if datetime.datetime.now() >= display_time + datetime.timedelta(minutes=1):
        display_image = prepared_image
        display_time = prepared_time
        prepared_image = None
        prepared_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)

    if display_image is not None:
        screen.blit(display_image, (0, 0))

        display.flip()
    if prepared_image is None:
        prepared_image = render_clock(pac_map, prepared_time)