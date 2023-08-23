import asyncio
import matplotlib.pyplot as plt
import numpy as np
from ping3 import ping
from collections import deque

async def ping_ip(ip, times):
    while True:
        try:
            response_time = ping(ip, timeout=1)
            if response_time is not None:
                times[ip].append(response_time)
            else:
                times[ip].append(-1)
        except Exception:
            times[ip].append(-1)

        # Limit the number of data points to 60 (1 minute of data at 1-second intervals)
        #times[ip] = times[ip][-60:]
        await asyncio.sleep(0.1)

async def plot_graph(ip, times, ax):
    ax.set_title(f"Ping Response Time - {ip}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Response Time (ms)")
    x = np.arange(60)
    line, = ax.plot([], [], label=ip)

    while True:
        y = np.array(times[ip])
        if len(y) > 0:
            line.set_data(x[:len(y)], y)

        ax.relim()
        ax.autoscale_view()

        plt.draw()
        plt.pause(1)  # Update the graph every 1 second
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    ips = ["8.8.8.8", "1.1.1.1", "192.168.110.1", "10.10.10.5"]
    times = {ip: deque(maxlen=60) for ip in ips}

    fig, axes = plt.subplots(len(ips), 1, sharex=True, sharey=False)
    plt.subplots_adjust(hspace=0.5)

    loop = asyncio.get_event_loop()
    tasks = [ping_ip(ip, times) for ip in ips]
    for i, ip in enumerate(ips):
        tasks.append(plot_graph(ip, times, axes[i]))

    loop.run_until_complete(asyncio.gather(*tasks))
