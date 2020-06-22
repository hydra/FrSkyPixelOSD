import math
import time

import frskyosd

class SYM:
    HOME_ARROW_FIRST = 0x60
    HEADING_N = 0x18
    HEADING_S = 0x19
    HEADING_E = 0x1A
    HEADING_W = 0x1B
    HEADING_DIVIDED_LINE = 0x1C
    HEADING_LINE = 0x1D

class OSDDemo:

    FAST_ERASE = False

    def __init__(self, osd):
        self.vars = {}
        self.pitch = 0
        self.roll = 0
        self.home_angle = 0
        self.osd = osd

        self.pitch_delta = 0.05
        self.roll_delta = 0.05
        self.max_pitch = math.radians(100)
        self.max_roll = math.pi / 4

    def var(self, name, initial, step, wrap=None):
        val = self.vars.get(name, initial)
        val += step
        if wrap is not None:
            if step > 0 and val > wrap:
                val = initial
            elif step < 0 and val < wrap:
                val = initial
        self.vars[name] = val
        return val

    def begin(self):
        self.osd.transaction_begin((0, 10))

    def commit(self):
        self.osd.transaction_commit()

    def rotate_home(self, delta):
        prev_angle = self.home_angle
        angle = prev_angle + 0.1
        if angle >= math.pi * 2 or angle <= -math.pi * 2:
            angle = 0

        self.home_angle = angle
        return angle, prev_angle

    def draw_logo(self):
        bounds_start = getattr(self, 'bounds_start', None) or 0
        bounds_start += 1
        if bounds_start > 288 - 100:
            bounds_start = 0
        self.bounds_start = bounds_start
        SYM.logo = 0x101
        logo_width = 6
        logo_height = 4
        xs = 12
        ys = 6
        self.osd.context_push()
        self.begin()
        self.osd.clip_to_rect((0, bounds_start, 360, 100))
        opts = 0
        if int((int(time.time()) / 5)) % 2 == 0:
            opts = frskyosd.BITMAP_OPTS.INVERSE
#            self.osd.set_color_inversion(True)
        self.osd.clear_screen()
        for ii in range(logo_height):
            for jj in range(logo_width):
                self.osd.draw_grid_chr(xs + jj, ys + ii, SYM.logo, opts)
                SYM.logo += 1
        self.commit()
        self.osd.context_pop()

    def draw_horizon_line_light(self, level, width, pos, margin, erase):
        self.osd.context_push()
        yoff = -10 if level > 0 else 10
        self.osd.set_line_outline_type(frskyosd.OUTLINE.BOTTOM)
        self.osd.set_stroke_color(frskyosd.COLOR.TRANSPARENT if erase else frskyosd.COLOR.WHITE)
        self.osd.set_line_outline_color(frskyosd.COLOR.TRANSPARENT if erase else frskyosd.COLOR.BLACK)
        # Horizontal strokes
        yc = -pos - 1
        sz = width / 2
        self.osd.move_to_point(-sz, yc)
        self.osd.stroke_line_to_point(-margin, yc)
        self.osd.move_to_point(margin, yc)
        self.osd.stroke_line_to_point(sz, yc)
        # Vertical strokes
        self.osd.set_line_outline_type(frskyosd.OUTLINE.LEFT)
        self.osd.move_to_point(-sz, yc)
        self.osd.stroke_line_to_point(-sz, yc + yoff)
        self.osd.set_line_outline_type(frskyosd.OUTLINE.RIGHT)
        self.osd.move_to_point(sz, yc)
        self.osd.stroke_line_to_point(sz, yc + yoff)
        self.osd.context_pop()

    def draw_horizon_line_thick(self, level, width, pos, margin, erase):
        self.osd.context_push()
        if level <= 0:
            self.osd.ctm_scale(1, -1)

        # Vertical strokes
        self.osd.fill_stroke_rect([-width / 2, -pos - 1, 3, -10])
        self.osd.fill_stroke_rect([width / 2, -pos - 1, -3, -10])
        # Horizontal strokes
        self.osd.fill_stroke_rect([-width / 2, -pos - 1, width / 2 - margin, 3])
        self.osd.fill_stroke_rect([width / 2, -pos - 1, -width / 2 + margin, 3])
        if not erase:
            # Paint leftover black lines on strokes with white
            self.osd.set_stroke_color(frskyosd.COLOR.WHITE)

            self.osd.move_to_point(-width / 2, -pos - 1)
            self.osd.stroke_line_to_point(-width / 2 + 3, -pos - 1)

            self.osd.move_to_point(width / 2, -pos - 1)
            self.osd.stroke_line_to_point(width / 2 - 3, -pos - 1)

            self.osd.set_stroke_color(frskyosd.COLOR.BLACK)

        self.osd.context_pop()


    def draw_horizon_line(self, light, level, width, pos, margin, erase):
        if light:
            self.draw_horizon_line_light(level, width, pos, margin, erase)
        else:
            self.draw_horizon_line_thick(level, width, pos, margin, erase)

    def draw_horizon_shape(self, light, pitch, roll, erase):
        width = 10*12
        height = 18*7
        thick = 3
        crosshairMargin = 6
        pixels_per_level = 3.5
        level_width = width * 3 / 4

        lx = (360 - width) / 2
        ty = (288 - height) / 2

        rect = [lx + 1, ty + 1, width - 2, height - 2]

        if erase and self.FAST_ERASE:
            self.osd.clear_rect(rect)
            return

        self.osd.context_push()

        if not erase:
            # Draw corners
            rx = lx + width
            by = ty + height

            self.osd.set_stroke_color(frskyosd.COLOR.WHITE)

            self.osd.move_to_point(lx, ty + 10)
            self.osd.stroke_line_to_point(lx, ty)
            self.osd.stroke_line_to_point(lx + 10, ty)

            self.osd.move_to_point(rx, ty + 10)
            self.osd.stroke_line_to_point(rx, ty)
            self.osd.stroke_line_to_point(rx - 10, ty)

            self.osd.move_to_point(lx, by - 10)
            self.osd.stroke_line_to_point(lx, by)
            self.osd.stroke_line_to_point(lx + 10, by)

            self.osd.move_to_point(rx, by - 10)
            self.osd.stroke_line_to_point(rx, by)
            self.osd.stroke_line_to_point(rx - 10, by)

        self.osd.clip_to_rect(rect)

        if erase:
            self.osd.set_stroke_and_fill_color(frskyosd.COLOR.TRANSPARENT)
            self.osd.set_line_outline_color(frskyosd.COLOR.TRANSPARENT)
        else:
            self.osd.set_stroke_color(frskyosd.COLOR.WHITE)
            self.osd.set_line_outline_color(frskyosd.COLOR.BLACK)

        pitch_degrees = math.degrees(pitch)
        pitch_center = int(round(pitch_degrees / 10))
        pitch_offset = -pitch_degrees * pixels_per_level

        self.osd.ctm_translate(0, pitch_offset)
        self.osd.context_push()
        self.osd.ctm_rotate(-roll)

        self.osd.ctm_translate(180, 144)

        for ii in range(pitch_center - 2, pitch_center + 3):
            if ii == 0:
                if light:
                    self.osd.set_line_outline_type(frskyosd.OUTLINE.BOTTOM)
                    self.osd.move_to_point(-width / 2, 0)
                    self.osd.stroke_line_to_point(-crosshairMargin, 0)
                    self.osd.move_to_point(width / 2, 0)
                    self.osd.stroke_line_to_point(crosshairMargin, 0)
                    pass
                else:
                    self.osd.fill_stroke_rect([-width / 2, -1, width / 2 - crosshairMargin, 3])
                    self.osd.fill_stroke_rect([width / 2, -1, -width / 2 + crosshairMargin, 3])
                continue

            level = ii * 10
            pos = level * pixels_per_level
            margin = 6
            self.draw_horizon_line(light, level, level_width, -pos, margin, erase)

        self.osd.context_pop()
        self.osd.ctm_translate(180, 144)
        self.osd.ctm_scale(0.5, 0.5)
        # Draw line numbers
        sx = math.sin(-roll)
        sy = math.cos(roll)
        for ii in range(pitch_center - 2, pitch_center + 3):
            if ii == 0:
                continue

            level = ii * 10
            s = str(abs(level))
            pos = level * pixels_per_level
            charY = 9 - pos * 2
            cx = -18 if len(s) > 2 else -12
            if erase:
                self.osd.draw_str_mask(cx + (pitch_offset + pos) * sx * 2, -charY - (pitch_offset + pos) * (1 - sy) * 2, s, frskyosd.COLOR.TRANSPARENT)
            else:
                self.osd.draw_str(cx + (pitch_offset + pos) * sx * 2, -charY - (pitch_offset + pos) * (1 - sy) * 2, s)
        self.osd.context_pop()

    def draw_horizon(self, light, pitch, roll):
        self.begin()
        if self.pitch is not None or self.roll is not None:
            self.draw_horizon_shape(light, self.pitch, self.roll, True)
        self.draw_horizon_shape(light, pitch, roll, False)
        self.commit()

        self.pitch = pitch
        self.roll = roll

    def do_draw_ahi(self, light):
        if self.pitch <= -self.max_pitch:
            self.pitch_delta = abs(self.pitch_delta)
        elif self.pitch >= self.max_pitch:
            self.pitch_delta = -abs(self.pitch_delta)

        if self.roll <= -self.max_roll:
            self.roll_delta = abs(self.roll_delta)
        elif self.roll >= self.max_roll:
            self.roll_delta = -abs(self.roll_delta)


        pitch = self.pitch + self.pitch_delta
        roll = self.roll + self.roll_delta

        self.draw_horizon(light, pitch, roll)

    def draw_ahi(self):
        self.do_draw_ahi(False)

    def draw_ahi_light(self):
        self.do_draw_ahi(True)

    def draw_foo(self):
        self.begin()
        self.osd.clear_screen()
        self.osd.draw_grid_str(10, 10, 'FOO')
        self.commit()

    def draw_home_bitmap(self, angle, erase):
        degs = math.degrees(angle) + 11
        if degs >= 360:
            degs = 0
        offset = degs * 2 / 45
        sym = SYM.HOME_ARROW_FIRST + offset
        error = math.radians(angle - offset * 22.5)

        self.osd.context_push()
        self.osd.ctm_rotate(error)
        self.osd.ctm_translate(180, 144)
        if erase:
            self.osd.draw_chr_mask(-6, -9, sym, frskyosd.COLOR.TRANSPARENT)
        else:
            self.osd.draw_chr(-6, -9, sym)
        self.osd.context_pop()

    def draw_home_shape(self, angle, erase):
        self.osd.context_push()
        self.osd.ctm_rotate(-angle)
        self.osd.ctm_translate(180, 144)
        if erase:
            self.osd.set_fill_color(frskyosd.COLOR.TRANSPARENT)
            self.osd.set_stroke_color(frskyosd.COLOR.TRANSPARENT)
        else:
            self.osd.set_fill_color(frskyosd.COLOR.WHITE)
            self.osd.set_stroke_color(frskyosd.COLOR.BLACK)

        self.osd.fill_stroke_triangle((0, 6), (6, -6), (-6, -6))
        if not erase:
            self.osd.set_fill_color(frskyosd.COLOR.TRANSPARENT)
            self.osd.fill_stroke_triangle((0, -2), (6, -7), (-6, -7))
            self.osd.set_stroke_color(frskyosd.COLOR.TRANSPARENT)
            self.osd.move_to_point(6, -7)
            self.osd.stroke_line_to_point(-6, -7)

        self.osd.context_pop()

    def draw_home_indicator(self, angle, erase):
        #self.osd.context_push()
        self.draw_home_shape(angle, erase)
        #self.osd.ctm_translate(30, 0)
        #self.draw_home_bitmap(angle, erase)
        #self.osd.context_pop()

    def draw_home(self):
        angle, prev_angle = self.rotate_home(0.1)
        self.begin()
        self.draw_home_indicator(prev_angle, True)
        self.draw_home_indicator(angle, False)
        self.commit()

    def draw_triangle(self):
        angle, prev_angle = self.rotate_home(0.1)
        self.begin()
        self.osd.context_push()
        self.osd.ctm_rotate(angle)
        self.osd.ctm_translate(180, 144)
        self.osd.clear_screen()
        self.osd.fill_stroke_triangle((0, 10), (-5, -20), (17, -40))
        self.osd.context_pop()
        self.commit()

    def draw_rect(self):
        angle, prev_angle = self.rotate_home(0.1)
        self.begin()
        self.osd.context_push()
        self.osd.ctm_rotate(angle)
        self.osd.ctm_translate(180, 144)
        self.osd.clear_screen()
        self.osd.fill_stroke_rect((-50, -100, 100, 200))
        self.osd.context_pop()
        self.commit()

    def draw_compass(self):
        heading = self.var('heading', 0, 1, 360)
        cw = 9 * self.osd.info.gridWidth
        ch = self.osd.info.gridHeight
        rect = [
            self.osd.info.pixelWidth / 2 - cw / 2,
            self.osd.info.pixelHeight / 2 - ch / 2,
            cw, ch]

        graph = [
                SYM.HEADING_LINE,
                SYM.HEADING_E,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
                SYM.HEADING_S,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
                SYM.HEADING_W,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
                SYM.HEADING_N,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
                SYM.HEADING_E,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
                SYM.HEADING_S,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
                SYM.HEADING_W,
                SYM.HEADING_LINE,
                SYM.HEADING_DIVIDED_LINE,
                SYM.HEADING_LINE,
        ]

        h = heading

        if h >= 180:
            h -= 360

        hh = h * 4
        hh = hh + 720 + 45
        hh = hh // 90

        p = ((heading * 2 + 22.5) % 45) - 22.5

        self.begin()
        self.osd.context_push()
        self.osd.clear_rect(rect)
        self.osd.clip_to_rect(rect)
        s = ''.join([chr(graph[ii]) for ii in range(hh, hh + 12)])
        offset = round((p / 45) * self.osd.info.gridWidth)
        self.osd.draw_str(rect[0] - self.osd.info.gridWidth - offset, rect[1], s)
        self.osd.context_pop()
        self.osd.draw_str(rect[0], rect[1] + self.osd.info.gridHeight, '%03d' % heading, opts=frskyosd.BITMAP_OPTS.ERASE_TRANSPARENT)
        self.commit()

    def draw_grid(self):
        self.begin()
        opts = frskyosd.BITMAP_OPTS.ERASE_TRANSPARENT
        for ii in range(0, self.osd.info.gridRows):
            s = str(ii+1)
            self.osd.draw_grid_str(0, ii, s, opts)
            self.osd.draw_grid_str(self.osd.info.gridColumns - len(s), ii, s, opts)
        for ii in range(1, self.osd.info.gridColumns - 1):
            s = chr(ord('A') + ii - 1)
            self.osd.draw_grid_str(ii, 5, s, opts)
        self.commit()

    def draw_grid_lines(self):
        self.begin()
        opts = 0
        for ii in range(0, self.osd.info.gridRows):
            s = 'This is line {}'.format(ii+1).upper()
            self.osd.draw_grid_str((self.osd.info.gridColumns - len(s)) / 2, ii, s, opts)
        self.commit()

    def draw_grid_lines_full(self):
        self.begin()
        opts = 0
        for ii in range(0, self.osd.info.gridRows):
            s = 'This is line {} with {} slots'.format(ii+1, self.osd.info.gridColumns).upper()
            while len(s) < self.osd.info.gridColumns:
                if self.osd.info.gridColumns - len(s) >= 2:
                    s = '+' + s + '+'
                else:
                    s = s + '-'
            self.osd.draw_grid_str((self.osd.info.gridColumns - len(s)) / 2, ii, s, opts)
        self.commit()

def main():
    import argparse

    parser = argparse.ArgumentParser()

    draw_choices = ('logo', 'ahi', 'ahi_light', 'compass', 'foo', 'home', 'triangle', 'rect', 'grid', 'grid_lines', 'grid_lines_full')

    parser.add_argument('--trace', default=False, action='store_true', dest='trace', help='Print all data sent/received')
    parser.add_argument('--profile-at', dest='profile_at', type=str, help='Screen point to draw profiling information at')
    parser.add_argument('--once', default=False, action='store_true', dest='once', help='Draw the element once at exit')
    parser.add_argument('port', type=str, help='OSD serial port')
    parser.add_argument('draw', type=str, help='Demo element to draw', choices=draw_choices)
    args = parser.parse_args()

    osd = frskyosd.OSD(args.port, trace=args.trace, profile_at=args.profile_at)
    if not osd.connect():
        return 1

    demo = OSDDemo(osd)

    draw = getattr(demo, 'draw_' + args.draw)

    osd.drawing_reset()
    osd.clear_screen()
    while True:
        draw()
        if args.once:
            break
        time.sleep(0.1)


if __name__ == '__main__':
    import sys
    sys.exit(main() or 0)
