import numpy as np

import matplotlib as mpl
from matplotlib.patches import Rectangle
from matplotlib.legend_handler import HandlerBase

COLOR_TABLE_1 = ["#b74f6fff","#628395ff","#dfd5a5ff","#dbad6aff","#cf995fff"]
class Color_Wheel:
    # rotate color wheel
    def __init__(self, color_table=COLOR_TABLE_1) -> None:
        self._color_table = color_table
        self._N = len(self._color_table)
    
    def __getitem__(self, i: int):
        i = i % self._N
        return self._color_table[i]

def get_color_table(cmap_name="viridis", N=10):
    cmap = mpl.cm.get_cmap(cmap_name)
    return [cmap(i) for i in np.linspace(0, 1, N)]
    
class CMAP_Selector:
    LUT_CMAP = {
        "Uniform": ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
        "Sequential": ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'],
        "Seq2": ["spring","summer","autumn","winter","cool","Wistia"],
        "Qualitative": ['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1',
                        'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c'],
        "Diverging": ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                        'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
        "hsv": ['hsv'],
    } 
    def __init__(self, style="Diverging") -> None:
        self._i = 0
        self._grp = self.LUT_CMAP[style]
        self._N = len(self._grp)
    
    def get_cmap(self):
        cmap = self._grp[self._i]
        self._i += 1 
        if self._i >= self._N:
            self._i = 0
        return cmap

    def __getitem__(self, i: int):
        i = i % self._N
        return self._grp[i]
    
    def get_cmap_handles(self, N_color: int, N_stripes: int=8):
        _cmap_list = [self[i] for i in range(N_color)]
        cmap_handles =  [Rectangle((0, 0), 1, 1) for _ in _cmap_list]
        handler_map = dict(zip(cmap_handles, [HandlerColormap(mpl.cm.get_cmap(cm), num_stripes=N_stripes) for cm in _cmap_list]))
        return cmap_handles, handler_map

class HandlerColormap(HandlerBase):
    def __init__(self, cmap, num_stripes=8, **kw):
        HandlerBase.__init__(self, **kw)
        self.cmap = cmap
        self.num_stripes = num_stripes
    def create_artists(self, legend, orig_handle, 
        xdescent, ydescent, width, height, fontsize, trans):
        stripes = []
        for i in range(self.num_stripes):
            s = Rectangle([xdescent + i * width / self.num_stripes, ydescent], 
                            width / self.num_stripes, 
                            height, 
                            fc=self.cmap((2 * i + 1) / (2 * self.num_stripes)), 
                            transform=trans)
            stripes.append(s)
        return stripes