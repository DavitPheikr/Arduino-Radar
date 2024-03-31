import numpy as np
import matplotlib.pyplot as plt
import serial

# Function to open serial port
def open_serial_port(port, baudrate):
    ser = serial.Serial(port, baudrate) 
    print("port {} opened successfully.".format(port)) # If serial port opened, print a message 
    return ser


# Function to close serial port
def close_serial_port(ser):
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed.")


# update plot
def update_plot(angle, distance):
    dists[int(angle)] = distance # update distance on a specific angle in array

    pols.set_data(theta, dists) # update polar plot with new distance 
    
    #update the line idicating max distance
    line1.set_data(np.repeat((angle*(np.pi/180.0)),2), np.linspace(0.0,r_max,2)) 
                   
    fig.canvas.draw_idle() # redraw canvas and lines and plot on it        
    ax.draw_artist(line1) 
    ax.draw_artist(pols)



# Creating Polar Plot
def create_polar_plot():

    # add a subplot to the figure and set background color
    ax = fig.add_subplot(111, polar=True, facecolor='#0E4D25')  
    
    # set the position of the subplot
    ax.set_position([-0.05, -0.05, 1.1, 1.05])  
    
    # maximum radial ditance to show
    r_max = 100.0  
    ax.set_ylim([0.0, r_max])  # set the y axis limits
    
    # set x axis limits to show a range from 0 to pi 
    ax.set_xlim([0, np.pi])  
    
    # set the color of marks
    ax.tick_params(axis='both', colors='#24ee1f')  
    
    # add grid lines
    ax.grid(color='#24ee1f', alpha=1.0)  
    
    # set radial ticks to be displayed at specific distances, 5 in total
    ax.set_rticks(np.linspace(0.0, r_max, 5))  
    
    # set angle ticks to be displayed at specific angles, 10 in total
    ax.set_thetagrids(np.linspace(0, 180.0, 10))  
    
    # generate angles from 0 to 180 degrees
    angles = np.arange(0, 181, 1)  
    
    # convert angles to radians
    theta = angles * (np.pi / 180.0)  
    
    # initialize an array of distances with ones
    dists = np.ones((len(angles),))  
    
    # plot markers, set their colors and etc.
    pols, = ax.plot([], linestyle='', marker='o', markerfacecolor='#5CBC5A',
                     markeredgecolor='#5CBC5A', markeredgewidth=1.0,
                     markersize=8.0, alpha=0.9)  
    
    # initialize sweeping arm 
    line1, = ax.plot([], color='#45B748', linewidth=3.0)  
    
    # return values
    return ax, r_max, dists, pols, theta, line1

# ------------------

# Opening Serial Port      
ser = open_serial_port("COM5", 9600)
fig = plt.figure(facecolor='#000002')
win = fig.canvas.manager.window # figure window
screen_res = win.wm_maxsize() # used for window formatting later
fig.set_dpi(150.0) # set figure resolution

# Create polar plot and adjust size
ax, r_max, dists, pols, theta, line1 = create_polar_plot()
fig.set_size_inches(0.96 * (screen_res[0] / 150), 0.96 * (screen_res[1] / 150))


# ---- Window Details

# Position plot on screen
plot_res = fig.get_window_extent().bounds 
win.wm_geometry(f'+{(screen_res[0] / 2) - (plot_res[2] / 2):.0f}+{(screen_res[1] / 2) - (plot_res[3] / 2):.0f}')

# Remove toolbar and set window title
fig.canvas.toolbar.pack_forget()
win.title('Arduino Radar')

# ----

# Draw canvas and store background for animation loop
fig.canvas.draw()
ax_background = fig.canvas.copy_from_bbox(ax.bbox)  # Store background


# Main Loop
try:

    while True:

        #reading serial data, decoding to utf-8 and replacing
        data = (ser.readline().decode('utf-8').replace('\r', '')).replace('\n', '')

        try:
            # Spliting data into angle and distance values
            angle, dist = map(float, data.split(','))
            if dist >= r_max:
                dist = 0.0  
                dists[int(angle)] = dist
            if angle % 5 ==0: # updating plot for every 3 degrees
                update_plot(angle, dist) # update for current angle and distance
                fig.canvas.blit(ax.bbox) # redraw
                fig.canvas.flush_events() # flushing events 
                plt.pause(0.002)  # pause to give plot time to update
            if not(plt.fignum_exists(fig.number)): # check if window is open, if not break
                break
 
        except ValueError:
            pass

    # If window is close, if statement above brakes from the while loop and we stop program execution
    plt.close('all')
    print("Window was closed, program stopped execution") 
except KeyboardInterrupt:
        plt.close('all')
        print('Keyboard button pressed, stopped execution')
finally:
        close_serial_port(ser)
        plt.show() 
