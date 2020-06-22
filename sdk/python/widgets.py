import math
import time

import utils

import frskyosd

class OSDWidgetsDemo:
    AHI_WIDTH = 10 * 12
    AHI_HEIGHT = 18 * 10
    AHI_LINE_INDICATOR_MARGIN = 6
    AHI_CROSSHAIR_MARGIN = 6

    SIDEBAR_WIDTH, SIDEBAR_HEIGHT = frskyosd.grid_size_to_pixels(6, 10)

    GRAPH_WIDTH, GRAPH_HEIGHT = frskyosd.grid_size_to_pixels(10, 3)

    ALT_M = 0xB1 # ALT(M) in INAV
    ALT_KM = 0xB2 # ALT(KM) in INAV

    def __init__(self, osd):
        self.osd = osd
        self.pitch = utils.Var(0, 0.01, math.radians(179.9))
        self.roll = utils.Var(0, 0.01, math.pi / 4)
        self.altitude = utils.Var(0, 500, -1000 * 100, 5000 * 100)

    def quantize(self, val, max_val, max_quant):
        if val < 0:
            val += max_val
        return (float(val) / max_val) * max_quant

    def _configure_ahi(self, style):
        if not getattr(self, '_ahi_config_done', False):
            w = self.AHI_WIDTH
            h = self.AHI_HEIGHT
            r = ((self.osd.info.pixelWidth - w) / 2, (self.osd.info.pixelHeight - h) / 2, w, h)
            self.osd.widget_ahi_set_config(r, style,
                self.AHI_CROSSHAIR_MARGIN, options=frskyosd.WIDGETS.AHI_OPTION_SHOW_CORNERS)
            self._ahi_config_done = True

    def _draw_ahi(self, style):
        self._configure_ahi(style)
        pitch, roll = self.pitch.next(), self.roll.next()
        max_val = 2 * math.pi
        max_quant = (1 << 12)
        p = self.quantize(pitch, max_val, max_quant)
        r = self.quantize(roll, max_val, max_quant)
        self.osd.widget_ahi_draw(p, r)

    def draw_ahi(self):
        self._draw_ahi(frskyosd.WIDGETS.AHI_STYLE_STAIRCASE)

    def draw_ahi_line(self):
        self._draw_ahi(frskyosd.WIDGETS.AHI_STYLE_LINE)

    def _sidebar_rect(self, right):
        y = (self.osd.info.pixelHeight - self.SIDEBAR_HEIGHT) / 2
        distance = (self.AHI_WIDTH + 12) / 2
        mid = self.osd.info.pixelWidth / 2
        if right:
            x = mid + distance
        else:
            x = mid - distance - self.SIDEBAR_WIDTH
        return (x, y, self.SIDEBAR_WIDTH, self.SIDEBAR_HEIGHT)

    def draw_sidebar(self):
        sid = 0
        if not getattr(self, '_sidebar_config_done', False):
            r = self._sidebar_rect(True)
            unit = frskyosd.Unit(100, self.ALT_M, 1000, self.ALT_KM)
            opts = 0
            self.osd.widget_sidebar_set_config(sid, r, opts, 10, 50 * 100, unit)
            self._sidebar_config_done = True
        altitude = self.altitude.next()
        self.osd.widget_sidebar_draw(sid, altitude)

    def _graph_rect(self):
        x = (self.osd.info.pixelWidth - self.GRAPH_WIDTH) / 2
        y = (self.osd.info.pixelHeight - self.GRAPH_HEIGHT) / 2
        return (x, y, self.GRAPH_WIDTH, self.GRAPH_HEIGHT)

    def draw_graph(self):
        gid = 0
        r = self._graph_rect()
        if not getattr(self, '_graph_config_done', False):
            unit = frskyosd.Unit(100, self.ALT_M, 1000, self.ALT_KM)
            opts = 0
            self.osd.widget_graph_set_config(gid, r, opts, 2, 3, unit)
            self._graph_config_done = True
        altitude = self.altitude.next()
        self.osd.widget_graph_draw(gid, altitude)
        s = '{:08}'.format(altitude)
        self.osd.draw_str(r[0], r[1] + r[3] + 1, s, opts=frskyosd.BITMAP_OPTS.ERASE_TRANSPARENT)


def main():
    import argparse

    parser = argparse.ArgumentParser()

    widget_choices = (
        'ahi',
        'ahi_line',
        'sidebar',
        'graph',
    )

    parser.add_argument('--trace', default=False, action='store_true', dest='trace', help='Print all data sent/received')
    parser.add_argument('--once', default=False, action='store_true', dest='once', help='Draw the widget once at exit')
    parser.add_argument('--profile-at', dest='profile_at', type=str, help='Screen point to draw profiling information at')
    parser.add_argument('port', type=str, help='OSD port')
    parser.add_argument('widget', type=str, help='Widget to draw', choices=widget_choices)
    args = parser.parse_args()

    osd = frskyosd.OSD(args.port, trace=args.trace, profile_at=args.profile_at)
    if not osd.connect():
        return 1

    demo = OSDWidgetsDemo(osd)

    draw = getattr(demo, 'draw_' + args.widget)

    osd.drawing_reset()
    osd.clear_screen()
    while True:
        osd.transaction_begin()
        draw()
        osd.transaction_commit()
        if args.once:
            break
        time.sleep(0.1)

if __name__ == '__main__':
    main()
