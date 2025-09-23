from IPython.display import display
import ipywidgets as widgets
import time
from matplotlib import pyplot as plt


def addjob(qmprog, qm):
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.queue.add(qmprog)
    # Wait for job to be loaded
    while job.status=="loading":
        print("Job is loading...")
        time.sleep(0.1)
    # Wait until job is running
    time.sleep(0.1)
    while job.status=="pending":
        q = job.position_in_queue()
        if q>0:
            print("Position in queue",q,end='\r')
        time.sleep(0.1)
    job=job.wait_for_execution()
    print("\nJob is running")
    return job
    
def rescale(ax,data):
    ymin,ymax=ax.get_ylim()
    dmin = data.min()
    dmax = data.max()
    delta = dmax-dmin
    if dmin<ymin or dmax>ymax:
        ax.set_ylim(dmin-0.05*delta, dmax+0.05*delta)
        
class ProgressPlot:
    def __init__(self):
        self.progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)
        self.progress_label = widgets.Label(value="??/??")
        self.button = widgets.Button(description='Abort',)
        self.button.on_click(self.stop)
        self.keeprunning = True
        with plt.ioff():
            self.fig = plt.figure()
    def stop(self,b):
        self.keeprunning = False
    def update(self,i,total):
        self.progress.value = float(i+1)/total
        self.progress_label.value = f"{i+1}/{total}"
        self.fig.canvas.draw_idle()
    def show(self):
        display(self.fig.canvas,widgets.HBox([self.button,self.progress,self.progress_label]))