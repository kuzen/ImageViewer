from core import Window
import imgui
import osmnx as ox


def export_map(G, node_color='#66ccff', node_size=15,
               node_alpha=1, node_edgecolor='none', node_zorder=1,
               edge_color='#ff0000', edge_linewidth=1, edge_alpha=1,
               xbias=1500, ybias=600, scale=0.5):

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
                           linewidths=edge_linewidth, alpha=edge_alpha, zorder=2)
    linesc = lc.get_segments()
    # ax.add_collection(lc)

    draw_list = imgui.get_window_draw_list()
    for p in linesc:
        points = ((p-[east, north])*[1, -1] /
                  [1.141255544679108e-5, 8.993216192195822e-6] +
                  [xbias, ybias])*scale
        if(len(points) > 2):
            draw_list.add_polyline(list(points),
                                   imgui.get_color_u32_rgba(
                                       1, 1, 0, edge_alpha),
                                   closed=False, thickness=edge_linewidth)
        else:
            draw_list.add_line(points[0][0], points[0][1],
                               points[1][0], points[1][1],
                               imgui.get_color_u32_rgba(1, 1, 0, edge_alpha),
                               edge_linewidth)


class MapViewer(Window):
    def __init__(self, filename='gdut_only_road.osm'):
        self.G = None
        self.setMap(filename)
        # self.updateG()
        super(MapViewer, self).__init__()

    def setMap(self, filename='gdut_only_road.osm'):
        self.G = ox.core.graph_from_file(filename)
        export_map(self.G)

    def updateG(self):
        pass

    def render(self):
        if self.G is None:
            self.setMap()
        else:
            # imgui_fig.fig(self.fig, height=250, title="f(x) = sin(x) / x")
            pass
            
        # imgui.end()
        # gl.glDeleteTextures([texture])
        # imgui.columns(1)
