import holoviews as hv
import param
import parambokeh
import numpy as np
from bokeh.io import curdoc

renderer = hv.renderer('bokeh').instance(mode='server')

class CurveExample(hv.streams.Stream):

    color = param.Color(default='#000000', precedence=0)

    element = param.ObjectSelector(default=hv.Curve,
                                   objects=[hv.Curve, hv.Scatter, hv.Area],
                                  precedence=0)

    amplitude = param.Number(default=2, bounds=(2, 5))
    
    frequency = param.Number(default=2, bounds=(1, 10))
    
    output = parambokeh.view.Plot()
    
    def view(self, *args, **kwargs):
        return self.element(self.amplitude*np.sin(np.linspace(0, np.pi*self.frequency)),
                        vdims=[hv.Dimension('y', range=(-5, 5))])(style=dict(color=self.color))
    
    def event(self, **kwargs):
        if not self.output or any(k in kwargs for k in ['color', 'element']):
            self.output = hv.DynamicMap(self.view, streams=[self])
        else:
            super(CurveExample, self).event(**kwargs)

example = CurveExample(name='HoloViews Example')
doc = parambokeh.Widgets(example, callback=example.event, on_init=True, mode='server',
                   view_position='right', doc=curdoc())
