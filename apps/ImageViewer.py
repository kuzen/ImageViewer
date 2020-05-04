from core import Window
import imgui
import cv2
from imgui_datascience import imgui_cv
import osmnx as ox
import os


def export_map(G, node_color='#66ccff', node_size=15,
               node_alpha=1, node_edgecolor='none', node_zorder=1,
               edge_color='#ff0000', edge_linewidth=1, edge_alpha=1):

    # node_Xs = [float(x) for _, x in G.nodes(data='x')]
    # node_Ys = [float(y) for _, y in G.nodes(data='y')]

    edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
    west, south, east, north = edges.total_bounds

    # bbox_aspect_ratio = (north-south)/(east-west)
    # fig_width = fig_height / bbox_aspect_ratio

    lines = []
    for u, v, data in G.edges(keys=False, data=True):
        if 'geometry' in data:
            xs, ys = data['geometry'].xy
            line = list(zip(xs, ys))
            lines.append(list(zip(xs, ys)))
        else:
            x1 = G.nodes[u]['x']
            y1 = G.nodes[u]['y']
            x2 = G.nodes[v]['x']
            y2 = G.nodes[v]['y']
            line = [(x1, y1), (x2, y2)]
            lines.append(line)

    lc = ox.LineCollection(lines, colors=edge_color,
                           linewidths=edge_linewidth,
                           alpha=edge_alpha, zorder=2)
    linesc = lc.get_segments()
    # ax.add_collection(lc)
    return linesc, east, north


def drawMap(linesc, east, north,
            xbias=1300, ybias=100, scale=0.5,
            edge_color='#ff0000', edge_linewidth=1, edge_alpha=1):
    draw_list = imgui.get_window_draw_list()
    pos = imgui.core.get_window_position()
    for p in linesc:
        points = ((p-[east, north])*[1, -1] /
                  [1.141255544679108e-5, 8.993216192195822e-6] +
                  [xbias, ybias])*scale + [pos[0], pos[1]]
        if(len(points) > 2):
            draw_list.add_polyline(list(points),
                                   imgui.get_color_u32_rgba(
                                       1, 0, 0, edge_alpha),
                                   closed=False, thickness=edge_linewidth)
        else:
            draw_list.add_line(points[0][0], points[0][1],
                               points[1][0], points[1][1],
                               imgui.get_color_u32_rgba(1, 0, 0, edge_alpha),
                               edge_linewidth)


class ImageViewer(Window):
    def __init__(self):
        self.fig = None
        self.path = None
        self.img = None
        self.G = None
        self.east = None
        self.north = None
        self.info = {}
        self.supportFile = ['.png', '.jpg', 'bmp']
        super(ImageViewer, self).__init__()

    def readImage(self, path):
        self.path = path
        print(self.path)
        height = 0
        width = 0
        if self.path is None:
            pass
        elif os.path.splitext(self.path)[-1] in self.supportFile:
            self.img = cv2.imread(self.path)
            height = str(self.img.shape[1])
            width = str(self.img.shape[0])
        elif os.path.splitext(self.path)[-1] == '.osm':
            G = ox.core.graph_from_file(self.path)
            self.G, self.east, self.north = export_map(G)
            height = '400'
            width = '600'
        size = str(os.path.getsize(path))
        fileformat = os.path.splitext(path)[-1]
        info = {'fileInfo': {
            'name': path,
            'size': size,
            'height': height,
            'width': width,
            'format': fileformat
        }}
        return info

    def render(self, *args):
        if args[0][0][0] == {}:
            path = None
        else:
            path = args[0][0][0]['path'][0]
        if path == self.path:
            if self.path is None:
                pass
            elif os.path.splitext(self.path)[-1] in self.supportFile:
                imgui_cv.image(self.img)
            elif os.path.splitext(self.path)[-1] == '.osm':
                drawMap(self.G, self.east, self.north)
        else:
            self.info = self.readImage(path)
        return self.info
