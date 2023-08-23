import speedtest, time, sys

def test_internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()

    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping

    return download_speed, upload_speed, ping

if __name__ == "__main__":
    while 1:
        load, up, ping = test_internet_speed()
        print(f"{load:.2f} Mbps/{up:.2f} Mbps : {ping} ms")
        sys.stdout.flush()
        time.sleep(0.1)
